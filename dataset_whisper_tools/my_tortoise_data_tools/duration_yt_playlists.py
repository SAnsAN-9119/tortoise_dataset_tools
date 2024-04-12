import os
import yt_dlp

def get_playlist_info(file_path):
    total_duration = 0
    total_videos = 0

    with open(file_path, 'r') as file:
        for line in file:
            playlist_url = line.strip()
            if playlist_url:
                print(f"Analyzing playlist: {playlist_url}")
                ydl_opts = {}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(playlist_url, download=False)
                    playlist_size = len(info.get('entries', []))

                    for entry in info.get('entries', []):
                        video_duration = entry.get('duration', 0)
                        total_duration += video_duration
                        total_videos += 1

                    print(f"Playlist size: {playlist_size} videos")

    print(f"Total duration: {format_duration(total_duration)}")
    print(f"Total videos: {total_videos}")

def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    # Path to the text file containing YouTube playlist URLs
    file_path = '../../../../audio/dataset_3_Ru/youtube_download_links_4.txt'
    get_playlist_info(file_path)