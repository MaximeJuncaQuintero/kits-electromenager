from app import db
from sqlalchemy import DECIMAL

class Kit(db.Model):
    __tablename__ = 'kits'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type_logement = db.Column(db.String(50))
    prix_total = db.Column(DECIMAL(10,2), nullable=False)
    produits = db.relationship('Produit', secondary='kit_produits')

class Produit(db.Model):
    __tablename__ = 'produits'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    prix = db.Column(DECIMAL(10,2), nullable=False)
    largeur = db.Column(DECIMAL(5,2))
    hauteur = db.Column(DECIMAL(5,2))
    profondeur = db.Column(DECIMAL(5,2))
    disponible = db.Column(db.Boolean, default=True)

# Table d'association pour la relation many-to-many entre Kit et Produit
kit_produits = db.Table('kit_produits',
    db.Column('kit_id', db.Integer, db.ForeignKey('kits.id'), primary_key=True),
    db.Column('produit_id', db.Integer, db.ForeignKey('produits.id'), primary_key=True)
)