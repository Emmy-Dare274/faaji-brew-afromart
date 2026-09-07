from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("our-story/", views.our_story, name="our_story"),
    path("terms-of-use/", views.terms_of_use, name="terms_of_use"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]