from flask import Flask, jsonify

app = Flask(__name__)

#Test de que el server está corriendo
@app.route('/ping')
def ping():
    return jsonify({"message": "pong!"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)