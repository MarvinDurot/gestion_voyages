# Gestion de voyages
Une application permettant de consulter et de trier un ensemble de voyages.

## Installation
*Commandes à lancer à la racine du projet*

* Installer les paquets Python requis : `pip install -r requirements.txt`.
* Créer la structure de la base de données : `python models.py`.
* Seeder la base de données avec un jeu d'essai aléatoire : `python seeder.py`.
* Lancer le serveur de l'application : `python server.py`.

## Utilisation
L'application est divisée en deux parties :
- la partie frontend accessible à tous.
- la partie backend accessible uniquement à l'administrateur.

La page d'accueil permet à l'utilisateur de choisir le type de tri utilisé pour afficher la liste des voyages disponibles.
On peut afficher les détails d'un voyages (transports, hébergements et avis) en cliquant sur l'un deux dans la liste.

La page d'administration permet de gérer les voyages et les villes, une authentification est requise.

Les identifiants par défaut sont "admin", "admin".
