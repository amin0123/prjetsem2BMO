from pytube import YouTube

def Download(link):
    try:
        yt_object = YouTube(link)
        yt_object = yt_object.streams.get_highest_resolution()

        try:
            yt_object.download()
        except:
            print("error with download :(")
        
        print("download complete :)")
        
    except:
        print("please enter a valid URL")

link = input("YouTube URL to download: ")
Download(link)