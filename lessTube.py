#!/usr/bin/env python3
import os
import sys
import json
import random
import subprocess
import argparse
from pathlib import Path

# Configuration
BASE_DIR = '/home/arshilegorky/lessYoutube'
VIDEO_DIR = os.path.join(BASE_DIR, 'downloaded_videos')
DOWNLOADED_VIDEOS_FILE = os.path.join(BASE_DIR, 'downloaded_videos.json')

# New helper function for sorting videos by upload date
def sort_videos_by_upload_date(videos):
    """Sort videos by upload date (newest first), videos without date at the end."""
    # Separate videos with and without upload dates
    with_dates = [v for v in videos if v['upload_date']]
    without_dates = [v for v in videos if not v['upload_date']]
    
    # Sort videos with dates in descending order (newest first)
    with_dates.sort(key=lambda x: x['upload_date'], reverse=True)
    
    # Combine lists (videos with dates first, then without)
    return with_dates + without_dates

def get_all_videos():
    """Get all videos from the downloaded_videos directory including misc folder."""
    videos = []
    if not os.path.exists(VIDEO_DIR):
        return videos
    
    # Supported video extensions
    video_extensions = ('.mp4', '.webm', '.mkv', '.avi', '.mov')
    
    # Walk through all directories and find video files
    for root, dirs, files in os.walk(VIDEO_DIR):
        for file in files:
            # Skip info.json files - we'll handle them through video files
            if file.endswith('.info.json'):
                continue
                
            # Process video files
            if file.lower().endswith(video_extensions):
                video_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                info_path = os.path.join(root, base_name + '.info.json')
                channel_name = os.path.basename(root)
                
                # Handle videos with metadata
                if os.path.exists(info_path):
                    try:
                        with open(info_path, 'r') as f:
                            info = json.load(f)
                        
                        videos.append({
                            'title': info.get('title', 'Unknown Title'),
                            'channel': channel_name,
                            'path': video_path,
                            'id': info.get('id', ''),
                            'upload_date': info.get('upload_date', '')
                        })
                    except Exception as e:
                        print(f"Error reading {info_path}: {e}")
                        # Fallback to filename as title
                        videos.append({
                            'title': base_name,
                            'channel': channel_name,
                            'path': video_path,
                            'id': '',
                            'upload_date': ''
                        })
                
                # Handle miscellaneous videos without metadata
                else:
                    videos.append({
                        'title': base_name,  # Use filename as title
                        'channel': channel_name,
                        'path': video_path,
                        'id': '',
                        'upload_date': ''
                    })
    
    return videos

    
def list_videos(videos, channel_filter=None):
    """List all videos, optionally filtered by channel."""
    if channel_filter:
        videos = [v for v in videos if channel_filter.lower() in v['channel'].lower()]
    
    if not videos:
        print("No videos found.")
        return
    
    # Sort videos by upload date before listing
    videos = sort_videos_by_upload_date(videos)  # <-- ADDED SORTING

    print(f"Found {len(videos)} videos:")
    for i, video in enumerate(videos, 1):
        print(f"{i:3d}. {video['title']}")
        print(f"      Channel: {video['channel']}")
        print(f"      Date: {video['upload_date']}")
        print()

def search_videos(videos, search_term):
    """Search videos by title."""
    search_term = search_term.lower()
    matching_videos = [v for v in videos if search_term in v['title'].lower()]
    
    if not matching_videos:
        print(f"No videos found matching '{search_term}'.")
        return
    
    # Sort matching videos by upload date
    matching_videos = sort_videos_by_upload_date(matching_videos)  # <-- ADDED SORTING

    print(f"Found {len(matching_videos)} videos matching '{search_term}':")
    for i, video in enumerate(matching_videos, 1):
        print(f"{i:3d}. {video['title']}")
        print(f"      Channel: {video['channel']}")
        print(f"      Date: {video['upload_date']}")
        print()

