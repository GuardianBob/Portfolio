from django.shortcuts import render, redirect, render_to_response
from loginApp.models import User
from .models import Message, Comment
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from .forms import MessageForm, CommentForm, UpdateUserForm, UpdatePasswordForm
from loginApp.forms import Register_Form
from django.contrib import messages
import bcrypt
from django.utils import timezone
import datetime
from django.template import loader

# Create your views here.
def get_nav(request):
    nav = 'nav_out.html'
    if 'user_id' in request.session:
        nav = "nav_in.html"
    return nav

def demo_user(request):
    demo_user = {}

def validate_user(user_id):
    user = User.objects.get(id=user_id)
    return user.user_level

def admin(request):    
    context = {
        'page_title' : 'Admin Dashboard',        
    }

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    context = {
        'nav': get_nav(request),
        'admin' : user.user_level,
        'users' : User.objects.all(),
        'user_id': user.id,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)

def new_user(request):
    user_id = request.session['user_id']
    if validate_user(user_id) is False:
        return redirect('/dashboard')
    form = Register_Form()
    context = {
        'nav': get_nav(request),
        'user_id': user_id,
        'register_form': form,
        'page_title': 'Add User',
    }
    return render(request, 'add_user.html', context)


def edit_profile(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'nav': get_nav(request),
        'user': user,
        'user_id': user.id,
        'current_user': user,
        'page_title': 'Edit Profile',
        'form_title': 'profile',
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
    }
    return render(request, 'edit_user.html', context)


def show_user(request, user_id):
    user = User.objects.get(id=request.session['user_id'])    
    if len(User.objects.filter(id=user_id)) == 0:
        return redirect('/dashboard')
    profile = User.objects.get(id=user_id)
    messages = Message.objects.filter(user=profile)
    context = {
        'nav': get_nav(request),
        'profile': profile,
        'user': user,
        'user_id': user.id,
    }
    return render(request, 'profile.html', context)

def edit_user(request, user_id):
    context = {
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
        'update': '',        
    }    
    return render_edit_page(request, context, user_id)

def render_edit_page(request, context, user_id):
    current_user = User.objects.get(id=request.session['user_id'])
    if validate_user(current_user.id) is True:
        user = User.objects.get(id=user_id)
        form_title = user.full_name + ' : User ' + str(user_id)
    else:
        user = User.objects.get(id=request.session['user_id'])
        form_title = 'Profile'    
    user_level = "Normal"
    if current_user.user_level is True:
        user_level = "Admin"
    add_info = {
        'nav': get_nav(request),
        # 'admin' : current_user.user_level,
        'user': user,
        # 'user_id': current_user.id,
        'current_user': current_user,
        'user_id': current_user.id,
        'form_title': form_title,
        'page_title': 'Edit' + form_title,
        'level_select': {False:'Normal',True:'Admin'},
    }
    context.update(add_info)
    return render(request, 'edit_user.html', context)

def update_password(request):
    if request.method != "POST":
        return redirect("/register")
    check_form = UpdatePasswordForm(request.POST)
    if not check_form.is_valid():
        password_form = Register_Form()
        context = { 
            'password_form' : check_form,
            'form': UpdateUserForm(),
            # 'user_id': request.POST['user_id'],
            }
        return render_edit_page(request, context, request.POST['user_id'])
    else:
        user = User.objects.get(id=request.POST['user_id'])
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user.password = password
        user.save()
        print('success!')
        return success(request, request.POST['user_id'])

def success(request, user_id):
    context = {
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
        'update': 'Update successful!',
        }
    return render_edit_page(request, context, user_id)

def update_user(request):
    if request.method != "POST":
        return redirect("/login/register")
    if request.POST['user_id'] == '2' or request.POST['user_id'] == '3':
        return redirect('/dashboard')
    check_form = UpdateUserForm(request.POST)
    if not check_form.is_valid():
        print(check_form)
        context = { 
            'password_form' : UpdatePasswordForm(),
            'form': check_form,
            # 'user_id': request.POST['user_id'],                       
            }
        return render_edit_page(request, context, request.POST['user_id'])
    else:
        # print(request.POST)
        user = User.objects.get(id=request.POST['user_id'])
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        # user.user_level = request.POST['user_level']
        user.description = request.POST['description']
        user.save()
        print('success!')
        return success(request, request.POST['user_id'])

def remove_user(request, remove_id):
    user_id = request.session['user_id']
    if remove_id == '2' or remove_id == '3':
        return redirect('/dashboard')
    if validate_user(user_id) is False:
        return redirect('/dashboard')
    remove = User.objects.get(id=remove_id)
    remove.delete()
    return redirect('/dashboard/')

def post_message(request, profile_id):
    if request.method != "POST":
        return redirect(f"/users/show/{profile_id}")
    creator = User.objects.get(id=request.session['user_id'])
    Message.objects.create(message=request.POST['message'], user=User.objects.get(id=profile_id), created_by=creator)
    # return redirect(f'users/show/{profile_id}')
    return redirect(f'../{profile_id}')

def post_comment(request, profile_id):
    if request.method != "POST":
        return redirect(f"/users/show/{profile_id}")
    creator = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=request.POST['message_id'])
    Comment.objects.create(comment=request.POST['comment'], message=message, user=creator)
    return redirect(f'../{profile_id}')
