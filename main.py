from scrapper import *

def main() -> None:
    scrapper: LeBonCoinScrapper = LeBonCoinScrapper(recherche="feutres")
    result: List[ArticleDict] = scrapper.scrape()

    if result:
        for i, article in enumerate(result, 1):
            print(f"Article {i}\n")
            print("Titre : " + article["titre"])
            print("Prix  : " + article["prix"])
            print("Id    : " + article["id"])
            print("Url   : " + article["url"])
            print("-" * 20)
    else:
        print("Pas d'articles récupéré, captcha ?")
    
    print("Envoi de messages...")
    
    scrapper.send_message(result)

    scrapper.close()

if __name__ == "__main__":
    main()