# Service secondaire : gestion des cotes (grades_service.py)
from flask import Flask, request, jsonify

app = Flask(__name__)

students_grades = {}

@app.route('/init_student', methods=['POST'])
def init_student():
    data = request.json
    students_grades[data['id']] = {'name': data['name'], 'grades': []}
    return jsonify({'message': f"Espace notes créé pour {data['name']}"})

@app.route('/add_grade/<int:student_id>', methods=['POST'])
def add_grade(student_id):
    data = request.json
    if student_id in students_grades:
        students_grades[student_id]['grades'].append(data['grade'])
        return jsonify({'message': 'Note ajoutée'})
    return jsonify({'error': 'Etudiant non trouvé'}), 404

@app.route('/get_grades/<int:student_id>', methods=['GET'])
def get_grades(student_id):
    if student_id in students_grades:
        return jsonify(students_grades[student_id])
    return jsonify({'error': 'Etudiant non trouvé'}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
