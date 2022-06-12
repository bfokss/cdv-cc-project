from flask import render_template
import pandas as pd

from project import app, db
from project.models import User, Card, Event
import project.api


@app.route('/', methods=['GET'])
def index():
    query = db.session.query(
        Event.log_time,
        Event.event_type,
        Event.card_id,
        Card.user_id,
        User.id,
        User.first_name,
        User.last_name
    ).select_from(Event).join(Card, full=True).join(User, full=True).order_by(Event.log_time.desc())
    data = query.all()
    df = pd.DataFrame(data)

    getUser = db.session.query(
        User.first_name,
    ).select_from(User).join(Card, full=True).order_by(Event.log_time.desc())

    activeSession = False

    #userQuery = db.session.query(User).join(Card, full=True).order_by(Event.log_time.desc()).slice(1,2)
    userData = query.first()
    lastStartUser = query.filter(Event.event_type=='start')
    print(lastStartUser)
    #print(userData)
    #print(activeSession)

    return render_template('home/index.html', df=df, user=userData, activeSession=activeSession)


if __name__ == '__main__':
    app.run(debug=True)