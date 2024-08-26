import requests
from bs4 import BeautifulSoup

def fetch_image(recipe_name):
    search_url = f"https://www.food.com/search/{recipe_name.replace(' ', '%20')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first recipe card image
    image_tag = soup.find('img', class_='search-card__img')

    if image_tag:
        return image_tag['src']
    return None

# Example usage:
recipe_name = "Spaghetti Bolognese"
image_url = fetch_image(recipe_name)

if image_url:
    print(f"Image URL: {image_url}")
else:
    print("Image not found.")
