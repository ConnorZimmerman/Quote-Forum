#Py_Belt MODELS
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User


# Create your models here.
class QuoteManager(models.Manager):
    def quote_validator(self, postData, userId):
        response = {
            "errors" : []
            }
        if len(postData["author"]) < 4:
            response["errors"].append("Author must be more than 3 characters!")
        if len(postData["message"]) < 11: 
            response["errors"].append("Quote must be longer than 10 characters!")
        if len(response["errors"]) == 0:
            self.create(author = postData["author"], 
                                 message = postData["message"], 
                                 userPosting = User.objects.get(id = userId))
            user = User.objects.get(id=userId)
            user.count = len(Quote.objects.filter(userPosting_id = userId))
            user.save()
        return response

    def add_to_favorites(self, userId, quoteId):
        user = User.objects.get(id = userId)
        user.favorite_quotes.add(Quote.objects.get(id = quoteId))
        user.save()
        return

    def add_to_favorites_rewind(self, userAdding, quoteId, userDeleting):
        #print userDeleting
        #print userAdding
        if userAdding == userDeleting:
            print "*********************"
            return
        else:
            user = User.objects.get(id = userAdding)
            user.favorite_quotes.add(Quote.objects.get(id = quoteId))
            user.save()
            return

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.TextField()
    userPosting = models.ForeignKey(User, related_name = "quotes")
    favoritedUser = models.ManyToManyField(User, related_name="favorite_quotes")
    objects = QuoteManager()