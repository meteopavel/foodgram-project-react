# Generated by Django 3.2.3 on 2023-11-24 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=10, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorited', models.BooleanField(default=False, help_text='Поставьте галочку, чтобы добавить в избранное.', verbose_name='Избранное')),
                ('is_in_shopping_cart', models.BooleanField(default=False, help_text='Поставьте галочку, чтобы добавить в список покупок.', verbose_name='В списке покупок')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название рецепта')),
                ('image', models.ImageField(default=None, null=True, upload_to='recipes/images/', verbose_name='Изображение блюда')),
                ('text', models.TextField(verbose_name='Текст рецепта')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(max_length=32, verbose_name='Цвет тега')),
                ('slug', models.SlugField(verbose_name='Slug тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag')),
            ],
        ),
    ]