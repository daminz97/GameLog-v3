from .models import *

def notification_dot(request):
    pass
    # if request.user.is_authenticated:
    #     last_login = request.user.last_login
    #     new_feeds = Feed.objects.filter(date__gt=last_login)
    #     user_feeds = new_feeds.exclude(user=request.user).order_by('-date')
    #     if user_feeds:
    #         return {'notification': True}
    #     else:
    #         return {'notification': False}
    # else:
    #     return {'notification': False}