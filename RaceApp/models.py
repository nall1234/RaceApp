from django.db import models
import re
import bcrypt


class UserValidator(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 charaters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email address'
        email_check = User.objects.filter(email= postData['email'])
        if email_check:
            errors['email_check'] = 'User email already in use'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 charactors'
        if not postData['password'] == postData['confirm_password']:
            errors['confirm_password'] = 'Password must match'   
        return errors
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
                return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    def message_validator(self, postData):
        errors = {}   
        if len(postData['message']) < 1:
            errors['message'] = "Message must be at least 1 character long"
        return errors
    def comment_validator(self, postData):
        errors = {}   
        if len(postData['comment']) < 1:
            errors['comment'] = "Comments must be at least 1 character long"
        return errors
    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 charaters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email address'
        email_check = User.objects.filter(email= postData['email'])
        if email_check:
            errors['email_check'] = 'User email already in use'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    image = models.ImageField ( null = True, blank = True, upload_to ="images/", default = '/static/images/blank')
    objects = UserValidator()

class Run(models.Model):
    user = models.ForeignKey(User, related_name = 'run', on_delete = models.CASCADE)
    distance = models.FloatField()
    time = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)