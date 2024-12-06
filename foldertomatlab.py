from pydub import AudioSegment
import numpy as np
from pathlib import Path
from scipy.io import savemat

def folder_to_matlab(input_folder, output_folder=None):
    try:
        # Define input and output folders
        input_folder = Path(input_folder)
        if not input_folder.exists() or not input_folder.is_dir():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        if output_folder is None:
            output_folder = input_folder / "output"
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        # Iterate through MP3 files in the input folder
        files = sorted(input_folder.glob("*.mp3"))  # Adjust for other formats if needed
        if len(files) == 0:
            raise ValueError(f"No MP3 files found in {input_folder}")

        for idx, file in enumerate(files, start=1):
            try:
                # Load the audio file
                audio = AudioSegment.from_file(file, format="mp3")
                wav_data = np.array(audio.get_array_of_samples())
                wav_rate = audio.frame_rate

                # Determine the number of samples for 10 seconds
                max_samples = wav_rate * 10  # 10 seconds
                if len(wav_data) < max_samples:
                    print(f"Skipping {file.name}: Audio shorter than 10 seconds.")
                    continue
                
                # Slice the data for the first 10 seconds
                wav_data = wav_data[:max_samples]
                time_axis = np.linspace(0, 10, num=max_samples)  # Time axis for the first 10 seconds

                # Save to MATLAB .mat file
                output_filename = f"wavdatasong{idx}.mat"
                output_path = output_folder / output_filename
                data = {
                    "time": time_axis,
                    "amplitude": wav_data
                }
                savemat(output_path, data)
                print(f"Processed {file.name} -> {output_filename}")
            
            except Exception as e:
                print(f"Error processing {file.name}: {e}")
    
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except ValueError as value_error:
        print(f"Error: {value_error}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_folder = "C:/Users/hzhang/Downloads/AudioFiles"  # Replace with your folder path
output_folder = "C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop/ProcessedAudio"  # Replace or set to None
folder_to_matlab(input_folder, output_folder)