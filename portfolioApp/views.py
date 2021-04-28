from django.shortcuts import render, redirect

def index(request):
    if not 'user_id' in request.session:
        request.session['user_id'] = '3'
    context = {
        'nav': 'nav_out.html'
    }
    return render(request, 'index.html', context)

def get_page_info(page):
    pass
