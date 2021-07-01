from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class LogManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters long"

        if len(form['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters long"

        if not EMAIL_REGEX.match(form['email']):    
            errors['email'] = ("Invalid email address!")

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] ="Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
            
        if form['password'] != form['confirm_password']:
            errors['password'] = 'Passwords do not match'

        return errors
        
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        
        user= users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw
        )

    def quote(self, form):
        errors = {}
        if len(form['quote']) < 10:
            errors["quote"] = "Quote must be at least 10 chracters"

        return errors

    def author(self, form):
        errors = {}
        if len(form['author']) < 3:
            errors["author"] = "Author must be at least 3 chracters"

        return errors
        
    def account_validate(self,form):
        errors = {}
        if len(form['first_name']) < 1:
            errors["first_name"] = "First Name cannot be empty"

        if len(form['last_name']) < 1:
            errors["last_name"] = "Last Name cannot be empty"

        if not EMAIL_REGEX.match(form['email']):    
            errors['email'] = ("Invalid email address!")

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] ="Email already in use"
            
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = LogManager()

class Quote(models.Model):
    quote = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_quotes', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    
class Author(models.Model):
    author = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='quote', on_delete=models.CASCADE)

    