from django.shortcuts import render
from .models import Produit, Categorie


def home(request):

    categories = Categorie.objects.all()

    data = []

    for cat in categories:
        produits = Produit.objects.filter(categorie=cat)

        data.append({
            "categorie": cat,
            "produits": produits
        })

    return render(request, "website/home.html", {
        "data": data
    })


def produits(request):

    categorie = request.GET.get("categorie")

    produits = Produit.objects.all()

    if categorie:
        produits = produits.filter(categorie_id=categorie)

    return render(request, "website/produits.html", {
        "produits": produits
    })


def services(request):
    return render(request, "website/services.html")


def galerie(request):
    produits = Produit.objects.all()

    return render(request, "website/galerie.html", {
        "produits": produits
    })


def a_propos(request):
    return render(request, "website/a_propos.html")





from django.shortcuts import render, get_object_or_404
from .models import Produit

def produit_detail(request, id):
    produit = get_object_or_404(Produit, id=id)

    similaires = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:6]

    return render(request, "website/produit_detail.html", {
        "produit": produit,
        "similaires": similaires
    })


from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        message = request.POST.get("message")

        sujet = f"Nouveau message de {nom}"

        contenu = f"""
        Nom: {nom}
        Email: {email}
        Téléphone: {telephone}

        Message:
        {message}
        """

        send_mail(
            sujet,
            contenu,
            email,  # expéditeur
            ['tonemail@gmail.com'],  # ADMIN (toi)
            fail_silently=False,
        )

        messages.success(request, "Votre message a été envoyé avec succès. Nous vous répondrons très bientôt.")

    return render(request, "website/contact.html")




from django.shortcuts import render
from .models import Produit
from django.shortcuts import redirect

def search(request):

    query = request.GET.get('q', '').strip()

    produits = []

    if query:
        produits = Produit.objects.filter(nom__icontains=query)

    return render(request, "website/search.html", {
        "produits": produits,
        "query": query
    })


from django.http import HttpResponseRedirect

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def add_to_cart(request, produit_id):

    cart = request.session.get("cart", {})

    produit_id = str(produit_id)

    if produit_id in cart:
        cart[produit_id] += 1
    else:
        cart[produit_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    # 🔥 MESSAGE DE CONFIRMATION
    messages.success(request, "Produit ajouté au panier avec succès.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def increase_qty(request, produit_id):
    cart = request.session.get("cart", {})
    cart[str(produit_id)] = cart.get(str(produit_id), 0) + 1
    request.session["cart"] = cart
    return redirect("panier")


def decrease_qty(request, produit_id):
    cart = request.session.get("cart", {})

    if str(produit_id) in cart:
        cart[str(produit_id)] -= 1

        if cart[str(produit_id)] <= 0:
            del cart[str(produit_id)]

    request.session["cart"] = cart
    return redirect("panier")

def cart_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())



from .models import Produit
from django.shortcuts import render

def cart(request):
    cart = request.session.get('cart', {})

    produits = []
    total = 0

    for produit_id, qty in cart.items():
        produit = Produit.objects.get(id=produit_id)

        subtotal = produit.prix * qty
        total += subtotal

        produits.append({
            "produit": produit,
            "qty": qty,
            "subtotal": subtotal
        })

    return render(request, "website/cart.html", {
        "produits": produits,
        "total": total
    })

def checkout(request):
    request.session['cart'] = {}
    return render(request, "website/success.html")


from django.shortcuts import render
from .models import Produit

def panier(request):
    cart = request.session.get("cart", {})

    produits = []
    total = 0

    for produit_id, qty in cart.items():
        produit = Produit.objects.get(id=produit_id)

        subtotal = produit.prix * qty

        produits.append({
            "produit": produit,
            "qty": qty,
            "subtotal": subtotal
        })

        total += subtotal

    return render(request, "website/panier.html", {
        "produits": produits,
        "total": total
    })






from django.shortcuts import redirect

def supprimer_panier(request, produit_id):
    cart = request.session.get("cart", {})

    produit_id = str(produit_id)

    if produit_id in cart:
        del cart[produit_id]

    request.session["cart"] = cart

    return redirect("panier")


from django.contrib import messages
from .models import Commande, LigneCommande, Produit

def valider_commande(request):

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect("panier")

    if request.method == "POST":

        nom = request.POST.get("nom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        adresse = request.POST.get("adresse")

        commande = Commande.objects.create(
            nom=nom,
            telephone=telephone,
            email=email,
            adresse=adresse
        )

        total = 0

        for produit_id, qty in cart.items():

            produit = Produit.objects.get(id=produit_id)

            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=qty,
                prix=produit.prix
            )

            total += produit.prix * qty

        commande.total = total
        commande.save()

        request.session["cart"] = {}

        messages.success(
            request,
            "Votre commande a été validée avec succès."
        )

        return redirect("panier")

    return render(request, "website/checkout.html")