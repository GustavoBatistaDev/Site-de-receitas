# Generated by Django 4.1.4 on 2023-01-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_recipe_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]
