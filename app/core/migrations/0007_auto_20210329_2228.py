# Generated by Django 3.1.7 on 2021-03-29 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='core.Ingredient', verbose_name='Recipe Ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='core.Tag', verbose_name='Recipe Tags'),
        ),
    ]
