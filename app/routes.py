from flask import render_template, request, jsonify, redirect, url_for
from app import app, db
from app.models import Kit, Produit

@app.route('/')
def index():
    """Redirection vers la liste des kits"""
    return redirect(url_for('liste_kits'))

@app.route('/kits')
def liste_kits():
    """Affiche les kits disponibles par type de logement"""
    kits = Kit.query.all()
    return render_template('kits/liste.html', kits=kits)

@app.route('/kits/configurateur')
def configurateur():
    """Interface pour configurer un kit selon les dimensions"""
    return render_template('kits/configurateur.html')

@app.route('/api/produits/dimensions', methods=['POST'])
def verifier_dimensions():
    """API pour vérifier la compatibilité des produits"""
    dimensions = request.json
    produits_compatibles = Produit.query.filter(
        Produit.largeur <= dimensions['largeur'],
        Produit.hauteur <= dimensions['hauteur'],
        Produit.profondeur <= dimensions['profondeur']
    ).all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'dimensions': f"{p.largeur}x{p.hauteur}x{p.profondeur}"
    } for p in produits_compatibles])