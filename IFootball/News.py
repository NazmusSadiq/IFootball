import json
import requests
from bs4 import BeautifulSoup

class News:
    
    @staticmethod
    def show_news_in_home(news):
        article_content = News.scrape_news_paragraphs(news["link"])

        print(f"\n{article_content}\n")
            

    @staticmethod
    def get_fav_team_news_headlines(team_name):
        with open('espn_news_headlines.json', 'r') as file:
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

        paragraphs = soup.find_all('p')
        article_body = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        unwanted_intro = "welcome to espn india edition"
        if article_body and article_body.lower().startswith(unwanted_intro):
            article_body = article_body[len(unwanted_intro):].strip()
        if not article_body:
            article_body = "No content found in <p> tags."

        return article_body