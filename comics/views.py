from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
import time
import datetime
from .models import *
from django.contrib import messages
from django.db.models import Count

@login_required(login_url='/accounts/login/')
def edit_about(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        series_title = data["series"]
        series=Series.objects.get(title=series_title)
        if data.get("about") is not None:
            series.about = data["about"]
        series.save()
        return HttpResponse(status=204)

@login_required(login_url='/accounts/login/')
def favorites(request,username):
    user=User.objects.get(pk=request.user.id)
    series_list=user.favs.all()
    return render(request, "comics/series_list.html",{
        "series_list":series_list
    })
    
@login_required(login_url='/accounts/login/')
def edit_bio(request):
    user=User.objects.get(pk=request.user.id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("bio") is not None:
            user.bio = data["bio"]
        user.save()
        return HttpResponse(status=204)

def popular_series(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    for i in range(start, end + 1):
        list_series=Series.objects.annotate(count=Count('fav')).order_by('-count')[start:end]
    # Artificially delay speed of response
    time.sleep(0.2)
    return JsonResponse([series.serialize() for series in list_series], safe=False)
     

def popular_updates(request):
    days = int(request.GET.get("days"))
    upper_limit=datetime.datetime.now()
    lower_limit=upper_limit-datetime.timedelta(days=days)
    chapters=Chapter.objects.filter(timestamp__range=(lower_limit,upper_limit)).order_by('-views')
    return JsonResponse([chapter.serialize() for chapter in chapters], safe=False)
    
def latest_chapters(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    for i in range(start, end + 1):
        chapters=Chapter.objects.all().order_by('-timestamp')[start:end]
    # Artificially delay speed of response
    time.sleep(0.2)
    return JsonResponse([chapter.serialize() for chapter in chapters], safe=False)
     
def search(request):
    searchResults=[]
    search=request.GET.get('search')
    result=Series.objects.filter(title__contains=search)
    
    return render(request, "comics/series_list.html",{
        "series_list":result
    })

def delete_latest_chapter(request,series_title):
    if request.method == "POST":
        series=Series.objects.get(title=series_title)
        chapter_number=series.chapters.last().chap
        pages=GalleryImage.objects.filter(series=series, chap=chapter_number)
        for page in pages:
            page.file.delete(save=True)
        pages.delete()
        Chapter.objects.filter(series=series,chap=chapter_number).delete()
        messages.info(request, 'Chapter successfully deleted.'),
        return HttpResponseRedirect(reverse('series_detail',args=(series_title,)))
    

def chapter(request,series_title,chapter_number):
    series=Series.objects.get(title=series_title)
    chapter=Chapter.objects.get(series=series, chap=chapter_number)
    pages=GalleryImage.objects.filter(series=series, chap=chapter_number)
    if pages.exists()==True:
        chapter.views+=1
        chapter.save()
        prev_chap=None
        next_chap=None
        try:
            series.chapters.get(chap=chapter_number-1)
            prev_chap=chapter_number-1
        except:
            prev_chap=None
        try: 
            series.chapters.get(chap=chapter_number+1)
            next_chap=chapter_number+1
        except:
            next_chap=None
        return render(request, "comics/chapter.html", {
            "series":series,
            "chapter":chapter,
            "prev_chap":prev_chap,
            "next_chap":next_chap,
            "pages":pages
                })
    else:
        messages.warning(request, 'File is not valid.'),
        return HttpResponseRedirect(reverse('series_detail',args=(series_title,)))



class ChapterForm(ModelForm):
    class Meta:
        model=Chapter
        fields=['zip_import']

def series_detail(request,series_title):
    series=Series.objects.get(title=series_title)
    if request.method == "POST":
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter=form.save(commit=False)
            chapter.series=series
            if series.chapters.all().exists()==False:
                chapter.chap=1
            else:
                chapter.chap=series.chapters.last().chap+1
            chapter.save()
            chapter_number=chapter.chap
            if chapter.is_valid():
                chapter.to_gallery()
                messages.success(request, 'Chapter sucessfully uploaded.'),
                return HttpResponseRedirect(reverse('chapter',args=(series_title,chapter_number,)))
            else:
                chapter.delete_import()
                chapter.delete()
                return render(request, "comics/series_detail.html", {
                "form": ChapterForm(),
                "series": series,
                "message":messages.warning(request, 'File is not valid.')
                })
    return render(request, "comics/series_detail.html", {
            "form": ChapterForm(),
            "series": series,
            })
    

class SeriesForm(ModelForm):
    class Meta:
        model=Series
        fields=['cover','title','about']

@login_required(login_url='/accounts/login/')
def create_series(request):
    if request.method == "POST":
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series=form.save(commit=False)
            series.author=User.objects.get(pk=request.user.id)
            series.save()
            series_title=series.title
            return HttpResponseRedirect(reverse('series_detail',args=(series_title,)))
    return render(request, "comics/create_series.html", {
            "form": SeriesForm(),
            })

def series(request):
    series_list=Series.objects.all().order_by('-id')
    return render(request, "comics/series_list.html",{
        "series_list":series_list
    })
@login_required(login_url='/accounts/login/')
def follow_status(request,series_title):
    if request.method=='POST':
        user=User.objects.get(pk=request.user.id)
        series=Series.objects.get(title=series_title)
        if series in user.favs.all():
            user.favs.remove(series)
        else:
            user.favs.add(series)
        return HttpResponseRedirect(reverse('series_detail',args=(series_title,)))

def index(request):
    return render(request, "comics/index.html",{
        "page_obj":'meh'
    })

def profile(request,username):
    profile = User.objects.get(username=username)
    return render(request, "comics/profile.html",{
        "profile":profile,
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "comics/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "comics/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "comics/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "comics/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "comics/register.html")
