from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt, re

# Create your models here.
# DO NOT FORGET TO MAKE MIGRATIONS AND MIGRATE IF THE MODELS.PY GETS UPDATED.

#Below is your Manager that handles all the logic that will be seen in views.py, and information from your database
class UserManager(models.Manager):
    #Create a VALIDATION to verify the data that the user inputs into the input fields.
    #In this case, our function(def) is called validatex
    def validate(self, postData):
    #postData acts as request.post. it is just renamed.
        errors = []
    #Empty array where all errors will be .appended into
        if len (postData ["first_name"]) < 0:
    #if the first name field is left blank, an error will appear
            errors.append("First name field cannot be blank")
    #if it is less than 2 characters
        elif len(postData["first_name"]) < 2:
            errors.append("Must be between 2 - 45 characters")
    #will check if the user inputs the correct characters. In this case we are looking for only letters that has been placed in the First Name field.
        elif not re.search(r'^[A-Za-z]+$', postData["first_name"]):
            errors.append("First name must be letters only")
        if len (postData ["last_name"]) < 0:
            errors.append("Last name field cannot be blank")
        elif len (postData ["last_name"]) < 2:
            errors.append("Must be between 2- 45 characters")
        elif not re.search(r'^[A-Za-z]+$', postData["last_name"]):
            errors.append("Last name must be letters only")
    #Now working on the email field
        if len (postData["email"]) < 0:
            errors.append("Email field cannot be blank")
    #will check if the email is in proper format "example@gmail.com"
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append ("The entered email is not valid")
    #will check if the email already exists.
        elif len (User.objects.filter(email = postData["email"])) > 0:
            errors.append ("Entered email already exists")
    #Password Field:
        #checking length of password entered
        if len(postData["password"]) < 8:
            errors.append("Password must be 8 characters")
        #checking is passwords match. '!=' means is not equal to
        if postData["confirm"] != postData ["password"]:
            errors.append("Passwords do not match")
        #GO OVER THIS CODE!!
        if len(errors) == 0:
        #Adding user[]
            user = User.objects.create(first_name = postData["first_name"], last_name= postData["last_name"], email=postData["email"],pw_hash=bcrypt.hashpw(postData["password"].encode(),bcrypt.gensalt()))
            return (True, user)
        else:
            return(False, errors)

    #Next function is to authenticate an existing user
    def authenticate(self, postData):
        if "email" in postData and "password" in postData:
            try:
                user = User.objects.get(email=postData["email"])
            except User.DoesNotExist:
                return (False, "Invalid email/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid email/password combination.")
                # else:
                #     return (False, "Please enter login info.")

# Below is your database
class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    pw_hash = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
