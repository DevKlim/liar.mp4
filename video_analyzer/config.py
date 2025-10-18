from pathlib import Path

# Base project directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# --- Data Paths ---
DATA_DIR = PROJECT_ROOT / "data"
RAW_VIDEO_DIR = DATA_DIR / "videos"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# --- Processed Data Subdirectories ---
FRAME_DIR = PROCESSED_DATA_DIR / "frames"
LABEL_DIR = PROCESSED_DATA_DIR / "labels"
INDIVIDUAL_LABEL_DIR = LABEL_DIR / "individual"
AGGREGATED_LABEL_DIR = LABEL_DIR / "aggregated"

# --- Processing Parameters ---
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
FRAME_EXTRACTION_INTERVAL_SEC = 2 # Every other second
