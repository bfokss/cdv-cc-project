from project import app, db
from flask import render_template
from project.models import User, Card
import pandas as pd
from sqlalchemy import select

@app.route('/', methods=['GET'])
def index():
    query = select([
        User.id,
        User.first_name,
        User.last_name,
        Card.id.label('card_id')
    ]).join(Card, isouter=True)
    df = pd.read_sql(query, db.engine)
    return render_template('index.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)