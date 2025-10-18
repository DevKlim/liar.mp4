import cv2
import logging
from pathlib import Path
from tqdm import tqdm

from video_analyzer import config
from video_analyzer.utils.file_handler import find_video_files

def extract_frames(video_path: Path, output_dir: Path, interval_sec: int):
    """Extracts frames from a single video file."""
    video_name = video_path.stem
    frame_output_dir = output_dir / video_name
    frame_output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logging.error(f"Could not open video file: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        logging.warning(f"Could not determine FPS for {video_path}. Assuming 30.")
        fps = 30

    frame_interval = int(fps * interval_sec)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_cursor = 0
    saved_frame_count = 0

    with tqdm(total=total_frames, desc=f"Extracting {video_name}", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_cursor % frame_interval == 0:
                frame_filename = f"{video_name}_frame_{saved_frame_count:05d}.jpg"
                cv2.imwrite(str(frame_output_dir / frame_filename), frame)
                saved_frame_count += 1
            
            frame_cursor += 1
            pbar.update(1)

    cap.release()
    logging.info(f"Saved {saved_frame_count} frames from {video_name} to {frame_output_dir}")

def process_all_videos():
    """Finds and processes all videos in the raw data directory."""
    logging.info(" Starting Frame Extraction Step ")
    video_files = find_video_files(config.RAW_VIDEO_DIR)

    if not video_files:
        logging.warning("No video files found. Please add videos to data/videos.")
        return

    for video_path in video_files:
        extract_frames(
            video_path,
            config.FRAME_DIR,
            config.FRAME_EXTRACTION_INTERVAL_SEC
        )
    logging.info(" Frame Extraction Complete ")
