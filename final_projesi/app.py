from flask import Flask,render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # bu kutuphane sadece tarih ve saat  kayit ediyor 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari' #sesion bilgilerini tarayicida tutmak icin 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #database ne adina olucak
db= SQLAlchemy(app)

login_manager = LoginManager(app)  #kullanci gerekli bir sayfa mevcut ise :
login_manager.login_view = 'login'  #gereklı gıurıs ıcın hangı rota kullanılsın? logın rotasına gıt

class User(UserMixin, db.Model): 
    id =db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    name = db.Column(db.String(100), nullable=False) #name=form ıcındekı degerı al ve gonder
    email = db.Column(db.String(100), unique=True, nullable=False) #email verısı
    password = db.Column(db.String(100), nullable=False) #password verısı

     # ziyaretciler ile ilişkiyi  burada tanımlıyoruz:
    ziyaretciler = db.relationship('ziyaretci', back_populates='kullanici')


class ziyaretci(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    ad = db.Column(db.String(20), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)  # bu otomatik olarak  yaziyor gerekli kutuphaneler import ettim 
    kategori = db.Column(db.String(50), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        # Kullanıcıya ters  iliski 
              
    kullanici = db.relationship('User', back_populates='ziyaretciler')


@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('E-post veya sifre  hatali ! ', 'danger')
    return render_template("login.html")


@app.route('/register', methods=['GET' , 'POST'])
def register():
    if request.method =='POST':
        email = request.form.get('email') #regıster formundan gelen emaıl
        password = request.form.get('password') #regıster formundan gelen password
        
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger') #sayfa mesajları dondurme
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        name = request.form.get('name') 
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success') #sayfa mesajları dondurme
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/dashboard')
@login_required
def dashboard():
    ziyaretciler= ziyaretci.query.filter_by(kullanici_id=current_user.id).order_by(ziyaretci.id.desc()).all()
    return render_template('dashboard.html', ziyaretciler=ziyaretciler)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard/ziyaretci_ekle', methods=['GET' , 'POST'])
@login_required
def ziyaretci_ekle():
    if request.method == 'POST':
        ad= request.form.get('ad')
        icerik = request.form.get('icerik')
        kategori = request.form.get('kategori')

        
        # Kullanıcı girişi kontrolü 
        if current_user.is_authenticated:
             yeni_ziyaretci = ziyaretci(
                ad=ad,
                icerik=icerik,
                kategori=kategori,
                kullanici_id=current_user.id  # doğru kullanıcı ID'si
            )
             db.session.add(yeni_ziyaretci)
             db.session.commit()
             flash('Ziyaretçi başarıyla kaydedildi!', 'success')
             return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı girişi yapılmamış!', 'danger')
            return redirect(url_for('login'))
    
    return render_template("ziyaretci_ekle.html")

          #duzeltme islemler 
@app.route('/ziyaretci/duzenle/<int:ziyaretci_id>', methods=['GET', 'POST'])
@login_required
def ziyaretci_duzenle(ziyaretci_id):
    ziyaretci_kaydi = ziyaretci.query.get_or_404(ziyaretci_id)

        # Kullanıcı sadece kendi kayıtlarını düzenleyebilir
    if ziyaretci_kaydi.kullanici_id != current_user.id:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Formdan gelen değerler
        ziyaretci_kaydi.ad = request.form['ad']
        ziyaretci_kaydi.icerik = request.form['icerik']
        ziyaretci_kaydi.kategori = request.form['kategori']

        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template("ziyaretci_duzenle.html", ziyaretci=ziyaretci_kaydi)

            #silme islemler 

@app.route('/ziyaretci/sil/<int:ziyaretci_id>', methods=['POST'])
@login_required
def ziyaretci_sil(ziyaretci_id):
     ziyaretci_kaydi = ziyaretci.query.get_or_404(ziyaretci_id)
     
           # Kullanıcı sadece kendi kayıtlarını silebilmesi 
     if ziyaretci_kaydi.kullanici_id != current_user.id:
         flash('Bu kaydı silme yetkiniz yok!', 'danger')
         return render_template('dashboard')
     
     db.session.delete(ziyaretci_kaydi)
     db.session.commit()
     flash('Ziyaretçi kaydı silindi.', 'success')
     return redirect(url_for('dashboard'))

@app.route('/iletesim')
def iletesim():
    return render_template("iletesim.html")
@app.route('/hakkimizda')
def hakkimizda():
    return render_template("/hakkimizda.html")


#if __name__ == '__main__':
    #with app.app_context():
       # db.create_all()
   # app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

