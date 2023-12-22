import requests
import os
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv('./.env')

app = Flask(__name__)

URL = os.environ['DB_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#required for database running
app.app_context().push()


class City(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
        
    def __init__(self, name):
        self.name = name



@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()


    cities = City.query.all()

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=6eed6a07c2f3b41dff16354b6597af03&units=metric'

    weather_data = []
    for city in cities:

        r = requests.get(url.format(city.name)).json()

        weather = {
            'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    print(weather_data)

    return render_template("weather.html",weather_data=weather_data)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)





















