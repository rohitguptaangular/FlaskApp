from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask App", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/about')
def about():
    return jsonify({"app": "Flask CI/CD Demo", "version": "1.0.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
