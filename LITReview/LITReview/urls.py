"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^inscription/$', views.inscription),
    url(r'^loginMe/$', views.loginMe, name='login'),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
    url(r'^home/$', views.home),
    url(r'^unfollow/$', views.unfollow, name='unfollow'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^Abonnements/$', views.Abonnements),
    url(r'^create_ticket/$', views.create_ticket),
    url(r'^create_review/$', views.create_review),
    url(r'^flux/$', views.flux),
    url(r'^posts/$', views.posts),
    url(r'^add_review/$', views.add_review, name='add_review'),
    url(r'^update_ticket/$', views.update_ticket, name='update_ticket'),
    url(r'^delete_ticket/$', views.delete_ticket, name='delete_ticket'),
    url(r'^update_review/$', views.update_review, name='update_review'),
    url(r'^delete_review/$', views.delete_review, name='delete_review'),
]
