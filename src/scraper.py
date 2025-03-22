import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pprint import pprint
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from insert_data import insert_data
from database import create_tables, drop_tables

def scrape_github_data(url):
    
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data")
        exit()

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the projects
    projects = soup.find_all("article", class_="Box-row")

    list = []
    for r in projects:       
        # Get the project name
        project = r.h2.a.text.strip().replace("\n", "").replace(" ", "")
        matches = re.match(r"(.*)\/(.*)", project)
        user = matches[1]
        name = matches[2]
        
        # Get description
        description = r.find("p")
        description = description.text.strip() if description else None
        
        # Get the language
        language_t = r.find("span", itemprop="programmingLanguage")
        language = language_t.text.strip() if language_t else None
        
        # Get stars and forks
        stars = int(r.find("a", href=f"/{project}/stargazers").text.strip().replace(",",""))
        forks = int(r.find("a", href=f"/{project}/forks").text.strip().replace(",",""))
        url = f"https://github.com/{project}"
        
        list.append({
            'user': user,
            'name': name,
            'project': project,
            'description': description,
            'language': language,
            'stars': stars,
            'forks': forks,
            'url': url
        })
    
    return list

if __name__ == "__main__":
    create_tables()
    
    daily_data = scrape_github_data("https://github.com/trending?since=daily")
    insert_data(daily_data, 'daily')
    
    weekly_data = scrape_github_data("https://github.com/trending?since=weekly")
    insert_data(weekly_data, 'weekly')
    
    monthly_data = scrape_github_data("https://github.com/trending?since=monthly")
    insert_data(monthly_data, 'monthly')