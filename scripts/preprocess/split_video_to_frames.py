import cv2
import os
import argparse
from tqdm import tqdm

def split_video(video_path, output_dir, interval_sec):
    """
    Splits a video into frames at a specified interval.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save the extracted frames.
        interval_sec (int): The interval in seconds at which to capture frames.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_output_dir = os.path.join(output_dir, video_name)
    os.makedirs(frame_output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print(f"Warning: Could not determine FPS for {video_path}. Assuming 30 FPS.")
        fps = 30 # Default FPS if not available

    frame_interval = int(fps * interval_sec)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_count = 0
    saved_frame_count = 0

    with tqdm(total=total_frames, desc=f"Processing {video_name}") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_filename = f"{video_name}_frame_{saved_frame_count:05d}.jpg"
                output_path = os.path.join(frame_output_dir, frame_filename)
                cv2.imwrite(output_path, frame)
                saved_frame_count += 1
            
            frame_count += 1
            pbar.update(1)

    cap.release()
    print(f"Finished processing {video_name}. Saved {saved_frame_count} frames to {frame_output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Split videos into frames at a specified interval.")
    parser.add_argument("--videos_dir", type=str, default="data/videos", help="Directory containing video categories (real, deepfake, etc.).")
    parser.add_argument("--frames_dir", type=str, default="data/frames", help="Root directory to save the extracted frames.")
    parser.add_argument("--interval", type=int, default=2, help="Interval in seconds between frame captures.")
    args = parser.parse_args()

    print(f"Starting video processing...")
    print(f"Input video directory: {args.videos_dir}")
    print(f"Output frames directory: {args.frames_dir}")
    print(f"Frame capture interval: {args.interval} seconds")

    if not os.path.isdir(args.videos_dir):
        print(f"Error: The specified video directory does not exist: {args.videos_dir}")
        return

    # Find all video files in subdirectories
    video_files = []
    for root, _, files in os.walk(args.videos_dir):
        for file in files:
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_files.append(os.path.join(root, file))

    if not video_files:
        print("No video files found. Please place videos in subdirectories of 'data/videos/'.")
        return
        
    for video_path in video_files:
        split_video(video_path, args.frames_dir, args.interval)

if __name__ == "__main__":
    main()