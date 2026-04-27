from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfigurácia databázy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model databázy
class Sprava(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obsah = db.Column(db.String(200), nullable=False)

# Vytvorenie databázy (pri prvom spustení)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nova_sprava = request.form.get('content')
        if nova_sprava:
            db.session.add(Sprava(obsah=nova_sprava))
            db.session.commit()
        return redirect('/')
    
    vsetky_spravy = Sprava.query.all()
    return render_template('index.html', spravy=vsetky_spravy)

if __name__ == "__main__":
    app.run(debug=True)
