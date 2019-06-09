# Rapport Mini-projet 
# QSELF 2019

## HES-SO MSE 


Pedro Costa & Louis Delabays

---

## 1. Introduction

Dans le cadre du cours *Quantified Self*, il nous a été demandé de réaliser un projet en relation avec les thèmes vus durant le semestre. 

Notre projet a pour but de fournir un moyen de comparer des courses à pieds de manière un peu similaire à l'application **Strava**. Avec Strava, les segments ont été définis par un utilisateur qui a choisi un point de départ et un points d'arrivé d'une portion de sa course qu'il trouvait intéressant. Ensuite, pour chaque nouvelle course l'application détecte les portions qui correpsondent à un segment. Finalement, nous avons la possibiltié de comparer nos différents efforts sur ce segment ou de se comparer avec d'autres athlètes.

Ce que nous voulons réaliser est un peu différent: Notre application (script Python) trouvera d'elle même les segments intéressants sans l'intervention de l'utilisateur. Plusieurs courses à pieds seront fournies à l'application pour qu'elle trouve les portions communes des différentes courses à pieds. L'utilisateur pourra ensuite visualiser les courses et comparer les segments communs. Le descriptions complètes et détaillées du projet se trouve au chapitre suivant (*2. Description et but*).

Nous avons choisi d'utiliser des données existantes et ne pas avoir besoin d'en récolter au début du projet. Ces données sont des courses à pieds réalisé par Louis. Elles ont été enregistrées au moyen d'une montre GPS Garmin (Forerunner 645). Les détails sur l'extraction et l'exploitation de ces données sont décrite plus bas dans ce rapport (*3. Récupération des courses depuis la montre*)

Ce rapport décrit les différentes étapes effectuées depuis la récupération des données jusqu'à la visualisation/comparaison des segments.

Pour utiliser le projet il faut se référer au fichier **README.md** à la racine du projet.

## 2. Description et but

### 2.1 But du projet

Le but de ce projet est d'extraire les segments les plus interéssants à partir des courses à pied mise à disposition par un utilisateur. Dans un premier temps, toutes les courses sont confrontées à toutes les autres. Cette phase permet d'obtenir une liste de segments pour chaque course (chap. *4. Extraction des segments*). 

Avec la liste de segments d'une course, on extrait trois types de segments :

* le segment avec le plus de dénivelation positive
* le segment le plus long
* le segment avec la densité moyenne de segment la plus haute

Après avoir obtenu ces trois segments, il est possible d'effectuer  "l'inférence" d'une course. Cette étape consiste à trouver les autres courses disponibles qui passent aussi par l'un de ces trois segments. Nous avons appelé ça des *match*.

La dernière étape n'est autre que la visualition et la comparaison de la course de référence avec les courses qui ont matché un segment d'intérêts. 

### 2.2 Description

Ce point précise quelques détails de l'implémentation générale sur le projet.

* L'extraction des segments et l'inférence des courses requiert un temps de calcul passablement long (la complexité pour effectuer des comparaison *all vs all* est élevée). Pour éviter de devoir patienter pour visualiser les courses, les objets qui contiennent les données traitées sont enregistrés dans des fichiers *pickle*. Ce qui permet de les charger rapidement.

* L'ajout d'une nouvelle course parmis celle déjà à disposition nécessite de régénérer les listes de segments pour chaque course ou du moins partiellement. Ce cas d'utilisation, qui correspond à l'usage principale d'une telle application, n'est pas optimiser et n'a pas été testé durant le réalisation de ce projet.

* La génération des fichiers *html* par le package *gmplot* de Google nécessite une *API key* pour visualiser correctement les cartes. Le script Python vérifie si la variable d'environnement de cette clé est vide ou pas et construit les objets (GoogleMapPlotter) en conséquence. Si elle n'est pas présente, c'est le mode développeur qui s'affiche: Les cartes sont un peu grisée et un filigrane est appliqué.

### 2.3 Architecture logicielle




## 3. Récupération des courses depuis la montre

** Garmin en mode *USB Mass Storage*
** .fit 
** class Point
** en dataframe
** class race

Les fichiers de données `.fit` sont stockés dan sla mémoire interne de la montre GPS. Pour les récupérer, il faut que la montre soit configurer en *USB Mass Storage*, ainsi il suffit de la brancher à un ordinateur pour copier les fichiers `.fit` des activités effectuées. 

#### ----Capture d'écran ?----

Avec le package Python **fitparse** et sa classe **FitFile**, nous avons pu récupérer facilement les données contenues dans les fichiers `.fit`.
Ce fichier contient un certain nombre de points enregistrés chaque seconde (dépend du mode d'enregistrement configuré dans la montre). Chaque point renferme les valeurs suivantes:

* Timestamp
* todo...

...

Pour nos besoins, nous avons changé l'organisation des données des activité afin de simplifier leurs utlisations. Nous avons 2 manières de stocker les activités pour les exploiter ensuite:

* En liste de Point (nous avons créer la classe Point)
#### ----Capture d'écran ?----

* en Dataframe Pandas
#### ----Capture d'écran ?----


Et finalement, une classe Race ...


## 4. Extraction des segments

**Distance en 2 portion de 2 course --> "fenêtre glissante"
**Séparation des "morceaux" continuu pour obtenir une liste de segments
**Filtrage des segments trouvés
**Toutes les courses vs toutes les courses

** class RaceManager
** class segment

## 5. Recherche des segments pertinents

**3 types de segments : plus long, plus de déniv., plus de densité 
** class BestSegment

### 5.1 Segment avec le plus de dénivelation

### 5.2 Segment le plus long

### 5.3 Segment avec le plus de densité moyenne


## 6. Recherche des courses avec segments communs

**"inférence"
**on reprend les segments du pt précédents et on cherche quelle course "match"
**on obtient une liste de course et de segments --> visualisation/comparaison
** class RaceInferer

## 7. Visualisation des courses & segments

**Server
**Navigation

## 8. Conclusion

## 9. Perspectives d'améliorations

**ajouter des type de segment intéressant 
**prendre les 5 meilleures segments de chaque type (ex. les 5 meilleures segments de dénivelation) pour chaque course

** fait d'ajouter une nouvelle course au set de courses 

## 10. Bibliographie

---


