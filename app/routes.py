from flask import render_template, request, jsonify, redirect, url_for
from app import app, db
from app.models import Produit
from sqlalchemy import and_

@app.route('/')
def index():
    return render_template('kits/configurateur.html')

@app.route('/kits')
def liste_kits():
    """Affiche les kits disponibles par type de logement"""
    kits = Kit.query.all()
    return render_template('kits/liste.html', kits=kits)

@app.route('/kits/configurateur')
def configurateur():
    """Interface pour configurer un kit selon les dimensions"""
    return render_template('kits/configurateur.html')

@app.route('/api/kit/configurer', methods=['POST'])
def configurer_kit():
    data = request.json
    budget = float(data.get('budget')) if data.get('budget') else float('inf')
    produits_demandes = data.get('produits', {})
    
    suggestions = {}
    
    for categorie, dimensions in produits_demandes.items():
        largeur = float(dimensions.get('largeur', 0))
        hauteur = float(dimensions.get('hauteur', 0))
        profondeur = float(dimensions.get('profondeur', 0))
        
        produits_compatibles = Produit.query.filter(
            and_(
                Produit.categorie == categorie,
                Produit.largeur <= largeur,
                Produit.hauteur <= hauteur,
                Produit.profondeur <= profondeur,
                Produit.prix <= budget
            )
        ).order_by(
            (largeur - Produit.largeur) + 
            (hauteur - Produit.hauteur) + 
            (profondeur - Produit.profondeur)
        ).all()
        
        suggestions[categorie] = [{
            'id': p.id,
            'nom': p.nom,
            'prix': float(p.prix),
            'largeur': float(p.largeur),
            'hauteur': float(p.hauteur),
            'profondeur': float(p.profondeur)
        } for p in produits_compatibles]
    
    meilleures_suggestions = {}
    total = 0
    
    for categorie, produits in suggestions.items():
        if produits:
            meilleur_produit = produits[0]
            total += meilleur_produit['prix']
            
            if total <= budget:
                meilleures_suggestions[categorie] = [meilleur_produit]
            else:
                alternatives = [p for p in produits if p['prix'] <= (budget - (total - meilleur_produit['prix']))]
                if alternatives:
                    meilleures_suggestions[categorie] = [alternatives[0]]
                    total = total - meilleur_produit['prix'] + alternatives[0]['prix']
    
    return jsonify({
        'suggestions': meilleures_suggestions,
        'total': total
    })