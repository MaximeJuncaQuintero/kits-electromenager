from flask import render_template, request, jsonify, redirect, url_for, session
from app import app, db
from app.models import Produit, Kit, Intervention
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
    total_cost = 0
    
    for categorie, dimensions in produits_demandes.items():
        largeur = float(dimensions.get('largeur', 0))
        hauteur = float(dimensions.get('hauteur', 0))
        profondeur = float(dimensions.get('profondeur', 0))
        
        budget_restant = budget - total_cost
        
        produits_compatibles = Produit.query.filter(
            and_(
                Produit.categorie == categorie,
                Produit.largeur <= largeur,
                Produit.hauteur <= hauteur,
                Produit.profondeur <= profondeur,
                Produit.prix <= budget_restant
            )
        ).order_by(Produit.prix.desc()).all()
        
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
    
    # Sauvegarder les suggestions dans la session
    session['kit_suggestions'] = suggestions
    session['kit_total'] = total_cost
    
    return jsonify({
        'suggestions': suggestions,
        'total': total_cost
    })

@app.route('/dashboard')
def dashboard():
    """Affiche le tableau de bord du client"""
    try:
        # Récupérer le kit_id depuis l'URL ou prendre le premier kit
        kit_id = request.args.get('kit_id', type=int)
        
        # Récupérer tous les kits
        all_kits = Kit.query.all()
        
        if not all_kits:
            return redirect(url_for('configurateur'))
        
        # Organiser les kits par type de logement
        kits_by_type = {}
        types_logement = set()
        total_value = 0.0
        total_products = 0
        
        for k in all_kits:
            type_logement = k.type_logement or "Autre"
            if type_logement not in kits_by_type:
                kits_by_type[type_logement] = []
            kits_by_type[type_logement].append(k)
            types_logement.add(type_logement)
            
            # S'assurer que prix_total est un float et gérer le cas None
            try:
                if k.prix_total is not None:
                    prix = float(str(k.prix_total))
                else:
                    prix = 0.0
            except (ValueError, TypeError):
                prix = 0.0
                
            total_value += prix
            total_products += len(k.produits)
        
        # Calculer les économies totales (15% du total)
        total_savings = total_value * 0.15
        
        # Si kit_id est spécifié, prendre ce kit, sinon prendre le premier
        kit = Kit.query.get(kit_id) if kit_id else all_kits[0]
        
        # S'assurer que le prix total du kit sélectionné est aussi un float
        if kit and kit.prix_total:
            try:
                kit.prix_total = float(str(kit.prix_total))
            except (ValueError, TypeError):
                kit.prix_total = 0.0
        
        return render_template('dashboard.html',
                            kit=kit,
                            all_kits=all_kits,
                            types_logement=sorted(types_logement),
                            kits_by_type=kits_by_type,
                            total_value=total_value,
                            total_savings=total_savings,
                            total_products=total_products)

    except Exception as e:
        app.logger.error(f"Erreur dans le dashboard: {str(e)}")
        return "Une erreur s'est produite", 500

@app.route('/api/kits/<int:kit_id>', methods=['PUT'])
def update_kit(kit_id):
    """API pour mettre à jour un kit"""
    try:
        kit = Kit.query.get_or_404(kit_id)
        data = request.json
        
        if 'produits' in data:
            # Vérifier qu'il n'y a pas de doublons de catégorie
            categories_seen = set()
            new_products = []
            
            for produit_id in data['produits']:
                produit = Produit.query.get(produit_id)
                if produit:
                    if produit.categorie in categories_seen:
                        return jsonify({
                            'status': 'error',
                            'message': f'Un produit de la catégorie {produit.categorie} existe déjà dans ce kit'
                        }), 400
                    categories_seen.add(produit.categorie)
                    new_products.append(produit)
            
            # Si la validation passe, mettre à jour les produits
            kit.produits = new_products
            
            # Recalculer le prix total
            kit.prix_total = sum(p.prix for p in kit.produits)
        
        db.session.commit()
        return jsonify({'status': 'success'})
        
    except Exception as e:
        app.logger.error(f"Erreur lors de la mise à jour du kit: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

def calculate_savings(suggestions):
    """Calcule les économies réalisées par rapport à l'achat séparé"""
    total_prix = sum(p['prix'] for prods in suggestions.values() for p in prods)
    # Estimation des économies (20% par rapport à l'achat séparé)
    return round(total_prix * 0.2, 2)

kit = {
    'type_logement': str,
    'economies': float,
    'prix_total': float,
    'prix_leasing': float,
    'prix_abonnement': float,
    'produits': [{
        'nom': str,
        'dimensions': str,
        'classe_energie': str
    }]
}

@app.route('/api/produits')
def get_produits():
    """Récupérer les produits par catégorie"""
    categorie = request.args.get('categorie')
    if not categorie:
        return jsonify([])
    
    produits = Produit.query.filter_by(categorie=categorie).all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'categorie': p.categorie,
        'prix': float(p.prix),
        'largeur': float(p.largeur),
        'hauteur': float(p.hauteur),
        'profondeur': float(p.profondeur)
    } for p in produits])

@app.route('/api/kits/<int:kit_id>')
def get_kit(kit_id):
    """Récupérer les détails d'un kit"""
    kit = Kit.query.get_or_404(kit_id)
    return jsonify({
        'id': kit.id,
        'nom': kit.nom,
        'type_logement': kit.type_logement,
        'prix_total': float(kit.prix_total),
        'produits': [{
            'id': p.id,
            'nom': p.nom,
            'categorie': p.categorie,
            'prix': float(p.prix),
            'largeur': float(p.largeur),
            'hauteur': float(p.hauteur),
            'profondeur': float(p.profondeur)
        } for p in kit.produits]
    })