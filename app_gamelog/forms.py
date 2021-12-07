from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Game
import datetime

REGIONS = (
    ('', ''),
    ('Africa', 'Africa'),
    ('Asia', 'Asia'),
    ('Europe', 'Europe'),
    ('North America', 'North America'),
    ('South America', 'South America'),
)

GENDERS = (
    ('', ''),
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class LoginForm(forms.Form):
    login_username = forms.CharField(max_length=50, label='Username', required=True)
    login_password = forms.CharField(max_length=50, label='Password', required=True)

class SignupForm(forms.Form):
    signup_username = forms.CharField(max_length=50, label='Username', required=True)
    signup_email = forms.EmailField(max_length=100, label='Email', required=True)
    signup_gender = forms.ChoiceField(choices = GENDERS, label='Gender', required=False)
    signup_fname = forms.CharField(max_length=100, label='First Name', required=True)
    signup_lname = forms.CharField(max_length=100, label='Last Name', required=False)
    signup_password = forms.CharField(max_length=50, label='Password', required=True)
    signup_is_publisher = forms.BooleanField(label='Publisher?', required=False)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=50, label='Old password', required=True)
    new_password = forms.CharField(max_length=50, label='New password', required=True)
    verify_password = forms.CharField(max_length=50, label='Verify new password', required=True)

class ChangePasswordWithUsernameForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', required=True)
    old_password = forms.CharField(max_length=50, label='Old password', required=True)
    new_password = forms.CharField(max_length=50, label='New password', required=True)
    verify_password = forms.CharField(max_length=50, label='Verify new password', required=True)

PLATFORMS = (
    ('', ''),
    ('Steam', 'Steam'),
    ('PlayStation', 'PlayStation'),
    ('Xbox', 'Xbox'),
    ('Nintendo', 'Nintendo'),
)

GENRES = (
    ('', ''),
    ('Action', 'Action'),
    ('Adventure', 'Adventure'),
    ('Casual', 'Casual'),
    ('Role-playing', 'Role-playing'),
    ('Sandbox', 'Sandbox'),
    ('Simulation', 'Simulation'),
    ('Strategy', 'Strategy'),
    ('Sports', 'Sports'),
)

# search game by platform/genre
class SearchByOtherForm(forms.Form):
    search_platform = forms.ChoiceField(choices=PLATFORMS, label='Platform', required=False)
    search_genre = forms.ChoiceField(choices=GENRES, label='Genre', required=False)

# search game by name
class SearchByNameForm(forms.Form):
    search_name = forms.CharField(max_length=50, label='Game Name', required=False)

# update user profile
class ProfileUpdateForm(forms.Form):
    email = forms.CharField(max_length=100, label='Email', required=True)
    fname = forms.CharField(max_length=100, label='First Name', required=True)
    lname = forms.CharField(max_length=100, label='Last Name', required=True)

# add new game
class GameAddForm(forms.ModelForm):
    add_name = forms.CharField(max_length=1000, label='Game Name', required=True)
    add_platform = forms.ChoiceField(choices=PLATFORMS, label='Platform', required=True)
    add_genre = forms.ChoiceField(choices=GENRES, label='Genre', required=True)
    add_image_url = forms.CharField(max_length=10000, label='Image Link', required=True)
    add_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Released on')


    class Meta:
        model = Game
        fields = ('add_name', 'add_platform', 'add_genre', 'add_image_url', )

class GameAddToLibraryForm(forms.Form):
    price = forms.FloatField(label='Purchased at $')
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Purchased on')

class GameLogAddForm(forms.Form):
    duration = forms.FloatField(label='Time played')
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Played on')