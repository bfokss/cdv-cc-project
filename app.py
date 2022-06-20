from flask import render_template, request, redirect, url_for
import pandas as pd
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

    return render_template('main/index.html', userData=userData, userFirstRow=userFirstRow, isTraining=isTraining, userTrainings=userTrainings)


if __name__ == '__main__':
    app.run(debug=True)