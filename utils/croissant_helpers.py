import json
import os

def create_croissant_record_for_frame(frame_path, vlm_analysis):
    """
    Creates a CroissantML-like JSON structure for a single video frame.

    Args:
        frame_path (str): The path to the image file of the frame.
        vlm_analysis (dict): A dictionary containing the analysis from the VLM.
                             Expected keys: 'description', 'has_watermark',
                             'watermark_details', 'light_consistency_score',
                             'light_consistency_details', 'reflection_quality_score',
                             'reflection_details', 'other_artifacts'.

    Returns:
        dict: A dictionary representing the CroissantML record for the frame.
    """
    record = {
        "@context": "http://schema.org",
        "@type": "ImageObject",
        "name": os.path.basename(frame_path),
        "contentUrl": frame_path,
        "description": vlm_analysis.get("description", "No description generated."),
        "encodingFormat": "image/jpeg",
        "keywords": ["video-analysis", "ai-detection", "frame"],
        "isBasedOn": {
            "@type": "CreativeWork",
            "ai_analysis": {
                "has_watermark": vlm_analysis.get("has_watermark", None),
                "watermark_details": vlm_analysis.get("watermark_details", "N/A"),
                "light_consistency": {
                    "score": vlm_analysis.get("light_consistency_score", None),
                    "details": vlm_analysis.get("light_consistency_details", "N/A")
                },
                "reflection_quality": {
                    "score": vlm_analysis.get("reflection_quality_score", None),
                    "details": vlm_analysis.get("reflection_details", "N/A")
                },
                "other_artifacts": vlm_analysis.get("other_artifacts", [])
            }
        }
    }
    return record

def save_json(data, output_path):
    """Saves a dictionary to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)