"""sesh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from seshapi.views import register_user, check_user
from seshapi.views import UserView, SessionView, CommentView, AttendanceView, FollowView, FollowerView, FollowedView, PostView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'sessions', SessionView, 'session')
router.register(r'comments', CommentView, 'comment')
router.register(r'attendances', AttendanceView, 'attendance')
router.register(r'follows', FollowView, 'follow')
router.register(r'posts', PostView, 'post')

urlpatterns = [
# Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
# Requests to http://localhost:8000/checkuser will be routed to the login_user function
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('followers/<int:follower_id>', FollowerView.as_view(), name='followers'),
    path('followed/<int:followed_id>', FollowedView.as_view(), name='followed')
]
