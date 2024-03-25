from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("createListing", views.createListing, name="create"),
    path("item/<int:Id>/", views.viewItem, name="item"), 
    path("watchList/<int:Id>/", views.addOrRemoveToWatchList, name="watchList"),
    path("watchList", views.viewWatchList, name = "watch"),
    path("categories", views.categoriesList, name="categories"), 
    path("<str:name>", views.showCategoryItems, name="category")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
