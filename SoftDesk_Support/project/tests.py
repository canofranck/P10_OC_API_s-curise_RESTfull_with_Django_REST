from project.models import Contributor, Project, Issue, Comment
from project.serializers import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectUpdateSerializer,
    ContributorSerializer,
    ContributorDetailSerializer,
    IssueCreateSerializer,
    IssueDetailSerializer,
    IssueListSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)
from rest_framework.authtoken.models import Token
import pdb
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

""" Test des end point pour un utilsateur anonyme"""


# class AuthenticationTestCase(APITestCase):

#     def test_user_registration(self):
#         """
#         Test user registration.
#         """

#         url = "/api/user/"  # URL pour l'inscription de l'utilisateur
#         data = {
#             "username": "testuser",
#             "password": "password123",
#             "date_of_birth": 25,
#             "can_be_contacted": True,
#             "can_data_be_shared": True,
#         }
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_user_login(self):
#         """
#         Test user login.
#         """
#         url = "/api/token/"  # URL pour la connexion de l'utilisateur
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )
#         data = {
#             "username": "testuser",
#             "password": "password123",
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_token_refresh(self):
#         """
#         Test token refresh.
#         """
#         url = "/api/token/refresh/"  # URL pour le rafraîchissement du jeton
#         data = {"refresh": "testuser"}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class ProjectCRUDTestCase(APITestCase):
#     def setUp(self):
#         # Créer un utilisateur pour les tests
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )

#     def test_create_project(self):
#         """
#         Test creating a new project.
#         """
#         url = "/api/projects/"  # Utilisez l'URL de création de projet
#         data = {
#             "name": "Nouveau projet",
#             "project_type": "back-end",
#             # Autres champs requis pour la création du projet
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que le projet a été créé avec les bonnes données

#     def test_retrieve_project(self):
#         """
#         Test retrieving a project by its ID.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1
#         url = "/api/projects/1/"  # Utilisez l'URL de récupération du projet par ID
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que les données récupérées correspondent au projet avec ID = 1

#     def test_update_project(self):
#         """
#         Test updating a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1
#         url = "/api/projects/1/"  # Utilisez l'URL de mise à jour du projet par ID
#         data = {
#             "name": "Projet mis à jour",
#             "description": "Description mise à jour",
#             # Autres champs à mettre à jour
#         }
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que le projet a été mis à jour avec les bonnes données

#     def test_delete_project(self):
#         """
#         Test deleting a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1
#         url = "/api/projects/1/"  # Utilisez l'URL de suppression du projet par ID
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que le projet a été supprimé avec succès


# class IssueCRUDTestCase(APITestCase):
#     def setUp(self):
#         # Créer un utilisateur pour les tests
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )

#     def test_list_issues(self):
#         """
#         Test retrieving a list of issues related to a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1
#         url = "/api/projects/1/issues/"  # Utilisez l'URL de récupération de la liste des issues par ID de projet
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que les données récupérées correspondent à la liste des issues du projet

#     def test_create_issue(self):
#         """
#         Test creating an issue in a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1
#         url = "/api/projects/1/issues/"  # Utilisez l'URL de création d'une issue dans un projet
#         data = {
#             "title": "Nouvelle issue",
#             "description": "Description de la nouvelle issue",
#             # Autres champs requis pour la création de l'issue
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que l'issue a été créée avec les bonnes données

#     def test_update_issue(self):
#         """
#         Test updating an issue in a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1 et une issue avec ID = 1
#         url = "/api/projects/1/issues/1/"  # Utilisez l'URL de mise à jour d'une issue dans un projet
#         data = {
#             "title": "Issue mise à jour",
#             "description": "Description mise à jour de l'issue",
#             # Autres champs à mettre à jour
#         }
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que l'issue a été mise à jour avec les bonnes données

#     def test_delete_issue(self):
#         """
#         Test deleting an issue from a project.
#         """
#         # Supposons que vous avez un projet existant avec ID = 1 et une issue avec ID = 1
#         url = "/api/projects/1/issues/1/"  # Utilisez l'URL de suppression d'une issue dans un projet
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         # Assurez-vous que l'issue a été supprimée avec succès


# class CommentCRUDTestCase(APITestCase):
#     def setUp(self):
#         # Créer un utilisateur pour les tests
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )

