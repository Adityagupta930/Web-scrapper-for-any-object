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
        
        for i in range(5):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        image_urls = []
        images = wd.find_elements(By.CSS_SELECTOR, "img.mimg")
        
        for img in images[:num_images]:
            src = img.get_attribute('src')
            if src and src.startswith('http') and len(src) > 50:
                image_urls.append(src)
        
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
        
        full_path = os.path.join(folder_path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        
        image_hash = hashlib.md5(url.encode()).hexdigest()[:10]
        filename = f"{image_hash}.jpg"
        filepath = os.path.join(full_path, filename)
        
        if os.path.exists(filepath):
            return True
        
        image = Image.open(io.BytesIO(response.content))
        
        if image.size[0] < 200 or image.size[1] < 200:
            return False
        
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        if image.size[0] > 800 or image.size[1] > 800:
            image.thumbnail((800, 800), Image.Resampling.LANCZOS)
        
        image.save(filepath, 'JPEG', quality=90)
        return True
        
    except:
        return False

if __name__ == '__main__':
    # Mango queries - green and yellow mangoes on trees
    queries = [
        # Ripe mangoes (1000 images) - green and yellow on trees
        ("ripe green mango on tree", "mango_ripe"),
        ("ripe yellow mango on tree", "mango_ripe"),
        ("fresh mango tree fruit", "mango_ripe"),
        ("sweet mango hanging tree", "mango_ripe"),
        ("juicy mango tree branch", "mango_ripe"),
        ("perfect mango on tree", "mango_ripe"),
        ("mature mango tree fruit", "mango_ripe"),
        ("ready mango tree", "mango_ripe"),
        ("harvest mango tree", "mango_ripe"),
        ("mango tree ripe fruit", "mango_ripe"),
        ("golden mango tree", "mango_ripe"),
        ("yellow mango branch", "mango_ripe"),
        ("green mango tree ripe", "mango_ripe"),
        ("mango plantation ripe", "mango_ripe"),
        ("mango orchard tree", "mango_ripe"),
        ("organic mango tree", "mango_ripe"),
        ("natural mango tree fruit", "mango_ripe"),
        ("healthy mango tree", "mango_ripe"),
        ("mango tree hanging fruit", "mango_ripe"),
        ("mango tree growing fruit", "mango_ripe"),
        ("mango tree cluster", "mango_ripe"),
        ("bright mango tree", "mango_ripe"),
        ("vibrant mango tree fruit", "mango_ripe"),
        ("beautiful mango tree", "mango_ripe"),
        ("premium mango tree", "mango_ripe"),
        ("quality mango tree fruit", "mango_ripe"),
        ("excellent mango tree", "mango_ripe"),
        ("tropical mango tree", "mango_ripe"),
        ("alphonso mango tree", "mango_ripe"),
        ("kesar mango tree", "mango_ripe"),
        ("totapuri mango tree", "mango_ripe"),
        ("langra mango tree", "mango_ripe"),
        ("dasheri mango tree", "mango_ripe"),
        ("mango farm tree ripe", "mango_ripe"),
        ("mango garden tree", "mango_ripe"),
        ("mango grove tree", "mango_ripe"),
        ("mango cultivation tree", "mango_ripe"),
        ("mango agriculture tree", "mango_ripe"),
        ("mango farming tree", "mango_ripe"),
        ("mango growing tree", "mango_ripe"),
        ("mango production tree", "mango_ripe"),
        ("mango crop tree", "mango_ripe"),
        ("mango harvest tree", "mango_ripe"),
        ("mango season tree", "mango_ripe"),
        ("mangifera indica tree", "mango_ripe"),
        ("ripe mango branch", "mango_ripe"),
        ("mango tree fruit ready", "mango_ripe"),
        ("mango tree fruit fresh", "mango_ripe"),
        ("mango tree fruit sweet", "mango_ripe"),
        ("mango tree fruit juicy", "mango_ripe"),
        
        # Unripe mangoes (1000 images) - small green on trees
        ("unripe small mango tree", "mango_raw"),
        ("young small mango tree", "mango_raw"),
        ("tiny mango tree fruit", "mango_raw"),
        ("hard small mango tree", "mango_raw"),
        ("immature mango tree", "mango_raw"),
        ("early mango tree fruit", "mango_raw"),
        ("developing mango tree", "mango_raw"),
        ("growing small mango tree", "mango_raw"),
        ("mango tree unripe fruit", "mango_raw"),
        ("green mango tree unripe", "mango_raw"),
        ("small mango branch", "mango_raw"),
        ("tiny mango hanging tree", "mango_raw"),
        ("young mango tree fruit", "mango_raw"),
        ("mango plantation unripe", "mango_raw"),
        ("mango orchard unripe tree", "mango_raw"),
        ("mango farm unripe tree", "mango_raw"),
        ("mango garden unripe tree", "mango_raw"),
        ("small mango tree sour", "mango_raw"),
        ("small mango tree tart", "mango_raw"),
        ("small mango tree raw", "mango_raw"),
        ("small mango tree not ready", "mango_raw"),
        ("mango tree fruit young", "mango_raw"),
        ("mango tree fruit small", "mango_raw"),
        ("mango tree fruit hard", "mango_raw"),
        ("mango tree fruit green", "mango_raw"),
        
        # Rotten mangoes (1000 images) - on trees
        ("rotten mango tree fruit", "mango_rotten"),
        ("spoiled mango tree", "mango_rotten"),
        ("bad mango tree fruit", "mango_rotten"),
        ("moldy mango tree", "mango_rotten"),
        ("decayed mango tree fruit", "mango_rotten"),
        ("damaged mango tree", "mango_rotten"),
        ("bruised mango tree fruit", "mango_rotten"),
        ("old mango tree fruit", "mango_rotten"),
        ("overripe mango tree", "mango_rotten"),
        ("mango tree fruit mold", "mango_rotten"),
        ("mango tree fruit fungus", "mango_rotten"),
        ("mango tree fruit disease", "mango_rotten"),
        ("mango tree fruit rot", "mango_rotten"),
        ("mango tree fruit waste", "mango_rotten"),
        ("mango tree branch rotten", "mango_rotten"),
        ("mango tree hanging rotten", "mango_rotten"),
        ("mango plantation rotten", "mango_rotten"),
        ("mango farm rotten tree", "mango_rotten"),
        ("brown mango tree rotten", "mango_rotten"),
        ("black mango tree rotten", "mango_rotten"),
        ("soft mango tree rotten", "mango_rotten"),
        ("mushy mango tree", "mango_rotten"),
        ("wrinkled mango tree", "mango_rotten"),
        ("mango tree fruit spoiled", "mango_rotten"),
        ("mango tree fruit damaged", "mango_rotten")
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
    
    print("All mango downloads completed!")
