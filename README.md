# lessYoutube

A comprehensive solution for automatically downloading and managing YouTube content from your favorite channels.

## Features

- Automatically downloads new videos from subscribed YouTube channels
- Runs on system startup to keep your collection up-to-date
- Terminal-based search engine to browse and play your downloaded content
- Supports filtering by channel, searching by title, and random playback

## Components

### 1. YouTube Downloader (`youtube_downloader.py`)

Automatically downloads new videos from channels listed in `subs.csv`. It only downloads videos from the last 2 days to ensure content is current.

#### Features:
- Reads channel information from `subs.csv`
- Downloads only recent videos (last 2 days)
- Avoids downloading duplicates using a tracking system
- Organizes videos in folders by channel name
- Uses yt-dlp for reliable video downloading

### 2. Terminal Search Engine (`lessTube`)

A command-line tool to browse and play your downloaded videos.

#### Features:
- List all videos or filter by channel
- Search videos by title keywords
- Play a random video or specific video by index
- Uses VLC as primary player with mpv fallback

## Installation

1. Clone or download this repository to `~/lessYoutube`
2. Install required dependencies:
   ```bash
   pipx install yt-dlp
   sudo apt install vlc mpv  # For video playback (optional but recommended)
   ```
3. Make sure the scripts are executable:
   ```bash
   chmod +x youtube_downloader.py lessTube
   ```
4. Set up automatic startup:
   ```bash
   mkdir -p ~/.config/systemd/user/
   cp youtube-downloader.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable youtube-downloader.service
   ```

## Usage

### YouTube Downloader

The downloader runs automatically on system startup. To run manually:
```bash
./youtube_downloader.py
```

### lessTube Search Engine

Access your videos from anywhere using the `lessTube` command:

```bash
lessTube -l              # List all videos
lessTube -l "Reject"     # List videos from channels containing "Reject"
lessTube -s "Plants"     # Search for videos with "Plants" in the title
lessTube -r              # Play a random video
lessTube -p 3            # Play the video at index 3 from the last listing
```

## File Structure

```
~/lessYoutube/
├── subs.csv              # Your YouTube channel subscriptions
├── youtube_downloader.py # Automatic video downloader
├── lessTube              # Terminal search and playback tool
├── downloaded_videos/    # Downloaded videos organized by channel
├── downloaded_videos.json # Tracks downloaded videos to avoid duplicates
└── youtube-downloader.service # Systemd service for automatic startup
```

## Configuration

### Adding Channels

Add or remove channels by editing `subs.csv`:
```csv
Channel Id,Channel Url,Channel Title
UC-ufRLYrXxrIEApGn9VG5pQ,http://www.youtube.com/channel/UC-ufRLYrXxrIEApGn9VG5pQ,Reject Convenience
```

### Adjusting Download Settings

Modify `youtube_downloader.py` to change:
- Date range for downloads (`--dateafter` parameter)
- Maximum videos per channel (`MAX_VIDEOS_PER_CHANNEL`)

## Troubleshooting

### Videos Not Downloading
- Check your internet connection
- Verify channel URLs in `subs.csv` are correct
- Ensure yt-dlp is properly installed

### Playback Issues
- Make sure VLC or mpv is installed
- Check that video files exist in `downloaded_videos/` folders
- Verify file permissions

### Startup Service Not Working
- Check that the service file is in the correct location
- Run `systemctl --user status youtube-downloader.service` to check service status
- Review systemd logs with `journalctl --user-unit youtube-downloader.service`

## Requirements

- Python 3.6+
- yt-dlp
- VLC or mpv (for video playback)
- systemd (for automatic startup)

## License

This project is open-source and available under the MIT License.