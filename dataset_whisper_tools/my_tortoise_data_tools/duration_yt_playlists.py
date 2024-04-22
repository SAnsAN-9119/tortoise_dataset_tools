import requests
import json
import os
import isodate

def convert_duration(duration):
    duration = isodate.parse_duration(duration)
    return duration.total_seconds()

def format_duration(duration):
    duration_in_seconds = convert_duration(duration)
    hours = int(duration_in_seconds // 3600)
    minutes = int((duration_in_seconds % 3600) // 60)
    seconds = int(duration_in_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_video_duration(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails&key={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    duration = data['items'][0]['contentDetails']['duration']
    return convert_duration(duration)

def get_total_duration(filename, api_key):
    total_duration = 0
    with open(filename, 'r') as file:
        for line in file:
            video_id = line.strip().split(' ')[1]
            total_duration += get_video_duration(video_id, api_key)
    return format_duration(total_duration)

if __name__ == '__main__':
    api_key = os.getenv("YouTube_ASPEX_API_key")
    total_duration = get_total_duration('../../../../audio/dataset_1_Ru/original/downloaded.txt', api_key)
    print(f"Суммарная длительность видео: {total_duration}")
