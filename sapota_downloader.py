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
    # Sapota queries for 3000 images total (1000 per category)
    queries = [
        # Ripe sapota (1000 images) - 50 queries
        ("ripe sapota on tree", "sapota_ripe"),
        ("fresh sapota tree", "sapota_ripe"),
        ("sweet sapota branch", "sapota_ripe"),
        ("juicy sapota tree fruit", "sapota_ripe"),
        ("perfect sapota on branch", "sapota_ripe"),
        ("delicious sapota tree", "sapota_ripe"),
        ("mature sapota tree", "sapota_ripe"),
        ("ready sapota branch", "sapota_ripe"),
        ("harvest sapota tree", "sapota_ripe"),
        ("sapota tree ripe fruit", "sapota_ripe"),
        ("chikoo tree ripe fruit", "sapota_ripe"),
        ("sapodilla tree ripe", "sapota_ripe"),
        ("sapota plantation ripe tree", "sapota_ripe"),
        ("sapota tree harvest season", "sapota_ripe"),
        ("sapota tree picking ripe", "sapota_ripe"),
        ("organic ripe sapota tree", "sapota_ripe"),
        ("natural ripe sapota branch", "sapota_ripe"),
        ("healthy ripe sapota tree", "sapota_ripe"),
        ("sapota tree branch ripe", "sapota_ripe"),
        ("sapota tree hanging ripe", "sapota_ripe"),
        ("sapota tree growing ripe", "sapota_ripe"),
        ("sapota tree cluster ripe", "sapota_ripe"),
        ("sapota tree fruit fresh", "sapota_ripe"),
        ("sapota tree fruit ripe", "sapota_ripe"),
        ("sapota tree fruit ready", "sapota_ripe"),
        ("brown sapota tree", "sapota_ripe"),
        ("golden sapota tree", "sapota_ripe"),
        ("vibrant sapota branch", "sapota_ripe"),
        ("beautiful sapota tree", "sapota_ripe"),
        ("premium sapota tree", "sapota_ripe"),
        ("quality sapota branch", "sapota_ripe"),
        ("excellent sapota tree", "sapota_ripe"),
        ("finest sapota branch", "sapota_ripe"),
        ("best sapota tree", "sapota_ripe"),
        ("tropical sapota tree ripe", "sapota_ripe"),
        ("chikoo farm tree ripe", "sapota_ripe"),
        ("sapodilla farm tree ripe", "sapota_ripe"),
        ("sapota grove tree ripe", "sapota_ripe"),
        ("sapota garden tree ripe", "sapota_ripe"),
        ("sapota orchard tree ripe", "sapota_ripe"),
        ("sapota cultivation ripe", "sapota_ripe"),
        ("sapota agriculture ripe", "sapota_ripe"),
        ("sapota farming ripe", "sapota_ripe"),
        ("sapota growing ripe", "sapota_ripe"),
        ("sapota production ripe", "sapota_ripe"),
        ("sapota crop ripe", "sapota_ripe"),
        ("sapota harvest ripe", "sapota_ripe"),
        ("sapota season ripe", "sapota_ripe"),
        ("manilkara zapota tree ripe", "sapota_ripe"),
        ("chikoo plant tree ripe", "sapota_ripe"),
        
        # Unripe sapota (1000 images) - 25 queries
        ("unripe green sapota on tree", "sapota_raw"),
        ("young green sapota tree", "sapota_raw"),
        ("small green sapota branch", "sapota_raw"),
        ("hard green sapota tree", "sapota_raw"),
        ("immature green sapota branch", "sapota_raw"),
        ("early green sapota tree", "sapota_raw"),
        ("developing green sapota tree", "sapota_raw"),
        ("growing green sapota tree", "sapota_raw"),
        ("sapota tree unripe fruit", "sapota_raw"),
        ("chikoo tree unripe fruit", "sapota_raw"),
        ("sapota plantation unripe tree", "sapota_raw"),
        ("sapota branch unripe fruit", "sapota_raw"),
        ("sapota farm tree unripe", "sapota_raw"),
        ("sapota garden tree unripe", "sapota_raw"),
        ("green sapota tree sour", "sapota_raw"),
        ("green sapota tree tart", "sapota_raw"),
        ("green sapota tree bitter", "sapota_raw"),
        ("green sapota tree raw", "sapota_raw"),
        ("green sapota tree not ready", "sapota_raw"),
        ("sapota tree fruit unripe", "sapota_raw"),
        ("sapota tree fruit young", "sapota_raw"),
        ("sapota tree fruit small", "sapota_raw"),
        ("sapota tree fruit hard", "sapota_raw"),
        ("sapota tree fruit green", "sapota_raw"),
        ("sapota cultivation unripe", "sapota_raw"),
        
        # Rotten sapota (1000 images) - 25 queries  
        ("rotten sapota tree fruit", "sapota_rotten"),
        ("spoiled sapota tree fruit", "sapota_rotten"),
        ("bad sapota tree fruit", "sapota_rotten"),
        ("moldy sapota tree fruit", "sapota_rotten"),
        ("decayed sapota tree fruit", "sapota_rotten"),
        ("damaged sapota tree fruit", "sapota_rotten"),
        ("bruised sapota tree fruit", "sapota_rotten"),
        ("old sapota tree fruit", "sapota_rotten"),
        ("overripe sapota tree fruit", "sapota_rotten"),
        ("expired sapota tree fruit", "sapota_rotten"),
        ("sapota tree fruit mold", "sapota_rotten"),
        ("sapota tree fruit fungus", "sapota_rotten"),
        ("sapota tree fruit disease", "sapota_rotten"),
        ("sapota tree fruit rot", "sapota_rotten"),
        ("sapota tree fruit waste", "sapota_rotten"),
        ("sapota tree branch rotten", "sapota_rotten"),
        ("sapota tree hanging rotten", "sapota_rotten"),
        ("sapota tree growing rotten", "sapota_rotten"),
        ("sapota tree cluster rotten", "sapota_rotten"),
        ("chikoo tree fruit rotten", "sapota_rotten"),
        ("brown sapota tree rotten", "sapota_rotten"),
        ("black sapota tree rotten", "sapota_rotten"),
        ("soft sapota tree rotten", "sapota_rotten"),
        ("mushy sapota tree rotten", "sapota_rotten"),
        ("wrinkled sapota tree rotten", "sapota_rotten")
    ]
    
    images_path = 'C:/Users/adiya/Downloads/Fruit-Ripeness-Detection-main/images'
    os.makedirs(images_path, exist_ok=True)
    
    print(f"🤎 Downloading 3000 sapota images with {len(queries)} search queries...")
    
    for i, (query, folder) in enumerate(queries, 1):
        print(f"\n🔍 [{i}/{len(queries)}] Searching: {query}")
        
        urls = download_from_bing(query, 40)
        print(f"Found {len(urls)} URLs")
        
        if not urls:
            continue
        
        success = 0
        for j, url in enumerate(urls, 1):
            print(f"[{j}/{len(urls)}] ", end="")
            if save_image(url, images_path, folder):
                success += 1
                print("✓", end=" ")
            else:
                print("✗", end=" ")
        
        print(f"\n✅ Downloaded {success}/{len(urls)} images to {folder}")
        time.sleep(2)  # Delay between searches
    
    print("\n🎉 Sapota download complete!")
    
    # Show summary
    for folder in ["sapota_ripe", "sapota_raw", "sapota_rotten"]:
        folder_path = os.path.join(images_path, folder)
        if os.path.exists(folder_path):
            count = len([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
            print(f"📁 {folder}: {count} images")