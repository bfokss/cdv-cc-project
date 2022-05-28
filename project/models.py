from project import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', backref="users", lazy=True, uselist=False)

    def __repr__(self):
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, cards={self.cards})'

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'Card(id={self.id}, user_id={self.user_id}'