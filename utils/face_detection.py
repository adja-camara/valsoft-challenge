import cv2
import face_recognition
import numpy as np
from datetime import datetime

class FaceAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def detect_faces(self, frame):
        """Detect faces in a frame and return their locations"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces

    def analyze_emotion(self, face_image):
        """Analyze the emotion of a face and return a happiness score"""
        # Convert to RGB (face_recognition uses RGB)
        rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        
        # Get face landmarks
        face_landmarks = face_recognition.face_landmarks(rgb_face)
        
        if not face_landmarks:
            return 0.0
            
        # Simple happiness detection based on mouth shape
        mouth = face_landmarks[0]['bottom_lip']
        mouth_height = max(y for x, y in mouth) - min(y for x, y in mouth)
        
        # Normalize the score between 0 and 1
        happiness_score = min(mouth_height / 20, 1.0)
        
        return happiness_score

    def process_frame(self, frame):
        """Process a frame and return face locations with happiness scores"""
        faces = self.detect_faces(frame)
        results = []
        
        for (x, y, w, h) in faces:
            face_image = frame[y:y+h, x:x+w]
            happiness_score = self.analyze_emotion(face_image)
            
            results.append({
                'location': (x, y, w, h),
                'happiness_score': happiness_score,
                'timestamp': datetime.now().isoformat()
            })
            
        return results 