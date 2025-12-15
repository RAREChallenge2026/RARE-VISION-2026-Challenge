#!/usr/bin/env python3
import requests
import json
import os
import subprocess
from pathlib import Path
import time
from tqdm import tqdm

def download_galar_api():
    ARTICLE_ID = "25304616"
    DATA_DIR = Path("./galar_dataset")
    DOWNLOADS_DIR = DATA_DIR / "downloads"
    
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Fetching file list from Figshare API...")
    api_url = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}/files"
    
    response = requests.get(api_url)
    response.raise_for_status()
    files = response.json()
    
    print(f"Found {len(files)} files totaling ~562GB")
    
    for file_info in tqdm(files, desc="Downloading"):
        filename = file_info['name']
        download_url = file_info['download_url']
        filesize = file_info.get('size', 0) / (1024**3)
        
        if not filename.endswith(('.7z', '.zip')):
            print(f"Skipping non-archive: {filename}")
            continue
            
        output_path = DOWNLOADS_DIR / filename
        if output_path.exists():
            print(f"Already exists: {filename} ({filesize:.1f}GB)")
            continue
        
        print(f"\nDownloading {filename} ({filesize:.1f}GB)...")
        try:
            cmd = [
                "wget", "-c", "--tries=3", "--timeout=60",
                "--progress=bar:force:noscroll",
                "-O", str(output_path), download_url
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to download {filename}")
            continue
    
    print("\nExtracting archives...")
    archives = list(DOWNLOADS_DIR.glob("*.7z")) + list(DOWNLOADS_DIR.glob("*.zip"))
    
    for archive in tqdm(archives, desc="Extracting"):
        print(f"Extracting {archive.name}...")
        try:
            if archive.suffix == '.7z':
                subprocess.run(["7z", "x", str(archive), "-y", "-o" + str(DOWNLOADS_DIR)], 
                             check=True, capture_output=True)
            else:
                subprocess.run(["unzip", "-q", str(archive), "-d", str(DOWNLOADS_DIR)], 
                             check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Extraction failed for {archive.name}: {e}")
    
    print(f"\nDataset ready in {DATA_DIR}")
    print(f"Total size: {sum(f.stat().st_size for f in DATA_DIR.rglob('*') if f.is_file()) / (1024**3):.1f}GB")

if __name__ == "__main__":
    download_galar_api()
