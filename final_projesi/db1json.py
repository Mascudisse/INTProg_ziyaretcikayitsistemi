from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Modelin (aynı şekilde)

class User(db.Model): 
    id =db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    name = db.Column(db.String(100), nullable=False) #name=form ıcındekı degerı al ve gonder
    email = db.Column(db.String(100), unique=True, nullable=False) #email verisi
    password = db.Column(db.String(100), nullable=False) #password verısı


def export_users_to_json():
    with app.app_context():
        users =User.query.all()
        data = []
        for user in users:
            data.append({
                 'id': user.id,
                'name': user.name,
                'email': user.email,
                'password': user.password    # şifreler hashli şekilde yazılır
            })
            with open('users.json','w',encoding='utf-8') as file:
                json.dump(data,file, ensure_ascii=False, indent=4)


                print('kullancilar başarli ile user.json dosyasina  kaydedildi !!!!!')

if __name__  == '__main__':
    export_users_to_json()