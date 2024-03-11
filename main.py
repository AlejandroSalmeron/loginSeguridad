from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:losverdes@localhost/loginSeguridad'  # Cambia la URL por la de tu base de datos
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://192.168.1.228:8080"}})

db = SQLAlchemy(app)

# Definir el modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Crear la base de datos (solo necesitas ejecutar esto una vez)
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)  # Crea una instancia de LoginForm
    
    if request.method == 'POST':
        username = form.username.data   
        password = form.password.data
        
        usuario = Usuario.query.filter_by(username=username, password=password).first()
        if usuario:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    
    return render_template('login.html', form=form)

@app.route('/screen')
def screenLogin():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
