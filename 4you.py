from flask import Flask, request, jsonify, render_template, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdpd3B2dmxjdGV4b3loendhbXN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3Mjg2MDIsImV4cCI6MjA1NzMwNDYwMn0._30dmV9IxhYVSslmgW15SHP0FsCGMZGPBQblEjiOSxk"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('index.html', logged_in='user' in session)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email, password = data['email'], data['password']
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data['email'], data['password']
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        session['user'] = response.user
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"})

if __name__ == '__main__':
    app.run(debug=True)