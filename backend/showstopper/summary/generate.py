from datetime import date, datetime, timedelta, time
from typing import List, Set

from showstopper.audio.model import DialougeSegment
from showstopper.audio.ports import AudioTranscriber, TextGenerator
from showstopper.images.ports import ImageEmbedder
from showstopper.video.model import CombinedShot
from showstopper.video.ports import VideoSplicer, VideoSplitter, VideoVectorDatastore
from showstopper.video.shots import generate_video_shots
from showstopper.video.splicing import combine_video_segments


def find_clips_for_summary(
    video_id: str,
    summary: str,
    image_text_embedding_client: ImageEmbedder,
    vectorstore: VideoVectorDatastore,
):
    all_found_clips: List[CombinedShot] = []
    timestamps: Set[time] = set()

    sentences = summary.split(". ")
    si = 0

    while si < len(sentences):
        text_query_embedding = image_text_embedding_client.embed_text(
            sentences[si],
        )

        shots = vectorstore.get_video_shots(video_id, text_query_embedding[0].tolist())

        for i in range(0, len(shots)):
            shot = shots[i]

            if shot.start_time not in timestamps:
                all_found_clips.insert(((si + 1) * i) + si, shot)
                timestamps.add(shot.start_time)

        si += 1

    # TODO: use overlapping windows to check if clip already added
    filtered_clips: List[CombinedShot] = []
    total_time = timedelta(seconds=0)
    i = 0

    while total_time < timedelta(seconds=30):
        clip = all_found_clips[i]

        filtered_clips.append(clip)
        total_time += datetime.combine(date.today(), clip.end_time) - datetime.combine(
            date.today(), clip.start_time
        )
        i += 1

    return sorted(filtered_clips, key=lambda clip: clip.start_time)


def generate_text_summary_from_frames_and_subtitles(
    text_generator: TextGenerator, transcript: List[DialougeSegment]
) -> str:
    return text_generator.generate_text_with_content(
        "Given the dialouge for a video, generate a 5 sentence or less summary",
        content=" ".join(line.text for line in transcript),
    )


def generate_video_summary(
    video_id: str,
    input_video_filepath: str,
    output_video_filepath: str,
    video_splitter: VideoSplitter,
    video_splicer: VideoSplicer,
    image_embedder: ImageEmbedder,
    audio_transcriber: AudioTranscriber,
    text_generator: TextGenerator,
    vectorstore: VideoVectorDatastore,
):
    shots = generate_video_shots(
        input_video_filepath,
        video_splitter,
        image_embedder,
        audio_transcriber,
    )

    vectorstore.save_video_shots(video_id, shots)

    summary = generate_text_summary_from_frames_and_subtitles(
        text_generator,
        [
            DialougeSegment(
                start_time=shot.start_time, end_time=shot.end_time, text=shot.dialouge
            )
            for shot in shots
            if shot.dialouge is not None
        ],
    )

    summary_clips = find_clips_for_summary(
        video_id, summary, image_embedder, vectorstore
    )

    combine_video_segments(
        input_video_filepath,
        output_video_filepath,
        [(clip.start_time, clip.end_time) for clip in summary_clips],
        video_splicer,
    )
    # TODO: clear frames from vectordb
