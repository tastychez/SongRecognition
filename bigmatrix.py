from pydub import AudioSegment
import numpy as np
from pathlib import Path
from scipy.io import savemat

def folder_to_combined_matlab(input_folder, output_folder=None, output_filename="bigmatrix_waveform_data.mat"):
    try:
        input_folder = Path(input_folder)
        if not input_folder.exists() or not input_folder.is_dir():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        if output_folder is None:
            output_folder = input_folder / "output"
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        combined_time = []  # time matrices
        combined_amplitude = []  # amplitude matrices
        filenames = []  # keep track of the file names
        
        files = sorted(input_folder.glob("*.mp3"))  # can adjust for other formats if needed
        if len(files) == 0:
            raise ValueError(f"No MP3 files found in {input_folder}")

        for idx, file in enumerate(files, start=1):
            try:
                # Load the audio file
                audio = AudioSegment.from_file(file, format="mp3")
                wav_data = np.array(audio.get_array_of_samples())
                wav_rate = audio.frame_rate

                # determine the number of samples for 10 seconds
                max_samples = wav_rate * 10  # 10 seconds
                if len(wav_data) < max_samples:
                    print(f"Skipping {file.name}: Audio shorter than 10 seconds.")
                    continue
                
                # slice for the first 10 seconds
                wav_data = wav_data[:max_samples]

                # Apply chunk-based median filter
                chunk_size = 45  # 0.1 second chunks for 44100 Hz sample rate
                filtered_data = []
                for i in range(0, len(wav_data), chunk_size):
                    chunk = wav_data[i:i + chunk_size]
                    median_value = np.median(chunk)
                    filtered_data.extend([median_value] * len(chunk))
                wav_data = np.array(filtered_data)
                wav_data = wav_data[::chunk_size]

                time_axis = np.linspace(0, 10, num=max_samples)  # time axis for the first 10 seconds

                combined_time.append(time_axis)
                combined_amplitude.append(wav_data)
                filenames.append(file.name)
                print(f"Processed {file.name}")
            
            except Exception as e:
                print(f"Error processing {file.name}: {e}")
        
        combined_time = np.array(combined_time)
        combined_amplitude = np.array(combined_amplitude)

        output_path = output_folder / output_filename
        data = {
            "time": combined_time,        # time values
            "amplitude": combined_amplitude,  # amplitude values
            "filenames": filenames      
        }
        savemat(output_path, data)
        print(f"Combined waveform data saved to {output_path} as MATLAB-compatible .mat file")
    
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except ValueError as value_error:
        print(f"Error: {value_error}")
    except Exception as e:
        print(f"Error: {e}")

input_folder = "C:/Users/ewei/Downloads/MP3 Files"  # Replace with your folder path
output_folder = "./"  # Replace with your folder path
folder_to_combined_matlab(input_folder, output_folder)
