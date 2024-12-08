from pydub import AudioSegment
from scipy.io.wavfile import write as write_wav
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def mp3_to_wav_and_image(input_file, image_filename="poop.png"): #change here what u want ur output name to be 
    try:
        #convert MP3 to WAV
        audio = AudioSegment.from_file(input_file, format="mp3")
        wav_data = np.array(audio.get_array_of_samples())
        # print (wav_data)
        wav_rate = audio.frame_rate
        # # print("First 10 samples:", wav_data[wav_rate:(wav_rate+1000)])
        # print("Last 10 samples:", wav_data[-10:])
        # print (wav_rate)

        # find desktop path
        desktop_folder = Path("C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop")
        if not desktop_folder.exists():
            raise FileNotFoundError(f"Desktop folder not found: {desktop_folder}")
        
        wav_output_path = desktop_folder / "output.wav"
        write_wav(wav_output_path, wav_rate, wav_data.astype(np.int16))
        print(f"WAV file saved to {wav_output_path}")
        
        # Plot waveform 
        plt.figure(figsize=(20, 10))  # larger figure
        time_axis = np.linspace(0, len(wav_data) / wav_rate, num=len(wav_data))  # axis in seconds
        plt.plot(time_axis[:wav_rate * 10], wav_data[:wav_rate * 10], color="blue", linewidth=0.8, antialiased=True)  # plot 10 seconds

        plt.title("Audio Waveform")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
        plt.tight_layout()

        # high resolution
        image_output_path = desktop_folder / image_filename
        plt.savefig(image_output_path, dpi=300) 
        plt.close()
        print(f"High-resolution waveform image saved to {image_output_path}")
    
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"Error: {e}")

input_file = "C:/Users/hzhang/OneDrive - Olin College of Engineering/Desktop/test/Recording.mp3"  # Replace with your MP3 file path
mp3_to_wav_and_image(input_file)
