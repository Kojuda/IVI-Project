# IVI-Project
IVI Project
groupe 1

L'ensemble des scripts permettent d'extraire les annonces concernant des oiseaux de la plateforme Adpost.com afin des les stocker
dans une base de données SQL. Ces dernières sont ensuite parsées pour en tirer les informations utiles. Une étape plus fine d'une 
parsing consiste à inférer les espèces d'oiseaux qui concernent l'annonce pour les relier à une espèce de CITES. Les informations
une fois raffinées sont stockées dans des tables de la base de données pour être exportées au format CSV et analyser dans Tableau
Software.

Les sous-parties suivantes expliquent la répartition des données dans le dossier et la fonction des scripts. 

Les dépendances nécessaires : sqlalchemy, lxml, matlabplotlib, pandas, pipreqs, selenium, pysocks, requests, seaborn.


Ordres des scripts pour récolter les données (V=Veille possible/Interruption possible) :

    -> getCountries.py -> getArticles.py (V) -> getCodes.py (V)

Ordres des scripts pour parser les données :

    Baseline :
        -> parseCodes.py -> parseDirty.py
    Classification 1 :
        -> classification_1_parsing_birdorno.py -> classification_1_Cage.py -> classification_1_parsing_parrotorno.py
    Classification 2 et 3 :
        -> classification_2_and_3.py

Ordres des scripts pour l'analyse si disponible en script :

    Evaluation classification 2 et 3 :
        classification_2_and_3_evaluation.ipynb
    Visualisation classification 1 :
        classification_1_visualisation.ipynb
    Prétraitement pour Tableau Software :
        classification_to_analysis.ipynb



