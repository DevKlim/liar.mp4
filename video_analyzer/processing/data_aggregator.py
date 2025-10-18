import json
import logging
from pathlib import Path
from tqdm import tqdm

from video_analyzer import config
from video_analyzer.schemas.croissant import create_video_record
from video_analyzer.utils.file_handler import save_json

def aggregate_labels_for_video(label_dir: Path, output_dir: Path):
    """Aggregates all individual JSON labels for a single video."""
    json_files = sorted(label_dir.glob("*.json"))
    if not json_files:
        return

    video_name = label_dir.name
    all_frame_records = []
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            all_frame_records.append(json.load(f))

    aggregated_record = create_video_record(video_name, all_frame_records)
    output_path = output_dir / f"{video_name}_aggregated.json"
    save_json(aggregated_record, output_path)
    logging.info(f"Aggregated {len(all_frame_records)} labels for {video_name}.")

def aggregate_all_labels():
    """Finds all directories of individual labels and aggregates them."""
    logging.info("--- Starting Label Aggregation Step ---")
    if not config.INDIVIDUAL_LABEL_DIR.exists():
        logging.error("Individual labels directory not found. Please run the 'label' step first.")
        return

    label_subdirs = [d for d in config.INDIVIDUAL_LABEL_DIR.iterdir() if d.is_dir()]
    if not label_subdirs:
        logging.warning("No individual label directories found to aggregate.")
        return
        
    for label_dir in tqdm(label_subdirs, desc="Aggregating videos"):
        aggregate_labels_for_video(label_dir, config.AGGREGATED_LABEL_DIR)
        
    logging.info("--- Label Aggregation Complete ---")