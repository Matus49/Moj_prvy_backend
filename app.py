from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfigurácia databázy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model pre správy
class Sprava(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obsah = db.Column(db.String(200), nullable=False)

# Databáza študentov (hardcoded pre zobrazenie)
databaza_studentov = [
    {"id": 1, "name": "Matus", "surname": "Bucko", "nickname": "NEON1X", "photo": "https://i.pravatar.cc/300?u=1", "role": "Carry"},
    {"id": 2, "name": "Samo", "surname": "Haring", "nickname": "Topikar", "photo": "https://i.pravatar.cc/300?u=2", "role": "Support"},
    {"id": 3, "name": "Milan", "surname": "Kokina", "nickname": "RED BULL", "photo": "https://i.pravatar.cc/300?u=3", "role": "Jungler"},
    {"id": 4, "name": "Matej", "surname": "Randziak", "nickname": "Tankista", "photo": "https://i.pravatar.cc/300?u=4", "role": "Tank"},
    {"id": 5, "name": "Janka", "surname": "Vargova", "nickname": "Dzejna", "photo": "https://i.pravatar.cc/300?u=5", "role": "Mage"},
    {"id": 6, "name": "Martin", "surname": "Jelinek", "nickname": "Maťo", "photo": "https://i.pravatar.cc/300?u=6", "role": "Duelist"},
    {"id": 7, "name": "Markus", "surname": "Martis", "nickname": "Zid", "photo": "https://i.pravatar.cc/300?u=7", "role": "Initiator"},
    {"id": 8, "name": "Adrian", "surname": "Cervenka", "nickname": "Valorant Enjoyer", "photo": "https://i.pravatar.cc/300?u=8", "role": "Controller"},
    {"id": 9, "name": "Tomas", "surname": "Jurcak", "nickname": "Jurcacik", "photo": "https://i.pravatar.cc/300?u=9", "role": "Flanker"},
    {"id": 10, "name": "Marko", "surname": "Mihalicka", "nickname": "Jiggler", "photo": "https://i.pravatar.cc/300?u=10", "role": "Entry Fragger"},
]

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
    
    # --- LOGIKA ZORADZOVANIA ---
    # Získame parameter 'sort_by' z URL (napr. /?sort_by=name)
    sort_by = request.args.get('sort_by', 'id') # Predvolene podľa ID
    
    # Vytvoríme kópiu pôvodného zoznamu, aby sme ho nemenili globálne
    studenti_na_zobrazenie = databaza_studentov.copy()

    # Skontrolujeme, či chceme radiť podľa textových stĺpcov
    if sort_by in ['name', 'surname', 'nickname']:
        n = len(studenti_na_zobrazenie)
        # IMPLEMENTÁCIA TVOJHO BUBBLE SORTU (upravená pre slovníky a malé písmená)
        for i in range(n):
            for j in range(0, n - i - 1):
                # .lower() zabezpečí správne abecedné radenie bez ohľadu na veľkosť písmen
                if studenti_na_zobrazenie[j][sort_by].lower() > studenti_na_zobrazenie[j + 1][sort_by].lower():
                    # Výmena prvkov na základe tvojej logiky
                    studenti_na_zobrazenie[j], studenti_na_zobrazenie[j + 1] = studenti_na_zobrazenie[j + 1], studenti_na_zobrazenie[j]

    vsetky_spravy = Sprava.query.all()
    # Do šablóny posielame manuálne zoradený zoznam
    return render_template('index.html', students=studenti_na_zobrazenie, spravy=vsetky_spravy, aktualne_radenie=sort_by)

@app.route('/api/student/<int:student_id>')
def find_student(student_id):
    student = next((s for s in databaza_studentov if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
