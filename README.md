# Customer Happiness Tracker

An AI-powered tool that uses webcam and facial recognition to track and analyze customer happiness in real time.

## Features

- Real-time face detection and emotion analysis
- Customer happiness scoring
- Service time tracking
- Staff performance monitoring
- Data visualization and reporting

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Requirements

- Python 3.8 or higher
- Webcam
- Internet connection (for initial setup)

## Project Structure

- `app.py`: Main application file
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `models.py`: Database models
- `utils/`: Utility functions for face detection and emotion analysis 