
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("create_series", views.create_series, name="create_series"),
    path("series/<str:series_title>", views.series_detail, name="series_detail"),
    path("series", views.series, name="series"),
    path("series/<str:series_title>/<int:chapter_number>", views.chapter, name="chapter"),
    path("authors/<str:username>", views.profile, name="profile"),
    path("series/<str:series_title>/delete_latest_chapter", views.delete_latest_chapter, name="delete_latest_chapter"),
    path("latest_chapters", views.latest_chapters, name="latest_chapters"),
    path("popular_series", views.popular_series, name="popular_series"),
    path("popular_updates", views.popular_updates, name="popular_updates"),
    path("series/<str:series_title>/follow_status", views.follow_status, name="follow_status"),
    path("edit_bio", views.edit_bio, name="edit_bio"),
    path("favorites/<str:username>", views.favorites, name="favorites"),
    path("edit_about", views.edit_about, name="edit_about"),
] 
