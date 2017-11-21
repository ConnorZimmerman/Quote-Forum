#Pybelt Views
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import Quote
from ..login_registration.models import User
from django.contrib import messages

# Create your views here.
def Home(request):
    if "user" not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session["user"])
    context = {
        "user" : user,
        "quotes" : Quote.objects.all().exclude(favoritedUser = user.id),
        "quotesFavorited" : Quote.objects.filter(favoritedUser = user.id)
        }
    return render(request, 'py_belt/home.html', context)

def AddQuote(request):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    response = Quote.objects.quote_validator(request.POST, userId)
    for val in response["errors"]:
        messages.error(request, val, extra_tags="Login")
        return redirect('/py_belt')
    else:
        return redirect('/py_belt')

def AddToFavorites(request, quoteId):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    Quote.objects.add_to_favorites(userId, quoteId)
    return redirect('/py_belt')

def RemoveFromFavorites(request, quoteId):
    #creates a new instance of the quote before deleting it
    #holds on to users who favorited quote and gives back to specified users
    #except user who initially deleted (distinguished in models)
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    user = User.objects.get(id = userId)
    quote = Quote.objects.get(id=quoteId)
    userPosting = User.objects.get(id=quote.userPosting_id)
    newQuote = Quote.objects.create(author = quote.author, 
                                 message = quote.message, 
                                 userPosting = userPosting)
    allFavoritedUsers = User.objects.filter(id=quote.userPosting_id)
    user.favorite_quotes.get(id = quoteId).delete()
    userDeleting = userId
    print allFavoritedUsers
    for userAdding in allFavoritedUsers:
        Quote.objects.add_to_favorites_rewind(userAdding.id, newQuote.id, userDeleting)
    return redirect('/py_belt')

 #allFavoritedUsers = User.objects.all().filter(favorite_quotes = quoteId)
 #   user.favorite_quotes.get(id = quoteId).delete()
 #   userDeleting = userId
 #   print allFavoritedUsers
 #   for userAdding in allFavoritedUsers:
 #       print userAdding.id
 #       Quote.objects.add_to_favorites_rewind(userAdding.id, newQuote.id, userDeleting)
 #   return redirect('/py_belt')

def UserProfile(request, userId):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id = userId),
        "quotes" : Quote.objects.filter(userPosting_id = userId)
        }
    return render(request, 'py_belt/user.html', context)

def LogOut(request):
    request.session.clear()
    return redirect('/')

#userId = Review.objects.get(id = reviewId).user_id
#if userId != int(request.session["user"]):
#    return redirect('/')