import logging
from datetime import datetime

import azure.functions as func
from sqlalchemy import create_engine, text

from Config import CONNECTION_STRING


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Start request')

    try:
        req_body = req.get_json()
        log_time = req_body.get("log_time")
        card_id = req_body.get("card_id")

        if not log_time or not card_id:
            raise Exception("log_time or card_id not provided")
    except Exception as e:
        return func.HttpResponse(
            logging.error(e),
             f"Error when reading request's body: {e}",
             status_code=500
        )

    try:
        engine = create_engine(CONNECTION_STRING)
        with engine.connect() as connection:
            cards_found = connection.execute(text(f"select id from cards where id='{card_id}'")).all()

            if len(cards_found) == 0:
                return func.HttpResponse(f"Card not in the database", status_code=400)

            last_event = connection.execute(text(f"select log_time, event_type from events where card_id = '{card_id}' order by log_time desc")).first()
            last_event_type = None if last_event == None else last_event[1]
            print('last_event:', last_event)
            print('last_event_type:', last_event_type)

            # First event for card or last event was of type 'stop'
            if last_event_type == None or last_event_type == 'stop':
                new_event_type = 'start'
            
            # Last event was of type 'start'
            elif last_event_type == 'start':
                timestamp_format = '%Y-%m-%d %H:%M:%S'
                new_event_type = 'stop'
                start = last_event[0]
                finish = datetime.strptime(log_time, timestamp_format)
                time_delta = finish - start
                connection.execute(text(f"insert into trainings values ('{card_id}', '{start.strftime(timestamp_format)}', {time_delta.seconds})"))
                
            else:
                return func.HttpResponse("Unknown last event type", 500)

            connection.execute(text(f"insert into events values ('{log_time}', '{new_event_type}', '{card_id}')"))
            return func.HttpResponse(f"Inserted the row with values: {log_time}, '{new_event_type}', {card_id}", status_code=200)

    except Exception as e:
        logging.error(e)
        return func.HttpResponse(f"Error while accessing database: {e}", status_code=500)
