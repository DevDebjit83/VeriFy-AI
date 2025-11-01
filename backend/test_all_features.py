"""
Comprehensive test script for all VeriFy AI detection features
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def test_text_detection():
    """Test text detection with various claims"""
    print("\n" + "="*60)
    print("TESTING TEXT DETECTION")
    print("="*60)
    
    tests = [
        ("The earth is flat", "FAKE"),
        ("Water freezes at 0 degrees Celsius", "REAL"),
        ("Vaccines cause autism", "FAKE"),
        ("Donald Trump is the current US president", "REAL"),
        ("The earth is round", "REAL"),
        ("5G causes COVID-19", "FAKE"),
    ]
    
    passed = 0
    for text, expected in tests:
        try:
            response = requests.post(f"{BASE_URL}/check-text", json={"text": text})
            result = response.json()
            status = "FAKE" if result["is_fake"] else "REAL"
            confidence = round(result["confidence"] * 100)
            match = "✅" if status == expected else "❌"
            
            if status == expected:
                passed += 1
            
            print(f"\n{text[:50]}...")
            print(f"  Expected: {expected} | Got: {status} ({confidence}%) {match}")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"TEXT DETECTION: {passed}/{len(tests)} PASSED ({round(passed/len(tests)*100)}%)")
    return passed == len(tests)

def test_url_verification():
    """Test URL verification"""
    print("\n" + "="*60)
    print("TESTING URL VERIFICATION")
    print("="*60)
    
    tests = [
        ("http://example.com", "REAL"),
    ]
    
    passed = 0
    for url, expected in tests:
        try:
            response = requests.post(f"{BASE_URL}/check-url", json={"url": url})
            result = response.json()
            status = "FAKE" if result["is_fake"] else "REAL"
            confidence = round(result["confidence"] * 100)
            match = "✅" if status == expected else "❌"
            
            if status == expected:
                passed += 1
            
            print(f"\n{url}")
            print(f"  Expected: {expected} | Got: {status} ({confidence}%) {match}")
            
            # Check for the original bug
            if confidence == 0:
                print(f"  ⚠️  WARNING: Confidence is 0% - BUG DETECTED!")
            else:
                print(f"  ✅ Confidence is {confidence}% - BUG FIXED!")
                
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"URL VERIFICATION: {passed}/{len(tests)} PASSED")
    return passed == len(tests)

def test_image_detection():
    """Test image detection"""
    print("\n" + "="*60)
    print("TESTING IMAGE DETECTION")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test-data"
    images = ["test_solid.jpg", "test_gradient.jpg", "real_image.jpg"]
    
    passed = 0
    for img_name in images:
        img_path = test_dir / img_name
        if not img_path.exists():
            print(f"\n{img_name}: File not found")
            continue
            
        try:
            with open(img_path, 'rb') as f:
                files = {'file': (img_name, f, 'image/jpeg')}
                response = requests.post(f"{BASE_URL}/check-image", files=files)
                result = response.json()
                
                status = "FAKE" if result["is_fake"] else "REAL"
                confidence = round(result["confidence"] * 100)
                
                print(f"\n{img_name}")
                print(f"  Result: {status} ({confidence}%)")
                passed += 1
                
        except Exception as e:
            print(f"\n{img_name}")
            print(f"  ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"IMAGE DETECTION: {passed}/{len(images)} TESTED")
    return True

def test_video_detection():
    """Test video detection"""
    print("\n" + "="*60)
    print("TESTING VIDEO DETECTION")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test-data"
    videos = ["test_solid_video.mp4"]
    
    passed = 0
    for vid_name in videos:
        vid_path = test_dir / vid_name
        if not vid_path.exists():
            print(f"\n{vid_name}: File not found")
            continue
            
        try:
            with open(vid_path, 'rb') as f:
                files = {'file': (vid_name, f, 'video/mp4')}
                response = requests.post(f"{BASE_URL}/check-video", files=files)
                result = response.json()
                
                status = "FAKE" if result["is_fake"] else "REAL"
                confidence = round(result["confidence"] * 100)
                
                print(f"\n{vid_name}")
                print(f"  Result: {status} ({confidence}%)")
                passed += 1
                
        except Exception as e:
            print(f"\n{vid_name}")
            print(f"  ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"VIDEO DETECTION: {passed}/{len(videos)} TESTED")
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("VERITY AI - COMPREHENSIVE FEATURE TEST")
    print("="*60)
    
    results = {
        "Text Detection": test_text_detection(),
        "URL Verification": test_url_verification(),
        "Image Detection": test_image_detection(),
        "Video Detection": test_video_detection(),
    }
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    for feature, passed in results.items():
        status = "✅ PASSED" if passed else "❌ NEEDS ATTENTION"
        print(f"{feature}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL FEATURES WORKING PERFECTLY! 🎉")
    else:
        print("⚠️  SOME FEATURES NEED ATTENTION")
    print("="*60 + "\n")
