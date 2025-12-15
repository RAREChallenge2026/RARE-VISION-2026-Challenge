#!/usr/bin/env python3
import pandas as pd
import os
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import argparse

def split_galar_dataset(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    base_dir = Path("./galar_dataset")
    frames_dirs = [
        "Galar_Frames_1_to_10", "Galar_Frames_11_to_20", "Galar_Frames_21_to_29_2",
        "Galar_Frames_31_to_40", "Galar_Frames_41_to_50", "Galar_Frames_51_to_60",
        "Galar_Frames_61_to_70", "Galar_Frames_71_to_80_v2"
    ]
    labels_dir = base_dir / "Galar_labels_and_metadata/labels"
    
    output_dir = base_dir / "splits"
    output_dir.mkdir(exist_ok=True)
    
    all_recordings = {}
    
    print("Loading all CSV label files...")
    for csv_file in tqdm(sorted(labels_dir.glob("*.csv"))):
        recording_num = csv_file.stem
        df = pd.read_csv(csv_file)
        
        df['index'] = df['index'].astype(str).str.zfill(6)
        df['image_path'] = f"Galar_Frames_{recording_num.split('_')[1]}/recording_{recording_num}/frame_{df['index']}.png"
        df['recording'] = recording_num
        
        all_recordings[recording_num] = df
    
    print(f"Loaded {len(all_recordings)} recordings")
    
    recording_ids = list(all_recordings.keys())
    
    val_test_ratio = 1 - train_ratio
    train_ids, temp_ids = train_test_split(recording_ids, test_size=val_test_ratio, random_state=42)
    val_ids, test_ids = train_test_split(temp_ids, test_size=test_ratio/(val_test_ratio), random_state=42)
    
    splits = {
        'train': train_ids,
        'val': val_ids, 
        'test': test_ids
    }
    
    print(f"Split ratios - Train: {train_ratio:.1%}, Val: {val_ratio:.1%}, Test: {test_ratio:.1%}")
    print(f"Split sizes - Train: {len(train_ids)}, Val: {len(val_ids)}, Test: {len(test_ids)}")
    
    for split_name, ids in splits.items():
        split_df = pd.concat([all_recordings[rid] for rid in ids], ignore_index=True)
        output_path = output_dir / f"{split_name}.csv"
        split_df.to_csv(output_path, index=False)
        print(f"Saved {len(split_df)} samples to {output_path}")
    
    print(f"Splits saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Galar dataset into train/val/test")
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Train split ratio (default: 0.7)")
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation split ratio (default: 0.15)")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test split ratio (default: 0.15)")
    args = parser.parse_args()
    
    split_galar_dataset(args.train_ratio, args.val_ratio, args.test_ratio)
