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
    total_cost = 0  # Pour tracker le coût total
    
    for categorie, dimensions in produits_demandes.items():
        largeur = float(dimensions.get('largeur', 0))
        hauteur = float(dimensions.get('hauteur', 0))
        profondeur = float(dimensions.get('profondeur', 0))
        
        # Budget restant pour ce produit
        budget_restant = budget - total_cost
        
        produits_compatibles = Produit.query.filter(
            and_(
                Produit.categorie == categorie,
                Produit.largeur <= largeur,
                Produit.hauteur <= hauteur,
                Produit.profondeur <= profondeur,
                Produit.prix <= budget_restant  # Utiliser le budget restant
            )
        ).order_by(Produit.prix.desc()).all()  # Prendre le meilleur produit dans le budget
        
        if produits_compatibles:
            produit = produits_compatibles[0]
            total_cost += float(produit.prix)
            suggestions[categorie] = [{
                'id': produit.id,
                'nom': produit.nom,
                'prix': float(produit.prix),
                'largeur': float(produit.largeur),
                'hauteur': float(produit.hauteur),
                'profondeur': float(produit.profondeur)
            }]
    
    return jsonify({
        'suggestions': suggestions,
        'total': total_cost
    })