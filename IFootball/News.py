import json
import requests
from Queries import Queries
from bs4 import BeautifulSoup
from urllib.parse import unquote

class News:
    
    @staticmethod
    def show_news_in_home():

        with open('espn_news_headlines.json', 'r', encoding="utf-8") as file:
            news_data = json.load(file)
        displayed_news = set()
        matched_news = []
        
        for news in news_data:
            if news["title"] not in displayed_news:
                matched_news.append({"title": news["title"], "link": news["link"]})
                displayed_news.add(news["title"])
        
        return matched_news
            

    @staticmethod
    def get_fav_team_news_headlines(team_id):
        team_name = Queries.get_team_full_name_by_id(team_id)
        if(team_name==None):
            return
        with open('espn_news_headlines.json', 'r', encoding="utf-8") as file:
            news_data = json.load(file)

        keywords = team_name.lower().split()
        displayed_news = set()
        matched_news = []
        
        for news in news_data:
            title_lower = news["title"].lower()
            link_lower = news["link"].lower()

            title_match = any(keyword in title_lower for keyword in keywords)
            link_match = any(keyword in link_lower for keyword in keywords)

            if (title_match or link_match) and news["title"] not in displayed_news:
                matched_news.append({"title": news["title"], "link": news["link"]})
                displayed_news.add(news["title"])
        
        return matched_news
    

    def scrape_news_paragraphs(url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            page = requests.get(url, headers=headers)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

        soup = BeautifulSoup(page.text, 'lxml')
        
        img_wrap = soup.find('div', class_='img-wrap')
        if img_wrap:
            source_tag = img_wrap.find('source')  # Look for the first <source> tag within img-wrap
            img_url = source_tag['srcset'].split(',')[0].strip() if source_tag and 'srcset' in source_tag.attrs else "No image found"
        else:
            img_url = "No image found"
        
        paragraphs = soup.find_all('p')
        article_body = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        unwanted_intro = "welcome to espn india edition"
        if article_body and article_body.lower().startswith(unwanted_intro):
            article_body = article_body[len(unwanted_intro):].strip()
        if not article_body:
            article_body = "No content found in <p> tags."

        return article_body,img_url