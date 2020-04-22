from django.db import models
import re, bcrypt

class ShowManager(models.Manager):
    def new_validator(self, postData):
        user = User.objects.filter(email=postData['email'])
        errors= {}
        if (len(postData['first_name']) < 2):
            errors['first_name'] = 'First name must be at least 2 characters long.'
        
        if (len(postData['last_name']) < 2):
            errors['last_name'] = 'Last name must be at least 2 characters long.'
        
        if (len(postData['password']) < 8):
            errors['password'] = 'Password must be at least 8 characters long.'
        
        if postData['confirmed_pass'] != postData['password']:
            errors['password'] = 'Password must match the confirmation.'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address."

        if user:
            errors['email'] = "Email already registered"
        else:
            pass
        return errors


    def return_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])

        if (len(postData['email']) < 1):
            errors['email'] = "No email was entered."
        if (len(postData['password']) < 1):
            errors['password'] = "No password was entered."

        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                return errors
            else:
                errors['no_pass'] = 'Incorrect password'
        errors['no_email'] = 'Email is not registered'
        return errors



class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length= 255)
    password= models.CharField(max_length= 255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ShowManager()
