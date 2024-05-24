from datetime import time
from typing import List, Tuple

from showstopper.audio.model import DialougeSegment
from showstopper.video.model import CombinedShot, VideoShot
from showstopper.video.ports import VideoSplicer


def combine_video_segments(
    input_video_filename: str,
    output_video_filename: str,
    timestamp_windows: List[Tuple[time, time]],
    video_splicer: VideoSplicer,
):
    video_splicer.trim_video_with_windows(
        input_video_filename, output_video_filename, timestamp_windows
    )


def combine_shot_dialouge_windows(
    dialouge: List[DialougeSegment], shots: List[VideoShot]
) -> List[CombinedShot]:
    combined: List[CombinedShot] = []
    i = j = 0
    # current_timestamp = shots[0][0]
    current_timestamp = shots[0].start_frame.start_time

    while i < len(dialouge) and j < len(shots):
        # start_dialouge, end_dialouge = dialouge[i]
        # _, end_shot = shots[j]
        dialouge_segment = dialouge[i]
        video_shot = shots[j]

        # print(start_dialouge, end_dialouge)
        # print(start_shot, end_shot)
        # print("")

        # dialouge completely after shot
        # if start_dialouge > end_shot:
        if dialouge_segment.start_time > video_shot.end_frame.end_time:
            # combined.append((current_timestamp, end_shot))
            combined.append(
                CombinedShot(
                    start_time=current_timestamp,
                    end_time=video_shot.end_frame.end_time,
                    dialouge=None,
                    image_embedding=video_shot.image_embedding,
                )
            )
            j += 1
            current_timestamp = video_shot.end_frame.end_time
        # dialouge overlaps with current shot
        else:
            i += 1

            # dialouge finishes before shot and next dialouge starts after shot
            if (
                # end_dialouge < end_shot
                dialouge_segment.end_time < video_shot.end_frame.end_time
                and i < len(dialouge)
                and dialouge[i].start_time >= video_shot.end_frame.end_time
            ):
                # combined.append((current_timestamp, video_shot.end_frame.end_time))
                combined.append(
                    CombinedShot(
                        start_time=current_timestamp,
                        end_time=video_shot.end_frame.end_time,
                        dialouge=dialouge_segment.text,
                        image_embedding=video_shot.image_embedding,
                    )
                )
                j += 1
                current_timestamp = shots[j].start_frame.start_time
            # dialouge finishes after shot
            else:
                # combined.append((current_timestamp, dialouge_segment.end_time))
                combined.append(
                    CombinedShot(
                        start_time=current_timestamp,
                        end_time=dialouge_segment.end_time,
                        dialouge=dialouge_segment.text,
                        image_embedding=video_shot.image_embedding,
                    )
                )
                current_timestamp = dialouge_segment.end_time

                while (
                    j < len(shots)
                    and shots[j].end_frame.end_time < dialouge_segment.end_time
                ):
                    j += 1

    while j < len(shots):
        # combined.append((current_timestamp, shots[j][1]))
        combined.append(
            CombinedShot(
                start_time=current_timestamp,
                end_time=shots[j].end_frame.end_time,
                dialouge=None,
                image_embedding=video_shot.image_embedding,
            )
        )
        current_timestamp = shots[j].end_frame.end_time
        j += 1

    return combined
