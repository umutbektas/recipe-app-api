import uuid
import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('upload/recipe/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('E-Mail field is required.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(
        null=False,
        blank=False,
        max_length=255,
        unique=True,
        verbose_name='E-Mail'
    )
    first_name = models.CharField(
        null=True,
        blank=False,
        max_length=255,
        verbose_name='Firt Name'
    )
    last_name = models.CharField(
        null=True,
        blank=False,
        max_length=255,
        verbose_name='Last Name'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active ?'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is staff ?'
    )
    joined_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Joined date'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # defaults email, passwords

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Tag Name'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_tags',
        verbose_name='User'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['-name']


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Ingredient Name'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_ingredients',
        verbose_name='Ingredient User'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['-id']


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_recipes',
        null=False,
        blank=False,
        verbose_name='Recipe User'
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Recipe Title'
    )
    time_minutes = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name='Recipe Minutes'
    )
    price = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        verbose_name='Recipe Price'
    )
    link = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients_recipes',
        blank=False,
        verbose_name='Recipe Ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags_recipes',
        blank=False,
        verbose_name='Recipe Tags'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=recipe_image_file_path,
        verbose_name='Recipe Image'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Recipe Date'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at']
