from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def loginValidator(self, form):

        email = form['email']
        password = form['password']

        errors = {}

        if not password:
            errors['login_password'] = "Password cannot be blank."

        if not email:
            errors['login_email'] = "Email cannot be blank."
        elif not User.objects.filter(email=email):
            errors['login_email'] = "Email not found. Please register."
        else:
            # compare password to one in database
            user = User.objects.filter(email=email)[0]
            # if user.password != password:
            #     errors['login_password'] = "Incorrect password."

            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                    errors['login_password'] = "Incorrect password."

            return errors, user

        return errors, False

    def regValidator(self, form):

        fname = form['first_name']
        lname = form['last_name']
        email = form['email']
        password = form['password']
        confirm_pw = form['confirm_pw']
        PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,8}$')

        errors = {}

        if not fname:
            errors['reg_fname'] = "First name cannot be blank."
        elif len(fname) < 2:
            errors['reg_fname'] = "First name must be at least 2 characters."

        if not lname:
            errors['reg_lname'] = "Last name cannot be blank."
        elif len(lname) < 2:
            errors['reg_lname'] = "Last name must be at least 2 characters."

        if not email:
            errors['reg_email'] = "Email cannot be blank."
        elif User.objects.filter(email=email):
            errors['reg_email'] = "Email already exists. Please login."

        if not password:
            errors['reg_password'] = "Password cannot be blank."
        # elif not PASSWORD_REGEX.match(password):
        #     errors['reg_password'] = "Password must be at least 4 characters, no more than 8 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit."
        elif password != confirm_pw:
            errors['reg_confirm_pw'] = "Passwords must match."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
