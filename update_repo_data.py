#!/usr/bin/env python3
"""
Private script to update hero data and images in the ArkGWTrackerUploader repository
from the Fribbels Epic 7 Optimizer repository.

This script:
1. Fetches latest hero data from Fribbels
2. Downloads missing hero icons and skins
3. Updates the local repository files
4. Provides git commands to commit and push changes

Usage: python update_repo_data.py [--commit] [--push]
"""

import os
import json
import requests
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class RepoUpdater:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.data_path = self.base_path / "data"
        self.hero_data_path = self.data_path / "herodata.json"
        self.icons_dir = self.data_path / "images" / "icons"
        self.skins_dir = self.data_path / "images" / "skins"
        self.thumbnails_dir = self.data_path / "images" / "thumbnails"
        
        # Fribbels repository URLs
        self.fribbels_hero_data_url = "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cache/herodata.json"
        self.fribbels_image_base_url = "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cachedimages/"
        
        # Ensure directories exist
        self.icons_dir.mkdir(parents=True, exist_ok=True)
        self.skins_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnails_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_fribbels_data(self):
        """Fetch the latest hero data from Fribbels repository"""
        try:
            print("Fetching latest hero data from Fribbels repository...")
            response = requests.get(self.fribbels_hero_data_url, timeout=30)
            response.raise_for_status()
            
            hero_data = response.json()
            print(f"✓ Downloaded hero data for {len(hero_data)} heroes")
            return hero_data
            
        except Exception as e:
            print(f"✗ Failed to fetch hero data: {e}")
            return None
    
    def load_current_data(self):
        """Load the current hero data from the repository"""
        try:
            if self.hero_data_path.exists():
                with open(self.hero_data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✓ Loaded current hero data for {len(data)} heroes")
                return data
            else:
                print("No existing hero data found")
                return {}
        except Exception as e:
            print(f"✗ Failed to load current hero data: {e}")
            return {}
    
    def convert_to_repo_format(self, fribbels_data):
        """Convert Fribbels data format to repository format"""
        repo_data = {}
        
        for hero_name, hero_info in fribbels_data.items():
            if 'code' not in hero_info or 'assets' not in hero_info:
                continue
                
            code = hero_info['code']
            assets = hero_info['assets']
            
            # Extract icon URL
            icon_url = assets.get('icon', '')
            if not icon_url:
                continue
            
            # Create repository format entry
            repo_entry = {
                'code': code,
                'name': hero_info.get('name', hero_name),
                'rarity': hero_info.get('rarity', 5),
                'attribute': hero_info.get('attribute', 'fire'),
                'role': hero_info.get('role', 'warrior'),
                'assets': {
                    'icon': f"images/icons/{code}.png",
                    'thumbnail': f"images/thumbnails/{code}_l.png"
                },
                'skins': []
            }
            
            # Process skins if they exist
            if 'skins' in hero_info:
                for skin in hero_info['skins']:
                    if 'code' in skin and 'assets' in skin:
                        skin_code = skin['code']
                        skin_assets = skin['assets']
                        skin_icon_url = skin_assets.get('icon', '')
                        if skin_icon_url:
                            repo_entry['skins'].append({
                                'code': skin_code,
                                'name': skin.get('name', f"{hero_name} Skin"),
                                'assets': {
                                    'icon': f"images/skins/{skin_code}.png"
                                }
                            })
            
            repo_data[hero_name] = repo_entry
        
        return repo_data
    
    def get_existing_images(self):
        """Get separate sets of existing image filenames for each directory"""
        existing_icons = set()
        existing_skins = set()
        existing_thumbnails = set()
        
        # Check icons
        if self.icons_dir.exists():
            for file in self.icons_dir.glob("*.png"):
                existing_icons.add(file.name)
        
        # Check skins
        if self.skins_dir.exists():
            for file in self.skins_dir.glob("*.png"):
                existing_skins.add(file.name)
        
        # Check thumbnails
        if self.thumbnails_dir.exists():
            for file in self.thumbnails_dir.glob("*.png"):
                existing_thumbnails.add(file.name)
        

        
        return existing_icons, existing_skins, existing_thumbnails
    
    def download_image(self, url, filepath, retries=3):
        """Download an image from URL to filepath with retries"""
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Ensure directory exists
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return True
                
            except Exception as e:
                if attempt == retries - 1:
                    print(f"✗ Failed to download {url}: {e}")
                    return False
                else:
                    time.sleep(1)  # Wait before retry
        
        return False
    
    def download_missing_images(self, repo_data):
        """Download missing hero images"""
        existing_icons, existing_skins, existing_thumbnails = self.get_existing_images()
        missing_images = []
        
        # Collect all needed images
        for hero_name, hero_info in repo_data.items():
            # Check main icon
            icon_filename = f"{hero_info['code']}.png"
            if icon_filename not in existing_icons:
                icon_url = f"{self.fribbels_image_base_url}{hero_info['code']}_s.png"
                missing_images.append({
                    'url': icon_url,
                    'filepath': self.icons_dir / icon_filename,
                    'type': 'icon',
                    'hero': hero_name
                })
            
            # Check thumbnail
            thumbnail_filename = f"{hero_info['code']}.png"
            if thumbnail_filename not in existing_thumbnails:
                thumbnail_url = f"{self.fribbels_image_base_url}{hero_info['code']}_l.png"
                missing_images.append({
                    'url': thumbnail_url,
                    'filepath': self.thumbnails_dir / thumbnail_filename,
                    'type': 'thumbnail',
                    'hero': hero_name
                })

            
            # Check skins
            for skin in hero_info.get('skins', []):
                skin_filename = f"{skin['code']}.png"
                if skin_filename not in existing_skins:
                    skin_url = f"{self.fribbels_image_base_url}{skin['code']}.png"
                    missing_images.append({
                        'url': skin_url,
                        'filepath': self.skins_dir / skin_filename,
                        'type': 'skin',
                        'hero': hero_name,
                        'skin_code': skin['code']
                    })
        
        if not missing_images:
            print("✓ All hero images are up to date")
            return True
        
        print(f"Downloading {len(missing_images)} missing images...")
        
        # Download images with progress tracking
        successful_downloads = 0
        for i, image_info in enumerate(missing_images, 1):
            print(f"Downloading {i}/{len(missing_images)}: {image_info['hero']} ({image_info['type']})")
            
            if self.download_image(image_info['url'], image_info['filepath']):
                successful_downloads += 1
                print(f"  ✓ Downloaded {image_info['filepath'].name}")
            else:
                print(f"  ✗ Failed to download {image_info['filepath'].name}")
            
            # Small delay to be respectful to the server
            time.sleep(0.1)
        
        print(f"✓ Downloaded {successful_downloads}/{len(missing_images)} images successfully")
        return successful_downloads == len(missing_images)
    
    def save_hero_data(self, repo_data):
        """Save the hero data to the repository"""
        try:
            with open(self.hero_data_path, 'w', encoding='utf-8') as f:
                json.dump(repo_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved hero data for {len(repo_data)} heroes")
            return True
        except Exception as e:
            print(f"✗ Failed to save hero data: {e}")
            return False
    
    def check_for_updates(self):
        """Check if there are any updates available"""
        try:
            print("Checking for updates...")
            
            # Load current data
            current_data = self.load_current_data()
            if not current_data:
                print("No existing data found. Full update needed.")
                return True
            
            # Fetch latest data
            fribbels_data = self.fetch_fribbels_data()
            if not fribbels_data:
                return False
            
            # Convert to repo format
            repo_data = self.convert_to_repo_format(fribbels_data)
            
            # Compare hero counts
            if len(repo_data) != len(current_data):
                print(f"Hero count changed: {len(current_data)} -> {len(repo_data)}")
                return True
            
            # Check for new heroes
            current_codes = {hero_info['code'] for hero_info in current_data.values()}
            new_codes = {hero_info['code'] for hero_info in repo_data.values()}
            
            if new_codes != current_codes:
                new_heroes = new_codes - current_codes
                removed_heroes = current_codes - new_codes
                if new_heroes:
                    print(f"Found {len(new_heroes)} new heroes: {', '.join(new_heroes)}")
                if removed_heroes:
                    print(f"Found {len(removed_heroes)} removed heroes: {', '.join(removed_heroes)}")
                return True
            
            # Check for missing images
            existing_icons, existing_skins, existing_thumbnails = self.get_existing_images()
            missing_count = 0
            
            for hero_name, hero_info in repo_data.items():
                # Check main icon
                icon_filename = f"{hero_info['code']}.png"
                if icon_filename not in existing_icons:
                    missing_count += 1
                
                # Check thumbnail
                thumbnail_filename = f"{hero_info['code']}.png"
                if thumbnail_filename not in existing_thumbnails:
                    missing_count += 1
                
                # Check skins
                for skin in hero_info.get('skins', []):
                    skin_filename = f"{skin['code']}.png"
                    if skin_filename not in existing_skins:
                        missing_count += 1
            
            if missing_count > 0:
                print(f"Found {missing_count} missing images")
                return True
            else:
                print("All hero data and images are up to date")
                return False
                
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False
    
    def update_all(self):
        """Perform a complete update of hero data and images"""
        print("Starting repository update...")
        
        # Fetch latest data from Fribbels
        fribbels_data = self.fetch_fribbels_data()
        if not fribbels_data:
            print("Failed to fetch hero data. Update aborted.")
            return False
        
        # Convert to repository format
        repo_data = self.convert_to_repo_format(fribbels_data)
        if not repo_data:
            print("Failed to convert hero data. Update aborted.")
            return False
        
        # Save the hero data
        if not self.save_hero_data(repo_data):
            print("Failed to save hero data. Update aborted.")
            return False
        
        # Download missing images
        success = self.download_missing_images(repo_data)
        
        if success:
            print("✓ Repository update completed successfully!")
        else:
            print("⚠ Repository update completed with some errors.")
        
        return success
    
    def git_commit(self, message=None):
        """Commit changes to git"""
        try:
            if not message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"Update hero data and images - {timestamp}"
            
            # Add all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            print("✓ Added changes to git")
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
            print(f"✓ Committed changes: {message}")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Git commit failed: {e}")
            return False
    
    def git_push(self):
        """Push changes to remote repository"""
        try:
            subprocess.run(["git", "push"], check=True, capture_output=True)
            print("✓ Pushed changes to remote repository")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Git push failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Update hero data and images in the repository")
    parser.add_argument("--commit", action="store_true", help="Commit changes to git")
    parser.add_argument("--push", action="store_true", help="Push changes to remote repository")
    parser.add_argument("--check", action="store_true", help="Only check for updates, don't download")
    parser.add_argument("--message", type=str, help="Custom commit message")
    
    args = parser.parse_args()
    
    updater = RepoUpdater()
    
    if args.check:
        # Only check for updates
        if updater.check_for_updates():
            print("\nUpdates are available. Run without --check to download them.")
        else:
            print("\nNo updates needed.")
    else:
        # Perform full update
        if updater.update_all():
            if args.commit:
                message = args.message
                if updater.git_commit(message):
                    if args.push:
                        updater.git_push()
                else:
                    print("Failed to commit changes.")
        else:
            print("Update failed.")

if __name__ == "__main__":
    main() 