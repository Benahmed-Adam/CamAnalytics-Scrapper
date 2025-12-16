import os
import dotenv
import requests
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional
from selenium.webdriver.remote.webdriver import WebDriver

dotenv.load_dotenv()
NAVIGATOR: Optional[str] = os.environ.get("NAVIGATOR")

ArticleDict = Dict[str, str]

class LeBonCoinScrapper:
    url: str
    browser: WebDriver
    
    def __init__(self, recherche: str) -> None:
        self.url = "https://www.leboncoin.fr/recherche?text=" + urllib.parse.quote_plus(recherche) + "&sort=time&order=desc"
        
        if NAVIGATOR == "FIREFOX":
            self.browser = webdriver.Firefox()
        elif NAVIGATOR == "CHROME":
            self.browser = webdriver.Chrome()
        else:
            print("Non")
            exit(-1)
        
    def scrape(self, limit: int = 10) -> List[ArticleDict]:
        results: List[ArticleDict] = []
        
        try:
            self.browser.get(self.url)
            
            soup: BeautifulSoup = BeautifulSoup(self.browser.page_source, "html.parser")
            
            annonces: List[Tag] = soup.find_all("article")

            for annonce in annonces:
                if len(results) >= limit:
                    break
                
                title: str = annonce.find("p", {"data-test-id": "adcard-title"}).text
                price: str = annonce.find("p", {"data-test-id": "price"}).text
                relative_link: str = annonce.find("a")["href"]

                results.append({
                    "titre" : title,
                    "prix" : price.split("Baisse de prix")[0].strip(),
                    "id" : relative_link.split("/")[-1],
                    "url" : "https://www.leboncoin.fr" + relative_link
                })
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.browser.quit()

        return results