from django.db import models
from authentication.models import CustomUser
from django.conf import settings
import uuid


class Project(models.Model):
    PROJECT_TYPES = [
        ("back-end", "Back-end"),
        ("front-end", "Front-end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]
    name = models.CharField(max_length=255, help_text="Name of project")
    project_type = models.CharField(
        max_length=10, choices=PROJECT_TYPES, help_text="Type of project"
    )
    description = models.TextField(
        blank=True, help_text="Description  project"
    )
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=("created_time")
    )
    updated_time = models.DateTimeField(
        auto_now=True, verbose_name=("updated date")
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        related_name="project_author",
        verbose_name=("project author"),
        help_text="project author",
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through="Contributor",
        related_name="contributions",
        help_text="project contributors",
    )

    def __str__(self):
        return self.name


class Contributor(models.Model):
    contributor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributor_relationship",
        help_text="Project to which the contributor contributes",
    )

    def __str__(self):
        return f"{self.contributor.username} - {self.project.name}"


class Issue(models.Model):

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]
    STATUS_CHOICES = [
        ("TO_DO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_authors",
        blank=True,
        verbose_name=("issue author"),
        help_text="issue author",
    )
    title = models.CharField(max_length=255, help_text="issue title")
    description = models.TextField(help_text="description of issue")
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
        help_text="issue priority",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
        help_text="Project with associated issue",
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        default="BUG",
        help_text="tag of issue",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TO_DO",
        help_text="Statuts issue",
    )
    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_to",
        help_text="User assigned to issue",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=("created time")
    )

    def __str__(self):
        return f"{self.project.name} -{self.title} | {self.tag},  {self.priority},{self.status} "


class Comment(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=("created time")
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comment_authors",
        verbose_name=("comment author"),
        help_text="comment author",
    )
    name = models.CharField(
        max_length=100, verbose_name=("comment name"), help_text="comment name"
    )
    description = models.TextField(
        verbose_name=("comment body"), help_text="comment body"
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        blank=True,
        related_name="comments",
        verbose_name=("related issue"),
        help_text="Issue associated with comment",
    )
    issue_url = models.URLField(blank=True, verbose_name=("issue_link"))

    def __str__(self):
        return f"{self.name} | {self.issue}"
