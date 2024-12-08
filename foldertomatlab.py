from pydub import AudioSegment
import numpy as np
from pathlib import Path
from scipy.io import savemat

def folder_to_matlab(input_folder, output_folder=None):
    try:
        input_folder = Path(input_folder)
        if not input_folder.exists() or not input_folder.is_dir():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        if output_folder is None:
            output_folder = input_folder / "output"
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        files = sorted(input_folder.glob("*.mp3"))
        if len(files) == 0:
            raise ValueError(f"No MP3 files found in {input_folder}")

        target_rate = 44100 #CHANGED FREQUECNY SO IT IS CNSOSTNET

        for idx, file in enumerate(files, start=1):
            try:
                audio = AudioSegment.from_file(file, format="mp3")
                audio = audio.set_frame_rate(target_rate)
                wav_data = np.array(audio.get_array_of_samples())
                wav_rate = target_rate

                max_samples = wav_rate * 10
                if len(wav_data) < max_samples:
                    print(f"Skipping {file.name}: Audio shorter than 10 seconds.")
                    continue
                
                wav_data = wav_data[:max_samples:45]
                time_axis = np.linspace(0, 10, num=len(wav_data))
                
                output_filename = f"newupdated12.7withtimesteps{idx}.mat"
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

input_folder = "C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop/mp3 files"
output_folder = "C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop/BigMatrix"
folder_to_matlab(input_folder, output_folder)
