import unittest
from app import app, db
from app.models import Kit, Produit

class TestMVP(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/kits_test_db'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_liste_kits(self):
        response = self.client.get('/kits')
        self.assertEqual(response.status_code, 200)

    def test_configurateur(self):
        dimensions = {
            'largeur': 60,
            'hauteur': 170,
            'profondeur': 60
        }
        response = self.client.post('/api/produits/dimensions', 
                                json=dimensions)
        self.assertEqual(response.status_code, 200)

    def test_creation_kit(self):
        with app.app_context():
            kit = Kit(nom="Kit Studio", type_logement="Studio", prix_total=1500.00)
            db.session.add(kit)
            db.session.commit()
            self.assertIsNotNone(kit.id)

    def test_creation_produit(self):
        with app.app_context():
            produit = Produit(
                nom="Réfrigérateur A++",
                categorie="frigo",
                prix=500.00,
                largeur=60.00,
                hauteur=150.00,
                profondeur=60.00
            )
            db.session.add(produit)
            db.session.commit()
            self.assertIsNotNone(produit.id)

    def test_association_kit_produit(self):
        with app.app_context():
            kit = Kit(nom="Kit Test", type_logement="Studio", prix_total=700.00)
            produit = Produit(
                nom="Test Frigo",
                categorie="frigo",
                prix=500.00,
                largeur=60.00,
                hauteur=150.00,
                profondeur=60.00
            )
            db.session.add(kit)
            db.session.add(produit)
            kit.produits.append(produit)
            db.session.commit()
            
            kit_from_db = Kit.query.get(kit.id)
            self.assertEqual(len(kit_from_db.produits), 1)
            self.assertEqual(kit_from_db.produits[0].nom, "Test Frigo")