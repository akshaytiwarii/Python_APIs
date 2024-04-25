from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for doctors
doctors = [
    {"id": 1, "name": "Dr. Akshay", "specialty": "Neurologist"},
    {"id": 2, "name": "Dr. Pintu", "specialty": "Gynocologist"},
    {"id": 3, "name": "Dr. Sajid", "specialty": "Ortho"},
    {"id": 4, "name": "Dr. Jay", "specialty": "Cardiologist"}
]

# Sample data for doctor availability
availability = {
    1: {"Monday": 5, "Tuesday": 5, "Wednesday": 5, "Thursday": 5, "Friday": 5, "Saturday": 2},
    2: {"Monday": 4, "Tuesday": 4, "Wednesday": 4, "Thursday": 4, "Friday": 4, "Saturday": 2},
     3: {"Monday": 4, "Tuesday": 4, "Wednesday": 4, "Thursday": 4, "Friday": 4, "Saturday": 2},
      4: {"Monday": 4, "Tuesday": 4, "Wednesday": 4, "Thursday": 4, "Friday": 4, "Saturday": 2}
}

# Sample data for appointments
appointments = []

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((doctor for doctor in doctors if doctor['id'] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"error": "Doctor not found"}), 404

@app.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_availability(doctor_id):
    doctor_availability = availability.get(doctor_id)
    if doctor_availability:
        return jsonify(doctor_availability)
    else:
        return jsonify({"error": "Doctor not found"}), 404

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    if doctor_id:
        doctor_availability = availability.get(doctor_id)
        if doctor_availability:
            day = data.get('day')
            if day in doctor_availability and doctor_availability[day] > 0:
                doctor_availability[day] -= 1
                appointments.append(data)
                return jsonify({"message": "Appointment booked successfully"}), 201
            else:
                return jsonify({"error": "Doctor not available on specified day or maximum appointments reached"}), 400
        else:
            return jsonify({"error": "Doctor not found"}), 404
    else:
        return jsonify({"error": "Doctor ID not provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
