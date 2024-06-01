import json
import os
import sys
import tempfile

import pika
import requests
from supabase import create_client, Client

from showstopper.adapters.chroma import ChromaAdapter
from showstopper.adapters.ffmpeg import FFMpegAdapter
from showstopper.adapters.openai import CLIPImageTextEmbedder, OpenAIAdapter
from showstopper.summary.generate import generate_video_summary

from dotenv import load_dotenv

load_dotenv(".env")
from showstopper.config import env

print("creating clients...")

video_splitter = video_splicer = FFMpegAdapter()
image_embedder = CLIPImageTextEmbedder()
audio_transcriber = text_generator = OpenAIAdapter(open_ai_key=env.OPENAI_API_KEY)
vectorstore = ChromaAdapter()
supabase: Client = create_client(
    supabase_url=env.SUPABASE_URL, supabase_key=env.SUPABASE_KEY
)

upload_video_bucket = "uploaded-videos"
processed_video_bucket = "processed-videos"


def process_video(video_id):
    with tempfile.TemporaryDirectory() as tempdir:
        input_video = os.path.join(tempdir, f"{video_id}.input.mp4")
        output_video = os.path.join(tempdir, f"{video_id}.output.mp4")

        with open(input_video, "wb+") as f:
            res = supabase.storage.from_(upload_video_bucket).download(
                os.path.basename(input_video),
            )
            f.write(res)

        generate_video_summary(
            video_id,
            input_video,
            output_video,
            video_splitter,
            video_splicer,
            image_embedder,
            audio_transcriber,
            text_generator,
            vectorstore,
        )

        with open(output_video, "rb") as f:
            supabase.storage.from_(processed_video_bucket).upload(
                file=f,
                path=os.path.basename(output_video),
                file_options={"content-type": "video/mp4"},
            )

    # TODO: update video status
    return


def queue_processor():
    try:
        print("creating connection...")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=env.QUEUE_HOST,
                credentials=pika.PlainCredentials(
                    username=env.QUEUE_USER, password=env.QUEUE_PASS
                ),
            )
        )

        print("creating channel...")
        channel = connection.channel()

        print("declaring queue...")
        channel.queue_declare(queue="tasks", durable=True)

        def callback(ch, method, properties, body: bytes):
            print(f" [x] Recieved {body}")

            try:
                video_id = json.loads(body.decode("utf-8"))["video_id"]
            except Exception as e:
                print("could not parse video_id from payload")

            try:
                requests.put(
                    f"{env.BACKEND_HOST}/api/summaries/{video_id}",
                    json={"status": "PROCESSING"},
                )

                process_video(video_id)

                requests.put(
                    f"{env.BACKEND_HOST}/api/summaries/{video_id}",
                    json={"status": "FINISHED"},
                )
            except Exception as e:
                print("Encountered error processing message:", e)

                requests.put(
                    f"{env.BACKEND_HOST}/api/summaries/{video_id}",
                    json={"status": "ERRORED"},
                )

        print("preparing consumer...")
        channel.basic_consume(
            queue="tasks", on_message_callback=callback, auto_ack=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    # video_id = "messi-demo"

    # process_video(video_id)
    print("starting queue processor...")
    queue_processor()
