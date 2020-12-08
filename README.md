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
    ##########      getArticles.py      ##########
    ##########      getCodes.py     ##########
    ##########      parseCodes.py     ##########
    ##########      parseDirty.py     ##########
    ##########      repair_db.py     ##########
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

        