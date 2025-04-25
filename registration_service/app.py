# Flask app principale : Service d'inscription (registration_service.py)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'students.db')
db = SQLAlchemy(app)

# Modèle étudiant
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    has_paid = db.Column(db.Boolean, default=False)

# Créer la base
with app.app_context():
    db.create_all()

# Enregistrement de l'étudiant
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_student = Student(name=data['name'], email=data['email'])
    db.session.add(new_student)
    db.session.commit()
    notify_grades_service(new_student.id)  # Appel à la notification du service des cotes
    return jsonify({'message': 'Etudiant enregistré avec succès', 'id': new_student.id}), 201

# Confirmation du paiement
@app.route('/pay/<int:student_id>', methods=['POST'])
def pay(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Etudiant non trouvé'}), 404
    student.has_paid = True
    db.session.commit()
    return jsonify({'message': 'Paiement confirmé'})

# Notification vers le service des cotes
@app.route('/notify_grades/<int:student_id>', methods=['POST'])
def notify_grades_service(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Etudiant non trouvé'}), 404
    try:
        response = requests.post('https://service-cotes-production.up.railway.app/init_student', json={'id': student.id, 'name': student.name})
    except requests.exceptions.RequestException as e:
        response = requests.post('http://localhost:5001/init_student', json={'id': student.id, 'name': student.name})
        
    if response.status_code != 200:
        return jsonify({'error': 'Erreur lors de la notification au service des cotes'}), 500
    
    return jsonify({'status': 'notification envoyée', 'grades_response': response.json()})

# Récupérer tous les étudiants inscrits
@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    students_list = [{'id': student.id, 'name': student.name, 'email': student.email, 'has_paid': student.has_paid} for student in students]
    return jsonify({'students': students_list})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)