~~~~~~~~~~~~~~~~~~ RESSOURCES ~~~~~~~~~~~~~~~~~~

    ##########      db.py     ##########

        Ressource qui permet d'établir un interpréteur des tables de la base de données SQL
        avec sqlalchemy. Les colonnes et leur contraintes, le nom des tables et les fonctions pour
        interagir avec sont notamment définis dans la ressource.

    ##########      webdriver.py     ##########

        Ressource permettant d'utiliser les webdrivers pour faire du crawling avec plusieurs fonctions
        utiles.

    ##########      documentation.py     ##########

        Ressource permettant la documentation du matériel utilisé lors de l'utilisation de script, la date,
        les logs d'actions et les logs d'erreur. Assure la reproductibilité.

    ##########      http_requests.py     ##########

        Ressource permettant d'utiliser des requêtes HTTP via le module requests.

    ##########      outil_dns.py     ##########

        Ressource fournissant des fonctions permettant d'obtenir des informations des serveurs DNS. (inutilisées)

    ##########      outil_whois.py     ##########

        Ressource fournissant des fonctions permettant d'obtenir du protocol WHOIS. (inutilisées)

    ##########      project_utils.py     ##########

        Ressource permettant d'utiliser des fonctions courantes dans l'ensemble du projet (e.g. conversion du noms du pays
        en son abréviation.)

    ##########      regex_tools.py     ##########

        Ressources fournissant des functions utiles pour l'ensemble des travaux sur les expressions régulières. De plus, 
        l'ensemble des lexiques et dictionnaires utilisés pour générer les expressions régulières pour transformer
        des caractères dans une chaîne sont stockés dans ce module.



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

        Ce script fait partie de la première classification. Le but est de classer les annonces selon
        si elles mentionnent la présence d'oiseaux ou non. Selon des termes majoritairement anglais. Les
        résults sont stockés dans la table "classification_1_parse_bird_or_no

    ##########      classification_1_parsing_parrotorno.py     ##########

        Ce script fait partie de la première classification. Il permet d'établir la liste des mots recherchés
        dans une annonce et d'établir si ces mots font partie du lexique concernant les psittaciforems et/ou si
        ces mots font parties du lexique des espèces CITES de la table "mapping_cites". Les données sont stockées
        dans la table "classification_1_psittaciformes_or_no" (matches par annonce), "classification_1_regex" 
        (expressions régulières utilisées lors du script) et "classification_1_reg_map_match" (correspondance 
        entre une expression régulière/mot et une espèce de la table "mapping_cites") 

    ##########      classification_1_Cage.py     ##########

        Ce script fait partie de la première classification. Il cherche à établir la présence
        de cage dans les annonces qui contriburait au taux de faux-positifs. Les résultats sont 
        stockés dans la table "classification_1_cage"

    ##########      classification_2_and_3.py     ##########

        Ce script permet de faire la classification 2 et 3 en fonction des champs de texte des 
        annonces. Il génère des expressions régulières pour notamment détecter la mention d'oiseaux,
        la mention de perroquets, la mention des espèces de la table "mapping_cites", la mention de cages,
        la mention d'oeufs et la mention des papiers de regristrations CITES. L'assignation des espèces 
        est fait en créant une expression régulière en fonction des divers noms communs existants pour une
        espèce. La différence entre la classification 2 et 3 est la disposition des mots, respectivement 
        désordonnée et ordonnée selon le nom commun choisi. Les résultats sont stockées dans les tables 
        "classification_2_matching_ads" et "classification_3_matching_ads"

    ##########      classification_2_and_3_evaluation.ipynb     ##########

        Ce script permet de créer des sous-échantillons des classifications 2 et 3 avec une pondération
        suivant la règle log(1/sum(freq(assignation))) qui permet d'obtenir les assignations d'espèces rares
        dans une quantité plus raisonnable tout en rendant le tirage d'assignation très fréquentes proportionnel
        à leur apparition. Cela permet d'évaluer de manière plus complète les cas particulier de la classification
        avec un petit échantillon labelisé à la main. Le script évalue les statistiques d'évaluation une fois que 
        les tables sont remplies à la main pour mettre le score de classement de chaque annonce.

    ##########      classification_to_analysis.ipynb     ##########

        Ce script permet d'effectuer un prétraitement sur les résultats de la classification 2 et 3 afin
        d'être facilement utilisables par Tableau Software. Notamment, il sépare l'ensemble des espèces
        ayant eu un match par annonce en colonnes, puis les stack pour pouvoir avoir une ligne par match 
        spécifique. Sans cela, le trop grand nombre de colonnes n'est pas bien exploité par Tableau Software
        et il ne peut pas créer de relation entre les labels des colonnes et les valeurs d'une colonne entre
        2 tables. De plus, il permet de créer une table de la classification 1 au format "bag of words" utilisé
        pour la visualisation au format "small multiples" par le script "classification_1_visualisation.ipynb" 
        Les résultats sont stockés dans la table "classification_1_analysis", "classification_2_analysis"
        et "classification_3_analysis"

    ##########      classification_1_visualisation.ipynb     ##########

        Ce script permet de visualiser les occurrences des mots par espèce selon la classification 1 au format
        "small multiples". Les résultats sont sous la forme d'une image dans le répertoire /results/graphes


~~~~~~~~~~~~~~~~~~ FOLDERS ~~~~~~~~~~~~~~~~~~

    ##########      results     ##########

        -_-_-   DATABASES   -_-_-
            Contient la database SQL contenant toutes les tables. (project.db)
        -_-_-   Tableau_IVI   -_-_-
            Contient tous les fichiers Tableau Software utilisés pour l'analyse
            ainsi que les tables exportées au format CSV ou Excel
        -_-_-   *nom script*   -_-_-
            Contient les résultats d'un script spécifique. Notamment la documentation
            de son lancement, les codes des pages ou les screenshots des pages.

    ##########      graphes     ##########

        Contient les visualisations du script "classification_1_visualisation.ipynb"

    ##########      webdrivers     ##########

        Contient les webdrivers de Firefox et Chrome utilisés pour le crawling.

    ##########      ressources     ##########

        Contient tous les scripts utilisés comme ressources.

        