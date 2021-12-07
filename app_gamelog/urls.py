from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('games', views.games, name='games'),
    path('games/add_game', views.new_game, name='add_game'),
    path('games/search_by_other', views.search_by_other, name='search_by_other'),
    path('games/search_by_name', views.search_by_name, name='search_by_name'),
    path('games/<int:game_id>', views.game_detail, name='game_detail'),
    path('games/<int:game_id>/add_to_library', views.add_to_library, name='add_to_library'),
    path('games/<int:game_id>/remove_from_library', views.remove_from_library, name='remove_from_library'),
    path('games/<int:game_id>/add_log', views.add_log, name='add_log'),
    path('games/<int:game_id>/<int:log_id>/remove_log', views.remove_log, name='remove_log'),

    path('user/<str:username>/', views.user, name='profile'),
    path('user/<str:username>/follow', views.follow, name='follow'),
    path('user/<str:username>/unfollow', views.unfollow, name='unfollow'),
    path('user/<str:username>/publish_game', views.publish_game, name='publish_game'),
    path('user/<str:username>/following', views.followings, name='following'),
    path('user/<str:username>/followers', views.followers, name='follower'),

    path('user/<str:username>/analyses', views.analyses, name='analyses'),
    path('user/<str:username>/new_profile', views.new_profile, name='new_profile'),
    path('user/<str:username>/new_avatar', views.new_avatar, name='new_avatar'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('change_pass', views.change_pass, name='change_pass'),
    path('check_old_password', views.check_old_password, name='check_old_password'),
    path('check_match_old_password', views.check_match_old_password, name='check_match_old_password'),
    path('check_match_password', views.check_match_password, name='check_match_password'),
    path('logout', views.logout_view, name='logout'),
]