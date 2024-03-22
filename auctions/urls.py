from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("createListing", views.createListing, name="create"),
    path("item/<int:Id>/", views.viewItem, name="item")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
