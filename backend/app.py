from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from models import db, Patient
from algorithms.hospital_algorithms import fcfs, sjf, round_robin, priority_scheduling, srtf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-mediqueue-key'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/patient/register', methods=['POST'])
def register_patient():
    data = request.json
    new_patient = Patient(
        name=data.get('name'),
        arrival_time=data.get('arrival_time'),
        treatment_time=data.get('treatment_time'),
        emergency_level=data.get('emergency_level', 1)
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient registered", "patient": new_patient.to_dict()}), 201

@app.route('/queue/schedule', methods=['GET'])
def get_schedule():
    algorithm = request.args.get('algorithm', 'FCFS')
    
    # Get all patients that are waiting
    patients = Patient.query.filter_by(status='WAITING').all()
    
    if not patients:
        return jsonify({"gantt_chart": [], "processes": []})
        
    if algorithm == 'FCFS':
        completed, gantt = fcfs(patients)
    elif algorithm == 'SJF':
        completed, gantt = sjf(patients)
    elif algorithm == 'Priority':
        completed, gantt = priority_scheduling(patients)
    elif algorithm == 'Round Robin':
        completed, gantt = round_robin(patients, time_quantum=5) # 5 min default
    elif algorithm == 'SRTF':
        completed, gantt = srtf(patients)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400
        
    return jsonify({
        "algorithm": algorithm,
        "gantt_chart": gantt,
        "processes": [p.to_dict() for p in completed]
    })

@app.route('/metrics', methods=['GET'])
def get_metrics():
    # Return average metrics based on current schedule
    algorithm = request.args.get('algorithm', 'FCFS')
    patients = Patient.query.filter_by(status='WAITING').all()
    
    if not patients:
         return jsonify({"average_waiting_time": 0, "average_turnaround_time": 0})
         
    if algorithm == 'FCFS':
        completed, _ = fcfs(patients)
    elif algorithm == 'SJF':
        completed, _ = sjf(patients)
    elif algorithm == 'Priority':
        completed, _ = priority_scheduling(patients)
    elif algorithm == 'Round Robin':
        completed, _ = round_robin(patients)
    elif algorithm == 'SRTF':
        completed, _ = srtf(patients)
        
    total_wt = sum(p.waiting_time for p in completed)
    total_tat = sum(p.turnaround_time for p in completed)
    n = len(completed)
    
    return jsonify({
        "algorithm": algorithm,
        "average_waiting_time": round(total_wt / n, 2),
        "average_turnaround_time": round(total_tat / n, 2),
        "total_patients": n
    })

@app.route('/recommend', methods=['GET'])
def recommend_algorithm():
    patients = Patient.query.filter_by(status='WAITING').all()
    if not patients:
        return jsonify({"recommendation": "FCFS", "reason": "Queue is empty."})
        
    critical_count = sum(1 for p in patients if p.emergency_level >= 4)
    avg_treatment = sum(p.treatment_time for p in patients) / len(patients)
    
    if critical_count > 0:
        rec = "Priority"
        reason = f"There are {critical_count} critical emergencies. Priority scheduling with Aging is required."
    elif avg_treatment > 15:
        rec = "Round Robin"
        reason = "Long average treatment times detected. Round Robin ensures fairness."
    else:
        rec = "SJF"
        reason = "Queue mostly has short treatments. SJF will minimize average waiting time."
        
    return jsonify({"recommendation": rec, "reason": reason})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', '')).strip()

    # Hardcoded mock users for demonstration
    users = {
        "admin": {"password": "admin123", "role": "Administrator"},
        "doctor": {"password": "doctor123", "role": "Head Doctor"},
        "receptionist": {"password": "rec123", "role": "Front Desk Receptionist"}
    }

    if username in users and users[username]['password'] == password:
        token = jwt.encode({
            'user': username,
            'role': users[username]['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({"token": token, "role": users[username]['role'], "username": username}), 200
        
    return jsonify({"message": "Invalid credentials!"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
