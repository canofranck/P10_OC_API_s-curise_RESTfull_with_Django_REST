# OC_P10_SoftDesk Support : créez une API sécurisée RESTful en utilisant Django REST

créer un back-end performant et sécurisé via des points de terminaison d'API pour la conception d'une application de suivi de problèmes

## Fonctionnalités

L'API pour la gestion de projets collaboratifs, permets aux utilisateurs de créer des projets, des problèmes et des commentaires associés à ces projets.

Voici un aperçu des principales fonctionnalités :

Gestion des Utilisateurs :

Les utilisateurs peuvent s'inscrire et se connecter à l'application.
Les choix de confidentialité des utilisateurs sont respectés, avec des options pour autoriser le contact et le partage de données.
La conformité au RGPD est prise en compte, avec une vérification de l'âge des utilisateurs lors de l'inscription.

Gestion des Projets :

Les utilisateurs peuvent créer des projets et en devenir les auteurs et contributeurs.
Les détails tels que le nom, la description et le type de projet sont enregistrés lors de la création.
Seuls les contributeurs d'un projet ont accès à celui-ci et à ses ressources associées.

Création des Problèmes :

Les contributeurs peuvent créer des problèmes (issues) pour un projet donné.
Les problèmes peuvent être assignés à d'autres contributeurs, avec des options de priorité et de balise pour classifier l'importance et la nature du problème.
Un suivi de l'avancement est disponible avec des statuts tels que "À faire", "En cours" et "Terminé".

Création des Commentaires :

Les contributeurs peuvent commenter les problèmes pour faciliter la communication et la résolution.
Chaque commentaire est lié à un problème spécifique et est associé à un identifiant unique.

Informations Complémentaires :

Chaque ressource enregistrée dans l'application est horodatée pour suivre le moment de sa création.
Les auteurs de chaque ressource peuvent modifier ou supprimer leurs propres éléments.
Mise en Place de la Pagination :

Un système de pagination est implémenté pour gérer le listage des ressources et éviter les charges excessives.
Test des Points de Terminaison de l'API :

Tous les points de terminaison de l'API peuvent être testés à l'aide d'outils comme Postman ou curl, garantissant ainsi le bon fonctionnement des interactions avec l'application.

Pour plus de détails sur le fonctionnement de cette API, se référer à sa 
[documentation](https://documenter.getpostman.com/view/32512679/2sA3BhdZUw#3c21d3aa-f62b-479b-9ecc-a784e51a7bd1) (Postman).

## Installation & lancement

Commencez tout d'abord par installer Python 

Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/canofranck/P10_OC_API_s-curise_RESTfull_with_Django_REST
```
Placez vous dans le dossier P10_OC_API_s-curise_RESTfull_with_Django_REST, puis créez un nouvel environnement virtuel:
```
pip install pipenv
pipenv install
```
Ensuite, activez-le.
```
pipenv shell
```

Installez ensuite les packages requis:
```
pipenv install -r requirements.txt

```
Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:
```
python manage.py makemigrations
```
Puis: 
```
python manage.py migrate
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:
```
http://127.0.0.1:8000
```

## Informations
Pour Tester l'API vous pouvez soit passer POSTMAN (fortement recommandé) soit  par le serveur django une fois celui ci lancer 
aller sur la page ( du serveur [http://127.0.0.1:8000](http://127.0.0.1:8000))
En haut à droite utiliser le bouton login  et prenez un des utlisateurs de la liste des utilisateurs existant ci dessous.
Utiliser la liste des endpoints ci dessous pour tester L'API.
Pour changer d utilisateur il faut repasser par l'adresse de depart de l API : http://127.0.0.1:8000 , les pages etant protégé contre les utilisateurs non inscrits c est la seule page ou on peut changer d' utilisateur.

#### Liste des utilisateurs existants :

| *ID* | *Identifiant* | *Mot de passe* |
|------|---------------|----------------|
| 1    | admin-oc      | password-oc    |
| 2    | usertwo       | usertwo        |
| 3    | userthree     | userthree      |
| 4    | userfour      | userfour       |
| 5    | userfive      | userfive       |
| 6    | usersix       | usersix        |
| 7    | userone       | userone        |

#### Liste des points de terminaison de l'API (détaillés dans la [documentation](https://documenter.getpostman.com/view/32512679/2sA3BhdZUw#3c21d3aa-f62b-479b-9ecc-a784e51a7bd1)) :


| #   | *Point de terminaison de l'API*                                           | *Méthode HTTP* | *URL (base: http://127.0.0.1:8000)*                              |
|-----|---------------------------------------------------------------------------|----------------|------------------------------------------------------------------|
| 1   | Inscription de l'utilisateur                                              | POST           | /api/user/                                                       |
| 2   | Connexion de l'utilisateur                                                | POST           | /api/token/                                                      |
| 3   | Refresh Token de l'utilisateur                                            | POST           | /api/token/refresh/                                              |
| 4   | Récupérer la liste de tous les projets rattachés à l'utilisateur connecté | GET            | /api/projects                                                    |
| 5   | Créer un projet                                                           | POST           | /api/projects/                                                   |
| 6   | Récupérer les détails d'un projet via son id                              | GET            | /api/projects/:ID_PROJET/                                        |
| 7   | Mettre à jour un projet                                                   | PATCH          | /api/projects/:ID_PROJET/                                        |
| 8   | Supprimer un projet et ses problèmes                                      | DELETE         | /api/projects/:ID_PROJET/                                        |
| 9   | Ajouter un utilisateur (collaborateur) à un projet                        | POST           | /api/projects/:ID_PROJET/contributors/                           |
| 10  | Récupérer la liste de tous les utilisateurs attachés à un projet          | GET            | /api/projects/:ID_PROJET/contributors/                           |
| 11  | Supprimer un (collaborateur) utilisateur d'un projet                      | DELETE         | /api/projects/:ID_PROJET/contributors/:ID_CONTRIBUTOR/           |
| 12  | Récupérer la liste des Issues liés à un projet                            | GET            | /api/projects/:ID_PROJET/issues/                                 |
| 13  | Créer une Issue dans un projet                                            | POST           | /api/projects/:ID_PROJET/issues/                                 |
| 14  | Mettre à jour une Issue dans un projet                                    | PATCH          | /api/projects/:ID_PROJET/issues/:ID_ISSUE/                       |
| 15  | Supprimer une Issue d'un projet                                           | DELETE         | /api/projects/:ID_PROJET/issues/:ID_ISSUE/                       |
| 16  | Recupérer la listes des Comments d une issu liés a un projet              | GET            | /api/projects/:ID_PROJET/issues/:ID_ISSUE/comments/              |
| 17  | Créer un Comments dans une Issue                                          | POST           | /api/projects/:ID_PROJET/issues/:ID_ISSUE/comments/              |
| 18  | Mettre à jour un Comments dans une Issue                                  | PATCH          | /api/projects/:ID_PROJET/issues/:ID_ISSUE/comments/:ID_COMMENTS/ |
| 19  | Supprimer un Comments d une issu                                          | DELETE         | /api/projects/:ID_PROJET/issues/:ID_ISSUE/comments/:ID_COMMENTS/ |

