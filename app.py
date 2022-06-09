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

    return render_template('index.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)