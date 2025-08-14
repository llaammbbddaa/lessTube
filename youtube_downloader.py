#!/usr/bin/env python3
import csv
import os
import json
import subprocess
import sys
from datetime import datetime, timedelta

# Configuration
CSV_FILE = 'subs.csv'
VIDEO_DIR = 'downloaded_videos'
DOWNLOADED_VIDEOS_FILE = 'downloaded_videos.json'
MAX_VIDEOS_PER_CHANNEL = 1  # Limit to avoid downloading too many videos at once

def load_downloaded_videos():
    """Load the list of already downloaded videos from a JSON file."""
    if os.path.exists(DOWNLOADED_VIDEOS_FILE):
        with open(DOWNLOADED_VIDEOS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_downloaded_videos(downloaded_videos):
    """Save the list of downloaded videos to a JSON file."""
    with open(DOWNLOADED_VIDEOS_FILE, 'w') as f:
        json.dump(downloaded_videos, f, indent=2)

def read_channels_from_csv():
    """Read channel information from the CSV file."""
    channels = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            channels.append({
                'id': row['Channel Id'],
                'url': row['Channel Url'],
                'title': row['Channel Title']
            })
    return channels

def is_video_recent(upload_date_str):
    """Check if a video was uploaded within the last 2 days."""
    return True
    try:
        # Parse the upload date (format: YYYYMMDD)
        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
        # Get the date 2 days ago
        two_days_ago = datetime.now() - timedelta(days=2)
        # Check if the upload date is within the last 2 days
        return upload_date >= two_days_ago
    except ValueError:
        # If we can't parse the date, assume it's not recent
        print(upload_data_str)
        print("return false date")
        return False

def download_latest_videos(channel, downloaded_videos):
    """Download the latest videos from a channel that haven't been downloaded yet."""
    channel_id = channel['id']
    channel_title = channel['title']
    
    # Create directory for this channel if it doesn't exist
    channel_dir = os.path.join(VIDEO_DIR, channel_title)
    os.makedirs(channel_dir, exist_ok=True)
    
    # Check if we've already downloaded videos from this channel
    if channel_id not in downloaded_videos:
        downloaded_videos[channel_id] = []
    
    # Use yt-dlp to get the latest videos from the channel with upload dates
    try:
        # Get the latest videos from the channel (limit to MAX_VIDEOS_PER_CHANNEL)
        # Only get videos from the last 2 days
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--playlist-end', str(MAX_VIDEOS_PER_CHANNEL),
            '--print-json',
            '--no-warnings',
            '--dateafter', 'today-2days',
            f"{channel['url']}/videos"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error getting videos for channel {channel_title}: {result.stderr}")
            return downloaded_videos
            
        # Parse the video information
        video_data = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    video_info = json.loads(line)
                    video_data.append(video_info)
                except json.JSONDecodeError:
                    continue
        
        # Download videos that haven't been downloaded yet and are recent
        new_videos_downloaded = 0
        for video_info in video_data:
            video_id = video_info['id']
            # Check if the video was uploaded within the last 2 days
            upload_date = video_info.get('upload_date', '')
            if not is_video_recent(upload_date):
                continue  # Skip this video if it's not recent
            
            if video_id not in downloaded_videos[channel_id]:
                # Download the video
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                download_cmd = [
                    'yt-dlp',
                    '-o', os.path.join(channel_dir, '%(title)s.%(ext)s'),
                    '--no-overwrites',
                    '--no-post-overwrites',
                    '--add-metadata',
                    '--write-info-json',
                    video_url
                ]
                
                print(f"Downloading video {video_id} from channel {channel_title}")
                result = subprocess.run(download_cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    downloaded_videos[channel_id].append(video_id)
                    new_videos_downloaded += 1
                else:
                    print(f"Error downloading video {video_id}: {result.stderr}")
        
        if new_videos_downloaded > 0:
            print(f"Downloaded {new_videos_downloaded} new videos from {channel_title}")
        else:
            print(f"No new videos to download from {channel_title}")
            
    except Exception as e:
        print(f"Error processing channel {channel_title}: {str(e)}")
    
    return downloaded_videos

def main():
    """Main function to download new videos from all channels."""
    # Create the main video directory
    os.makedirs(VIDEO_DIR, exist_ok=True)
    
    # Load previously downloaded videos
    downloaded_videos = load_downloaded_videos()
    
    # Read channels from CSV
    channels = read_channels_from_csv()
    print(f"Found {len(channels)} channels in CSV file")
    
    # Download latest videos from each channel
    for channel in channels:
        print(f"Processing channel: {channel['title']}")
        downloaded_videos = download_latest_videos(channel, downloaded_videos)
    
    # Save the updated list of downloaded videos
    save_downloaded_videos(downloaded_videos)
    print("Finished downloading videos")

if __name__ == "__main__":
    main()
