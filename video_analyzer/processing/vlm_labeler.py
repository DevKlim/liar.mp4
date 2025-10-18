import logging
from pathlib import Path
from tqdm import tqdm
from typing import Dict, Any

from video_analyzer import config
from video_analyzer.schemas.croissant import create_frame_record
from video_analyzer.utils.file_handler import save_json

def analyze_frame_with_vlm(frame_path: Path) -> Dict[str, Any]:
    """
    Analyzes a single frame image using a VLM API.
    """
    logging.info(f"Analyzing {frame_path.name} with VLM... (mock response)")
    
    # Mock response. Replace this with a real API call to Gemini, etc.
    return {
        "description": "...",
        "has_watermark": bool,
        "watermark_details": "...",
        "light_consistency": {"score": ..., "details": "..."},
        "reflection_quality": {"score": 0.90, "details": "..."},
        "other_artifacts": ["minor background blur"]
    }

def label_frames_in_directory(frame_dir: Path, output_dir: Path):
    """Processes all frames in a given directory and saves their labels."""
    frames = sorted([p for p in frame_dir.iterdir() 
                     if p.suffix.lower() in config.IMAGE_EXTENSIONS
                     ])
    
    #checks out early if no frames in vid (0 seconds)
    if not frames:
        return

    video_name = frame_dir.name
    json_output_dir = output_dir / video_name
    json_output_dir.mkdir(parents=True, exist_ok=True)

    for frame_path in tqdm(frames, desc=f"Labeling {video_name}", unit="frame"):
        vlm_analysis = analyze_frame_with_vlm(frame_path)
        croissant_record = create_frame_record(frame_path, vlm_analysis)
        
        json_filename = frame_path.stem + ".json"
        save_json(croissant_record, json_output_dir / json_filename)
        
    logging.info(f"finished labeling for {video_name}.")

def label_all_frames():
    """Finds all directories of extracted frames and labels them."""
    logging.info(" Starting Frame Labeling Step ")
    if not config.FRAME_DIR.exists():
        logging.error("Frame directory not found. run 'extract' step first.")
        return

    frame_subdirs = [d for d in config.FRAME_DIR.iterdir() if d.is_dir()]
    if not frame_subdirs:
        logging.warning("No frame directories found to label.")
        return
    
    for frame_dir in frame_subdirs:
        label_frames_in_directory(frame_dir, config.INDIVIDUAL_LABEL_DIR)

    logging.info(" frame labeling complete ")
