from pytube import YouTube
link = input("Enter URL of video")
video = YouTube(link)
stream = video.stream.get_highest_resolution()
stream.download()