#     def test_list_comments(self):
#         """
#         Test listing comments related to an issue.
#         """
#         url = "/api/projects/1/issues/1/comments/"  # URL pour la liste des commentaires
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_comment(self):
#         """
#         Test creating a new comment.
#         """
#         url = "/api/projects/1/issues/1/comments/"  # URL pour la création de commentaire
#         data = {
#             "text": "Nouveau commentaire",
#             # Autres champs requis pour la création du commentaire
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_update_comment(self):
#         """
#         Test updating a comment.
#         """
#         url = "/api/projects/1/issues/1/comments/1/"  # URL pour la mise à jour du commentaire
#         data = {
#             "text": "Commentaire mis à jour",
#             # Autres champs à mettre à jour
#         }
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_delete_comment(self):
#         """
#         Test deleting a comment.
#         """
#         url = "/api/projects/1/issues/1/comments/1/"  # URL pour la suppression du commentaire
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class ContributorCRUDTestCase(APITestCase):
#     def setUp(self):
#         # Créer un utilisateur pour les tests
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )

#     def test_add_contributor(self):
#         """
#         Test adding a contributor to a project.
#         """
#         url = (
#             "/api/projects/1/contributors/"  # URL pour ajouter un contributeur
#         )
#         data = {
#             "user_id": 2,  # ID de l'utilisateur à ajouter en tant que contributeur
#             # Autres champs requis pour l'ajout de contributeur
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_list_contributors(self):
#         """
#         Test listing all contributors attached to a project.
#         """
#         url = "/api/projects/1/contributors/"  # URL pour la liste des contributeurs
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_contributor_detail(self):
#         """
#         Test retrieving details of a contributor in a project.
#         """
#         url = "/api/projects/1/contributors/2/"  # URL pour les détails d'un contributeur
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_remove_contributor(self):
#         """
#         Test removing a contributor from a project.
#         """
#         url = "/api/projects/1/contributors/2/"  # URL pour supprimer un contributeur
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class UserCRUDTestCase(APITestCase):
#     def setUp(self):
#         # Créer un utilisateur pour les tests
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )

#     def test_list_users(self):
#         """
#         Test listing all users (for administrators).
#         """
#         url = "/api/user/"  # URL pour la liste de tous les utilisateurs
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_user_detail(self):
#         """
#         Test retrieving details of a user.
#         """
#         url = "/api/user/1/"  # URL pour les détails d'un utilisateur
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_update_user(self):
#         """
#         Test updating a user's details.
#         """
#         url = "/api/user/1/"  # URL pour la modification des détails d'un utilisateur
#         data = {
#             # Les champs à mettre à jour
#         }
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_delete_user(self):
#         """
#         Test deleting a user.
#         """
#         url = "/api/user/1/"  # URL pour la suppression d'un utilisateur
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


""" Test des end point pour un utilsateur connecter"""


