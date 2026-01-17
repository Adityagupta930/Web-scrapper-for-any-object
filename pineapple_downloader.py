import requests
import os
from PIL import Image
import io
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = "C:/Users/adiya/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

def download_from_bing(query, num_images=50):
    """Download images from Bing Images"""
    
    service = Service(DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    
    wd = webdriver.Chrome(service=service, options=options)
    
    try:
        search_url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}&form=HDRSC2"
        wd.get(search_url)
        time.sleep(3)
        
        # Scroll to load more images
        for i in range(5):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Get image URLs
        image_urls = []
        images = wd.find_elements(By.CSS_SELECTOR, "img.mimg")
        
        for img in images[:num_images]:
            src = img.get_attribute('src')
            if src and src.startswith('http') and len(src) > 50:
                image_urls.append(src)
        
        # Try alternative selector if needed
        if len(image_urls) < 20:
            images = wd.find_elements(By.TAG_NAME, "img")
            for img in images[:num_images]:
                src = img.get_attribute('src') or img.get_attribute('data-src')
                if src and src.startswith('http') and 'logo' not in src.lower():
                    image_urls.append(src)
        
        return image_urls[:num_images]
        
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        wd.quit()

def save_image(url, folder_path, folder_name):
    """Save high-quality image to folder"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Create folder
        full_path = os.path.join(folder_path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        
        # Generate filename
        image_hash = hashlib.md5(url.encode()).hexdigest()[:10]
        filename = f"{image_hash}.jpg"
        filepath = os.path.join(full_path, filename)
        
        if os.path.exists(filepath):
            return True
        
        # Save image with quality checks
        image = Image.open(io.BytesIO(response.content))
        
        # Higher quality requirements - clear, close-up images
        if image.size[0] < 300 or image.size[1] < 300:
            return False
        
        # Check image sharpness (basic blur detection)
        import numpy as np
        gray = image.convert('L')
        gray_array = np.array(gray)
        laplacian_var = np.var(np.gradient(gray_array))
        if laplacian_var < 100:  # Too blurry
            return False
        
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        if image.size[0] > 800 or image.size[1] > 800:
            image.thumbnail((800, 800), Image.Resampling.LANCZOS)
        
        image.save(filepath, 'JPEG', quality=95)
        return True
        
    except:
        return False

if __name__ == '__main__':
    # Clear pineapple queries - pineapple should be clearly visible
    queries = [
        # Ripe pineapple (1000 images) - 50 queries
        ("ripe golden pineapple fruit", "pineapple_ripe"),
        ("fresh yellow pineapple", "pineapple_ripe"),
        ("sweet pineapple fruit", "pineapple_ripe"),
        ("juicy ripe pineapple", "pineapple_ripe"),
        ("perfect golden pineapple", "pineapple_ripe"),
        ("delicious pineapple fruit", "pineapple_ripe"),
        ("mature yellow pineapple", "pineapple_ripe"),
        ("ready pineapple fruit", "pineapple_ripe"),
        ("harvest pineapple", "pineapple_ripe"),
        ("ripe pineapple on tree", "pineapple_ripe"),
        ("pineapple plant fruit", "pineapple_ripe"),
        ("golden pineapple tree", "pineapple_ripe"),
        ("yellow pineapple growing", "pineapple_ripe"),
        ("organic ripe pineapple", "pineapple_ripe"),
        ("natural pineapple fruit", "pineapple_ripe"),
        ("healthy pineapple", "pineapple_ripe"),
        ("pineapple crown fruit", "pineapple_ripe"),
        ("tropical pineapple", "pineapple_ripe"),
        ("bright pineapple fruit", "pineapple_ripe"),
        ("vibrant golden pineapple", "pineapple_ripe"),
        ("beautiful pineapple", "pineapple_ripe"),
        ("premium pineapple fruit", "pineapple_ripe"),
        ("quality pineapple", "pineapple_ripe"),
        ("excellent pineapple fruit", "pineapple_ripe"),
        ("finest pineapple", "pineapple_ripe"),
        ("best pineapple fruit", "pineapple_ripe"),
        ("whole ripe pineapple", "pineapple_ripe"),
        ("complete pineapple fruit", "pineapple_ripe"),
        ("full pineapple", "pineapple_ripe"),
        ("pineapple with crown", "pineapple_ripe"),
        ("pineapple spiky skin", "pineapple_ripe"),
        ("pineapple diamond pattern", "pineapple_ripe"),
        ("pineapple texture", "pineapple_ripe"),
        ("pineapple leaves crown", "pineapple_ripe"),
        ("cut ripe pineapple", "pineapple_ripe"),
        ("sliced pineapple fruit", "pineapple_ripe"),
        ("pineapple pieces", "pineapple_ripe"),
        ("pineapple chunks", "pineapple_ripe"),
        ("pineapple rings", "pineapple_ripe"),
        ("fresh pineapple slices", "pineapple_ripe"),
        ("juicy pineapple pieces", "pineapple_ripe"),
        ("sweet pineapple chunks", "pineapple_ripe"),
        ("golden pineapple slices", "pineapple_ripe"),
        ("yellow pineapple pieces", "pineapple_ripe"),
        ("ripe pineapple segments", "pineapple_ripe"),
        ("pineapple fruit flesh", "pineapple_ripe"),
        ("pineapple pulp", "pineapple_ripe"),
        ("pineapple core", "pineapple_ripe"),
        ("pineapple inside", "pineapple_ripe"),
        
        # Unripe pineapple (1000 images) - 40 queries
        ("unripe green pineapple", "pineapple_raw"),
        ("young small pineapple", "pineapple_raw"),
        ("small green pineapple fruit", "pineapple_raw"),
        ("hard pineapple fruit", "pineapple_raw"),
        ("immature pineapple", "pineapple_raw"),
        ("early pineapple fruit", "pineapple_raw"),
        ("developing pineapple", "pineapple_raw"),
        ("growing pineapple fruit", "pineapple_raw"),
        ("pineapple unripe fruit", "pineapple_raw"),
        ("green pineapple on tree", "pineapple_raw"),
        ("young pineapple plant", "pineapple_raw"),
        ("small pineapple growing", "pineapple_raw"),
        ("tiny pineapple fruit", "pineapple_raw"),
        ("green pineapple crown", "pineapple_raw"),
        ("unripe pineapple texture", "pineapple_raw"),
        ("hard green pineapple", "pineapple_raw"),
        ("sour pineapple fruit", "pineapple_raw"),
        ("tart pineapple", "pineapple_raw"),
        ("bitter pineapple fruit", "pineapple_raw"),
        ("raw pineapple", "pineapple_raw"),
        ("not ready pineapple", "pineapple_raw"),
        ("pineapple fruit young", "pineapple_raw"),
        ("pineapple fruit small", "pineapple_raw"),
        ("pineapple fruit hard", "pineapple_raw"),
        ("pineapple fruit green", "pineapple_raw"),
        ("whole unripe pineapple", "pineapple_raw"),
        ("complete green pineapple", "pineapple_raw"),
        ("full unripe pineapple", "pineapple_raw"),
        ("green pineapple with crown", "pineapple_raw"),
        ("unripe pineapple spiky", "pineapple_raw"),
        ("green pineapple pattern", "pineapple_raw"),
        ("unripe pineapple leaves", "pineapple_raw"),
        ("cut unripe pineapple", "pineapple_raw"),
        ("sliced green pineapple", "pineapple_raw"),
        ("unripe pineapple pieces", "pineapple_raw"),
        ("green pineapple chunks", "pineapple_raw"),
        ("hard pineapple slices", "pineapple_raw"),
        ("sour pineapple pieces", "pineapple_raw"),
        ("unripe pineapple flesh", "pineapple_raw"),
        ("green pineapple inside", "pineapple_raw"),
        
        # Rotten pineapple (1000 images) - 35 queries
        ("rotten brown pineapple", "pineapple_rotten"),
        ("spoiled pineapple fruit", "pineapple_rotten"),
        ("bad pineapple", "pineapple_rotten"),
        ("moldy pineapple fruit", "pineapple_rotten"),
        ("decayed pineapple", "pineapple_rotten"),
        ("damaged pineapple fruit", "pineapple_rotten"),
        ("bruised pineapple", "pineapple_rotten"),
        ("old pineapple fruit", "pineapple_rotten"),
        ("overripe pineapple", "pineapple_rotten"),
        ("expired pineapple fruit", "pineapple_rotten"),
        ("pineapple with mold", "pineapple_rotten"),
        ("pineapple fungus", "pineapple_rotten"),
        ("pineapple disease", "pineapple_rotten"),
        ("pineapple rot", "pineapple_rotten"),
        ("waste pineapple", "pineapple_rotten"),
        ("rotten pineapple tree", "pineapple_rotten"),
        ("spoiled pineapple plant", "pineapple_rotten"),
        ("damaged pineapple growing", "pineapple_rotten"),
        ("brown pineapple fruit", "pineapple_rotten"),
        ("black pineapple", "pineapple_rotten"),
        ("soft rotten pineapple", "pineapple_rotten"),
        ("mushy pineapple", "pineapple_rotten"),
        ("wrinkled pineapple", "pineapple_rotten"),
        ("whole rotten pineapple", "pineapple_rotten"),
        ("complete spoiled pineapple", "pineapple_rotten"),
        ("full rotten pineapple", "pineapple_rotten"),
        ("rotten pineapple crown", "pineapple_rotten"),
        ("spoiled pineapple leaves", "pineapple_rotten"),
        ("cut rotten pineapple", "pineapple_rotten"),
        ("sliced spoiled pineapple", "pineapple_rotten"),
        ("rotten pineapple pieces", "pineapple_rotten"),
        ("moldy pineapple chunks", "pineapple_rotten"),
        ("bad pineapple slices", "pineapple_rotten"),
        ("rotten pineapple flesh", "pineapple_rotten"),
        ("spoiled pineapple inside", "pineapple_rotten")
    ]
    
    folder_path = "dataset"
    
    for query, folder_name in queries:
        print(f"Downloading images for: {query}")
        
        image_urls = download_from_bing(query, 30)
        print(f"Found {len(image_urls)} image URLs")
        
        saved_count = 0
        for i, url in enumerate(image_urls):
            if save_image(url, folder_path, folder_name):
                saved_count += 1
                print(f"Saved image {saved_count} for {folder_name}")
            
            if saved_count >= 25:
                break
        
        print(f"Completed {query}: {saved_count} images saved")
        time.sleep(2)
    
    print("All pineapple downloads completed!")