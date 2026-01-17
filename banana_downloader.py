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

def download_from_bing(query, num_images=20):
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
        
        # Scroll to load images
        for i in range(3):
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
        if len(image_urls) < 10:
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
    # Banana queries for 3000 images total (1000 per category)
    queries = [
        # Ripe banana (1000 images) - 50 queries
        ("ripe yellow banana on tree", "banana_ripe"),
        ("fresh yellow banana tree", "banana_ripe"),
        ("sweet yellow banana branch", "banana_ripe"),
        ("juicy yellow banana tree fruit", "banana_ripe"),
        ("perfect yellow banana on branch", "banana_ripe"),
        ("delicious yellow banana tree", "banana_ripe"),
        ("mature yellow banana tree", "banana_ripe"),
        ("ready yellow banana branch", "banana_ripe"),
        ("harvest yellow banana tree", "banana_ripe"),
        ("banana tree ripe yellow fruit", "banana_ripe"),
        ("banana plantation ripe tree", "banana_ripe"),
        ("banana tree harvest season", "banana_ripe"),
        ("banana tree picking ripe", "banana_ripe"),
        ("organic ripe banana tree", "banana_ripe"),
        ("natural ripe banana branch", "banana_ripe"),
        ("healthy ripe banana tree", "banana_ripe"),
        ("banana tree branch ripe", "banana_ripe"),
        ("banana tree bunch ripe", "banana_ripe"),
        ("banana tree hanging ripe", "banana_ripe"),
        ("banana tree growing ripe", "banana_ripe"),
        ("banana tree cluster ripe", "banana_ripe"),
        ("banana tree fruit fresh", "banana_ripe"),
        ("banana tree fruit ripe", "banana_ripe"),
        ("banana tree fruit ready", "banana_ripe"),
        ("bright yellow banana tree", "banana_ripe"),
        ("golden yellow banana tree", "banana_ripe"),
        ("vibrant yellow banana branch", "banana_ripe"),
        ("beautiful yellow banana tree", "banana_ripe"),
        ("premium yellow banana tree", "banana_ripe"),
        ("quality yellow banana branch", "banana_ripe"),
        ("excellent yellow banana tree", "banana_ripe"),
        ("finest yellow banana branch", "banana_ripe"),
        ("best yellow banana tree", "banana_ripe"),
        ("tropical banana tree ripe", "banana_ripe"),
        ("cavendish banana tree ripe", "banana_ripe"),
        ("plantain tree ripe", "banana_ripe"),
        ("banana grove tree ripe", "banana_ripe"),
        ("banana farm tree ripe", "banana_ripe"),
        ("banana garden tree ripe", "banana_ripe"),
        ("banana orchard tree ripe", "banana_ripe"),
        ("banana cultivation ripe", "banana_ripe"),
        ("banana agriculture ripe", "banana_ripe"),
        ("banana farming ripe", "banana_ripe"),
        ("banana growing ripe", "banana_ripe"),
        ("banana production ripe", "banana_ripe"),
        ("banana crop ripe", "banana_ripe"),
        ("banana harvest ripe", "banana_ripe"),
        ("banana season ripe", "banana_ripe"),
        ("banana palm tree ripe", "banana_ripe"),
        ("banana plant tree ripe", "banana_ripe"),
        
        # Unripe banana (1000 images) - 25 queries
        ("unripe green banana on tree", "banana_raw"),
        ("young green banana tree", "banana_raw"),
        ("small green banana branch", "banana_raw"),
        ("hard green banana tree", "banana_raw"),
        ("immature green banana branch", "banana_raw"),
        ("early green banana tree", "banana_raw"),
        ("developing green banana tree", "banana_raw"),
        ("growing green banana tree", "banana_raw"),
        ("banana tree unripe fruit", "banana_raw"),
        ("banana plantation unripe tree", "banana_raw"),
        ("banana branch unripe fruit", "banana_raw"),
        ("banana tree bunch unripe", "banana_raw"),
        ("banana farm tree unripe", "banana_raw"),
        ("banana garden tree unripe", "banana_raw"),
        ("green banana tree sour", "banana_raw"),
        ("green banana tree tart", "banana_raw"),
        ("green banana tree bitter", "banana_raw"),
        ("green banana tree raw", "banana_raw"),
        ("green banana tree not ready", "banana_raw"),
        ("banana tree fruit unripe", "banana_raw"),
        ("banana tree fruit young", "banana_raw"),
        ("banana tree fruit small", "banana_raw"),
        ("banana tree fruit hard", "banana_raw"),
        ("banana tree fruit green", "banana_raw"),
        ("banana cultivation unripe", "banana_raw"),
        
        # Rotten banana (1000 images) - 25 queries  
        ("rotten banana tree fruit", "banana_rotten"),
        ("spoiled banana tree fruit", "banana_rotten"),
        ("bad banana tree fruit", "banana_rotten"),
        ("moldy banana tree fruit", "banana_rotten"),
        ("decayed banana tree fruit", "banana_rotten"),
        ("damaged banana tree fruit", "banana_rotten"),
        ("bruised banana tree fruit", "banana_rotten"),
        ("old banana tree fruit", "banana_rotten"),
        ("overripe banana tree fruit", "banana_rotten"),
        ("expired banana tree fruit", "banana_rotten"),
        ("banana tree fruit mold", "banana_rotten"),
        ("banana tree fruit fungus", "banana_rotten"),
        ("banana tree fruit disease", "banana_rotten"),
        ("banana tree fruit rot", "banana_rotten"),
        ("banana tree fruit waste", "banana_rotten"),
        ("banana tree branch rotten", "banana_rotten"),
        ("banana tree bunch rotten", "banana_rotten"),
        ("banana tree hanging rotten", "banana_rotten"),
        ("banana tree growing rotten", "banana_rotten"),
        ("banana tree cluster rotten", "banana_rotten"),
        ("brown banana tree rotten", "banana_rotten"),
        ("black banana tree rotten", "banana_rotten"),
        ("soft banana tree rotten", "banana_rotten"),
        ("mushy banana tree rotten", "banana_rotten"),
        ("spotted banana tree rotten", "banana_rotten")
    ]
    
    images_path = 'C:/Users/adiya/Downloads/Fruit-Ripeness-Detection-main/images'
    os.makedirs(images_path, exist_ok=True)
    
    print(f"🍌 Downloading 3000 banana images with {len(queries)} search queries...")
    
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
    
    print("\n🎉 Banana download complete!")
    
    # Show summary
    for folder in ["banana_ripe", "banana_raw", "banana_rotten"]:
        folder_path = os.path.join(images_path, folder)
        if os.path.exists(folder_path):
            count = len([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
            print(f"📁 {folder}: {count} images")