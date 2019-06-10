# Rapport Mini-projet 
# QSELF 2019

## HES-SO MSE 


Pedro Costa & Louis Delabays

---

## 1. Introduction

Dans le cadre du cours *Quantified Self*, il nous a été demandé de réaliser un projet en relation avec les thèmes vus durant le semestre. 

Notre projet a pour but de fournir un moyen de comparer des courses à pieds de manière un peu similaire à l'application **Strava**. Avec Strava, les segments ont été définis par un utilisateur qui a choisi un point de départ et un points d'arrivé d'une portion de sa course qu'il trouvait intéressant. Ensuite, pour chaque nouvelle course l'application détecte les portions qui correpsondent à un segment. Finalement, nous avons la possibilité de comparer nos différents efforts sur ce segment ou de se comparer avec d'autres athlètes.

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

...


## 3. Récupération des courses depuis la montre

Les fichiers de données `.fit` sont stockés dan sla mémoire interne de la montre GPS. Pour les récupérer, il faut que la montre soit configurer en *USB Mass Storage*, ainsi il suffit de la brancher à un ordinateur pour copier les fichiers `.fit` des activités effectuées. 

Avec le package Python **fitparse** et sa classe **FitFile**, nous avons pu récupérer facilement les données contenues dans les fichiers `.fit`.
Ce fichier contient un certain nombre de points enregistrés chaque seconde (dépend du mode d'enregistrement configuré dans la montre). Chaque point renferme les valeurs suivantes:

* `timestamp` :  Date et heure de la mesure
* `position_lat` : Latitude 
* `position_long` : Longitude
* `distance` : Distance parcourue depuis le début de l'activité
* `enhanced_altitude` : Altitude corrigée (à vérifier)
* `altitude` : Altitude
* `enhanced_speed` : Vitesse corrigée [m/s] (à vérifier)
* `speed` : Vitesse [m/s]
* `heart_rate` : Fréquence cardique
* `cadence` : Cadence de course [step/minute]
* `temperature` : température
* `fractional_cadence` : (?) Valeur soit 0, soit 0.5


Pour nos besoins, nous avons changé l'organisation des données des activité afin de simplifier leurs utlisations. Nous avons 2 manières de stocker les activités pour les exploiter ensuite:

* En liste d'objet `Point` (nous avons créer la classe Point)
* en Dataframe Pandas

Et finalement, une classe `Race` contient les 2 représentations de l'activité. Toutes les activités sont stockées dans une classe `RaceManager` dont les autres fonctionnalités sont détaillées par la suite. 

## 4. Extraction des segments

### 4.1 Comparaison des courses (deux à deux)

Pour trouver les portions communes entre deux courses, nous avons implémenté plusieurs classes qui permettent d'effectuer ces opérations. Dans un premier temps, nous avons cherché des librairies pour trouver les plus longues portions communes. Par exemple, l'algorithme LCSS (Longest Common Subsequence) qui est utilisé pour trouver des mots/pharses à partir de lettre ou de phonèmes. Malheureusement, les seuls implémentations trouvées pour des trajectoires en deux dimensons ne permettaient pas de faire le traitment que nous avions besoin. En effet, les coordonnées GPS des différentes courses à pieds sont toutes diffférentes. Par conséquent, il faut que nous puissions définir une *tolérance* pour laquelle nous considérons que les coordonnées sont tout de même *identiques*.

Afin d'extraire les portions communes entre deux courses, nous avons travaillé avec des fenêtres de dix points à la fois: On prend les dix premiers points de la courses de références que l'on compare avec ceux de la deuxième course. Ensuite, on fait avancer le fenêtre de dix points de la deuxième course et l'on compare à nouveau avec la course de référence. Les figures ci-dessous illustrent ce processus:

## IMAGE 

Une fois que la première fenêtre est passée devant toute la deuxième course, on l'avance de cinq points (cette valeur a été trouvée par essais; avancer de plusieurs points permet de diminuer le temps de calculs). Pour la simplicité de l'explication, la fenêtre n'est avancer que d'un point dans ces figures:

## IMAGE

Pour définir qu'une fenêtre *matche* avec l'autre course, les dix distances points-à-points sont sommées et si elle est inférieur à un seuil, alors on stocke le fenêtre de dix points. Pour extraire les segments, on sépare les parties continues et discontinues: 

## IMAGE

On obtient une liste de portions communes aux deux courses et pour améliorer les étapes suivantes, les trajectoires communes sont moyennées:

## IMAGE / screen

Finalement, les portions communes sont transformées en objet `Segment` qui contient les points des courses sources et la trajectoire moyennées. Cette objet permet également de retrouver les deux courses qui ont permis de trouver ce segment.


### 4.2 Au niveau de l'application

La procédure décrite au *point 4.1* est effectuée dans l'application pour chaque course contre toutes les autres courses. Ainsi, dans l'objet `RaceManager`, il y a un dictionnaire avec une clé par course qui contient une liste de tous les segments trouvées pour cette clé. Cette liste de segments en contient souvent plusieurs dizaines et ils sont pour la plupart très similaire. L'étape de traitement suivante extrait parmis les segments de la liste les plus pertinents selon plusieurs critères.

## 5. Recherche des segments pertinents

Etant donné le nombre trop important de segments trouvés pour chaque course (chapitre précédent), nous avons décidé de nous focaliser sur trois types de segments, à savoir le segment le plus long, celui avec le plus de dévivelation positive et celui avec la densité moyenne la plus élevée.

Pour extraire les segments les plus pertinents pour chaque type, nous avons implémenté la classe `BestSegment`.

### 5.1 Segment avec le plus de dénivelation



### 5.2 Segment le plus long



### 5.3 Segment avec le plus de densité moyenne

Ce dernier type de segment est celui qui nécessite le plus d'opérations et de temps à l'extration. Mais c'est aussi un segment très intéressant car, normalement, un nombre plus important de courses vont matcher avec lui. Donc, cela permet de le comparer avec un plus grand nombre d'efforts différents du même utiliateurs.

La première étape consiste à créer une *density map* pour chaque course à partir de tous les segments trouvés au chapitre 4. Pour cela,  

## IMAGE density map


## IMAGE avec density > à ...




## 6. Recherche des courses avec segments communs

**"inférence"
**on reprend les segments du pt précédents et on cherche quelle course "match"
**on obtient une liste de course et de segments --> visualisation/comparaison
** class `RaceInferer`

## 7. Visualisation des courses & segments

**Server
**Navigation
**Visualisation

## 8. Conclusion

**Intéressant de travailler sur ces sets de données
**Toute la chaine de l'extraction jusqu'à la visualisation est fonctionnelle
**

## 9. Perspectives d'améliorations

**ajouter des type de segment intéressant 
**prendre les 5 meilleures segments de chaque type (ex. les 5 meilleures segments de dénivelation) pour chaque course

** fait d'ajouter une nouvelle course au set de courses 

**mutlithreading pour accélerer les traitements des courses

** Etendre le set de course pour voir si ça fonctionne vraiment bien

## 10. Bibliographie

---


