#PyBelt URLs
from django.conf.urls import url
from . import views

urlpatterns = [
    url('add/quote/validation$', views.AddQuote),
    url(r'add_to_list/(?P<quoteId>\d+)$', views.AddToFavorites),
    url(r'remove_from_list/(?P<quoteId>\d+)$', views.RemoveFromFavorites),
    url(r'users/(?P<userId>\d+)$', views.UserProfile),
    url(r'logOut', views.LogOut),
    url(r'^', views.Home),
]