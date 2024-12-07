from pydub import AudioSegment
import numpy as np
from pathlib import Path
from scipy.io import savemat

def mp3_to_matlab(input_file, output_filename="poop3.mat"):
    try:
        # Convert MP3 to WAV
        audio = AudioSegment.from_file(input_file, format="mp3")
        wav_data = np.array(audio.get_array_of_samples())
        wav_rate = audio.frame_rate

        # Determine the number of samples corresponding to 10 seconds
        max_samples = wav_rate * 10  # 10 seconds of audio
        if len(wav_data) < max_samples:
            raise ValueError("The audio file is shorter than 10 seconds.")

        # Slice the data for the first 10 seconds
        wav_data = wav_data[:max_samples:45]
        time_axis = np.linspace(0, 10, num=max_samples)  # Time axis for the first 10 seconds

        # Find desktop path
        desktop_folder = Path("C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop")
        if not desktop_folder.exists():
            raise FileNotFoundError(f"Desktop folder not found: {desktop_folder}")

        # Save data to a MATLAB .mat file
        data = {
            "time": time_axis,        # x-axis: time in seconds
            "amplitude": wav_data     # y-axis: amplitude values
        }
        output_path = desktop_folder / output_filename
        savemat(output_path, data)  # Save to .mat file
        print(f"Waveform data (first 10 seconds) saved to {output_path} as MATLAB-compatible .mat file")
    
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except ValueError as value_error:
        print(f"Error: {value_error}")
    except Exception as e:
        print(f"Error: {e}")

input_file = "C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop/Recording.mp3" # Replace with your MP3 file path
mp3_to_matlab(input_file)
