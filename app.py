from flask import Flask, render_template, Response, request, jsonify
from models import db, Customer, CustomerSession
from utils.face_detection import FaceAnalyzer
import cv2
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happiness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
face_analyzer = FaceAnalyzer()

camera = cv2.VideoCapture(0)
latest_score = 0.0  # For live updating

def generate_frames():
    global latest_score
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = face_analyzer.process_frame(frame)
            if results:
                latest_score = results[0]['happiness_score']

            for result in results:
                x, y, w, h = result['location']
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Happiness: {result['happiness_score']:.2f}", 
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    sessions = CustomerSession.query.all()
    return jsonify([session.to_dict() for session in sessions])

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.json
    customer = Customer.query.filter_by(name=data['customer_name']).first()
    if not customer:
        customer = Customer(name=data['customer_name'])
        db.session.add(customer)
        db.session.commit()
    
    session = CustomerSession(
        customer_id=customer.id,
        happiness_score=data['happiness_score'],
        server_name=data.get('server_name'),
        order_details=data.get('order_details')
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify(session.to_dict()), 201

@app.route('/api/sessions/<int:session_id>/score', methods=['PUT'])
def update_score(session_id):
    session = CustomerSession.query.get_or_404(session_id)
    data = request.json
    session.happiness_score = data.get('happiness_score', session.happiness_score)
    db.session.commit()
    return jsonify(session.to_dict())

@app.route('/api/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = CustomerSession.query.get_or_404(session_id)
    data = request.json
    if 'service_time' in data:
        session.service_time = data['service_time']
    if 'exit_time' in data:
        session.exit_time = datetime.fromisoformat(data['exit_time'])
    db.session.commit()
    return jsonify(session.to_dict())

@app.route('/api/sessions/<int:session_id>/complete', methods=['PUT'])
def complete_session(session_id):
    session = CustomerSession.query.get_or_404(session_id)
    exit_time = datetime.utcnow()
    session.exit_time = exit_time
    session.service_time = (exit_time - session.entry_time).total_seconds()
    db.session.commit()
    return jsonify(session.to_dict())

@app.route('/api/happiness_score')
def get_latest_score():
    return jsonify({'happiness_score': latest_score})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
