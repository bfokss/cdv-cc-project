from project import app, db, api
from flask import render_template
from flask_restful import Resource, reqparse, abort
from project.models import User, Card, Event
import pandas as pd
from datetime import datetime

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

        try:
            log_time_parsed = datetime.strptime(log_time, '%Y-%m-%d %H:%M:%S.%f')
            log_time_parsed = log_time_parsed.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            abort(400, message='wrong log_time format. Was expecting YYYY-MM-DD HH:MM:SS.ff')

        if event_type not in ('start', 'stop'):
            abort(400, message='event_type must be either start or stop')

        card_exists = Card.query.filter_by(id=card_id).first()
        if not card_exists:
            abort(400, message='card must be in the database')

        new_event = Event(log_time=log_time_parsed, event_type=event_type, card_id=card_id)
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