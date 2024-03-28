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

## Installation & lancement

Commencez tout d'abord par installer Python 

Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/canofranck/P10_OC_API_s-curise_RESTfull_with_Django_REST
```
Placez vous dans le dossier P10_OC_API_s-curise_RESTfull_with_Django_REST, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
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
Administration du site :
```
http://127.0.0.1:8000/admin

```
Utilisateur de test :
```

```


