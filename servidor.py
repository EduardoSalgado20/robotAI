from flask import Flask

app = Flask(__name__)

@app.route('/mover_robot', methods=['GET'])
def mover_robot():
    # Código para controlar los motores y mover el robot
    mover_adelante()
    return 'El robor se esta moviendo', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
