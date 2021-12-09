from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .forms import *
from .models import *

import json
from django.db.models import Q
from django.conf.urls.static import static

avatar_dict = {
    'avatar_user': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcReeDtnaKLjD5A4wMd54A_D7XiNZEQUtzmB1tgcwuz5uyPaF8VcNZhswodqWn7-9lgRf3Q&usqp=CAU',
    'avatar_shiba': 'https://64.media.tumblr.com/4b4cc63028ac84403c18cf4ec7d10e2f/tumblr_pmsix9Xv0V1ulz545_1280.png',
    'avatar_gamer': 'https://cdn1.iconfinder.com/data/icons/game-design-butterscotch-vol-1/256/Game_Controller-512.png',
    'avatar_person': 'https://pic2.zhimg.com/v2-46f739c6c4abf8df1e0dcd9969227561_b.jpeg',
    'avatar_shenteng': 'http://i0.hdslb.com/bfs/archive/d4fda9ad20a200929c8a4c1e12c6c42c15b5a572.png',
    'avatar_kitten': 'https://i.pinimg.com/736x/9f/d6/fd/9fd6fdce9134c79a2bcb7f34158068d5.jpg',
}

def index(request):
    if request.user.is_authenticated:
        # followship_targets = User.objects.filter(target__in=Followship.objects.filter(user_from=request.user))
        # request_user_feeds = Feed.objects.filter(Q(user=request.user) | Q(user__in=followship_targets)).order_by('-date')
        all_feeds = Feed.objects.all().exclude(user=request.user).order_by('-date')
        # follow_feeds = non_user_feeds.filter(target__in=Followship.objects.filter(user_from=request.user))
        context = {
            'all_feeds': all_feeds,

        }
        return render(request, 'app_gamelog/index.html', context)
    else:
        context = {
            'signup_form': SignupForm(),
            'login_form': LoginForm(),
            'reset_pass_with_username_form': ChangePasswordWithUsernameForm(),
        }
        return render(request, 'app_gamelog/authentication.html', context)

