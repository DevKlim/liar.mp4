from pathlib import Path
from typing import Dict, Any

def create_frame_record(frame_path: Path, vlm_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a CroissantML-inspired JSON structure for a single video frame."""
    record = {
        "@context": "http://schema.org",
        "@type": "ImageObject",
        "name": frame_path.name,
        "contentUrl": str(frame_path.relative_to(frame_path.parents[2])), # Relative path
        "description": vlm_analysis.get("description", "No description provided."),
        "encodingFormat": "image/jpeg",
        "isBasedOn": {
            "@type": "CreativeWork",
            "ai_analysis": {
                "has_watermark": vlm_analysis.get("has_watermark"),
                "watermark_details": vlm_analysis.get("watermark_details"),
                "light_consistency": vlm_analysis.get("light_consistency"),
                "reflection_quality": vlm_analysis.get("reflection_quality"),
                "other_artifacts": vlm_analysis.get("other_artifacts", [])
            }
        }
    }
    return record

def create_video_record(video_name: str, frame_records: list) -> Dict[str, Any]:
    """Creates an aggregated CroissantML-like record for a video."""
    return {
        "@context": "http://schema.org",
        "@type": "VideoObject",
        "name": video_name,
        "description": f"Aggregated AI analysis for all frames from the video '{video_name}'.",
        "hasPart": frame_records
    }