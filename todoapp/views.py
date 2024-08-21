from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from todoapp.forms import TodoForm
from todoapp.models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='user_login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm()
        todos = Todo.objects.filter(user = user).order_by('priority')
        return render(request, 'index.html',context={'form':form ,'todos':todos})

# def user_login(request):  # Renamed from 'login' to 'user_login'
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Using 'auth_login' to avoid conflict
                return redirect('home')
            else:
                context = {
                    "form": form,
                }
                return render(request, 'login.html', context=context)

def user_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        # If form is invalid or authentication fails, re-render the login page with errors
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        # Optionally handle other HTTP methods
        return HttpResponse(status=405)  # Method Not Allowed

# def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('user_login')  # Redirect to the renamed login view
        else:
            return render(request, 'signup.html', context=context)

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to the login page after successful signup
            return redirect('user_login')
        else:
            # Add form errors to the context and re-render the signup page
            context = {
                "form": form
            }
            return render(request, 'signup.html', context=context)
    else:
        # Optionally handle other HTTP methods
        return HttpResponse(status=405)  # Method Not Allowed
    
@login_required(login_url='user_login')    
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
    form = TodoForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        print(todo)
        return redirect("home")
    else:
        return render(request, 'index.html',context={'form':form})
    
def signout(request):
    logout(request)
    return redirect('user_login')

def delete_todo(request,id):
    print(id)
    Todo.objects.get(pk =id).delete()
    return redirect('home')

def change_todo(request,id,status):
    todo = Todo.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')