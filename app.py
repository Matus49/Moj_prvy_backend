from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Sprava(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obsah = db.Column(db.String(200), nullable=False)


databaza_studentov = [
    {"id": 1, "name": "Matus", "surname": "Bucko", "nickname": "NEON1X", "photo": "https://www.1day.sk/jagermeister-35-0-7l", "role": "Carry"},
    {"id": 2, "name": "Samo", "surname": "Haring", "nickname": "Topikar", "photo": "https://www.youtube.com/watch?v=IVX6pUeKCqc", "role": "Support"},
    {"id": 3, "name": "Milan", "surname": "Kokina", "nickname": "RED BULL", "photo": "https://en.wikipedia.org/wiki/Red_Bull", "role": "Jungler"},
    {"id": 4, "name": "Matej", "surname": "Randziak", "nickname": "Tankista", "photo": "https://wiki.warthunder.com/unit/ussr_t_34_85_zis_53", "role": "Tank"},
    {"id": 5, "name": "Janka", "surname": "Vargova", "nickname": "Dzejna", "photo": "https://cl.pinterest.com/jota_zzz87/hatsune-miku/", "role": "Mage"},
    {"id": 6, "name": "Martin", "surname": "Jelinek", "nickname": "Jeliman", "photo": "https://x.com/PetrosKecyaPoli/status/1249059078363627522", "role": "Duelist"},
    {"id": 7, "name": "Markus", "surname": "Martis", "nickname": "Markus", "photo": "https://lingolandedu.com/en/english-english-dictionary/jew", "role": "Initiator"},
    {"id": 8, "name": "Adrian", "surname": "Cervenka", "nickname": "Ado", "photo": "https://www.reddit.com/r/formuladank/comments/1new964/proud_gooner/", "role": "Controller"},
    {"id": 9, "name": "Tomas", "surname": "Jurcak", "nickname": "Jurcacik", "photo": "https://www.ferex.sk/detail/velkokapacitny-kontajner-zatvoreny-7-m3", "role": "Flanker"},
    {"id": 10, "name": "Marko", "surname": "Mihalicka", "nickname": "Maro", "photo": "https://www.teraz.sk/sport/hk-nitra-zvitazili-v-zapase-s-hkm-zvo/911092-clanok.html", "role": "Entry Fragger"},
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
    

    sort_by = request.args.get('sort_by', 'id')
    

    studenti_na_zobrazenie = databaza_studentov.copy()

    if sort_by in ['name', 'surname', 'nickname']:
        n = len(studenti_na_zobrazenie)

        for i in range(n):
            for j in range(0, n - i - 1):

                if studenti_na_zobrazenie[j][sort_by].lower() > studenti_na_zobrazenie[j + 1][sort_by].lower():

                    studenti_na_zobrazenie[j], studenti_na_zobrazenie[j + 1] = studenti_na_zobrazenie[j + 1], studenti_na_zobrazenie[j]

    vsetky_spravy = Sprava.query.all()

    return render_template('index.html', students=studenti_na_zobrazenie, spravy=vsetky_spravy, aktualne_radenie=sort_by)

@app.route('/api/student/<int:student_id>')
def find_student(student_id):
    student = next((s for s in databaza_studentov if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
