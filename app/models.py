from app import db
from datetime import datetime

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

class Kit(db.Model):
    __tablename__ = 'kits'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type_logement = db.Column(db.String(50))
    prix_total = db.Column(db.DECIMAL(10,2), nullable=False)
    
    # Relations
    produits = db.relationship('Produit', secondary='kit_produits')

# Table d'association pour Kit-Produit
kit_produits = db.Table('kit_produits',
    db.Column('kit_id', db.Integer, db.ForeignKey('kits.id'), primary_key=True),
    db.Column('produit_id', db.Integer, db.ForeignKey('produits.id'), primary_key=True)
)

class Intervention(db.Model):
    __tablename__ = 'interventions'
    id = db.Column(db.Integer, primary_key=True)
    kit_id = db.Column(db.Integer, db.ForeignKey('kits.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))  # 'installation', 'maintenance', 'reparation'
    description = db.Column(db.Text)
    statut = db.Column(db.String(20))  # 'planifié', 'en_cours', 'terminé'