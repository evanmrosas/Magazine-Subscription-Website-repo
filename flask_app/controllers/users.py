from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login-reg')

@app.route('/login-reg')
def login_reg():
    return render_template('login_reg.html')

@app.route('/registration', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    else:
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password" : bcrypt.generate_password_hash(request.form['password'])
            }
        User.add_user(data)
        print("REGISTERED")
        user_id = User.get_by_email(data)
        session['user_name'] = user_id.first_name
        session['user_id'] = user_id.id
        return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    val_user = User.get_by_email(data)
    if not val_user:
        flash("Invalid Email/Password", 'login-error')
        return redirect("/")
    if not bcrypt.check_password_hash(val_user.password, request.form['password']):
        flash("Invalid Email/Password", 'login-error')
        return redirect('/')
    session['user_id'] = val_user.id
    session['user_name'] = val_user.first_name
    print("LOGGED IN")
    return redirect("/dashboard")

@app.route('/user/account', methods=['POST', 'GET'])
def account_page():
    if request.method == 'POST':
        if not User.validate_update(request.form):
            return redirect('/user/account')
        else:
            data = {
                "id": session['user_id'],
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": request.form['email'],
                }
            print(data)
            session['user_name'] = request.form['first_name']
            User.update_user(data)
            return redirect('/dashboard')
    else:
        user = User.get_by_id({'id': session['user_id']})
        magazines = User.get_user_magazines(session['user_id'])
        return render_template('account.html', user=user, magazines=magazines, old_email=user.email)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')