import os
import subprocess
import platform
from pathlib import Path

def play_sound():
    if platform.system() == 'Windows':
        import winsound
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    else:  # Linux
        os.system('aplay /usr/share/sounds/gnome/default/alerts/drip.ogg')

def main(file_path, output_dir, save_by_playlist=False):
    '''
    This script is used to download youtube playlists, easily and simply for datasets.
    Follow the comments below.
    '''

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Path to the download archive file
    download_archive = os.path.join(output_dir, 'downloaded.txt')

    # Open file and read each line (each URL)
    with open(file_path, 'r') as file:
        for line in file:
            playlist_url = line.strip()  # Remove any leading/trailing whitespace

            if playlist_url:  # If the line is not empty
                print(f'Downloading playlist: {playlist_url}')

                if save_by_playlist:
                    output_template = os.path.join(output_dir, '%(playlist_title)s/%(title)s.%(ext)s')
                else:
                    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

                # Define the yt-dlp command
                yt_dlp_cmd = [
                    'yt-dlp',
                    '-i',  # Ignore errors
                    '-o', output_template,  # Output template
                    '--no-part',  # Do not use .part files
                    '-f', 'bestaudio',  # Select the best audio quality
                    '--extract-audio',  # Only extract audio, not video
                    '--download-archive', download_archive,  # Skip videos listed in the archive file
                    playlist_url  # URL of the video or playlist you want to download
                ]

                # Run the command
                try:
                    subprocess.run(yt_dlp_cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f'An error occurred while downloading the playlist: {playlist_url}')
                    print(str(e))

    # Play a sound when all downloads are finished
    play_sound()

if __name__ == "__main__":
    # Path to the text file containing YouTube playlist URLs
    file_path = '../../../audio/dataset_3_Ru/youtube_download_links_3.txt'
    # Prompt for the output directory
    output_dir = '../../../audio/dataset_3_Ru/'
    # Set save_by_playlist to True to create subfolders for each playlist
    save_by_playlist = True
    main(file_path, output_dir, save_by_playlist)