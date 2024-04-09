from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


CustomUserModel = get_user_model()


class CustomUserAPITestCase(APITestCase):
    def test_user_can_register(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "age": 25,
            "can_be_contacted": True,
            "can_data_be_shared": False,
        }
        response = self.client.post("/api/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login(self):
        # Vous pouvez implémenter ce test si vous avez une vue pour la connexion des utilisateurs
        pass

    def test_user_can_access_own_profile(self):
        user = CustomUserModel.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(user)
        response = self.client.get(f"/api/users/{user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_edit_own_profile(self):
        # Testez la modification du profil de l'utilisateur connecté
        pass

    def test_user_can_delete_own_account(self):
        # Testez la suppression du compte de l'utilisateur connecté
        pass

    def test_user_cannot_access_other_profiles(self):
        # Testez que l'utilisateur ne peut pas accéder aux profils des autres utilisateurs
        pass

    def test_admin_can_access_all_users(self):
        admin = CustomUserModel.objects.create_superuser(
            username="admin", password="adminpassword"
        )
        self.client.force_login(admin)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_edit_user_profiles(self):
        # Testez que l'administrateur peut modifier les profils des utilisateurs
        pass

    def test_admin_can_delete_user_accounts(self):
        # Testez que l'administrateur peut supprimer les comptes des utilisateurs
        pass

    def test_unauthenticated_user_cannot_access_protected_resources(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
