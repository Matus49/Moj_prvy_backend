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

# sprav program aby fungoval nech funguje vyhladavanie
