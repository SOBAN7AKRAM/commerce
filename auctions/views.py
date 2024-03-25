from django.contrib.auth import authenticate, login, logout
from . models import AuctionListing, Bid, Comments, WatchList
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        'auctionlist' : AuctionListing.objects.all(), 
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
    
@login_required(login_url='login')
def createListing(request):
    if request.method == "POST":
        form = createListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            initialBid = form.cleaned_data["initialBid"]
            picture = form.cleaned_data["picture"]
            category = form.cleaned_data["category"]
            if User.is_authenticated:
                ac = AuctionListing(title=title, description=description, initialBid=initialBid, image=picture, category=category, owner = request.user)
                ac.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/create.html', {
                'form' : form
            })
    form = createListingForm(label_suffix='')
    return render(request, "auctions/create.html", {
        'form': form,
    })
def isOwner(request, ac):
    if request.user.is_authenticated:
        if request.user == ac.owner:
            return True
    return False
def getStatus(ac):
    if ac.isActive:
        return "Open"
    return "Closed"
def isWinner(request, noOfBids, ac, highestBid):
    if request.user.is_authenticated and ac.isActive == False and isOwner(request, ac) == False:
        if noOfBids != 0:
            winner = Bid.objects.filter(bidOn = ac, bid = highestBid)
            if winner is not None:
                if winner.first().buyer == request.user:
                    return True
    return False 
class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...'}),
        required=False,
        label='',
        error_messages={'required': ''}
    )
    comment.widget.attrs.update(required = True)
def viewItem(request, Id):
    ac = AuctionListing.objects.get(id=Id)
    highestBid = Bid.objects.filter(bidOn = ac).aggregate(Max('bid'))['bid__max']
    # To Check if item is in user watchlist or not
    noOfBids = Bid.objects.filter(bidOn = ac).count()
    flag = True
    message = None
    form = CommentForm(request.POST)
    if request.user.is_authenticated:
        try:
            wc = WatchList.objects.get(watchUser = request.user)
        except WatchList.DoesNotExist:
            flag = False
        if flag:
            if not wc.products.contains(ac):
                flag = False
    else:
        flag = False
    Owner = isOwner(request, ac)
    if request.method == "POST" and Owner:
        ac.isActive=False
        ac.save()
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, 'auctions/login.html')
        if 'comment_submit' in request.POST:
            if form.is_valid():
                comment = form.cleaned_data["comment"]
                if request.user.is_authenticated:
                    commentModel = Comments(commentedOn = ac, Comment = comment, commentor = request.user)
                    commentModel.save()
        else:
            newBid = int(request.POST["bidInput"])
            if (highestBid is None or newBid > highestBid) and newBid > ac.initialBid:
                newObj = Bid.objects.create(bidOn = ac, bid = newBid, buyer = request.user)
                highestBid = newBid
                noOfBids += 1
                newObj.save()
            else:
                message = "Your bid Should be greater than current bid"
        
        
    if highestBid is None:
        highestBid = ac.initialBid  
    getComments = None
    try:
        getComments = Comments.objects.filter(commentedOn = ac).all()
    except Comments.DoesNotExist:
        pass
    return render(request, 'auctions/item.html', {
        'auctionList': ac, 
        'isWatchListItem' : flag,
        'isOwner' : Owner,
        'status' : getStatus(ac),
        'highestBid' : highestBid,
        'noOfBids': noOfBids,
        'message' : message, 
        'isWinner': isWinner(request, noOfBids, ac, highestBid),
        'comments': getComments,
        'commentForm' : form
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

@login_required(login_url='login')
def addOrRemoveToWatchList(request, Id):
    wc, created = WatchList.objects.get_or_create(watchUser = request.user)
    if request.method == "POST" and request.user.is_authenticated:
        ac = AuctionListing.objects.get(id=Id)
        if wc.products.contains(ac):
            wc.products.remove(ac)
            return HttpResponseRedirect(reverse("item",kwargs={'Id': Id}))
        else:
            wc.products.add(ac)
        wc.save()
    if (wc):
            products = wc.products.all()
    else:
            products =[]
    return render(request, 'auctions/watchList.html', {
        'products': products,
        'isEmpty' : len(products) == 0
    })
@login_required(login_url='login')
def viewWatchList(request):
    flag = True
    try:
        wc = WatchList.objects.get(watchUser = request.user)
    except WatchList.DoesNotExist:
        flag = False
    if flag:
        products = wc.products.all()
    else:
        products = []
    return render(request, 'auctions/watchList.html', {
        'products': products,
        'isEmpty' : len(products) == 0
    })
    
def categoriesList(request):
    categories = [category for _, category in AuctionListing.categories.choices]
    categories.remove('None')
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })
def showCategoryItems(request, name):
    cat = extractCategory(name)
    ac = AuctionListing.objects.filter(category = cat).all()
    return render(request, 'auctions/category.html', {
        'category': name, 
        'auctionlist': ac
    })
def extractCategory(name):
    if name == 'Fashion':
        return 'Fsh'
    elif name == 'Toys':
        return 'Ty'
    elif name == 'Electronics':
        return 'Elec'
    elif name == 'Books':
        return 'Book'
    elif name == 'Sports':
        return 'sports'