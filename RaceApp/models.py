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
        user = User.objects.get(id= request.sesssion['current_user'])
        errors = {}   
        if len(postData['comment']) < 1:
            errors['comment'] = "Comments must be at least 1 character long"
        return errors
    def edit_validator(self, postData, id):
        user = User.objects.get(id= id)
        errors = {}
        if len(postData['first_name']) == 1:
            errors['first_name'] = 'First Name must be at least 2 charaters long'
        if len(postData['last_name']) == 1:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if postData['email'] == user.email:
            pass
        else:
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
    image = models.ImageField ( null = True, blank = True, upload_to ="images/", default = 'images/blank.jpg')
    objects = UserValidator()

class Run(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, related_name = 'run', on_delete = models.CASCADE)
    distance = models.FloatField()
    time = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)


class MessageValidator(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['message']) < 2:
            errors['message'] = 'Message must be at least 1 charaters long'
        return errors

class Message(models.Model):
    message = models.TextField(max_length = 255)
    message_creator = models.ForeignKey(User, related_name = "message", on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    objects = MessageValidator()

class CommentValidator(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comment']) < 2:
            errors['comment'] = 'Comment must be at least 1 charaters long'
        return errors

class Comment(models.Model):
    comment = models.TextField(max_length = 255)
    comment_message = models.ForeignKey(Message, related_name = 'message_comment', on_delete = models.CASCADE)
    comment_creator = models.ForeignKey(User, related_name = 'created_comment', on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    objects = CommentValidator()


class Race(models.Model):
    runner = models.ForeignKey(User, related_name = 'race', on_delete = models.CASCADE)
    week = models.PositiveIntegerField()
    distance_goal = models.FloatField()
    sunday_completed = models.BooleanField(default = False)
    monday_completed = models.BooleanField(default = False)
    tuesday_completed = models.BooleanField(default = False)
    wednesday_completed = models.BooleanField(default = False)
    thursday_completed = models.BooleanField(default = False)
    friday_completed = models.BooleanField(default = False)
    saturday_completed = models.BooleanField(default = False)
    sunday = models.FloatField()
    monday = models.FloatField()
    tuesday = models.FloatField()
    wednesday = models.FloatField()
    thursday = models.FloatField()
    friday = models.FloatField()
    sat = models.FloatField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
