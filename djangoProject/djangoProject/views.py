from rest_framework import viewsets, generics, permissions
from .models import VideoGame, Cart, CartItem, Order
from .serializers import VideoGameSerializer, CartSerializer, CartItemSerializer, OrderSerializer

from django.shortcuts import render

def index(request):
    return render(request, 'djangoProject/index.html')  # Chemin vers le template

# ViewSet for VideoGames (No authentication required)
class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer
    permission_classes = [permissions.AllowAny]  # Accessible à tout le monde

# Views for Cart (Requires authentication)
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

# ViewSet for Orders (Requires authentication)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        # Calculer le total des prix dans le panier
        total_price = sum([item.game.price * item.quantity for item in cart.items.all()])
        # Créer la commande
        order = serializer.save(user=self.request.user, total_price=total_price)
        # Ajouter les items du panier à la commande
        for item in cart.items.all():
            OrderItem.objects.create(order=order, game=item.game, quantity=item.quantity)
        # Vider le panier après validation de la commande
        cart.items.all().delete()
