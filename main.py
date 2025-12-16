from scrapper import *

def main() -> None:
    scrapper: LeBonCoinScrapper = LeBonCoinScrapper(recherche="une cible de fléchettes avec les fléchettes")
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

if __name__ == "__main__":
    main()