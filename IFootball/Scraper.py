import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

# Define the list of URLs
urls = [
    'https://www.espn.in/football/league/_/name/eng.1',
    'https://www.espn.in/football/league/_/name/esp.1',
    'https://www.espn.in/football/league/_/name/ita.1',
    'https://www.espn.in/football/league/_/name/ger.1',
    'https://www.espn.in/football/league/_/name/fra.1',
    'https://www.espn.in/football/league/_/name/uefa.champions'
]

# Asynchronous function to fetch page content
async def fetch_page(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            return await response.text()
    except Exception as e:
        print(f"Failed to retrieve data from {url}: {e}")
        return None

# Asynchronous function to extract headlines from a page
async def extract_headlines(url, session):
    page_content = await fetch_page(url, session)
    news_data = []
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        news_headlines = soup.find_all('h1')
        for headline in news_headlines:
            a_tag = headline.find('a')
            if a_tag:
                news_title = a_tag.get_text().strip()
                news_link = a_tag.get('href')
                if news_link:
                    if news_link.startswith('/football/'):
                        news_link = f'https://www.espn.in{news_link}'
                    elif not news_link.startswith('http'):
                        news_link = f'https://www.espn.in/football{news_link}'
                    
                    # Append to news data without fetching content to save time
                    news_data.append({"title": news_title, "link": news_link})
    return news_data

# Main function to gather all data concurrently
async def gather_all_news():
    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }) as session:
        tasks = [extract_headlines(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Use a set to track unique titles
        unique_titles = set()
        all_news_data = []

        for result in results:
            if result:
                for item in result:
                    title = item["title"]
                    if title not in unique_titles:
                        unique_titles.add(title)
                        all_news_data.append(item)

        return all_news_data

# Write to JSON file
json_file = 'espn_news_headlines.json'


news_data = asyncio.run(gather_all_news())
with open(json_file, mode='w', encoding='utf-8') as file:
    json.dump(news_data, file, indent=4, ensure_ascii=False)

print(f"Data has been written to {json_file}")
