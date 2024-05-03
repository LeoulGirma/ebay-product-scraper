import requests
from bs4 import BeautifulSoup

def extract_ebay_listings(url, max_listings=None):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check response status
    if response.status_code != 200:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        return []
    
    # Print the HTTP response status code
    print(f"HTTP Response Status Code: {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all listings that match the 's-item' class
    listings = soup.find_all('li', class_='s-item')
    products = []

    # Determine the number of listings to process
    listing_count = max_listings if max_listings is not None else len(listings)

    # Process listings based on the specified count
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

# URL of the eBay page
url = "https://www.ebay.com/b/Mens-Hats/52365/bn_738858"
product_list = extract_ebay_listings(url, max_listings=None)  # Set to None to process all listings or specify a number
print(product_list)
