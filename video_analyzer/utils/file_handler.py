import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any

from video_analyzer import config

def find_video_files(directory: Path) -> List[Path]:
    """Recursively finds all video files in a directory."""
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(config.VIDEO_EXTENSIONS):
                video_files.append(Path(root) / file)
    return video_files

def save_json(data: Dict[str, Any], output_path: Path):
    """Saves a dictionary to a JSON file."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to write JSON to {output_path}: {e}")