# Generated by Django 5.0.1 on 2024-11-21 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="return",
            name="attended_school",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="return",
            name="owned_home",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
