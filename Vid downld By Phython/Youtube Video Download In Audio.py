from pytube import YouTube
from moviepy.editor import *

# Ask user for the video URL
url = input("Enter the video URL: ")

# Create a YouTube object and get the highest resolution stream
yt = YouTube(url)
stream = yt.streams.filter(only_audio=True).first()

# Download the audio
print("Downloading audio...")
audio_file = stream.download()
print("Audio download completed!")

# Convert the audio to MP3
print("Converting audio to MP3...")
audio = AudioFileClip(audio_file)
audio.write_audiofile(audio_file.replace(".webm", ".mp3"))
print("Conversion completed!")
