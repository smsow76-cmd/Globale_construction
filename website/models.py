from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='produits/')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nom
    

from .models import Produit
from django.shortcuts import render
from .models import Produit, Categorie

def galerie(request):
    produits = Produit.objects.all()

    return render(request, "website/galerie.html", {
        "produits": produits
    })



class Message(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
    

from django.db import models


class Commande(models.Model):
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)

    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande N°{self.id} - {self.nom}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name="lignes"
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField(default=1)

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def sous_total(self):
        return self.quantite * self.prix

    def __str__(self):
        return self.produit.nom