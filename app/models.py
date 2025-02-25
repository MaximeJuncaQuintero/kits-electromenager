from app import db

class Produit(db.Model):
    __tablename__ = 'produits'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.DECIMAL(10,2), nullable=False)
    largeur = db.Column(db.DECIMAL(5,2))
    hauteur = db.Column(db.DECIMAL(5,2))
    profondeur = db.Column(db.DECIMAL(5,2))
    disponible = db.Column(db.Boolean, default=True)