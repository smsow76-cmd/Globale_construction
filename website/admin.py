from django.contrib import admin
from .models import Produit, Categorie, Message, Commande, LigneCommande

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Message)


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nom",
        "telephone",
        "liste_produits",
        "total",
        "date",
    )

    search_fields = ("nom", "telephone", "email")
    list_filter = ("date",)
    inlines = [LigneCommandeInline]

    def liste_produits(self, obj):
        return ", ".join(
            [f"{ligne.produit.nom} (x{ligne.quantite})" for ligne in obj.lignes.all()]
        )

    liste_produits.short_description = "Produits"