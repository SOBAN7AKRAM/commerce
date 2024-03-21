from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    pass
class AuctionListing(models.Model):
    class categories(models.TextChoices):
        fashion = 'Fsh', _('Fashion')
        toys = 'Ty', _('Toys')
        electronics = 'Elec', _('Electronics')
        books = 'Book', _('Books')
        sports = 'sports', _('Sports')
        none = '', _('None')
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(blank=True)
    initialBid = models.IntegerField(default = 0)
    category = models.CharField(max_length=64, choices = categories, default = categories.none, blank = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "owner")
    
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidOn = models.ForeignKey(AuctionListing, on_delete = models.CASCADE, related_name = "bidOn")
    bid = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "buyer")
    def __str__(self):
        return f"{self.buyer.first_name} made {self.bid} on {self.bidOn.title}"
    
    
class Comments(models.Model):
    commentedOn = models.ForeignKey(AuctionListing, on_delete = models.CASCADE, related_name = "commentsOn")
    Comment = models.TextField()
    commentor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "commentor")
    def __str__(self):
        return f"{self.commentor} comment '{self.Comment}' on {self.commentedOn.title}" 