# Generated by Django 5.0.4 on 2024-04-12 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_issue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM', help_text='issue priority', max_length=20),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('TO DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')], default='TO_DO', help_text='Statuts issue', max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('back-end', 'Back-end'), ('front-end', 'Front-end'), ('iOS', 'iOS'), ('android', 'Android')], help_text='Type of project', max_length=10),
        ),
    ]