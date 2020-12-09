# IVI-Project
IVI Project
groupe 1

L'ensemble des scripts permettent d'extraire les annonces concernant des oiseaux de la plateforme Adpost.com afin des les stocker
dans une base de données SQL. Ces dernières sont ensuite parsées pour en tirer les informations utiles. Une étape plus fine d'une 
parsing consiste à inférer les espèces d'oiseaux qui concernent l'annonce pour les relier à une espèce de CITES. Les informations
une fois raffinées sont stockées dans des tables de la base de données pour être exportées au format CSV et analyser dans Tableau
Software.

Les sous-parties suivantes expliquent la répartition des données dans le dossier et la fonction des scripts. 

Les dépendances nécessaires : sqlalchemy, lxml, matlabplotlib, pandas, pipreqs, selenium, pysocks, requests.

~~~~~~~~~~~~~~~~~~ RESSOURCES ~~~~~~~~~~~~~~~~~~

    ##########      db.py     ##########
    ##########      webdriver.py     ##########
    ##########      documentation.py     ##########
    ##########      http_requests.py     ##########
    ##########      outil_dns.py     ##########
    ##########      outil_whois.py     ##########
    ##########      project_utils.py     ##########
    ##########      regex_tools.py     ##########



~~~~~~~~~~~~~~~~~~ SCRIPTS ~~~~~~~~~~~~~~~~~~

    ##########      getCountries.py     ##########

        Simple script qui extrait les quelques liens correspondant aux différents pays de Adpost.com Les données
        sont stockées dans la table "country"
    
    ##########      getArticles.py      ##########

        Ce code parcourt l'ensemble des pages d'annonces d'oiseaux de chaque pays de Adpost.com en prélevant les urls et en
        enregistrant le code client et le screenshot de la première page visionnée par le webdriver pour documenter la structure
        du site au moment du crawling. Les urls sont sauvegardé dans la base de données SQL avec status destiné à un autre script
        pour vérifier l'état de leur extraction. Les données sont stockées dans la table "urls_ads"
    
    ##########      getCodes.py     ##########

        Ce script parcourt les urls des annonces récoltées dans la base de données dans la table "urls_ades"
        pour extraire les codes clients des annonces ainsi que le screenshot de ces dernières. Les noms des codes
        extraits sont stockés dans la table "ads_codes" et les données comprenant les codes clients et les screenshots
        sont stockées dans le sous-répertoire de "results" concernant ce script.

    ##########      parseCodes.py     ##########

        Le script itère à travers la base de données pour parser les données de tous les codes clients récoltés sous les
        différents répertoires de la plateforme Adpost.com. Les données sont stockées dans la table "parse_codes"

    ##########      parseDirty.py     ##########

        Ce script permet de prendre les données brutes parsées dans la table "parse_ads" pour parser cette fois le texte de 
        l'annonce est retiré des informations pertinentes. Certains champs sont aussi rendus plus propres afin de pouvoir être
        manipulés par un outil d'analyse. (e.g. le champ concernent l'argent)

    ##########      repair_db.py     ##########

        Ce script a servi à corriger la table des urls de la base de données pour rajouter un identifiant unique car
        le numéro de l'annonce s'est révélé être unique uniquement pour un répertoire de la plateforme concernant un pays.

    ##########      classification_1_parsing_birdorno.py     ##########
    ##########      classification_1_parsing_parrotorno.py     ##########
    ##########      classification_1_Cage.py     ##########
    ##########      classification_2_and_3.py     ##########
    ##########      classification_2_and_3_evaluation.ipynb     ##########
    ##########      classification_to_analysis.ipynb     ##########


~~~~~~~~~~~~~~~~~~ FOLDERS ~~~~~~~~~~~~~~~~~~
    ##########      results     ##########
        -_-_-   DATABASES   -_-_-
        -_-_-   Tableau_IVI   -_-_-
        -_-_-   *nom script*   -_-_-

    ##########      graphes     ##########

    ##########      webdrivers     ##########

    ##########      ressources     ##########

        