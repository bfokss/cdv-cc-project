from Config import CONNECTION_STRING

import logging
import azure.functions as func
from sqlalchemy import create_engine, text


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

            last_event_type = connection.execute(text(f"select event_type from events order by log_time desc")).first()

            if len(last_event_type) == 0 or last_event_type[0] == 'stop':
                new_event_type = 'start'
            elif last_event_type[0] == 'start':
                new_event_type = 'stop'
            else:
                return func.HttpResponse("Unknown last event type", 500)

            connection.execute(text(f"insert into events values ('{log_time}', '{new_event_type}', '{card_id}')"))
            return func.HttpResponse(f"Inserted the row with values: {log_time}, '{new_event_type}', {card_id}", status_code=200)

    except Exception as e:
        logging.error(e)
        return func.HttpResponse(f"Error while trying to connect to db: {e})", status_code=500)