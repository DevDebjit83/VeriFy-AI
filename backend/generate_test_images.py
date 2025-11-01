"""
Generate test images and test deepfake detection
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

def create_real_images():
    """Create realistic-looking images (REAL)"""
    print("\n📸 Generating REAL test images...")
    
    # 1. Natural gradient image (like a sky)
    img1 = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img1)
    for y in range(512):
        color = int(135 + (y / 512) * 120)  # Blue gradient
        draw.rectangle([(0, y), (512, y+1)], fill=(color, color, 255))
    img1.save('test_real_sky.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_real_sky.jpg (Natural gradient)")
    
    # 2. Landscape-like image
    img2 = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img2)
    # Sky
    for y in range(300):
        draw.rectangle([(0, y), (512, y+1)], fill=(135, 206, 235))
    # Ground
    for y in range(300, 512):
        draw.rectangle([(0, y), (512, y+1)], fill=(34, 139, 34))
    # Add some "trees"
    for i in range(10):
        x = i * 50 + 30
        draw.ellipse([(x, 250), (x+40, 310)], fill=(0, 100, 0))
    img2.save('test_real_landscape.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_real_landscape.jpg (Simple landscape)")
    
    # 3. Natural photo-like texture
    arr = np.random.randint(100, 200, (512, 512, 3), dtype=np.uint8)
    img3 = Image.fromarray(arr)
    img3 = img3.filter(ImageFilter.GaussianBlur(radius=5))  # Natural blur
    img3.save('test_real_texture.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_real_texture.jpg (Natural texture)")
    
    return ['test_real_sky.jpg', 'test_real_landscape.jpg', 'test_real_texture.jpg']

def create_deepfake_images():
    """Create artificial/deepfake-like images (FAKE)"""
    print("\n🤖 Generating DEEPFAKE/ARTIFICIAL test images...")
    
    # 1. Perfectly uniform color (unnatural)
    img1 = Image.new('RGB', (512, 512), color=(255, 0, 0))
    img1.save('test_fake_solid.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_fake_solid.jpg (Perfectly uniform - unnatural)")
    
    # 2. Artificial checkerboard pattern
    img2 = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img2)
    for i in range(16):
        for j in range(16):
            color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
            draw.rectangle([(i*32, j*32), ((i+1)*32, (j+1)*32)], fill=color)
    img2.save('test_fake_checkerboard.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_fake_checkerboard.jpg (Artificial pattern)")
    
    # 3. Digital noise (common in AI-generated images)
    arr = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
    img3 = Image.fromarray(arr)
    img3.save('test_fake_noise.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_fake_noise.jpg (Random noise - AI artifact)")
    
    # 4. Geometric shapes (unnatural composition)
    img4 = Image.new('RGB', (512, 512), color=(200, 200, 200))
    draw = ImageDraw.Draw(img4)
    draw.ellipse([(100, 100), (400, 400)], fill=(255, 0, 0))
    draw.rectangle([(200, 200), (300, 300)], fill=(0, 0, 255))
    img4.save('test_fake_geometric.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_fake_geometric.jpg (Unnatural geometric)")
    
    # 5. Perfect gradient (too perfect to be real)
    img5 = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img5)
    for y in range(512):
        color = int((y / 512) * 255)
        draw.rectangle([(0, y), (512, y+1)], fill=(color, color, color))
    img5.save('test_fake_gradient.jpg', 'JPEG', quality=95)
    print("  ✅ Created: test_fake_gradient.jpg (Too perfect gradient)")
    
    return ['test_fake_solid.jpg', 'test_fake_checkerboard.jpg', 'test_fake_noise.jpg', 
            'test_fake_geometric.jpg', 'test_fake_gradient.jpg']

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING TEST IMAGES FOR DEEPFAKE DETECTION")
    print("="*70)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    real_images = create_real_images()
    fake_images = create_deepfake_images()
    
    print("\n" + "="*70)
    print("✅ IMAGE GENERATION COMPLETE!")
    print("="*70)
    print(f"\nREAL Images: {len(real_images)}")
    for img in real_images:
        print(f"  - {img}")
    
    print(f"\nFAKE/DEEPFAKE Images: {len(fake_images)}")
    for img in fake_images:
        print(f"  - {img}")
    
    print("\n" + "="*70)
    print("Next: Run test_image_detection.py to test these images")
    print("="*70 + "\n")
