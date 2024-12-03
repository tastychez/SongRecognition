from pydub import AudioSegment

def splice_mp3(input_file, output_file, duration=10):
    try:
        # Load the MP3 file explicitly
        audio = AudioSegment.from_file(input_file, format="mp3")
        
        if len(audio) == 0:
            print("Error: Input file has no audio content.")
            return
        
        # Truncate or pad to the desired duration
        spliced_audio = audio[:duration * 1000]  # duration in milliseconds

        # Export the result with a specified bitrate
        spliced_audio.export(output_file, format="mp3", bitrate="192k")
        print(f"Spliced audio saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_file = "C:/Users/hzhang/Downloads/spotifydown.com - Perfect Night.mp3"  # Replace with your input file name
output_file = "output.mp3"  # Replace with your desired output file name
splice_mp3(input_file, output_file)
