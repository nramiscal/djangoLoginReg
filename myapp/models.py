from django.db import models
import re

class UserManager(models.Manager):
    def loginValidator(self, form):

        email = form['email']
        password = form['password']

        errors = {}

        if not email:
            errors['email'] = "Email cannot be blank."
        elif not User.objects.filter(email=email):
            errors['email'] = "Email not found. Please register."
        else:
            # compare password to one in database
            user = User.objects.filter(email=email)[0]
            if user.password != password:
                errors['password'] = "Incorrect password."

        if not password:
            errors['password'] = "Password cannot be blank."

        return errors

    def regValidator(self, form):

        fname = form['first_name']
        lname = form['last_name']
        email = form['email']
        password = form['password']
        confirm_pw = form['confirm_pw']
        PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,8}$')

        errors = {}

        if not fname:
            errors['fname'] = "First name cannot be blank."
        elif len(fname) < 2:
            errors['fname'] = "First name must be at least 2 characters."

        if not lname:
            errors['lname'] = "Last name cannot be blank."
        elif len(lname) < 2:
            errors['lname'] = "Last name must be at least 2 characters."

        if not email:
            errors['email'] = "Email cannot be blank."
        elif User.objects.filter(email=email):
            errors['email'] = "Email already exists. Please login."

        if not password:
            errors['password'] = "Password cannot be blank."
        elif not PASSWORD_REGEX.match(password):
            errors['password'] = "Password must be at least 4 characters, no more than 8 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit."
        elif password != confirm_pw:
            errors['password'] = "Passwords must match."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
