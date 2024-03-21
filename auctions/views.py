from django.contrib.auth import authenticate, login, logout
from . models import AuctionListing, Bid, Comments
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator

from .models import User


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class createListingForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
        required=True,
        label=mark_safe('Title <span class="required">*</>')
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        required=True,
        label=mark_safe('Description <span class="required">*</>')
    )
    initialBid = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)],
        label=mark_safe('Initial Bid <span class="required">*</>')
    )
    picture = forms.ImageField(
        label = 'Choose an Image:',
        required=False
    )
    category = forms.ChoiceField(
        label = 'Category:',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=AuctionListing.categories.choices,
        required=False
    )
    initialBid.widget.attrs.update({'class': 'form-control', 'placeholder': "Initial Bid"})
    picture.widget.attrs.update({'class': 'form-control'})
    
    
def createListing(request):
    form = createListingForm(label_suffix='')
    return render(request, "auctions/create.html", {
        'form': form,
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
