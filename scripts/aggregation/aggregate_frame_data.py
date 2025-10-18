import os
import json
import argparse
from tqdm import tqdm
from utils.croissant_helpers import save_json

def aggregate_data(labeled_frames_dir, output_dir):
    """
    Aggregates individual frame JSON files into a single JSON file per video.
    """
    video_name = os.path.basename(labeled_frames_dir)
    json_files = sorted([f for f in os.listdir(labeled_frames_dir) if f.endswith('.json')])

    if not json_files:
        print(f"No JSON files to aggregate in {labeled_frames_dir}")
        return

    all_frames_data = []
    for file_name in json_files:
        file_path = os.path.join(labeled_frames_dir, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_frames_data.append(data)

    # Create the aggregated video-level structure
    aggregated_video_data = {
        "@context": "http://schema.org",
        "@type": "VideoObject",
        "name": video_name,
        "description": f"Aggregated AI analysis for all frames from the video '{video_name}'.",
        "hasPart": all_frames_data # Embeds all frame records
    }
    
    # Save the aggregated file
    output_filename = f"{video_name}_aggregated.json"
    output_path = os.path.join(output_dir, output_filename)
    save_json(aggregated_video_data, output_path)
    
    print(f"Aggregated {len(all_frames_data)} frames for '{video_name}' into {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Aggregate frame-level JSON data into video-level JSON files.")
    parser.add_argument("--input_dir", type=str, default="data/croissant_data/frames", help="Directory with subdirs of labeled frame JSONs.")
    parser.add_argument("--output_dir", type=str, default="data/croissant_data/videos", help="Directory to save aggregated video JSON files.")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory not found: {args.input_dir}")
        return

    video_dirs = [d for d in os.listdir(args.input_dir) if os.path.isdir(os.path.join(args.input_dir, d))]

    if not video_dirs:
        print(f"No labeled frame directories found in {args.input_dir}.")
        return

    for video_dir_name in tqdm(video_dirs, desc="Aggregating videos"):
        full_path = os.path.join(args.input_dir, video_dir_name)
        aggregate_data(full_path, args.output_dir)

if __name__ == "__main__":
    main()