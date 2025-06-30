from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'yek-ramez-sirri'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')

        if not name or not email or not message_text:
            flash('لطفاً همه فیلدها را پر کنید.', 'error')
            return redirect(url_for('home'))

        new_message = Message(name=name, email=email, message=message_text)
        db.session.add(new_message)
        db.session.commit()

        flash('ممنون از نظرت!  به زودی از ایمیل پاسخت رو خواهیم داد', 'success')
        return redirect(url_for('home'))

    messages = Message.query.all()
    return render_template('index.html', messages=messages)

import os

if name == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
