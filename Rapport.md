# Rapport Mini-projet 
# QSELF 2019

## HES-SO MSE 


Pedro Costa & Louis Delabays

---

## 1. Introduction

Dans le cadre du cours *Quantified Self*, il nous a été demandé de réaliser un projet en relation avec les thèmes vus durant le semestre. 

Notre projet a pour but de fournir un moyen de comparer des courses à pieds de manière un peu similaire à l'application **Strava**. Avec Strava, les segments ont été définis par un utilisateur qui a choisi un point de départ et un points d'arrivé d'une portion de sa course qu'il trouvait intéressant. Ensuite, pour chaque nouvelle course l'application détecte les portions qui correpsondent à un segment. Finalement, nous avons la possibiltié de comparer nos différents efforts sur ce segment ou de se comparer avec d'autres athlètes.

Ce que nous voulons réaliser est un peu différent: Notre application (script Python) trouvera d'elle m^eme les segments intéressants sans l'intervention de l'utilisateur. Plusieurs courses à pieds seront fournies à l'application pour qu'elle trouve les portions communes des différentes courses à pieds. L'utilisateur pourra ensuite visualiser les courses et comparer les segments communs. Le descriptions complètes et détaillées du projet se trouve au chapitre suivant (*2. Description et but*).

Nous avons choisi d'utiliser des données existantes et ne pas avoir besoin d'en récolter au début du projet. Ces données sont des courses à pieds réalisé par Louis. Elles ont été enregistrées au moyen d'une montre GPS Garmin (Forerunner 645). Les détails sur l'extraction et l'exploitation de ces données sont décrite plus bas dans ce rapport (*3. Récupération des courses depuis la montre*)

Ce rapport décrit les différentes étapes effectuées depuis la récupération des données jusqu'à la visualisation/comparaison des segments. 

## 2. Description et but

**les segments pertinents sont choisis selon plusieurs critères...

## 3. Récupération des courses depuis la montre

** Garmin en mode *USB Mass Storage*
** .fit 
** class Point
** en dataframe
** class race


## 4. Extraction des segments

**Distance en 2 portion de 2 course --> "fen^etre glissante"
**Séparation des "morceaux" continuu pour obtenir une liste de segments
**Filtrage des segments trouvés
** Toutes les courses vs toutes les courses

** class RaceManager
** class segment

## 5. Recherche des segments pertinents

**3 types de segments : plus long, plus de déniv., plus de densité 
** class BestSegment

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

## 10. Bibliographie

---


