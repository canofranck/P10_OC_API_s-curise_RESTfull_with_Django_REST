from django.contrib import admin
from .models import Project, Issue, Comment, Contributor


class ProjetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project_type",
        "description",
        "created_time",
        "author",
    )


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("contributor", "project")


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "description",
        "priority",
        "project",
        "tag",
        "status",
        "assigned_to",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        "description",
        "uuid",
        "created_time",
        "issue",
        "issue_url",
    )


admin.site.register(Project, ProjetAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
