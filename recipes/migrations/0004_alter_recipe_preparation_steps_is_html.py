# Generated by Django 4.1.4 on 2023-01-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_preparation_steps_is_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_steps_is_html',
            field=models.BooleanField(default=True),
        ),
    ]