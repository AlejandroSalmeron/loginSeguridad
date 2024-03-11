from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, AutForm
from twilio.rest import Client
import random

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

class Autenticacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50))

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
            return render_template('autenticacion.html')
        else:
            return jsonify({'success': False})
    
    return render_template('login.html', form=form)

""" @app.route('/autenticacion', methods=['GET', 'POST'])
def autenticacion():
    form = AutForm(request.form)
    codigo_gen = 0
    if request.method == 'POST':
        codigo_gen = generar_codigo()
        account_sid = 'AC068ba767acae01b4579aad2a710f4c68'
        auth_token = '159e441ababa926ff0ef2905a4bb567b'

        try:
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body="Este es tu codigo de verificación: " + codigo_gen,
                from_="+14083356840",
                to="+524776793407"
                )

            print("Mensaje enviado correctamente con SID:", message.sid)
            return render_template('inicio.html')
        except Exception as e:
             print("Error al enviar el mensaje:", str(e))
        cod_aut = Autenticacion(codigo=codigo_gen)
        db.session.add(cod_aut)
        db.session.commit()
        return render_template('inicio.html')
        #codigo = form.codigo.data   
        
        usuario = Autenticacion.query.filter_by(codigo=codigo).first()
        if usuario:
            return render_template('autenticacion.html')
        else:
            return jsonify({'success': False})  """


def generar_codigo():
    codigo = ""
    for _ in range(4):
        codigo += str(random.randint(0, 9))
    return codigo

# Ejemplo de uso:
codigo_generado = generar_codigo()
print("Código generado:", codigo_generado)

@app.route('/screen')
def screenLogin():
    return render_template('login.html')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True, port=8080)
