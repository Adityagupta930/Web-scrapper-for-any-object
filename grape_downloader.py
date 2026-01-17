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
    """Save image to folder"""
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
        
        # Save image
        image = Image.open(io.BytesIO(response.content))
        
        if image.size[0] < 100 or image.size[1] < 100:
            return False
        
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        if image.size[0] > 600 or image.size[1] > 600:
            image.thumbnail((600, 600), Image.Resampling.LANCZOS)
        
        image.save(filepath, 'JPEG', quality=85)
        return True
        
    except:
        return False

if __name__ == '__main__':
    # Grape queries for 3000 images total (1000 per category)
    queries = [
        # Ripe grapes (1000 images) - 50 queries
        ("ripe purple grapes bunch", "grape_ripe"),
        ("fresh grape cluster vine", "grape_ripe"),
        ("sweet grape bunch hanging", "grape_ripe"),
        ("juicy grape cluster ready", "grape_ripe"),
        ("perfect grape bunch vine", "grape_ripe"),
        ("delicious grape cluster fresh", "grape_ripe"),
        ("mature grape bunch vineyard", "grape_ripe"),
        ("ready grape cluster harvest", "grape_ripe"),
        ("harvest grape bunch ripe", "grape_ripe"),
        ("grape vine ripe cluster", "grape_ripe"),
        ("grape vineyard ripe bunch", "grape_ripe"),
        ("grape vine harvest season", "grape_ripe"),
        ("grape cluster picking ripe", "grape_ripe"),
        ("organic ripe grape bunch", "grape_ripe"),
        ("natural ripe grape cluster", "grape_ripe"),
        ("healthy ripe grape vine", "grape_ripe"),
        ("grape vine bunch ripe", "grape_ripe"),
        ("grape vine hanging ripe", "grape_ripe"),
        ("grape vine growing ripe", "grape_ripe"),
        ("grape vine cluster ripe", "grape_ripe"),
        ("red grape bunch ripe", "grape_ripe"),
        ("green grape cluster ripe", "grape_ripe"),
        ("black grape bunch ripe", "grape_ripe"),
        ("bright grape cluster vine", "grape_ripe"),
        ("vibrant grape bunch fresh", "grape_ripe"),
        ("beautiful grape cluster", "grape_ripe"),
        ("premium grape bunch", "grape_ripe"),
        ("quality grape cluster", "grape_ripe"),
        ("excellent grape bunch", "grape_ripe"),
        ("finest grape cluster", "grape_ripe"),
        ("best grape bunch vine", "grape_ripe"),
        ("wine grape cluster ripe", "grape_ripe"),
        ("table grape bunch ripe", "grape_ripe"),
        ("concord grape cluster", "grape_ripe"),
        ("cabernet grape bunch", "grape_ripe"),
        ("merlot grape cluster", "grape_ripe"),
        ("chardonnay grape bunch", "grape_ripe"),
        ("grape vineyard cluster ripe", "grape_ripe"),
        ("grape farm bunch ripe", "grape_ripe"),
        ("grape garden cluster ripe", "grape_ripe"),
        ("grape orchard bunch ripe", "grape_ripe"),
        ("grape cultivation ripe", "grape_ripe"),
        ("grape agriculture ripe", "grape_ripe"),
        ("grape farming ripe", "grape_ripe"),
        ("grape growing ripe", "grape_ripe"),
        ("grape production ripe", "grape_ripe"),
        ("grape crop ripe", "grape_ripe"),
        ("grape harvest ripe", "grape_ripe"),
        ("grape season ripe", "grape_ripe"),
        ("vitis vinifera ripe", "grape_ripe"),
        
        # Unripe grapes (1000 images) - 25 queries
        ("unripe small grape cluster", "grape_raw"),
        ("young small grape bunch", "grape_raw"),
        ("tiny grape cluster vine", "grape_raw"),
        ("hard small grape bunch", "grape_raw"),
        ("immature small grape cluster", "grape_raw"),
        ("early small grape bunch", "grape_raw"),
        ("developing small grape cluster", "grape_raw"),
        ("growing small grape bunch", "grape_raw"),
        ("grape vine unripe cluster", "grape_raw"),
        ("grape vineyard unripe bunch", "grape_raw"),
        ("grape vine unripe fruit", "grape_raw"),
        ("grape farm unripe cluster", "grape_raw"),
        ("grape garden unripe bunch", "grape_raw"),
        ("small grape cluster sour", "grape_raw"),
        ("small grape bunch tart", "grape_raw"),
        ("small grape cluster bitter", "grape_raw"),
        ("small grape bunch raw", "grape_raw"),
        ("small grape cluster not ready", "grape_raw"),
        ("grape vine fruit unripe", "grape_raw"),
        ("grape vine fruit young", "grape_raw"),
        ("grape vine fruit small", "grape_raw"),
        ("grape vine fruit hard", "grape_raw"),
        ("grape vine fruit tiny", "grape_raw"),
        ("grape cultivation unripe", "grape_raw"),
        ("grape growing unripe", "grape_raw"),
        
        # Rotten grapes (1000 images) - 25 queries  
        ("rotten grape cluster vine", "grape_rotten"),
        ("spoiled grape bunch old", "grape_rotten"),
        ("bad grape cluster moldy", "grape_rotten"),
        ("moldy grape bunch decay", "grape_rotten"),
        ("decayed grape cluster", "grape_rotten"),
        ("damaged grape bunch", "grape_rotten"),
        ("bruised grape cluster", "grape_rotten"),
        ("old grape bunch spoiled", "grape_rotten"),
        ("overripe grape cluster", "grape_rotten"),
        ("expired grape bunch", "grape_rotten"),
        ("grape cluster mold", "grape_rotten"),
        ("grape bunch fungus", "grape_rotten"),
        ("grape cluster disease", "grape_rotten"),
        ("grape bunch rot", "grape_rotten"),
        ("grape cluster waste", "grape_rotten"),
        ("grape vine rotten cluster", "grape_rotten"),
        ("grape vine hanging rotten", "grape_rotten"),
        ("grape vine growing rotten", "grape_rotten"),
        ("grape vineyard rotten", "grape_rotten"),
        ("grape farm rotten", "grape_rotten"),
        ("brown grape cluster rotten", "grape_rotten"),
        ("black grape bunch rotten", "grape_rotten"),
        ("withered grape cluster", "grape_rotten"),
        ("dried grape bunch rotten", "grape_rotten"),
        ("shriveled grape cluster", "grape_rotten")
    ]
    
    folder_path = "dataset"
    
    for query, folder_name in queries:
        print(f"Downloading images for: {query}")
        
        image_urls = download_from_bing(query, 40)
        print(f"Found {len(image_urls)} image URLs")
        
        saved_count = 0
        for i, url in enumerate(image_urls):
            if save_image(url, folder_path, folder_name):
                saved_count += 1
                print(f"Saved image {saved_count} for {folder_name}")
            
            if saved_count >= 20:
                break
        
        print(f"Completed {query}: {saved_count} images saved")
        time.sleep(2)
    
    print("All grape downloads completed!")