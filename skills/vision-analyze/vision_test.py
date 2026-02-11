#!/usr/bin/env python3
"""Quick Google Vision API test"""

import os
import sys
import json
import base64

# Get credentials from gcloud
creds_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
if os.path.exists(creds_path):
    with open(creds_path) as f:
        creds = json.load(f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

def analyze_image(image_path):
    """Analyze image using Google Vision API"""
    try:
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        
        with open(image_path, "rb") as f:
            content = f.read()
        
        image = vision.Image(content=content)
        
        # Label detection
        response = client.label_detection(image=image)
        labels = response.label_annotations
        
        print("🖼️  **Image Analysis:**")
        print("\n**Labels detected:**")
        for label in labels[:5]:
            print(f"  • {label.description} ({label.score*100:.1f}% confidence)")
        
        # OCR
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            print("\n**Text detected (OCR):**")
            print(f"  '{texts[0].description[:200]}...'" if len(texts[0].description) > 200 else f"  '{texts[0].description}'")
        else:
            print("\n**No text detected**")
            
        return True
        
    except ImportError:
        print("Error: google-cloud-vision not installed")
        print("Run: pip install google-cloud-vision")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vision_test.py <image-file>")
        sys.exit(1)
    
    analyze_image(sys.argv[1])
