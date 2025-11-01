"""
Comprehensive URL verification testing with REAL and FAKE URLs
"""
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_url(url, expected_status, description):
    """Test a single URL"""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print(f"Expected: {expected_status}")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/check-url",
            json={"url": url},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            status = "FAKE" if result["is_fake"] else "REAL"
            confidence = round(result["confidence"] * 100)
            
            match = "✅" if status == expected_status else "❌"
            color = "PASS" if status == expected_status else "FAIL"
            
            print(f"Got: {status} (Confidence: {confidence}%)")
            print(f"Analysis: {result.get('analysis', 'N/A')[:100]}...")
            print(f"Result: {match} {color}")
            
            if confidence == 0:
                print("⚠️  WARNING: Confidence is 0% - CONFIDENCE BUG!")
                return False
            elif confidence < 50:
                print(f"⚠️  WARNING: Low confidence ({confidence}%)")
            
            return status == expected_status
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE URL VERIFICATION TEST")
    print("Testing REAL URLs (legitimate sources) and FAKE URLs (known misinformation)")
    print("="*70)
    
    # REAL URLs - Legitimate, trustworthy sources
    real_urls = [
        ("https://www.cdc.gov", "CDC - Official health organization"),
        ("https://www.who.int", "WHO - World Health Organization"),
        ("https://www.nasa.gov", "NASA - Official space agency"),
        ("https://www.nih.gov", "NIH - National Institutes of Health"),
        ("https://www.bbc.com/news", "BBC News - Reputable news source"),
        ("https://www.reuters.com", "Reuters - International news agency"),
        ("https://www.nature.com", "Nature - Scientific journal"),
        ("https://www.sciencemag.org", "Science Magazine"),
        ("https://en.wikipedia.org", "Wikipedia - General encyclopedia"),
        ("http://example.com", "Example.com - Test domain"),
    ]
    
    # FAKE/SUSPICIOUS URLs - Known misinformation or conspiracy sites
    # Note: These are examples - testing suspicious patterns
    fake_urls = [
        ("https://naturalnews.com", "Natural News - Known for misinformation"),
        ("https://infowars.com", "Infowars - Conspiracy theories"),
        ("https://beforeitsnews.com", "Before It's News - Unverified claims"),
        ("https://worldtruth.tv", "World Truth TV - Conspiracy content"),
    ]
    
    print("\n" + "="*70)
    print("TESTING REAL/LEGITIMATE URLS")
    print("="*70)
    
    real_passed = 0
    real_total = len(real_urls)
    
    for url, description in real_urls:
        if test_url(url, "REAL", description):
            real_passed += 1
        time.sleep(1)  # Rate limiting
    
    print("\n" + "="*70)
    print("TESTING FAKE/SUSPICIOUS URLS")
    print("="*70)
    
    fake_passed = 0
    fake_total = len(fake_urls)
    
    for url, description in fake_urls:
        if test_url(url, "FAKE", description):
            fake_passed += 1
        time.sleep(1)  # Rate limiting
    
    # Final Results
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    print(f"\nREAL URLs: {real_passed}/{real_total} correct ({round(real_passed/real_total*100)}%)")
    print(f"FAKE URLs: {fake_passed}/{fake_total} correct ({round(fake_passed/fake_total*100) if fake_total > 0 else 0}%)")
    
    total_passed = real_passed + fake_passed
    total_tests = real_total + fake_total
    overall_accuracy = round(total_passed/total_tests*100) if total_tests > 0 else 0
    
    print(f"\nOVERALL ACCURACY: {total_passed}/{total_tests} ({overall_accuracy}%)")
    
    if overall_accuracy >= 80:
        print("\n🎉 URL VERIFICATION: EXCELLENT!")
    elif overall_accuracy >= 60:
        print("\n✅ URL VERIFICATION: GOOD (needs improvement)")
    else:
        print("\n⚠️  URL VERIFICATION: NEEDS FIXING!")
    
    print("="*70 + "\n")
    
    return overall_accuracy >= 80

if __name__ == "__main__":
    main()
