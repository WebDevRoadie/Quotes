from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def registration(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        request.session['user_name'] = new_user.first_name
        messages.success(request, "You have successfully registered!")
        return redirect('/dashboard')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    messages.success(request, "You have successfully logged in!")
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_id': user,
        'quote': Quote.objects.all()
    }
    return render(request, 'dashboard.html', context)

def post_quote(request):
    errors = User.objects.quote(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/dashboard')
    Quote.objects.create(quote=request.POST['quote'], poster=User.objects.get(id=request.session['user_id']))
    Author.objects.create(author=request.POST['author'], poster=User.objects.get(id=request.session['user_id']))
    return redirect('/dashboard')

def posted_by(request, id):
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, 'posted_by.html', context)

def account(request, id):
    context = {
        'user': User.objects.get(id=id)
        }
    return render(request, 'account.html', context)

def delete(request, id):
    destroyed = Quote.objects.get(id=id)
    destroyed.delete()
    return redirect('/dashboard')

def edit(request, id):
    errors = User.objects.account_validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/account/{id}')
    else:
        edit_user = User.objects.get(id=id)
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.email = request.POST['email']
        edit_user.save()
    return redirect('/dashboard')

def like(request, id):
    liked_message = Quote.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/dashboard')
