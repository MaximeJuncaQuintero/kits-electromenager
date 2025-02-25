from app import app, db
from app.models import Produit

def seed_database():
    # Nettoyage des tables
    db.create_all()
    try:
        db.session.execute(db.text('TRUNCATE TABLE produits CASCADE'))
        db.session.commit()
    except Exception as e:
        print(f"Erreur lors du nettoyage: {e}")
        db.session.rollback()

    # RÉFRIGÉRATEURS
    refrigerateurs = [
        # Table-top (pour très petits espaces)
        Produit(
            nom="BEKO TSE1284N - Table-top 101L",
            categorie="frigo",
            prix=219.99,
            largeur=48.0,
            hauteur=84.0,
            profondeur=54.0
        ),
        Produit(
            nom="LIEBHERR TP1434 - Table-top 122L",
            categorie="frigo",
            prix=329.99,
            largeur=55.4,
            hauteur=85.0,
            profondeur=62.3
        ),
        # Une porte (différentes hauteurs)
        Produit(
            nom="BEKO RSSE415M23W - 1 porte 342L",
            categorie="frigo",
            prix=399.99,
            largeur=54.5,
            hauteur=146.0,
            profondeur=60.0
        ),
        Produit(
            nom="BOSCH KSV29VLEP - 1 porte 290L",
            categorie="frigo",
            prix=599.99,
            largeur=56.0,
            hauteur=161.0,
            profondeur=65.0
        ),
        # Doubles-portes
        Produit(
            nom="HAIER HDR3619FNMN - Double-portes 360L",
            categorie="frigo",
            prix=549.99,
            largeur=59.5,
            hauteur=190.5,
            profondeur=65.5
        ),
        Produit(
            nom="SAMSUNG RT32K5000S9 - Double-portes 321L",
            categorie="frigo",
            prix=499.99,
            largeur=60.2,
            hauteur=171.5,
            profondeur=66.8
        ),
        # Combinés (différentes profondeurs)
        Produit(
            nom="BEKO RCNA366K40WN - Combiné 324L",
            categorie="frigo",
            prix=469.99,
            largeur=59.5,
            hauteur=185.3,
            profondeur=59.8
        ),
        Produit(
            nom="SAMSUNG RB34T602EWW - Combiné 340L",
            categorie="frigo",
            prix=649.99,
            largeur=59.5,
            hauteur=185.3,
            profondeur=65.8
        ),
        # Américains (grands espaces)
        Produit(
            nom="LG GSL561PZZE - Américain 601L",
            categorie="frigo",
            prix=1299.99,
            largeur=91.2,
            hauteur=179.0,
            profondeur=71.7
        ),
        Produit(
            nom="SAMSUNG RS68A8522S9 - Américain 634L",
            categorie="frigo",
            prix=1199.99,
            largeur=91.2,
            hauteur=178.0,
            profondeur=71.6
        )
    ]

    # LAVE-LINGE
    lave_linges = [
        # Ultra-compact
        Produit(
            nom="CANDY SmartPro CST360L-S - 6kg",
            categorie="lave-linge",
            prix=279.99,
            largeur=46.5,
            hauteur=69.5,
            profondeur=43.5
        ),
        # Compact
        Produit(
            nom="CANDY AQUA1042DE/2-47 - 4kg",
            categorie="lave-linge",
            prix=299.99,
            largeur=51.0,
            hauteur=69.0,
            profondeur=44.0
        ),
        # Standard (différentes profondeurs)
        Produit(
            nom="BOSCH WAN28238FF - 8kg",
            categorie="lave-linge",
            prix=549.99,
            largeur=59.8,
            hauteur=84.8,
            profondeur=60.0
        ),
        Produit(
            nom="SAMSUNG WW90T534DTW - 9kg",
            categorie="lave-linge",
            prix=599.99,
            largeur=60.0,
            hauteur=85.0,
            profondeur=55.0
        ),
        # Grande capacité
        Produit(
            nom="LG F24V9BSTA - 12kg",
            categorie="lave-linge",
            prix=899.99,
            largeur=60.0,
            hauteur=85.0,
            profondeur=65.0
        ),
        # Chargement par le haut
        Produit(
            nom="WHIRLPOOL TDLR7220FR - 7kg Top",
            categorie="lave-linge",
            prix=399.99,
            largeur=40.0,
            hauteur=90.0,
            profondeur=60.0
        ),
        Produit(
            nom="VEDETTE VT602B - 6kg Top",
            categorie="lave-linge",
            prix=329.99,
            largeur=40.0,
            hauteur=85.0,
            profondeur=60.0
        )
    ]

    # Plaques de cuisson (différentes tailles et technologies)
    plaques_cuisson = [
        # 2 zones (petit espace)
        Produit(
            nom="BRANDT BPI6210B - Induction 2 zones",
            categorie="plaque",
            prix=199.99,
            largeur=29.0,
            hauteur=5.1,
            profondeur=52.0
        ),
        # 3 zones
        Produit(
            nom="SAUTER SPI6300W - Induction 3 zones",
            categorie="plaque",
            prix=299.99,
            largeur=45.0,
            hauteur=5.4,
            profondeur=51.0
        ),
        # 4 zones standards
        Produit(
            nom="BOSCH PUE611BF1E - Induction 4 zones",
            categorie="plaque",
            prix=399.99,
            largeur=59.2,
            hauteur=5.1,
            profondeur=52.2
        ),
        Produit(
            nom="WHIRLPOOL AKT8090NE - Vitrocéramique 4 zones",
            categorie="plaque",
            prix=249.99,
            largeur=58.0,
            hauteur=4.9,
            profondeur=51.0
        ),
        # 5 zones (grand espace)
        Produit(
            nom="SIEMENS EX875LYE3E - Induction 5 zones FlexInduction",
            categorie="plaque",
            prix=899.99,
            largeur=81.2,
            hauteur=5.1,
            profondeur=52.0
        )
    ]

    # Fours (différentes capacités et systèmes d'ouverture)
    fours = [
        # Compact
        Produit(
            nom="BOSCH CMG633BS1 - Compact multifonction",
            categorie="four",
            prix=899.99,
            largeur=59.5,
            hauteur=45.5,
            profondeur=54.8
        ),
        # Standard
        Produit(
            nom="WHIRLPOOL AKP738IX - Catalyse",
            categorie="four",
            prix=299.99,
            largeur=59.5,
            hauteur=59.5,
            profondeur=56.4
        ),
        Produit(
            nom="ELECTROLUX EOD3C50TX - Catalyse",
            categorie="four",
            prix=449.99,
            largeur=59.4,
            hauteur=59.4,
            profondeur=56.7
        ),
        # Grande capacité
        Produit(
            nom="BOSCH HBA573BR1 - Pyrolyse 71L",
            categorie="four",
            prix=599.99,
            largeur=59.5,
            hauteur=59.5,
            profondeur=54.8
        ),
        # Porte latérale
        Produit(
            nom="SIEMENS HB578A0S6 - Pyrolyse porte latérale",
            categorie="four",
            prix=899.99,
            largeur=59.5,
            hauteur=59.5,
            profondeur=54.8
        )
    ]

    # Lave-vaisselle (différentes capacités)
    lave_vaisselles = [
        # Ultra compact
        Produit(
            nom="BOSCH SKS51E32EU - 6 couverts pose libre",
            categorie="lave-vaisselle",
            prix=349.99,
            largeur=45.0,
            hauteur=45.0,
            profondeur=55.0
        ),
        # Compact
        Produit(
            nom="CANDY CDCP8/E-S - 8 couverts",
            categorie="lave-vaisselle",
            prix=299.99,
            largeur=55.0,
            hauteur=59.0,
            profondeur=50.0
        ),
        # Standard
        Produit(
            nom="BOSCH SMS2ITW45E - 12 couverts",
            categorie="lave-vaisselle",
            prix=499.99,
            largeur=60.0,
            hauteur=84.5,
            profondeur=60.0
        ),
        Produit(
            nom="WHIRLPOOL WFC3C24PF - 14 couverts",
            categorie="lave-vaisselle",
            prix=399.99,
            largeur=60.0,
            hauteur=85.0,
            profondeur=59.0
        ),
        # Grande capacité
        Produit(
            nom="SIEMENS SN258W00ME - 14 couverts A+++",
            categorie="lave-vaisselle",
            prix=699.99,
            largeur=60.0,
            hauteur=84.5,
            profondeur=60.0
        )
    ]

    # Ajout de tous les produits
    tous_les_produits = (refrigerateurs + lave_linges + 
                        plaques_cuisson + fours + lave_vaisselles)
    
    for produit in tous_les_produits:
        db.session.add(produit)
    
    db.session.commit()
    print(f"Base de données peuplée avec {len(tous_les_produits)} produits!")

if __name__ == "__main__":
    with app.app_context():
        seed_database() 