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
    events = db.relationship('Event', backref='events', lazy=True, uselist=True)
    
    def __repr__(self):
        return f'Card(id={self.id}, user_id={self.user_id})'

class Event(db.Model):
    __tablename__ = 'events'

    log_time = db.Column(db.DateTime, primary_key=True)
    event_type = db.Column(db.String(5), nullable=False)
    card_id = db.Column(db.String(20), db.ForeignKey('cards.id'), nullable=False)

    def __repr__(self):
        return f'Event(log_time={self.log_time}, event_type={self.event_type}, card_id={self.card_id})'

class Training(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(20), db.ForeignKey('cards.id'), nullable=False)
    shift_length = db.Column(db.Integer, nullable=False) # in seconds

    def __repr__(self):
        return f'Training(id={self.id}, card_id={self.card_id}, shift_length={self.shift_length})'
