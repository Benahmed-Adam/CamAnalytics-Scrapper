import os
import json
import time
import dotenv
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup, Tag, Any
from typing import List, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()
NAVIGATOR: Optional[str] = os.environ.get("NAVIGATOR")
COOKIES_JSON_STRING: Optional[str] = os.environ.get("COOKIES")

COOKIES: List[Dict[str, Any]] = []

if COOKIES_JSON_STRING:
    try:
        COOKIES = json.loads(COOKIES_JSON_STRING)
    except Exception as e:
        print(f"Erreur avec les cookies : {e}")
        exit(-1)
else:
    print("Les cookies ne sont pas là")
    exit(-1)

ArticleDict = Dict[str, str]

class LeBonCoinScrapper:
    url: str
    browser: WebDriver
    
    def __init__(self, recherche: str) -> None:
        self.url = "https://www.leboncoin.fr/recherche?text=" + urllib.parse.quote_plus(recherche) + "&sort=time&order=asc"
        
        if NAVIGATOR == "FIREFOX":
            self.browser = webdriver.Firefox()
        elif NAVIGATOR == "CHROME":
            self.browser = webdriver.Chrome()
        else:
            print("Non")
            exit(-1)
        
        self.browser.get("https://leboncoin.fr")

        for cookie in COOKIES:
            cookie_data = {
                "name": cookie["name"],
                "value": cookie["value"],
                "domain": cookie["domain"],
                "path": cookie["path"],
                "secure": cookie["secure"],
                "httpOnly": cookie["httpOnly"],
            }
                
            self.browser.add_cookie(cookie_data)
        
    def scrape(self, limit: int = 10) -> List[ArticleDict]:
        results: List[ArticleDict] = []
        
        try:
            self.browser.get(self.url)

            bouton_accepter = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            
            bouton_accepter.click()
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
            print(f"Erreurr : {e}")

        return results
    
    def send_message(self, results: List[ArticleDict]) -> None:
        for r in results:
                self.browser.get(f"https://leboncoin.fr/reply/{r['id']}")

                try:
                    textarea = WebDriverWait(self.browser, 20).until(
                        EC.presence_of_element_located((By.ID, "body"))
                    )
                    time.sleep(0.5)
                    textarea.clear()
                    time.sleep(1)
                    textarea.send_keys("Votre bien est-t il toujours disponible ?")
                    
                    button = WebDriverWait(self.browser, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Envoyer']"))
                    )
                    
                    button.click()
                    
                    print(f"Message envoyé pour l'annonce ID: {r["id"]}")
                except Exception as e:
                    print(f"Erreur : {e}")
                    continue
    
    def close(self) -> None:
        self.browser.close()