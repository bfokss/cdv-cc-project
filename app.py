from project import app, db, api
from flask import render_template
from flask_restful import Resource, reqparse
from project.models import User, Card, Event
import pandas as pd

events_post_reqparse = reqparse.RequestParser()
events_post_reqparse.add_argument('log_time', type=str, help='log_time is required', location='json', required=True)
events_post_reqparse.add_argument('event_type', type=str, help='event_type is required', location='json', required=True)
events_post_reqparse.add_argument('card_id', type=str, help='card_id is required', location='json', required=True)


class EventApi(Resource):
    def post(self):
        args = events_post_reqparse.parse_args()
        log_time = args['log_time']
        event_type = args['event_type']
        card_id = args['card_id']

        new_event = Event(log_time=log_time, event_type=event_type, card_id=card_id)
        db.session.add(new_event)
        db.session.commit()

        return {'message': 'new event added'}, 201

api.add_resource(EventApi, '/api/events')


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