@login_required(login_url='index')
def games(request):
    context = {
        'search_by_other_form': SearchByOtherForm(),
        'search_by_name_form': SearchByNameForm(),
        'add_game_form': GameAddForm(),
        'games': Game.objects.all(),
    }
    return render(request, 'app_gamelog/games.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    name = game.name
    publisher = game.publisher
    platform = game.platform
    genre = game.genre
    image_url = game.image_url

    user = request.user
    is_publisher = user.is_publisher
    ownership = OwnGame.objects.filter(user=user, game=game).first()
    logs = GameLog.objects.filter(user=user, game=game).order_by('-date')
    if ownership is not None:
        owned = True
    else:
        owned = False
    context = {
        'game_id': game_id,
        'name': name,
        'publisher': publisher,
        'platform': platform,
        'genre': genre,
        'image_url': image_url,
        'owned': owned,
        'add_to_library_form': GameAddToLibraryForm(),
        'add_log_form': GameLogAddForm(),
        'logs': logs,
        'is_publisher': is_publisher,
    }
    return render(request, 'app_gamelog/game_detail.html', context)

def add_to_library(request, game_id):
    if request.method == "POST":
        game = get_object_or_404(Game, pk=game_id)
        user = request.user
        price = request.POST['price']
        date = request.POST['date']
        ownership = OwnGame(user=user, game=game, price=price, date=date)
        ownership.save()

        # user purchased game feed
        personal_feed = Feed(user=user, action='purchased', game=game, value=price, date=date)
        personal_feed.save()
        return redirect('game_detail', game_id=game_id)

def remove_from_library(request, game_id):
    user = request.user
    game = get_object_or_404(Game, pk=game_id)
    ownership = get_object_or_404(OwnGame, user=user, game=game)

    feed = get_object_or_404(Feed, user=user, action='purchased', game=game, value=ownership.price, date=ownership.date)
    if request.method == "POST":
        ownership.delete()
        feed.delete()
        return redirect('game_detail', game_id=game_id)

def add_log(request, game_id):
    if request.method == "POST":
        user = request.user
        game = get_object_or_404(Game, pk=game_id)
        duration = request.POST['duration']
        date = request.POST['date']
        log = GameLog(user=user, game=game, duration=duration, date=date)
        log.save()

        personal_feed = Feed(user=user, action='played', game=game, value=duration, date=date)
        personal_feed.save()                         
        return redirect('game_detail', game_id=game_id)

def remove_log(request, game_id, log_id):
    log = get_object_or_404(GameLog, pk=log_id)
    game = get_object_or_404(Game, pk=game_id)
    feed = get_object_or_404(Feed, user=request.user, action='played', game=game, value=log.duration, date=log.date)
    if request.method == "POST":
        log.delete()
        feed.delete()
        return redirect('game_detail', game_id=game_id)

def new_game(request):
    if request.is_ajax():
        add_name = request.POST['add_name']
        add_platform = request.POST['add_platform']
        add_genre = request.POST['add_genre']
        add_image_url = request.POST['add_image_url']
        game = Game(name=add_name,
                    platform=add_platform,
                    genre=add_genre,
                    image_url=add_image_url)
        game.save()
        response = {
            'msg': "Game Added!"
        }
        return JsonResponse(response)

def publish_game(request, username):
    if request.method == "POST":
        add_name = request.POST['add_name']
        add_platform = request.POST['add_platform']
        add_genre = request.POST['add_genre']
        add_image_url = request.POST['add_image_url']
        add_date = request.POST['add_date']
        publisher = request.user
        game = Game(name=add_name,
                    platform=add_platform,
                    genre=add_genre,
                    image_url=add_image_url,
                    publisher=publisher)
        game.save()
        publication = PublishGame(publisher=publisher,
                                    game=game,
                                    date=add_date)
        publication.save()

        feed = Feed(user=publisher,
                     action='published',
                     game=game,
                     date=add_date)
        feed.save()
        return redirect('profile', username=username)

def search_by_other(request):
    if request.is_ajax():
        platform = request.GET['search_platform']
        genre = request.GET['search_genre']
        game_list = Game.objects.filter(Q(platform=platform) | Q(genre=genre)).values()
        if not game_list:
            return JsonResponse({'error': "Not found."})
        else:
            return render(request, 'app_gamelog/search_results.html', {'games': list(game_list)})

def search_by_name(request):
    if request.is_ajax():
        name = request.GET['search_name']
        game = Game.objects.filter(name=name).values()
        if not game:
            return JsonResponse({'error': 'Not found.'})
        else:
            return render(request, 'app_gamelog/search_results.html', {'games': list(game)})

@login_required(login_url='index')
def user(request, username):
    load_user = get_object_or_404(User, username=username)
    request_user = request.user
    email = load_user.email
    gender = load_user.gender
    fname = load_user.first_name
    lname = load_user.last_name
    avatar = load_user.avatar
    fullname = load_user.get_full_name()

    is_publisher = request_user.is_publisher

    followship = Followship.objects.filter(user_from=request_user, user_target=load_user).first()
    followers = Followship.objects.filter(user_target=load_user)
    user_followed = Followship.objects.filter(user_from=load_user)

    if is_publisher:
        request_user_game_owned = Game.objects.filter(publishgame__in=PublishGame.objects.filter(publisher=request_user))
    else:
        request_user_game_owned = Game.objects.filter(owngame__in=OwnGame.objects.filter(user=request_user))
    
    if load_user.is_publisher:
        load_user_game_owned = Game.objects.filter(publishgame__in=PublishGame.objects.filter(publisher=load_user))
    else:
        load_user_game_owned = Game.objects.filter(owngame__in=OwnGame.objects.filter(user=load_user))

    if followship is not None:
        follow = True
    else:
        follow = False
    
    request_user_feeds = Feed.objects.filter(user=request_user).order_by('-date')
    load_user_feeds = Feed.objects.filter(user=load_user).order_by('-date')
    context = {
        'load_user': load_user,
        'request_user': request_user,
        'fullname': fullname,
        'username': username,
        'email': email,
        'gender': gender,
        'fname': fname,
        'lname': lname,
        'avatar': avatar,
        'is_publisher': is_publisher,
        'profile_update_form': ProfileUpdateForm(),
        'avatar_dict': avatar_dict,
        'follow': follow,
        'request_user_feeds': request_user_feeds,
        'load_user_feeds': load_user_feeds,
        'request_user_game_owned': request_user_game_owned,
        'load_user_game_owned': load_user_game_owned,
        'publish_game_form': GameAddForm(),
        'followers': followers,
        'user_followed': user_followed,
    }
    return render(request, 'app_gamelog/user.html', context)

def new_profile(request, username):
    if request.method == "POST":
        if request.is_ajax():
            load_user = get_object_or_404(User, username=username)
            request_user = request.user
            new_email = request.POST['new_email']
            new_fname = request.POST['new_fname']
            new_lname = request.POST['new_lname']
            user = request.user
            user.email = new_email
            user.first_name = new_fname
            user.last_name = new_lname
            user.save()
            response = {
                'load_user_id': load_user.id,
                'request_user_id': request_user.id,
                'fullname': new_fname+' '+new_lname,
                'email': new_email,
                'fname': new_fname,
                'lname': new_lname,
            }
            return JsonResponse(response)

def new_avatar(request, username):
    if request.method == "POST":
        if request.is_ajax():
            new_avatar = request.POST['new_avatar']
            user = get_object_or_404(User, username=username)
            user.avatar = new_avatar
            user.save()
            return JsonResponse({'avatar': new_avatar})

def follow(request, username):
    user_from = request.user
    user_target = get_object_or_404(User, username=username)
    if request.method == "POST":
        followship = Followship(user_from=user_from, user_target=user_target)
        followship.save()

        feed = Feed(user=user_from, action='followed', target_user=user_target, date=followship.date)
        feed.save()
        return redirect('profile', username=username)

def unfollow(request, username):
    user_from = request.user
    user_target = get_object_or_404(User, username=username)
    followship = get_object_or_404(Followship, user_from=user_from, user_target=user_target)
    feed = get_object_or_404(Feed, user=user_from, action='followed', target_user=user_target, date=followship.date)
    if request.method == "POST":
        followship.delete()
        feed.delete()
        return redirect('profile', username=username)

def followings(request, username):
    load_user = get_object_or_404(User, username=username)
    request_user = request.user
    following = Followship.objects.filter(user_from=load_user)

    context = {
        'following': following,
        'load_user': load_user,
        'request_user': request_user,
    }
    return render(request, 'app_gamelog/user_list.html', context)

def followers(request, username):
    load_user = get_object_or_404(User, username=username)
    request_user = request.user
    followers = Followship.objects.filter(user_target=load_user)

    context = {
        'followers': followers,
        'load_user': load_user,
        'request_user': request_user,
    }
    return render(request, 'app_gamelog/user_list.html', context)

@login_required(login_url='index')
def analyses(request, username):
    load_user = get_object_or_404(User, username=username)
    request_user = request.user
    if load_user.id != request_user.id:
        return redirect('profile', username=load_user.username)
    times_logs = GameLog.objects.filter(user=request_user)
    costs_logs = OwnGame.objects.filter(user=request_user)
    steam_cost, xbox_cost, ps_cost, nin_cost = 0.0, 0.0, 0.0, 0.0
    total_cost = 0
    month_time = {}

    for log in costs_logs:
        if log.game.platform == 'Steam':
            steam_cost += log.price
        elif log.game.platform == 'Xbox':
            xbox_cost += log.price
        elif log.game.platform == 'PlayStation':
            ps_cost += log.price
        else:
            nin_cost += log.price
    
    total_expenses = steam_cost + xbox_cost + ps_cost + nin_cost
    
    for log in times_logs:
        month = log.date.strftime('%B')
        if month in month_time:
            month_time[month] += log.duration
        else:
            month_time[month] = log.duration
    
    context = {
        'costs': [
            {'platform': 'Steam', 'num': steam_cost, 'perct': round(100*steam_cost/total_expenses, 2)},
            {'platform': 'Xbox', 'num': xbox_cost, 'perct': round(100*xbox_cost/total_expenses, 2)},
            {'platform': 'PlayStation', 'num': ps_cost, 'perct': round(100*ps_cost/total_expenses, 2)},
            {'platform': 'Nintendo', 'num': nin_cost, 'perct': round(100*nin_cost/total_expenses, 2)},
        ],
        'times': month_time
    }

    return render(request, 'app_gamelog/analyses.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
                'msg': 'Invalid username or password',
                'signup_form': SignupForm(),
                'login_form': LoginForm(),
                'reset_pass_with_username_form': ChangePasswordWithUsernameForm(),
            }
            return render(request, 'app_gamelog/authentication.html', context)
    else:
        context = {
            'only-login': True,
            'login_form': LoginForm(),
        }
        return render(request, 'app_gamelog/authentication.html', context)

def signup_view(request):
    if request.method == "POST":
        username = request.POST['signup_username']
        email = request.POST['signup_email']
        gender = request.POST['signup_gender']
        fname = request.POST['signup_fname']
        lname = request.POST['signup_lname']
        password = request.POST['signup_password']
        avatar = avatar_dict['avatar_user']
        is_publisher = request.POST.get('signup_is_publisher', '')

        if is_publisher:
            if User.objects.filter(username=username).exists():
                context = {
                    'msg': 'Username exists.',
                    'signup_form': SignupForm(),
                    'login_form': LoginForm(),
                    'reset_pass_with_username_form': ChangePasswordWithUsernameForm(),
                }
                return render(request, 'app_gamelog/authentication.html', context)
            publisher = User(username=username,
                        email=email,
                        first_name=fname,
                        avatar=avatar,
                        is_publisher=True)
            publisher.set_password(password)
            publisher.save()
            context = {
                'only_login': True,
                'login_form': LoginForm(),
            }
            return render(request, 'app_gamelog/authentication.html', context)
        else:
            if User.objects.filter(username=username).exists():
                context = {
                    'msg': 'Username exists.',
                    'signup_form': SignupForm(),
                    'login_form': LoginForm(),
                    'reset_pass_with_username_form': ChangePasswordWithUsernameForm(),
                }
                return render(request, 'app_gamelog/authentication.html', context)
            user = User(username=username,
                        email=email,
                        gender = gender,
                        first_name=fname,
                        last_name=lname,
                        avatar=avatar)
            user.set_password(password)
            user.save()
            context = {
                'only_login': True,
                'login_form': LoginForm(),
            }
            return render(request, 'app_gamelog/authentication.html', context)
    else:
        context = {
            'signup_form': SignupForm(),
            'login_form': LoginForm(),
            'reset_pass_with_username_form': ChangePasswordWithUsernameForm(),
        }
        return render(request, 'app_gamelog/authentication.html', context)
    
def change_pass(request):
    if request.method == "POST" and request.is_ajax():
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        verify_password = request.POST['verify_password']
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({'msg': 'Please enter the correct old password.'})
        elif old_password == new_password:
            return JsonResponse({'msg': 'New password is same as the old one.'})
        elif new_password != verify_password:
            return JsonResponse({'msg': 'Passwords do not match.'})
        elif new_password == '':
            return JsonResponse({'msg': 'New password cannot be empty.'})
        else:
            user.set_password(new_password)
            user.save()
            return JsonResponse({'msg': 'Success! Redirect to login page in 3s...'})
    else:
        context = {
            'reset_pass': True,
            'reset_pass_form': ChangePasswordForm(),
        }
        return render(request, 'app_gamelog/authentication.html', context)

def check_old_password(request):
    if request.method == "GET" and request.is_ajax():
        user = request.user
        keyin_password = request.GET['keyin_password']
        if user.check_password(keyin_password):
            return JsonResponse({'msg': ''})
        else:
            return JsonResponse({'msg': 'Unmatched old password.'})

def check_match_old_password(request):
    if request.method == "GET" and request.is_ajax():
        old_password = request.GET['old_password']
        new_password = request.GET['new_password']
        if new_password == old_password:
            return JsonResponse({'msg': 'Same as old password.'})
        else:
            return JsonResponse({'msg': ''})

def check_match_password(request):
    if request.method == "GET" and request.is_ajax():
        new_password = request.GET['new_password']
        verify_password = request.GET['verify_password']
        if new_password != verify_password:
            return JsonResponse({'msg': 'Passwords do not match.'})
        else:
            return JsonResponse({'msg': ''})

def logout_view(request):
    logout(request)
    return redirect('index')