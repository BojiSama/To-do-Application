# Generated by Django 4.1.7 on 2023-04-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_task_complete_task_created_task_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
    ]
