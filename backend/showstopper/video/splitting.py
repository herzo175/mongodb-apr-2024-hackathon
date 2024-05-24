from typing import List

from showstopper.images.embeddings import generate_image_embeddings, images_same
from showstopper.images.ports import ImageCaptioner, ImageEmbedder
from showstopper.video.model import VideoFrame, VideoShot
from showstopper.video.ports import VideoSplitter


def generate_video_frames(
    input_video_filename: str, output_dir: str, video_splitter: VideoSplitter
) -> List[VideoFrame]:
    return video_splitter.create_video_frames(input_video_filename, output_dir, 8)


def cut_video_shots(
    frames: List[VideoFrame],
    similarity_threshold: float,
    image_embedder: ImageEmbedder,
) -> List[VideoShot]:
    chunk_size = 10

    # Split frames into batches of chunk_size
    # Each chunk starts with the last frame of the previous chunk
    chunks = [
        frames[max(0, (i * chunk_size) - 1) : (i + 1) * chunk_size]
        for i in range((len(frames) + chunk_size - 1) // chunk_size)
    ]

    shot_windows: List[VideoShot] = []
    last_frame = frames[0]

    for chunk in chunks:
        embeddings = generate_image_embeddings(
            [frame.file_path for frame in chunk], image_embedder
        )

        for i in range(1, len(embeddings)):
            emb_1, emb_2 = embeddings[i - 1], embeddings[i]

            if not images_same(emb_1, emb_2, similarity_threshold):
                # shot_windows.append((last_frame, chunk[i - 1]))
                # TODO: get median embedding for all frames in shot
                # TODO: reset
                shot_windows.append(
                    VideoShot(
                        start_frame=last_frame,
                        end_frame=chunk[i - 1],
                        image_embedding=emb_1,
                    )
                )

                last_frame = chunk[i]

    return shot_windows
