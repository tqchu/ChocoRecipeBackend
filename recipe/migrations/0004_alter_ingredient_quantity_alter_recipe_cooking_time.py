# Generated by Django 4.1.7 on 2023-05-16 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0003_alter_recipe_cooking_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="quantity",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.IntegerField(),
        ),
    ]
