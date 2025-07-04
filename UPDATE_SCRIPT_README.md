# Repository Update Script

This private script (`update_repo_data.py`) automatically updates the hero data and images in your repository from the Fribbels Epic 7 Optimizer repository.

## Features

- **Automatic Updates**: Fetches the latest hero data from Fribbels repository
- **Image Downloads**: Downloads missing hero icons and skins
- **Format Conversion**: Converts Fribbels format to your repository format
- **Git Integration**: Optional commit and push functionality
- **Update Checking**: Check for updates without downloading

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements_update.txt
   ```

## Usage

### Basic Update
```bash
python update_repo_data.py
```
This will:
- Fetch latest hero data from Fribbels
- Download any missing images
- Update your local `data/herodata.json` file

### Check for Updates Only
```bash
python update_repo_data.py --check
```
This will check if there are any updates available without downloading them.

### Update and Commit
```bash
python update_repo_data.py --commit
```
This will update the data and commit the changes to git.

### Update, Commit, and Push
```bash
python update_repo_data.py --commit --push
```
This will update the data, commit changes, and push to the remote repository.

### Custom Commit Message
```bash
python update_repo_data.py --commit --message "Add new heroes from latest update"
```

## What Gets Updated

### Hero Data (`data/herodata.json`)
- Hero information (name, code, rarity, attribute, role)
- Asset paths for icons and thumbnails
- Skin information and asset paths

### Images
- **Icons**: `data/images/icons/{hero_code}.png`
- **Skins**: `data/images/skins/{skin_code}.png`
- **Thumbnails**: `data/images/thumbnails/{hero_code}_l.png`

## Repository Format

The script converts Fribbels data to your repository format:

```json
{
  "Hero Name": {
    "code": "c1001",
    "name": "Hero Name",
    "rarity": 5,
    "attribute": "fire",
    "role": "warrior",
    "assets": {
      "icon": "images/icons/c1001.png",
      "thumbnail": "images/thumbnails/c1001_l.png"
    },
    "skins": [
      {
        "code": "c1001_s01",
        "name": "Hero Name Skin",
        "assets": {
          "icon": "images/skins/c1001_s01.png"
        }
      }
    ]
  }
}
```

## Error Handling

- **Network Issues**: The script retries failed downloads up to 3 times
- **Missing Images**: Continues with other images if some fail to download
- **Git Issues**: Provides clear error messages for git operations

## Scheduling Updates

You can set up automated updates using:

### Windows Task Scheduler
1. Open Task Scheduler
2. Create a new Basic Task
3. Set trigger (e.g., daily at 2 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `update_repo_data.py --commit --push`

### Cron Job (Linux/Mac)
```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * cd /path/to/ArkGWTrackerUploader && python update_repo_data.py --commit --push
```

## Notes

- The script is respectful to the Fribbels repository with small delays between downloads
- Only missing images are downloaded to avoid unnecessary bandwidth usage
- The script maintains your existing repository structure
- Git operations require proper authentication to be set up

## Troubleshooting

### Permission Errors
Make sure you have write permissions to the repository directory.

### Git Authentication
Ensure your git credentials are configured:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Network Issues
If downloads fail, check your internet connection and try again later.

### Missing Dependencies
Install required packages:
```bash
pip install requests pathlib2
``` 