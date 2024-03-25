from pytube import YouTube

# Ask user for the video URL
url = input("Enter Youtube Video Link")

# Create a YouTube object and get the highest resolution stream
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()

# Download the video
print("Downloading...")
stream.download()
print("Download completed!")
