import ffmpeg


def video_to_images(video_path, output_path):
    # Use ffmpeg to extract frames at 1 frame per second
    (
        ffmpeg.input(video_path)
        .filter('fps', fps=1)
        .output(output_path + '/image_%04d.png')
        .run()
    )


# Example usage
video_path = 'video.mp4'
output_path = 'output_images'
video_to_images(video_path, output_path)
