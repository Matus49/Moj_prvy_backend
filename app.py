from flask import Flask, jsonify, request

app = Flask(__name__)

databaza = {
    "students": [
    {    
        "id":1,
        "name":"Matus",
        "surname":"Bucko",
        "nickname":"NEON1X",
        "photo":"https://i.pravatar.cc/300?u=1",
    },
    {
        "id":2,
        "name":"Samo",
        "surname":"Haring",
        "nickname":"Topikar",
        "photo":"https://i.pravatar.cc/300?u=2",
    },
    {
        "id":3,
        "name":"Milan",
        "surname":"Kokina",
        "nickname":"RED BULL",
        "photo":"https://i.pravatar.cc/300?u=3",
    },
    {
        "id":4,
        "name":"Matej",
        "surname":"Randziak",
        "nickname":"Tankista",
        "photo":"https://i.pravatar.cc/300?u=4",

    },
    {
        "id":5,
        "name":"Janka",
        "surname":"Vargova",
        "nickname":"Dzejna",
        "photo":"https://i.pravatar.cc/300?u=5",

    },
    {
        "id":6,
        "name":"Martin",
        "surname":"Jelinek",
        "nickname":"",
        "photo":"https://i.pravatar.cc/300?u=6",
    

    },
        {
        "id":7,
        "name":"Markus",
        "surname":"Martis",
        "nickname":"Zid",
        "photo":"https://i.pravatar.cc/300?u=7",
    

    },
        {
        "id":8,
        "name":"Adrian",
        "surname":"Cervenka",
        "nickname":"Valorant Enjoyer",
        "photo":"https://i.pravatar.cc/300?u=8",
    

    },
        {
        "id":9,
        "name":"Tomas",
        "surname":"Jurcak",
        "nickname":"Jurcacik",
        "photo":"https://i.pravatar.cc/300?u=9",
    

    },
        {
        "id":10,
        "name":"Marko",
        "surname":"Mihalicka",
        "nickname":"Jiggler",
        "photo":"https://i.pravatar.cc/300?u=10",
    

    },
    ]
}
@app.route("/api")
def api():
    return jsonify((databaza))
    
# 1. Jednoduchý GET endpoint
@app.route('/api/student/int:student_id>')
def find_student(student_id):
    for student in databaza["students"]:
        if student["id"] == student_id:
            return jsonify(student)

    student = databaza["students"][student_id - 1]
    return jsonify(student),


if __name__ == '__main__':
    app.run(debug=True)



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