class user_authenticated(APITestCase):

    def setUp(self):
        # Crée un utilisateur enregistré
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

        # Connecte l'utilisateur
        self.client.force_login(self.user)

        # Créer un projet pour les tests
        self.project = Project.objects.create(
            name="Projet de test",
            description="Description du projet de test",
            author=self.user,
            # Ajoutez d'autres champs requis pour créer un projet
        )

        # Vérifier si l'utilisateur auteur existe déjà
        self.author_user = (
            get_user_model().objects.filter(username="author").first()
        )
        if not self.author_user:
            # Créer un utilisateur auteur du projet s'il n'existe pas
            self.author_user = get_user_model().objects.create_user(
                username="author", password="password123"
            )

        # Vérifier si le projet existe déjà
        self.project = Project.objects.filter(name="Nom du projet 1").first()
        if not self.project:
            # Créer un projet s'il n'existe pas
            self.project = Project.objects.create(
                name="Nom du projet 1", author=self.author_user
            )

        # Vérifier si l'utilisateur contributeur existe déjà
        self.contributor_user = (
            get_user_model().objects.filter(username="contributor").first()
        )
        if not self.contributor_user:
            # Créer un utilisateur contributeur s'il n'existe pas
            self.contributor_user = get_user_model().objects.create_user(
                username="contributor", password="password456"
            )
        # Ajouter l'utilisateur contributeur en tant que contributeur au projet
        self.project.contributors.add(self.contributor_user)

    def test_user_login(self):
        """
        Test user login.
        """
        url = "/api/token/"  # URL pour la connexion de l'utilisateur

        data = {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test projet

    def test_create_project(self):
        """
        Test creating a new project.
        """
        url = "/api/projects/"  # Utilisez l'URL de création de projet
        data = {
            "name": "Nouveau projet",
            "project_type": "back-end",
            "description": "Description",
            # Autres champs requis pour la création du projet
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assurez-vous que le projet a été créé avec les bonnes données

    def test_retrieve_project(self):
        """
        Test retrieving a project by its ID.
        """
        # Supposons que vous avez un projet existant avec ID = 1
        url = "/api/projects/1/"  # Utilisez l'URL de récupération du projet par ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assurez-vous que les données récupérées correspondent au projet avec ID = 1

    def test_update_project(self):
        """
        Test updating a project.
        """

        # Supposons que vous avez un projet existant avec ID = 1
        url = "/api/projects/1/"  # Utilisez l'URL de mise à jour du projet par ID
        data = {
            "name": "Projet mis à jour",
            "description": "Description mise à jour",
            # Autres champs à mettre à jour
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assurez-vous que le projet a été mis à jour avec les bonnes données

    def test_delete_project(self):
        """
        Test deleting a project.
        """
        # Supposons que vous avez un projet existant avec ID = 1
        url = "/api/projects/1/"  # Utilisez l'URL de suppression du projet par ID
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )  # car pas de reponse en delete

    # # test crud issue

    def test_list_issues(self):
        """
        Test retrieving a list of issues related to a project.
        """
        # Supposons que vous avez un projet existant avec ID = 1
        url = "/api/projects/1/issues/"  # Utilisez l'URL de récupération de la liste des issues par ID de projet
        # Crée une issue associée au projet avec l'ID 1

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assurez-vous que les données récupérées correspondent à la liste des issues du projet

    def create_issue_endpoint_access_author(self):
        # Se connecter en tant qu'auteur du projet
        self.client.force_login(self.author_user)
        # Accéder à l'endpoint pour créer une issue
        url = "/api/projects/{}/issues/".format(self.project.id)
        response = self.client.get(url)
        # Vérifier que l'accès est autorisé (status HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_issue_endpoint_access_contributor(self):
        # Se connecter en tant que contributeur du projet
        self.client.force_login(self.contributor_user)
        # Accéder à l'endpoint pour créer une issue
        url = url = "/api/projects/{}/issues/".format(self.project.id)
        response = self.client.get(url)
        # Vérifier que l'accès est autorisé (status HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_issue_author(self):
        """
        Test updating an issue in a project.
        """
        # Supposons que vous avez un projet existant avec ID = 1 et une issue avec ID = 1
        self.client.force_login(self.user)
        # Créer une issue dans le projet
        issue = Issue.objects.create(
            title="Nouvelle issue",
            description="Description de la nouvelle issue",
            priority="MEDIUM",
            tag="BUG",
            status="TO DO",
            project=self.project,
            assigned_to=self.user,
            author=self.user,
        )

        # Accéder à l'endpoint pour créer une issue
        url = "/api/projects/{}/issues/{}/".format(self.project.id, issue.id)
        print("projet  id  dans author: ", self.project.id)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assurez-vous que l'issue a été mise à jour avec les bonnes données

    def test_update_issue_contributor(self):
        """
        Test updating an issue in a project.
        """
        # project = Project.objects.create(
        #     name="Nom du projet2",
        #     description="Description du projet",
        #     author=self.author_user,
        # )
        # Créer une issue dans le projet
        self.client.force_login(self.user)

        # Créer un auteur de projet différent

        # Créer un projet pour les tests avec un auteur différent
        # self.project = Project.objects.create(
        #     name="Projet de test",
        #     description="Description du projet de test",
        #     author=self.author_user,  # Utiliser un autre utilisateur comme auteur du projet
        #     # Ajoutez d'autres champs requis pour créer un projet
        # )

        issue = Issue.objects.create(
            title="Nouvelle issue",
            description="Description de la nouvelle issue",
            priority="MEDIUM",
            tag="BUG",
            status="TO DO",
            project=self.project,
            assigned_to=self.user,
            author=self.author_user,
        )
        # Supposons que vous avez un projet existant avec ID = 1 et une issue avec ID = 1
        # Ajouter l'utilisateur actuellement authentifié en tant que contributeur au projet
        contributor = Contributor.objects.create(
            contributor=self.user, project=self.project
        )

        # Accéder à l'endpoint pour créer une issue
        url = "/api/projects/{}/issues/{}/".format(self.project.id, issue.id)
        print("projet : ", self.project)
        print("issu : ", issue)
        print("contributor : ", contributor)
        print("url : ", url)
        print("projet  id : ", self.project.id)
        # pdb.set_trace()
        # Obtenez le token de l'utilisateur
        token = Token.objects.get(user=self.user)

        # Ajoutez le token à la requête
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assurez-vous que l'issue a été mise à jour avec les bonnes données

    # def test_delete_issue(self):
    #     """
    #     Test deleting an issue from a project.
    #     """
    #     # Supposons que vous avez un projet existant avec ID = 1 et une issue avec ID = 1
    #     url = "/api/projects/1/issues/1/"  # Utilisez l'URL de suppression d'une issue dans un projet
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Assurez-vous que l'issue a été supprimée avec succès

    # # test crud comments

    # def setUp(self):
    #     # Créer un utilisateur pour les tests
    #     self.user = User.objects.create_user(
    #         username="testuser", password="password123"
    #     )

    # def test_list_comments(self):
    #     """
    #     Test listing comments related to an issue.
    #     """
    #     url = "/api/projects/1/issues/1/comments/"  # URL pour la liste des commentaires
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_comment(self):
    #     """
    #     Test creating a new comment.
    #     """
    #     url = "/api/projects/1/issues/1/comments/"  # URL pour la création de commentaire
    #     data = {
    #         "text": "Nouveau commentaire",
    #         # Autres champs requis pour la création du commentaire
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_comment(self):
    #     """
    #     Test updating a comment.
    #     """
    #     url = "/api/projects/1/issues/1/comments/1/"  # URL pour la mise à jour du commentaire
    #     data = {
    #         "text": "Commentaire mis à jour",
    #         # Autres champs à mettre à jour
    #     }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_comment(self):
    #     """
    #     Test deleting a comment.
    #     """
    #     url = "/api/projects/1/issues/1/comments/1/"  # URL pour la suppression du commentaire
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # test contributor

    # def setUp(self):
    #     # Créer un utilisateur pour les tests
    #     self.user = User.objects.create_user(
    #         username="testuser", password="password123"
    #     )

    # def test_add_contributor(self):
    #     """
    #     Test adding a contributor to a project.
    #     """
    #     url = (
    #         "/api/projects/1/contributors/"  # URL pour ajouter un contributeur
    #     )
    #     data = {
    #         "user_id": 2,  # ID de l'utilisateur à ajouter en tant que contributeur
    #         # Autres champs requis pour l'ajout de contributeur
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_contributors(self):
    #     """
    #     Test listing all contributors attached to a project.
    #     """
    #     url = "/api/projects/1/contributors/"  # URL pour la liste des contributeurs
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_contributor_detail(self):
    #     """
    #     Test retrieving details of a contributor in a project.
    #     """
    #     url = "/api/projects/1/contributors/2/"  # URL pour les détails d'un contributeur
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_remove_contributor(self):
    #     """
    #     Test removing a contributor from a project.
    #     """
    #     url = "/api/projects/1/contributors/2/"  # URL pour supprimer un contributeur
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # testuser

    # def setUp(self):
    #     # Créer un utilisateur pour les tests
    #     self.user = User.objects.create_user(
    #         username="testuser", password="password123"
    #     )

    # def test_list_users(self):
    #     """
    #     Test listing all users (for administrators).
    #     """
    #     url = "/api/user/"  # URL pour la liste de tous les utilisateurs
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_detail(self):
    #     """
    #     Test retrieving details of a user.
    #     """
    #     url = "/api/user/1/"  # URL pour les détails d'un utilisateur
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_user(self):
    #     """
    #     Test updating a user's details.
    #     """
    #     url = "/api/user/1/"  # URL pour la modification des détails d'un utilisateur
    #     data = {
    #         # Les champs à mettre à jour
    #     }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_user(self):
    #     """
    #     Test deleting a user.
    #     """
    #     url = "/api/user/1/"  # URL pour la suppression d'un utilisateur
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
