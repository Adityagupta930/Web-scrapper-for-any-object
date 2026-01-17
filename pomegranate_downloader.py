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
    # Pomegranate queries for 3000 images total (1000 per category)
    queries = [
        # Ripe pomegranate (1000 images) - 50 queries
        ("ripe red pomegranate tree", "pomegranate_ripe"),
        ("fresh pomegranate fruit tree", "pomegranate_ripe"),
        ("sweet pomegranate tree branch", "pomegranate_ripe"),
        ("juicy pomegranate tree fruit", "pomegranate_ripe"),
        ("perfect pomegranate tree", "pomegranate_ripe"),
        ("delicious pomegranate tree", "pomegranate_ripe"),
        ("mature pomegranate tree", "pomegranate_ripe"),
        ("ready pomegranate tree", "pomegranate_ripe"),
        ("harvest pomegranate tree", "pomegranate_ripe"),
        ("pomegranate tree ripe fruit", "pomegranate_ripe"),
        ("pomegranate orchard ripe", "pomegranate_ripe"),
        ("pomegranate tree harvest", "pomegranate_ripe"),
        ("pomegranate tree picking", "pomegranate_ripe"),
        ("organic ripe pomegranate", "pomegranate_ripe"),
        ("natural ripe pomegranate", "pomegranate_ripe"),
        ("healthy ripe pomegranate", "pomegranate_ripe"),
        ("pomegranate tree branch", "pomegranate_ripe"),
        ("pomegranate tree hanging", "pomegranate_ripe"),
        ("pomegranate tree growing", "pomegranate_ripe"),
        ("pomegranate tree cluster", "pomegranate_ripe"),
        ("red pomegranate tree ripe", "pomegranate_ripe"),
        ("bright pomegranate tree", "pomegranate_ripe"),
        ("vibrant pomegranate tree", "pomegranate_ripe"),
        ("beautiful pomegranate tree", "pomegranate_ripe"),
        ("premium pomegranate tree", "pomegranate_ripe"),
        ("quality pomegranate tree", "pomegranate_ripe"),
        ("excellent pomegranate tree", "pomegranate_ripe"),
        ("finest pomegranate tree", "pomegranate_ripe"),
        ("best pomegranate tree", "pomegranate_ripe"),
        ("wonderful pomegranate tree", "pomegranate_ripe"),
        ("pomegranate farm ripe", "pomegranate_ripe"),
        ("pomegranate garden ripe", "pomegranate_ripe"),
        ("pomegranate cultivation", "pomegranate_ripe"),
        ("pomegranate agriculture", "pomegranate_ripe"),
        ("pomegranate farming", "pomegranate_ripe"),
        ("pomegranate growing", "pomegranate_ripe"),
        ("pomegranate production", "pomegranate_ripe"),
        ("pomegranate crop ripe", "pomegranate_ripe"),
        ("pomegranate season ripe", "pomegranate_ripe"),
        ("punica granatum ripe", "pomegranate_ripe"),
        ("pomegranate tree fruit", "pomegranate_ripe"),
        ("pomegranate tree ready", "pomegranate_ripe"),
        ("pomegranate tree fresh", "pomegranate_ripe"),
        ("pomegranate tree sweet", "pomegranate_ripe"),
        ("pomegranate tree juicy", "pomegranate_ripe"),
        ("pomegranate tree perfect", "pomegranate_ripe"),
        ("pomegranate tree mature", "pomegranate_ripe"),
        ("pomegranate tree harvest", "pomegranate_ripe"),
        ("pomegranate tree organic", "pomegranate_ripe"),
        ("pomegranate tree natural", "pomegranate_ripe"),
        
        # Unripe pomegranate (1000 images) - 25 queries
        ("unripe small pomegranate", "pomegranate_raw"),
        ("young small pomegranate", "pomegranate_raw"),
        ("tiny pomegranate tree", "pomegranate_raw"),
        ("hard small pomegranate", "pomegranate_raw"),
        ("immature pomegranate", "pomegranate_raw"),
        ("early pomegranate tree", "pomegranate_raw"),
        ("developing pomegranate", "pomegranate_raw"),
        ("growing pomegranate", "pomegranate_raw"),
        ("pomegranate tree unripe", "pomegranate_raw"),
        ("pomegranate orchard unripe", "pomegranate_raw"),
        ("pomegranate tree young", "pomegranate_raw"),
        ("pomegranate farm unripe", "pomegranate_raw"),
        ("pomegranate garden unripe", "pomegranate_raw"),
        ("small pomegranate sour", "pomegranate_raw"),
        ("small pomegranate tart", "pomegranate_raw"),
        ("small pomegranate bitter", "pomegranate_raw"),
        ("small pomegranate raw", "pomegranate_raw"),
        ("small pomegranate not ready", "pomegranate_raw"),
        ("pomegranate tree fruit unripe", "pomegranate_raw"),
        ("pomegranate tree fruit young", "pomegranate_raw"),
        ("pomegranate tree fruit small", "pomegranate_raw"),
        ("pomegranate tree fruit hard", "pomegranate_raw"),
        ("pomegranate tree fruit tiny", "pomegranate_raw"),
        ("pomegranate cultivation unripe", "pomegranate_raw"),
        ("pomegranate growing unripe", "pomegranate_raw"),
        
        # Rotten pomegranate (1000 images) - 25 queries  
        ("rotten pomegranate tree", "pomegranate_rotten"),
        ("spoiled pomegranate fruit", "pomegranate_rotten"),
        ("bad pomegranate tree", "pomegranate_rotten"),
        ("moldy pomegranate fruit", "pomegranate_rotten"),
        ("decayed pomegranate tree", "pomegranate_rotten"),
        ("damaged pomegranate fruit", "pomegranate_rotten"),
        ("bruised pomegranate tree", "pomegranate_rotten"),
        ("old pomegranate fruit", "pomegranate_rotten"),
        ("overripe pomegranate tree", "pomegranate_rotten"),
        ("expired pomegranate fruit", "pomegranate_rotten"),
        ("pomegranate fruit mold", "pomegranate_rotten"),
        ("pomegranate fruit fungus", "pomegranate_rotten"),
        ("pomegranate fruit disease", "pomegranate_rotten"),
        ("pomegranate fruit rot", "pomegranate_rotten"),
        ("pomegranate fruit waste", "pomegranate_rotten"),
        ("pomegranate tree rotten", "pomegranate_rotten"),
        ("pomegranate tree spoiled", "pomegranate_rotten"),
        ("pomegranate tree damaged", "pomegranate_rotten"),
        ("pomegranate orchard rotten", "pomegranate_rotten"),
        ("pomegranate farm rotten", "pomegranate_rotten"),
        ("brown pomegranate rotten", "pomegranate_rotten"),
        ("black pomegranate rotten", "pomegranate_rotten"),
        ("withered pomegranate", "pomegranate_rotten"),
        ("dried pomegranate rotten", "pomegranate_rotten"),
        ("shriveled pomegranate", "pomegranate_rotten")
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
    
    print("All pomegranate downloads completed!")