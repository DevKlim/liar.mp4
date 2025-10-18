import argparse
import logging

from video_analyzer.processing.frame_extractor import process_all_videos
from video_analyzer.processing.vlm_labeler import label_all_frames
from video_analyzer.processing.data_aggregator import aggregate_all_labels

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main CLI entry point for the video analysis pipeline."""
    parser = argparse.ArgumentParser(description="Video Analysis Pipeline CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Command to extract frames from videos
    parser_extract = subparsers.add_parser("extract", help="Extract frames from videos.")
    parser_extract.set_defaults(func=process_all_videos)

    # Command to label frames using a VLM
    parser_label = subparsers.add_parser("label", help="Label extracted frames with a VLM.")
    parser_label.set_defaults(func=label_all_frames)

    # Command to aggregate individual frame labels
    parser_aggregate = subparsers.add_parser("aggregate", help="Aggregate frame labels into video-level files.")
    parser_aggregate.set_defaults(func=aggregate_all_labels)

    args = parser.parse_args()
    args.func()

if __name__ == "__main__":
    main()