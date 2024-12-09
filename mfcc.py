import librosa
import numpy as np
from pydub import AudioSegment
from pathlib import Path
from scipy.io import savemat
from scipy.signal import medfilt


def extract_mfcc(audio_file, duration=10, sr=44100, n_mfcc=13):

    y = []
    # Load the audio file
    if not isinstance(audio_file, Path):
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_frame_rate(44100) # set framerates to mp3 standards
        y = np.array(audio.get_array_of_samples(), dtype=np.float32)
        y = np.trim_zeros(y)  # Remove leading zeros
    else:
        y, sr = librosa.load(audio_file, sr=sr)  # y is the audio time series, sr is the sampling rate

    # Determine the number of samples for the specified duration
    max_samples = sr * duration

    # Trim the audio to the specified duration
    y = y[:max_samples]

    # Compute MFCC (Mel-frequency cepstral coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # Flatten the MFCCs
    mfcc = mfcc.flatten()

    return mfcc, sr


def extract_mfcc_from_folder(input_folder, output_folder, duration=10, sr=44100, n_mfcc=13):
    mfcc_list = []
    filenames = []
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    files = sorted(input_folder.glob("*.mp3")) + sorted(input_folder.glob("*.m4a")) # can adjust file 
    if len(files) == 0:
        raise ValueError(f"No MP3 files found in {input_folder}")
    
    for idx, file in enumerate(files, start=1):
        try:
            mfcc, sr = extract_mfcc(file)
            mfcc_list.append(mfcc)
            filenames.append(file.name)
            print(f"Processed {file.name} -> {file.stem}")
        
        except Exception as e:
            print(f"Error processing {file.name}: {e}")

        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except ValueError as value_error:
            print(f"Error: {value_error}")
        except Exception as e:
            print(f"Error: {e}")

    output_path = output_folder / "training_songs.mat"
    data = {
                "amplitude": mfcc_list,
                "filenames": filenames  
            }
    savemat(output_path, data)

if __name__ == "__main__":

    audio_file = 'Britney Spears - Toxic (Instrumental).mp3'  # Replace with your audio file path
    mfcc, sr = extract_mfcc(audio_file)
    data = {
        'amplitude': mfcc
    }
    audio_file = audio_file.replace('.mp3', '.mat')
    savemat('./' + audio_file, data)
    

    # extract_mfcc_from_folder("C:/Users/ewei/Downloads/mp3s", "./")