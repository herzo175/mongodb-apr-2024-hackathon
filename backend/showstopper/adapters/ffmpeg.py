from datetime import datetime, timedelta
import os
from time import time
from typing import List, Tuple
import tempfile
import uuid

import ffmpeg

from showstopper.video.model import VideoFrame
from showstopper.video.ports import VideoSplicer, VideoSplitter


def create_video_clip(
    source_video_file: str,
    output_video_file: str,
    start_timestamp: str,
    end_timestamp: str,
):
    ffmpeg.input(source_video_file, ss=start_timestamp, to=end_timestamp).output(
        output_video_file
    ).run(overwrite_output=True)


def combine_video_clips(video_clip_files: List[str], output_video_filename: str):
    # Combine outfile paths into a txt file
    with tempfile.TemporaryDirectory() as tempdir:
        combined_file = f"{tempdir}/{str(uuid.uuid4())[:8]}.txt"

        with open(combined_file, "w") as fp:
            fp.write("\n".join(video_clip_files))

        # Combine clips using source files
        ffmpeg.input(combined_file, format="concat", safe=0).output(
            output_video_filename, c="copy"
        ).run(overwrite_output=True)


class FFMpegAdapter(VideoSplitter, VideoSplicer):
    def get_video_frame_rate(self, source_video_filename: str) -> int:
        probe = ffmpeg.probe(source_video_filename)

        return int(probe["streams"][0]["avg_frame_rate"].split("/")[0])

    def create_video_frames(
        self, source_video_filename: str, output_dir: str, fps: int
    ) -> List[VideoFrame]:
        source_fps = self.get_video_frame_rate(source_video_filename)

        ffmpeg.input(source_video_filename).filter(
            "select", f"not(mod(n,{fps}))"
        ).output(os.path.join(output_dir, "frame%d.png"), vsync="vfr").run(
            overwrite_output=True
        )

        return [
            VideoFrame(
                index=i,
                file_path=os.path.join(output_dir, frame),
                start_time=(
                    datetime.min + timedelta(seconds=(i * fps) / source_fps)
                ).time(),
                end_time=(
                    datetime.min + timedelta(seconds=((i + 1) * fps) / source_fps)
                ).time(),
            )
            for i, frame in enumerate(
                sorted(
                    os.listdir(output_dir),
                    key=lambda name: int(name.replace("frame", "").replace(".png", "")),
                )
            )
        ]

    def split_audio_video(self, source_video_filename: str, output_audio_filename: str):
        ffmpeg.input(source_video_filename).output(output_audio_filename).run(
            overwrite_output=True
        )

    def trim_video_with_windows(
        self,
        source_video_file: str,
        output_video_file: str,
        timestamp_windows: List[Tuple[time, time]],
    ):
        with tempfile.TemporaryDirectory() as tempdir:
            # generate clips from source video by time stamp window
            outfiles = []

            for window in timestamp_windows:
                out = f"{tempdir}/{str(uuid.uuid4())[:8]}.mp4"

                create_video_clip(
                    source_video_file, out, str(window[0]), str(window[1])
                )
                outfiles.append(f"file {out}")

            combine_video_clips(outfiles, output_video_file)
