from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import *
from django.contrib import messages

def index(request):
    context = {
    "time": strftime("%b %d, %Y  %H:%M %p", gmtime())
    }
    return render(request, "index.html", context)
   

def register(request):
    if request.method == "GET":
        return redirect("/")
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        # messages.success(request, "You have successfully registered!")
        return redirect('/main')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    # messages.success(request, "You have successfully logged in!")
    return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)


def main(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    books = Book.objects.all()
    context = {
        'user': user,
        'books': books,
    }
    return render(request, 'main.html', context)


#Create book function
def create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.create(title = request.POST['title'], description = request.POST['description'], user_uploaded = user)

    add_book_Fav = Book.objects.get(id=book.id)
    user.users_liked_books.add(add_book_Fav)
   
    return redirect('/main')

def show_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    
    context = {
        'user': user,
        'book': book,
    }

    return render(request, 'showbook.html', context)


def edit_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.get(id=id)
    book.title = request.POST['title']
    book.description = request.POST['description']
    book.save()
   
    return redirect('/main')

 
def delete_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    delete_book = Book.objects.get(id=id)
    print("session user id: " + str(request.session['user_id']))
    print("Message user id: " + str(delete_book.user_uploaded.id))
    if ((request.session['user_id']) == delete_book.user_uploaded.id):
        delete_book.delete()
    
    return redirect('/main')   


def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.users_liked_books.add(book)

    return redirect('/main')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.users_liked_books.remove(book)

    return redirect('/main')
    
