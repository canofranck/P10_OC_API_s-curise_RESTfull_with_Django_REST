"""
URL configuration for SoftDesk_Support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from authentication.views import CustomUserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from project.views import (
    ProjectViewSet,
    AdminProjectListView,
    ContributorViewSet,
    IssueViewSet,
)

router = routers.SimpleRouter()
router.register(r"api/projects", ProjectViewSet, basename="project")
# create url like: api/projects/1/contributors/ or api/projects/1/issues/
project_router = routers.NestedSimpleRouter(
    router, r"api/projects", lookup="project"
)
project_router.register(
    r"contributors", ContributorViewSet, basename="project-contributors"
)
project_router.register(r"issues", IssueViewSet, basename="project-issues")
router.register("user", CustomUserViewSet, basename="user")
# router.register("projects", ProjectViewSet, basename="project")
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(project_router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/admin/projects/",
        AdminProjectListView.as_view({"get": "list"}),
        name="admin_project_list",
    ),
]
