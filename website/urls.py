from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produits/', views.produits, name='produits'),
    path('services/', views.services, name='services'),
    path('galerie/', views.galerie, name='galerie'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('contact/', views.contact, name='contact'),
    path('produit/<int:id>/', views.produit_detail, name='produit_detail'),
    path('search/', views.search, name='search'),
    path('add-to-cart/<int:produit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('panier/', views.panier, name='panier'),


    path(
    "supprimer/<int:produit_id>/",
    views.supprimer_panier,
    name="supprimer_panier"
),

path(
    "valider-commande/",
    views.valider_commande,
    name="valider_commande"
),

path('increase/<int:produit_id>/', views.increase_qty, name='increase_qty'),
path('decrease/<int:produit_id>/', views.decrease_qty, name='decrease_qty'),
]