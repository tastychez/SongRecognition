import argparse
from pydub import AudioSegment

def splice_mp3(input_file, output_file, duration=10):
    try:
        # load mp3
        audio = AudioSegment.from_file(input_file, format="mp3")
        
        if len(audio) == 0:
            print("Error: Input file has no audio content.")
            return
        
        # truncate to duration you want
        spliced_audio = audio[:duration * 1000]  # duration in milliseconds

        # Export the result with a specified bitrate
        spliced_audio.export(output_file, format="mp3", bitrate="192k")
        print(f"Spliced audio saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Splice an MP3 file to a specified duration.")
    parser.add_argument("input_file", type=str, help="Path to the input MP3 file.")
    parser.add_argument("output_file", type=str, help="Path to save the spliced MP3 file.")
    parser.add_argument("--duration", type=int, default=10, help="Duration to splice in seconds (default: 10 seconds).")

    args = parser.parse_args()

    splice_mp3(args.input_file, args.output_file, args.duration)
