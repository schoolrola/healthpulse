import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Setup database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Initialize the database
db.init_app(app)

# Models
class HealthCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    treatments = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create all database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fqr_dam')
def fqr_dam():
    return render_template('fqr_dam.html')

@app.route('/rbw')
def rbw():
    return render_template('rbw.html')

@app.route('/dght_dam')
def dght_dam():
    return render_template('dght_dam.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            message = ContactMessage(
                name=request.form['name'],
                email=request.form['email'],
                subject=request.form['subject'],
                message=request.form['message']
            )
            db.session.add(message)
            db.session.commit()
            flash('تم إرسال رسالتك بنجاح!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال رسالتك. يرجى المحاولة مرة أخرى.', 'error')

    return render_template('contact.html')