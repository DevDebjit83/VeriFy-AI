"""
Comprehensive Image Detection Test
Tests both REAL and DEEPFAKE images to verify model accuracy
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def test_image(image_path, expected_status, description):
    """Test a single image"""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"File: {image_path}")
    print(f"Expected: {expected_status}")
    print("-" * 70)
    
    try:
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return False
        
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/check-image", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            status = "FAKE" if result["is_fake"] else "REAL"
            confidence = round(result["confidence"] * 100)
            
            match = "✅" if status == expected_status else "❌"
            result_text = "PASS" if status == expected_status else "FAIL"
            
            print(f"Got: {status} (Confidence: {confidence}%)")
            print(f"Analysis: {result.get('analysis', 'N/A')[:100]}...")
            print(f"Result: {match} {result_text}")
            
            if confidence == 0:
                print("⚠️  WARNING: Confidence is 0%")
            elif confidence < 60:
                print(f"⚠️  WARNING: Low confidence ({confidence}%)")
            
            return status == expected_status
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE IMAGE DETECTION TEST")
    print("Testing REAL vs DEEPFAKE/ARTIFICIAL images")
    print("="*70)
    
    # Test REAL images
    real_tests = [
        ("test_real_sky.jpg", "REAL", "Natural sky gradient"),
        ("test_real_landscape.jpg", "REAL", "Simple landscape scene"),
        ("test_real_texture.jpg", "REAL", "Natural texture with blur"),
    ]
    
    # Test FAKE/DEEPFAKE images
    fake_tests = [
        ("test_fake_solid.jpg", "FAKE", "Solid color (unnatural)"),
        ("test_fake_checkerboard.jpg", "FAKE", "Checkerboard pattern (artificial)"),
        ("test_fake_noise.jpg", "FAKE", "Random noise (AI artifact)"),
        ("test_fake_geometric.jpg", "FAKE", "Geometric shapes (unnatural)"),
        ("test_fake_gradient.jpg", "FAKE", "Perfect gradient (too perfect)"),
    ]
    
    print("\n" + "="*70)
    print("TESTING REAL IMAGES")
    print("="*70)
    
    real_passed = 0
    for image_file, expected, desc in real_tests:
        if test_image(image_file, expected, desc):
            real_passed += 1
    
    print("\n" + "="*70)
    print("TESTING FAKE/DEEPFAKE IMAGES")
    print("="*70)
    
    fake_passed = 0
    for image_file, expected, desc in fake_tests:
        if test_image(image_file, expected, desc):
            fake_passed += 1
    
    # Calculate results
    real_total = len(real_tests)
    fake_total = len(fake_tests)
    total_passed = real_passed + fake_passed
    total_tests = real_total + fake_total
    
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    
    print(f"\nREAL Images: {real_passed}/{real_total} correct ({round(real_passed/real_total*100) if real_total > 0 else 0}%)")
    print(f"FAKE Images: {fake_passed}/{fake_total} correct ({round(fake_passed/fake_total*100) if fake_total > 0 else 0}%)")
    
    overall_accuracy = round(total_passed/total_tests*100) if total_tests > 0 else 0
    print(f"\nOVERALL ACCURACY: {total_passed}/{total_tests} ({overall_accuracy}%)")
    
    print("\n" + "="*70)
    if overall_accuracy >= 90:
        print("🎉 DEEPFAKE DETECTION: EXCELLENT!")
    elif overall_accuracy >= 75:
        print("✅ DEEPFAKE DETECTION: GOOD")
    elif overall_accuracy >= 60:
        print("⚠️  DEEPFAKE DETECTION: MODERATE (needs improvement)")
    else:
        print("❌ DEEPFAKE DETECTION: POOR (needs major fixes)")
    print("="*70 + "\n")
    
    # Detailed breakdown
    print("DETAILED BREAKDOWN:")
    print(f"  True Positives (FAKE detected as FAKE): {fake_passed}/{fake_total}")
    print(f"  True Negatives (REAL detected as REAL): {real_passed}/{real_total}")
    print(f"  False Positives (REAL detected as FAKE): {real_total - real_passed}/{real_total}")
    print(f"  False Negatives (FAKE detected as REAL): {fake_total - fake_passed}/{fake_total}")
    print()
    
    return overall_accuracy >= 75

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
