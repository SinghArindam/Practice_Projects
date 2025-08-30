import argparse
import ffmpeg
import sys

def create_gif_with_ffmpeg(input_path, output_path, speed_factor, frame_rate):
    """
    Converts a video to a GIF using a direct FFmpeg command.
    """
    try:
        print(f"Processing '{input_path}' with FFmpeg...", file=sys.stderr)

        stream = ffmpeg.input(input_path)

        # Apply video filters:
        # 'setpts' changes the timestamp of the frames. Dividing by the speed_factor speeds it up.
        # 'fps' sets the output frame rate.
        stream = ffmpeg.filter(stream, 'setpts', f'{1.0/speed_factor}*PTS')
        stream = ffmpeg.filter(stream, 'fps', frame_rate)
        
        stream = ffmpeg.output(stream, output_path)
        
        # Run the FFmpeg command.
        # overwrite_output=True allows overwriting existing files.
        # quiet=True suppresses the verbose FFmpeg console output.
        ffmpeg.run(stream, overwrite_output=True, quiet=True)

        print(f"Successfully created '{output_path}'", file=sys.stderr)

    except ffmpeg.Error as e:
        print("An FFmpeg error occurred:", file=sys.stderr)
        # FFmpeg's detailed error is in stderr, so we print it.
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a video to GIF using FFmpeg, with options for speed and FPS."
    )
    
    parser.add_argument("input_video", help="The path to the source video file.")
    parser.add_argument("output_gif", help="The desired path for the output GIF file.")
    
    parser.add_argument(
        '--speed', 
        type=float, 
        default=1.0, 
        help="A factor to speed up the video (e.g., 2 for double speed). Default: 1.0."
    )
    
    parser.add_argument(
        '--fps', 
        type=int, 
        default=15, 
        help="Frames per second for the output GIF. Default: 15."
    )
    
    args = parser.parse_args()
    
    create_gif_with_ffmpeg(
        input_path=args.input_video, 
        output_path=args.output_gif, 
        speed_factor=args.speed, 
        frame_rate=args.fps
    )

# python "utils\vid2gif.py" "assets/chess_gui_v1.mp4" "assets/chess_gui_v1_ffmpeg.gif" --speed 4 --fps 20