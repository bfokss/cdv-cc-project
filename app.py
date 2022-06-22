from flask import render_template, request, redirect, url_for
import pandas as pd
import re
from project import app, db
from project.models import User, Card, Event

USER_TRAININGS_LIMIT = 10


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def user_index():
    userId = request.args.get('id')

    userExists = db.session.query(User.id).filter_by(id=userId).first() is not None

    
    if ('id' not in request.args) or (not userExists):
        return redirect(url_for('index'))
    

    query = db.session.query(
        Event.log_time,
        Event.event_type,
        Event.card_id,
        Card.user_id,
        User.id,
        User.first_name,
        User.last_name
    ).select_from(Event).join(Card, full=True).join(User, full=True).filter(User.id==userId).order_by(Event.log_time.desc())

    data = query.all()
    userFirstRow = query.first()
    userData = pd.DataFrame(data)


    trainings = db.session.query(Event.log_time, Event.event_type, Card.user_id, User.first_name).select_from(Event).join(Card, full=True).join(User, full=True).filter(User.id==userId,Event.event_type=="start").order_by(Event.log_time.desc()).limit(USER_TRAININGS_LIMIT)
    userTrainings = pd.DataFrame(trainings)

    isTraining = userData['event_type'][0]=='start'

    return render_template('main/user/index_user.html', userData=userData, userFirstRow=userFirstRow, isTraining=isTraining, userTrainings=userTrainings)


@app.route('/users/list', methods=['GET'])
def user_list():
    users = db.session.query(
        Card.user_id,
        User.first_name,
        User.last_name,
        Card.id
    ).select_from(User).join(Card, full=True).all()
    usersData = pd.DataFrame(users)
    return render_template('main/user/list_users.html', usersData = usersData)


@app.route('/users/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'GET':
        return render_template('main/user/add_user.html')
    
    if request.method == 'POST':
        user_first_name = request.form['user_first_name']
        user_last_name = request.form['user_last_name']

        new_user = User(first_name = user_first_name, last_name = user_last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_list'))

@app.route('/users/assign', methods=['GET', 'POST'])
def user_assign():
    if request.method == 'GET':
        users = db.session.query(
            User.id,
            User.first_name,
            User.last_name
        ).select_from(User).all()

        cards = db.session.query(
            Card.id,
            Card.user_id
        ).select_from(Card).all()

        usersData = pd.DataFrame(users)
        cardsData = pd.DataFrame(cards)

        return render_template('main/user/assign_user.html', usersData=usersData, cardsData=cardsData)
    
    if request.method == 'POST':
        

        user_id = request.form['user_id']
        user_id = re.sub(r"[^\d]","",user_id)
        card_id = request.form['card_id']

        card = Card.query.filter_by(id=card_id).first()
        if card:
            card.user_id = user_id
            db.session.commit()

        return redirect(url_for('card_list'))

@app.route('/cards/list', methods=['GET'])
def card_list():
    cards = db.session.query(
        Card.id,
        Card.user_id,
        User.first_name,
        User.last_name,
    ).select_from(Card).join(User).all()
    cardsData = pd.DataFrame(cards)
    return render_template('main/card/list_cards.html', cardsData = cardsData)

@app.route('/cards/add', methods=['GET', 'POST'])
def card_add():
    if request.method == 'GET':
        users = db.session.query(
            User.id,
            User.first_name,
            User.last_name
        ).select_from(User).join(Card, full=True).filter_by(user_id=None).all()

        usersData = pd.DataFrame(users)

        return render_template('main/card/add_card.html', usersData=usersData)
    
    if request.method == 'POST':
        card_id = request.form['card_id']
        user_id = request.form['user_id']
        user_id = re.sub(r"[^\d]","",user_id)

        new_card = Card(id = card_id, user_id = user_id)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('card_list'))





if __name__ == '__main__':
    app.run(debug=True)