from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ziyaretci_ekle')
def ziyaretci_ekle():
    return render_template("ziyaretci_ekle.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/iletesim')
def iletesim():
    return render_template("iletesim.html")
@app.route('/hakkimizda')
def hakkimizda():
    return render_template("/hakkimizda.html")

@app.route('/ziyaretci_duzenle')
def ziyaretci_duzenle(id):
    return render_template("ziyaretci_duzenle.html")


if __name__== '__main__':
    app.run(debug=True)