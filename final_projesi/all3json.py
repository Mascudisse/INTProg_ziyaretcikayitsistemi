from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# modeller
class User(UserMixin, db.Model): 
    id =db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 

class ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    ad = db.Column(db.String(20), nullable=False)
    tarih = db.Column(db.Date, default=datetime.utcnow)
    kategori = db.Column(db.String(50), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('ziyaretciler', lazy=True))

    

# JSON'a aktarım fonksiyonu

def export_all_to_json():
    with app.app_context():
        users = User.query.all()
        data = []
        for user in users:
            user_data ={
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'ziyaretciler': []
            }
            for ziyaretci in user.ziyaretciler:
                ziyaretci_data = {
                    'id' :ziyaretci.id,
                    'ad': ziyaretci.ad,
                    "tarih":ziyaretci.tarih.isoformat(),  # Otomatik tarih
                    'kategori': ziyaretci.kategori,
                    'icerik': ziyaretci.icerik,

                }
                user_data['ziyaretciler'].append(ziyaretci_data)

            data.append(user_data)

            with open('kullanicilar_ve_ziyaretciler.json', 'w', encoding='utf-8') as file:
                 json.dump(data, file, ensure_ascii=False, indent=4)

            print("Veriler başariyla kullanicilar_ve_ziyaretciler.json dosyasina kaydedildi!!!!!!!")


if __name__ == '__main__':
    export_all_to_json()