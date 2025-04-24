# Flask app principale : Service d'inscription (registration_service.py)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
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
    response = requests.post('http://localhost:5001/init_student', json={'id': student.id, 'name': student.name})
    return jsonify({'status': 'notification envoyée', 'grades_response': response.json()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)