# Generated by Django 4.1.7 on 2023-04-25 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0011_remove_task_test_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='future_date',
            field=models.DateTimeField(null=True),
        ),
    ]
