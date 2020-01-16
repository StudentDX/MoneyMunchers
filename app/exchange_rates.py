import urllib.request as request
from app.models import db, Exchanges
import json

url = 'https://api.exchangeratesapi.io/latest?base=USD'
req = request.Request(url)
data = json.loads(request.urlopen(req).read())

def update_rates():
    for entry in data['rates']:
        if entry in [e.currency for e in Exchanges.query.all()]:
            Exchanges.query.filter_by(currency=entry).rate = data['rates'][entry]
            db.session.commit()