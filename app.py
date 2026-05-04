from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfigurácia databázy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Statické dáta (presunuté z druhého súboru)
students_db = {
    "students": [
        {"id": 1, "name": "Matus", "surname": "Bucko", "nickname": "NEON1X", "photo": "https://i.pravatar.cc/300?u=1"},
        {"id": 2, "name": "Samo", "surname": "Haring", "nickname": "Topikar", "photo": "https://i.pravatar.cc/300?u=2"},
        # ... pridaj ostatných študentov sem ...
    ]
}

# Model databázy pre správy
class Sprava(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obsah = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# --- CESTY PRE WEB (HTML) ---
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

# --- CESTY PRE API (JSON) ---
@app.route("/api")
def api():
    return jsonify(students_db)

@app.route('/api/student/<int:student_id>')
def find_student(student_id):
    for student in students_db["students"]:
        if student["id"] == student_id:
            return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
