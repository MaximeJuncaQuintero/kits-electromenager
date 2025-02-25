from app import app, db
from app.models import Kit, Produit

def seed_database():
    # Nettoyage des tables
    db.create_all()
    try:
        db.session.execute(db.text('TRUNCATE TABLE kit_produits CASCADE'))
        db.session.execute(db.text('TRUNCATE TABLE kits CASCADE'))
        db.session.execute(db.text('TRUNCATE TABLE produits CASCADE'))
        db.session.commit()
    except Exception as e:
        print(f"Erreur lors du nettoyage: {e}")
        db.session.rollback()

    # Création des produits avec données réelles
    refrigerateurs = [
        Produit(
            nom="BEKO RSSE415M23W",
            categorie="frigo",
            prix=399.99,
            largeur=54.5,
            hauteur=146.0,
            profondeur=60.0
        ),
        Produit(
            nom="SAMSUNG RB34T602EWW",
            categorie="frigo",
            prix=649.99,
            largeur=59.5,
            hauteur=185.3,
            profondeur=65.8
        ),
        Produit(
            nom="BOSCH KGN36VWED",
            categorie="frigo",
            prix=699.99,
            largeur=60.0,
            hauteur=186.0,
            profondeur=66.0
        )
    ]

    lave_linges = [
        Produit(
            nom="BOSCH WAN28238FF",
            categorie="lave-linge",
            prix=549.99,
            largeur=59.8,
            hauteur=84.8,
            profondeur=60.0
        ),
        Produit(
            nom="ELECTROLUX EW6F3914RA",
            categorie="lave-linge",
            prix=429.99,
            largeur=60.0,
            hauteur=85.0,
            profondeur=57.5
        ),
        Produit(
            nom="SAMSUNG WW90T534DTW",
            categorie="lave-linge",
            prix=599.99,
            largeur=60.0,
            hauteur=85.0,
            profondeur=55.0
        )
    ]

    plaques_cuisson = [
        Produit(
            nom="BOSCH PUE611BF1E",
            categorie="plaque",
            prix=399.99,
            largeur=59.2,
            hauteur=5.1,
            profondeur=52.2
        ),
        Produit(
            nom="SAUTER SPI4664B",
            categorie="plaque",
            prix=329.99,
            largeur=58.0,
            hauteur=5.4,
            profondeur=51.0
        )
    ]

    fours = [
        Produit(
            nom="BOSCH HBA573BR1",
            categorie="four",
            prix=599.99,
            largeur=59.5,
            hauteur=59.5,
            profondeur=54.8
        ),
        Produit(
            nom="ELECTROLUX EOD3C50TX",
            categorie="four",
            prix=449.99,
            largeur=59.4,
            hauteur=59.4,
            profondeur=56.7
        )
    ]

    lave_vaisselles = [
        Produit(
            nom="BOSCH SMS2ITW45E",
            categorie="lave-vaisselle",
            prix=499.99,
            largeur=60.0,
            hauteur=84.5,
            profondeur=60.0
        ),
        Produit(
            nom="ELECTROLUX ESF8650ROW",
            categorie="lave-vaisselle",
            prix=599.99,
            largeur=59.6,
            hauteur=85.0,
            profondeur=62.5
        )
    ]

    # Ajout des produits
    tous_les_produits = refrigerateurs + lave_linges + plaques_cuisson + fours + lave_vaisselles
    for produit in tous_les_produits:
        db.session.add(produit)
    db.session.commit()

    # Création des kits réalistes
    kit_studio = Kit(
        nom="Kit Studio Premium",
        type_logement="Studio 18-25m²",
        prix_total=1299.97
    )
    kit_studio.produits.extend([
        refrigerateurs[0],    # BEKO compact
        lave_linges[1],       # ELECTROLUX
        plaques_cuisson[1]    # SAUTER
    ])

    kit_t2 = Kit(
        nom="Kit T2 Confort+",
        type_logement="T2 30-45m²",
        prix_total=1999.96
    )
    kit_t2.produits.extend([
        refrigerateurs[1],    # SAMSUNG
        lave_linges[0],       # BOSCH
        plaques_cuisson[0],   # BOSCH
        fours[1]              # ELECTROLUX
    ])

    kit_t3 = Kit(
        nom="Kit T3 Excellence",
        type_logement="T3 50-65m²",
        prix_total=2849.95
    )
    kit_t3.produits.extend([
        refrigerateurs[2],     # BOSCH
        lave_linges[2],        # SAMSUNG
        plaques_cuisson[0],    # BOSCH
        fours[0],              # BOSCH
        lave_vaisselles[0]     # BOSCH
    ])

    kit_invest = Kit(
        nom="Kit Investisseur",
        type_logement="Studio/T1 LMNP",
        prix_total=1599.96
    )
    kit_invest.produits.extend([
        refrigerateurs[0],    # BEKO
        lave_linges[1],      # ELECTROLUX
        plaques_cuisson[1],  # SAUTER
        fours[1]             # ELECTROLUX
    ])

    # Ajout des kits
    db.session.add(kit_studio)
    db.session.add(kit_t2)
    db.session.add(kit_t3)
    db.session.add(kit_invest)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        seed_database()
        print("Base de données peuplée avec succès!") 