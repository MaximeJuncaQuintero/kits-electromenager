from flask import render_template, request, jsonify, redirect, url_for, session
from app import app, db
from app.models import Produit, Kit, Intervention
from sqlalchemy import and_, func
from decimal import Decimal

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

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
    try:
        # Récupérer le filtre d'appartement et l'ID du kit
        appartement_filter = request.args.get('appartement', 'all')
        kit_id = request.args.get('kit_id', type=int)
        
        # Récupérer tous les kits
        query = Kit.query
        if appartement_filter != 'all':
            query = query.filter(Kit.appartement == appartement_filter)
        all_kits = query.all()
        
        # Initialiser les statistiques
        total_value = Decimal('0')
        total_savings = Decimal('0')
        total_products = 0
        
        # Calculer les statistiques sur les kits filtrés
        for kit in all_kits:
            kit_price = Decimal(str(kit.prix_total)) if not isinstance(kit.prix_total, Decimal) else kit.prix_total
            total_value += kit_price
            total_savings += kit_price * Decimal('0.15')  # 15% d'économies
            total_products += len(kit.produits)

        # Récupérer les appartements uniques en utilisant une requête distincte
        appartements = [appart[0] for appart in db.session.query(Kit.appartement).distinct().filter(Kit.appartement != None).order_by(Kit.appartement).all()]
        
        # Récupérer le kit sélectionné
        selected_kit = None
        if kit_id:
            selected_kit = Kit.query.get(kit_id)
            if not selected_kit:
                return "Kit non trouvé", 404
        
        return render_template('dashboard.html',
                             all_kits=all_kits,
                             total_value=float(total_value),
                             total_savings=float(total_savings),
                             total_products=total_products,
                             appartements=appartements,
                             selected_appartement=appartement_filter,
                             kit=selected_kit,
                             Decimal=Decimal)
                             
    except Exception as e:
        app.logger.error(f"Erreur dans le dashboard: {str(e)}")
        return "Une erreur est survenue lors du chargement du dashboard", 500

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

@app.route('/api/kits/<int:kit_id>', methods=['DELETE'])
def supprimer_kit(kit_id):
    """Supprimer un kit"""
    try:
        kit = Kit.query.get_or_404(kit_id)
        db.session.delete(kit)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Kit supprimé avec succès'})
    except Exception as e:
        db.session.rollback()
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

@app.route('/api/kit/sauvegarder', methods=['POST'])
def sauvegarder_kit():
    """Sauvegarder un kit configuré"""
    try:
        data = request.json
        suggestions = session.get('kit_suggestions', {})
        
        if not suggestions:
            return jsonify({
                'status': 'error',
                'message': 'Aucun kit à sauvegarder'
            }), 400
        
        # Créer un nouveau kit
        nouveau_kit = Kit(
            nom=data.get('nom', 'Nouveau Kit'),
            appartement=data.get('appartement'),
            prix_total=Decimal(str(session.get('kit_total', 0)))
        )
        
        # Ajouter les produits au kit
        for categorie, produits in suggestions.items():
            for p in produits:
                produit = Produit.query.get(p['id'])
                if produit:
                    nouveau_kit.produits.append(produit)
        
        db.session.add(nouveau_kit)
        db.session.commit()
        
        # Vider la session
        session.pop('kit_suggestions', None)
        session.pop('kit_total', None)
        
        # Construire l'URL de redirection avec l'appartement
        redirect_url = url_for('dashboard', kit_id=nouveau_kit.id)
        if nouveau_kit.appartement:
            redirect_url = url_for('dashboard', kit_id=nouveau_kit.id, appartement=nouveau_kit.appartement)
        
        return jsonify({
            'status': 'success',
            'kit_id': nouveau_kit.id,
            'redirect_url': redirect_url,
            'message': 'Kit sauvegardé avec succès'
        })
        
    except Exception as e:
        app.logger.error(f"Erreur lors de la sauvegarde du kit: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500