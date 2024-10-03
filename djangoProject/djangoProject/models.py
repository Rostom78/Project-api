from django.db import models
from django.contrib.auth.models import AbstractUser


class VideoGame(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='game_images/')  # Nécessite Pillow pour gérer les images
    stock = models.IntegerField()
    release_date = models.DateField()
    platform = models.CharField(max_length=100)  # Par exemple : PC, Xbox, PlayStation

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.game.title} in Cart {self.cart.id}"
class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.game.title} in Order {self.order.id}"
