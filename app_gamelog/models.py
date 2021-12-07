from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime

# Create your models here.
GENDERS = [
    ('',''),
    ('Male', 'Male'),
    ('Female', 'Female'),
]

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, default='')
    password = models.CharField(max_length=100)
    avatar = models.CharField(max_length=10000)

    is_publisher = models.BooleanField(blank=True, default=False)

    REQUIRED_FIELDS = ['email', 'gender', 'first_name', 'password', 'avatar']

    def __str__(self):
        return str(self.id) + ' ' + self.username + (' publisher' if self.is_publisher else '')


class Game(models.Model):
    PLATFORMS = [
        ('', ''),
        ('Steam', 'Steam'),
        ('PlayStation', 'PlayStation'),
        ('Xbox', 'Xbox'),
        ('Nintendo', 'Nintendo'),
    ]

    GENRES = [
        ('', ''),
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Casual', 'Casual'),
        ('Role-playing', 'Role-playing'),
        ('Sandbox', 'Sandbox'),
        ('Simulation', 'Simulation'),
        ('Strategy', 'Strategy'),
        ('Sports', 'Sports'),
    ]

    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
    platform = models.CharField(max_length=100, choices=PLATFORMS)
    genre = models.CharField(max_length=100, choices=GENRES)
    image_url = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.id) + ' ' + self.name + ' @ ' + self.platform

class OwnGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username + ' ' + self.game.name

class PublishGame(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.publisher.username + ' > ' + self.game.name

class Followship(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    user_target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user_from.username + ' > ' + self.user_target.username

class GameLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    duration = models.FloatField(default=0.0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username + ' > ' + self.game.name + ' > ' + self.date.strftime("%m/%d/%Y")

class Feed(models.Model):
    ACTIONS = [
        ('played', 'played'),
        ('purchased', 'purchased'),
        ('published', 'published'),
        ('followed', 'followed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_user')
    action = models.CharField(max_length=100, choices=ACTIONS)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='target_user')
    value = models.FloatField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        if self.game:
            return self.user.username + ' ' + self.action + ' ' + self.game.name + ' ' + str(self.value) + ' ' + self.date.strftime("%m/%d/%Y")
        else:
            return self.user.username + ' ' + self.action + ' ' + self.target_user.username + ' ' + str(self.value) + ' ' + self.date.strftime("%m/%d/%Y")