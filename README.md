# LeBonCoin Scraper

Un scraper Python pour récupérer les 10 annonces les plus récentes sur Leboncoin.fr correspondant à une recherche donnée.

Ce scrapper utilise Selenium pour charger la page et BeautifulSoup pour parser et extraire les informations des annonces.

## Fonctionnalité

- Extraction de :
  - Titre de l'annonce
  - Prix
  - ID de l'annonce
  - URL complète de l'annonce

## Fonctionnalités non implémentées

**Envoi automatique de messages aux vendeurs** :  
Cette fonctionnalité n'a pas été implémentée pour les raisons suivantes :

- Abscence d'api publique permettant d'envoyer des messages
- Le site impose une connexion obligatoire à un compte utilisateur pour envoyer un message.
- Cela entrainerai donc le non respect des conditions d'utilisation du site et non respect de la loi.

## Prérequis

- Python 3.13+
- Bibliothèques Python :
  - selenium
  - beautifulsoup4
  - python-dotenv

Installez-les avec :
```bash
pip install -r requirements.txt
```

## Configuration

Modifier ou créer le fichier `.env` à la racine du projet avec :
```
NAVIGATOR=FIREFOX  # ou CHROME
```

## Utilisation

1. Placez vous à la racine du projet.

2. Exécutez le script :
```bash
python main.py
```

Le script effectuera automatiquement une recherche sur LeBonCoin pour la requête **"une cible de fléchettes avec les fléchettes"** et affichera dans la console les 10 annonces les plus récentes, avec pour chacune :
- Le titre
- Le prix
- L’ID de l’annonce
- L’URL vers l'annonce

3. **Pour modifier la recherche**  
Ouvrez le fichier `main.py` et changez la ligne dans la fonction `main()` :
```python
scrapper: LeBonCoinScrapper = LeBonCoinScrapper(recherche="une cible de fléchettes avec les fléchettes")
```
Exemples de recherches :
- `"télévision"`
- `"vélo électrique"`
- `"fiat multipla"`

## Exemple de sortie

```bash
> python main.py

Article 1

Titre : Jeu de fléchettes Crane
Prix  : 15 €
Id    : 3113445927
Url   : https://www.leboncoin.fr/ad/jeux_jouets/3113445927
--------------------
Article 2

Titre : Pistolets à fléchettes BOOMCO avec cibles
Prix  : 60 €
Id    : 3113415426
Url   : https://www.leboncoin.fr/ad/jeux_jouets/3113415426
--------------------
Article 3

Titre : Darts fléchettes électronique café pointes métal très bon état
Prix  : 1 000 €
Id    : 3113344081
Url   : https://www.leboncoin.fr/ad/sport_plein_air/3113344081

...

```