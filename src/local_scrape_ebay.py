import os
from bs4 import BeautifulSoup

def extract_ebay_listings_from_file(file_path, max_listings=None):
    # print("Current Working Directory:", os.getcwd())
    # print("Trying to open the file:", file_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up two levels from the current file
    full_path = os.path.join(base_dir, file_path)
    print(f"Trying to open the file: {full_path}")

    with open(full_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')

    listings = soup.find_all('li', class_='s-item')
    products = []

    listing_count = max_listings if max_listings is not None else len(listings)

    for index, item in enumerate(listings[:listing_count]):
        title_tag = item.find('h3', class_='s-item__title')
        title = title_tag.text if title_tag else 'No title found'
        
        price_tag = item.find('span', class_='s-item__price')
        price = price_tag.text if price_tag else 'No price found'
        
        shipping_tag = item.find('span', class_='s-item__shipping')
        shipping = shipping_tag.text if shipping_tag else 'No shipping info'
        
        image_tag = item.find('img', class_='s-item__image-img')
        image_url = image_tag['src'] if image_tag else 'No image URL'
        
        print(f"Processing listing {index + 1}: {title}")

        products.append({
            'title': title,
            'price': price,
            'shipping': shipping,
            'image_url': image_url
        })

    return products

# file_path = "..\data\Men's Hats for Sale - eBay.html"
# product_list = extract_ebay_listings_from_file(file_path, max_listings=None)  # Set to None to process all listings
# print(product_list)
