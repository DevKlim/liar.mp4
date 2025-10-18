# AI Video Detection System

This project provides a robust pipeline for detecting AI-generated or manipulated videos. It systematically extracts frames from videos, analyzes them with a Visual Language Model (VLM), and structures the resulting metadata in a CroissantML-inspired format for model training.

## Features
- **Modular Pipeline**: Each step of the process—frame extraction, VLM labeling, and data aggregation—is a separate, executable command.
- **Centralized Configuration**: All file paths and key parameters are managed in a single configuration file for easy modification.
- **Dockerized Environment**: The entire application is containerized with Docker, ensuring a consistent and reproducible runtime environment.
- **Professional Structure**: The codebase follows standard Python project conventions for maintainability and scalability.

## Quickstart with Docker

**Prerequisites:** Docker and Docker Compose must be installed.

### 1. Place Videos
Add your source videos to the relevant subdirectories inside `data/videos/` (e.g., `data/videos/real/`, `data/videos/deepfake/`).

### 2. Build and Start the Service
From the project root, build the Docker image and start the container in the background.

```bash
docker-compose build
docker-compose up -d
```

### 3. Run the Processing Pipeline
Execute each step of the pipeline using the `docker-compose exec` command. The `main.py` script serves as the command-line interface (CLI).

**Step A: Extract Frames**
Extracts frames from all videos in the `data/videos` directory and saves them to `data/processed/frames`.

```bash
docker-compose exec analyzer python main.py extract
```

**Step B: Label Frames**
Analyzes each frame using the VLM and saves the output as individual JSON files in `data/processed/labels/individual`.

```bash
docker-compose exec analyzer python main.py label
```

**Step C: Aggregate Labels**
Combines the individual frame labels into one master JSON file per video, stored in `data/processed/labels/aggregated`.

```bash
docker-compose exec analyzer python main.py aggregate
```

### 4. Stop the Service
When you're finished, stop and remove the container. Your data in the `data/` directory will remain on your host machine.

```bash
docker-compose down
```

## Local Development (Alternative)
If you prefer not to use Docker:

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the pipeline:**
    ```bash
    python main.py extract
    python main.py label
    python main.py aggregate
    ```