def play_random_video(videos):
    """Play a random video."""
    if not videos:
        print("No videos available to play.")
        return
    
    video = random.choice(videos)
    print(f"Playing: {video['title']}")
    print(f"Channel: {video['channel']}")
    
    # Try to play the video with VLC
    try:
        result = subprocess.run(['vlc', video['path']], check=True)
    except FileNotFoundError:
        # VLC not found, try mpv as fallback
        try:
            subprocess.run(['mpv', video['path']], check=True)
        except FileNotFoundError:
            print("Error: Neither VLC nor mpv player found. Please install VLC or mpv to play videos.")
            print("For VLC:")
            print("  On Ubuntu/Debian: sudo apt install vlc")
            print("  On Fedora: sudo dnf install vlc")
            print("  On macOS: brew install vlc")
            print("For mpv:")
            print("  On Ubuntu/Debian: sudo apt install mpv")
            print("  On Fedora: sudo dnf install mpv")
            print("  On macOS: brew install mpv")
        except subprocess.CalledProcessError:
            print("Error playing video with mpv.")
    except subprocess.CalledProcessError:
        # VLC encountered an error, try mpv as fallback
        try:
            subprocess.run(['mpv', video['path']], check=True)
        except FileNotFoundError:
            print("Error: Neither VLC nor mpv player found. Please install VLC or mpv to play videos.")
            print("For VLC:")
            print("  On Ubuntu/Debian: sudo apt install vlc")
            print("  On Fedora: sudo dnf install vlc")
            print("  On macOS: brew install vlc")
            print("For mpv:")
            print("  On Ubuntu/Debian: sudo apt install mpv")
            print("  On Fedora: sudo dnf install mpv")
            print("  On macOS: brew install mpv")
        except subprocess.CalledProcessError:
            print("Error playing video with mpv.")

def play_video_by_index(videos, index):
    """Play a video by its index number."""
    if not videos:
        print("No videos available to play.")
        return
    
    if index < 1 or index > len(videos):
        print(f"Invalid video index. Please choose a number between 1 and {len(videos)}.")
        return
    
    # Get the video at the specified index (1-based indexing)
    videos = sort_videos_by_upload_date(videos)
    video = videos[index - 1]
    print(f"Playing: {video['title']}")
    print(f"Channel: {video['channel']}")
    
    # Try to play the video with VLC
    try:
        result = subprocess.run(['vlc', video['path']], check=True)
    except FileNotFoundError:
        # VLC not found, try mpv as fallback
        try:
            subprocess.run(['mpv', video['path']], check=True)
        except FileNotFoundError:
            print("Error: Neither VLC nor mpv player found. Please install VLC or mpv to play videos.")
            print("For VLC:")
            print("  On Ubuntu/Debian: sudo apt install vlc")
            print("  On Fedora: sudo dnf install vlc")
            print("  On macOS: brew install vlc")
            print("For mpv:")
            print("  On Ubuntu/Debian: sudo apt install mpv")
            print("  On Fedora: sudo dnf install mpv")
            print("  On macOS: brew install mpv")
        except subprocess.CalledProcessError:
            print("Error playing video with mpv.")
    except subprocess.CalledProcessError:
        # VLC encountered an error, try mpv as fallback
        try:
            subprocess.run(['mpv', video['path']], check=True)
        except FileNotFoundError:
            print("Error: Neither VLC nor mpv player found. Please install VLC or mpv to play videos.")
            print("For VLC:")
            print("  On Ubuntu/Debian: sudo apt install vlc")
            print("  On Fedora: sudo dnf install vlc")
            print("  On macOS: brew install vlc")
            print("For mpv:")
            print("  On Ubuntu/Debian: sudo apt install mpv")
            print("  On Fedora: sudo dnf install mpv")
            print("  On macOS: brew install mpv")
        except subprocess.CalledProcessError:
            print("Error playing video with mpv.")

def run_downloader():
    """Run the youtube_downloader.py script located in the same directory."""
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    downloader_script = os.path.join(BASE_DIR, "youtube_downloader.py")
    
    if not os.path.exists(downloader_script):
        print(f"Error: youtube_downloader.py not found in {current_dir}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, downloader_script], check=True)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running youtube_downloader.py: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Search and play downloaded YouTube videos')
    # Add new download flag
    parser.add_argument('-d', '--download', action='store_true', 
                        help='Run youtube_downloader.py to download new videos')
    # Existing flags
    parser.add_argument('-r', '--random', action='store_true', help='Play a random video')
    parser.add_argument('-s', '--search', help='Search videos by title')
    parser.add_argument('-l', '--list', nargs='?', const='all', help='List videos (optionally from a specific channel)')
    parser.add_argument('-p', '--play', type=int, help='Play a video by its index number')
    parser.add_argument('path', nargs='?', default='.', help='Path to search in (default: current directory)')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Run downloader first if requested
    if args.download:
        run_downloader()
    
    # Get videos (reload if download was run)
    videos = get_all_videos()
    
    # Process other commands
    if args.random:
        play_random_video(videos)
    elif args.search:
        search_videos(videos, args.search)
    elif args.play:
        play_video_by_index(videos, args.play)
    elif args.list:
        if args.list == 'all':
            list_videos(videos)
        else:
            list_videos(videos, args.list)
    elif not args.download:  # Show help if only -d was used
        parser.print_help()

if __name__ == "__main__":
    main()
