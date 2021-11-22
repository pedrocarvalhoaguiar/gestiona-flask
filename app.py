from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/pedri/OneDrive/Documentos/gestiona-flask/gestiona.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id ).first()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['submit-button'] == 'login':
            return login()
        if request.form['submit-button'] == 'register':
            return register()

    return render_template('index.html')

def register():
    name = request.form['register-name']
    email = request.form['register-email']
    passowrd = request.form['register-password']
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email já cadastrado")
        return render_template('index.html', register=False)
    else:
        user = User(name, email, passowrd)
        db.session.add(user)
        db.session.commit()
        flash('Registro completo! Por favor, faça o login')
        return render_template('index.html', login=False)

def login():
    email = request.form['login-email']
    password = request.form['login-password']

    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash("Email não encontrado")
        return render_template('index.html', login=False)
    
    elif not user.verify_password(password):
        flash("Senha incorreta")
        return render_template('index.html', login=False)
    else:
        login_user(user)
        flash("logado com sucesso")
        return(redirect(url_for('home')))

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)