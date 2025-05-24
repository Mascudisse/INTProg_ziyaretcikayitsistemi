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
    id =db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    name = db.Column(db.String(100), nullable=False) #name=form ıcındekı degerı al ve gonder
    email = db.Column(db.String(100), unique=True, nullable=False) #email verısı
    password = db.Column(db.String(100), nullable=False) #password verısı


class ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    ad = db.Column(db.String(20), nullable=False)
    tarih = db.Column(db.Date, default=datetime.utcnow)
    kategori = db.Column(db.String(50), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    user = db.relationship('User', backref=db.backref('ziyaretciler', lazy=True))

    # JSON'a aktarım fonksiyonu

def export_ziyaretciler_to_json():
    with app.app_context():
        ziyaretciler = ziyaretci.query.all()
        data = []
        for z in ziyaretciler:
            data.append({
                'id' : z.id,
                'ad': z.ad,
                'kategori': z.kategori,
                'icerik': z.icerik,
                'kullanici_id': z.kullanici_id,
                "tarih":z.tarih.isoformat(),  # Otomatik tarih
                'kullanici_adi': z.user.name if z.user else None

            })
            with open('ziyaretciler.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

                print("ziyaretciler başarıyla gunlukler.json dosyasına kaydedildi!")

# Ana fonksiyon
if __name__ =='__main__':
    export_ziyaretciler_to_json()

              
 