from django.shortcuts import render, redirect
from loginApp.models import User
from .models import Trip
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from .forms import TripForm
from django.contrib import messages
import pytz
from django.utils import timezone
from datetime import datetime

def get_nav(request):
    nav = 'nav_out.html'
    if 'user_id' in request.session:
        nav = "nav_in.html"
    return nav

def oops(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user, 
        'nav': get_nav(request),
        'nav_title': "Sorry, that doesn't exist!",
        'page_title': '$#!+ ! Whoops!'   
    }

def render_trip_page(request, context):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    add_info = {
        'user': user, 
        'nav': get_nav(request),
    }
    context.update(add_info)
    return render(request, 'edit_trip.html', context)

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    trips = Trip.objects.all()
    nav_title = ""
    context = {
        'user': user, 
        'nav': get_nav(request),
        'nav_title': ' ',
        'page_title': 'Dashboard',
        'trips': trips,       
    }
    return render(request, 'trip_dash.html', context)


def trips(request, trip_id, extra=''):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if not Trip.objects.get(id=trip_id):
        return oops(request)
    trip = Trip.objects.get(id=trip_id)
    context = {
        'user': user, 
        'nav': get_nav(request),
        'nav_title': 'Read about this trip!',
        'page_title': 'View Trip',  
        'trip': trip
    }
    context.update(extra)
    return render(request,'trip.html', context)

def new_trip(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    form = TripForm()
    context = {
        'nav_title': 'Create a Trip!',
        'page_title': 'New Trip',
        'form': form,   
        'action': 'create'
    }
    return render_trip_page(request, context)

def create_trip(request):
    if request.method != "POST":
        return redirect("/trips/new")
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    check_form = TripForm(request.POST)
    if not check_form.is_valid():
        # print(check_form)
        context = {
            'form': check_form, 
            'action': 'create'                  
            }
        return render_trip_page(request, context)
    trip = Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], details=request.POST['details'], planned_by=user)
    return redirect('/tripbuddy')

def join_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if not Trip.objects.get(id=trip_id):
        return oops(request)
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.joined_by.add(user)
    trip.save()
    return redirect('/tripbuddy')

def edit_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if not Trip.objects.get(id=trip_id):
        return oops(request)    
    trip = Trip.objects.get(id=trip_id)
    if not trip.planned_by.id == user.id:
        return redirect('/tripbuddy')
    form = TripForm()
    form.fields['destination'].initial = trip.destination
    form.fields['start_date'].initial = trip.start_date.date()
    form.fields['end_date'].initial = trip.end_date.date()
    form.fields['details'].initial = trip.details
    context = {
        'nav_title': "Let's edit your trip!",
        'page_title': 'Edit Trip', 
        'form': form,  
        'trip': trip, 
        'action': 'update',
    }
    return render_trip_page(request, context)

def update_trip(request):
    if request.method != "POST":
        return redirect("")
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    check_form = TripForm(request.POST)
    print(check_form.errors)
    if not check_form.is_valid():
        print(check_form)
        trip = Trip.objects.get(id=request.POST['trip_id'])
        context = {
            'form': check_form,  
            'action': 'update',
            }
        
        return render_trip_page(request, context)
    trip = Trip.objects.get(id=request.POST['trip_id'])
    print(request.POST['details'])
    trip.destination = request.POST['destination']
    trip.start_date = request.POST['start_date']
    trip.end_date = request.POST['end_date']
    trip.details = request.POST['details']
    trip.save()
    return redirect('/tripbuddy')

def remove_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    if trip.planned_by.id == user.id:
        trip.delete()
    return redirect('/tripbuddy')

def delete_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    if trip.planned_by.id != request.session['user_id']:
        return redirect('/tripbuddy')
    info = {
        'delete': True,
    }
    return trips(request, trip.id, info)

def cancel_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.joined_by.remove(user)
    trip.save()
    return redirect('/tripbuddy')


