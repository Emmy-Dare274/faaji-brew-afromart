from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("our-story/", views.our_story, name="our_story"),
    path("terms-of-use/", views.terms_of_use, name="terms_of_use"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("delivery-returns/", views.delivery_returns, name="delivery_returns"),
    path("faq/", views.faq, name="faq"),
    path("contact-us/", views.contact_us, name="contact_us"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
