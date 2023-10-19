import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Create an empty DataFrame to store the data
df = pd.DataFrame(columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])

# Scrape data from multiple pages (20 pages)
for page in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}'

    headers = {
        'User-Agent': 'Your User Agent'  # Set your user agent
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in product_items:
            product_url_element = item.find('a', class_='a-link-normal s-no-outline')
            product_name_element = item.find('span', {'class': 'a-text-normal'})
            product_price_element = item.find('span', {'class': 'a-price-whole'})
            rating_element = item.find('span', {'class': 'a-icon-alt'})
            num_reviews_element = item.find('span', {'class': 'a-size-base s-underline-text'})

            # Check if elements exist before extracting data
            if product_url_element:
                product_url = product_url_element['href']
            else:
                product_url = 'N/A'

            if product_name_element:
                product_name = product_name_element.text
            else:
                product_name = 'N/A'

            if product_price_element:
                product_price = product_price_element.text
            else:
                product_price = 'N/A'

            if rating_element:
                rating = rating_element.text
            else:
                rating = 'N/A'

            if num_reviews_element:
                num_reviews = num_reviews_element.text
            else:
                num_reviews = 'N/A'

            # Add the data to the DataFrame
            df = df.append({
                'Product URL': f"https://amazon.in/{product_url}",
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews
            }, ignore_index=True)
    else:
        print(f"Failed to retrieve page {page} with status code {response.status_code}")

    # Add a delay to avoid overwhelming the server
    time.sleep(2)  # You can adjust the delay as needed

# Save the DataFrame to a CSV file
df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
