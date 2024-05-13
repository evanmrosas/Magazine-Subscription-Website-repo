from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.magazine import Magazine

@app.route('/dashboard', methods=['GET'])
def all_magazines():
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        magazines = Magazine.get_all_magazines()
        return render_template('dashboard.html', magazines = magazines)

@app.route('/magazines/new')
def new_magazine_page():
    return render_template('new_magazine.html')

@app.route('/add-magazine', methods=['POST'])
def add_magazine():
    if not Magazine.validate_magazine(request.form):
        return redirect('/magazines/new')
    else:
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "user_id": session['user_id']
            }
        print(data)
        Magazine.add_magazine(data)
        return redirect('/dashboard')

@app.route('/magazines/view/<int:id>')
def view_magazine_page(id):
    magazine = Magazine.view_magazine({"id":id})
    return render_template('view_magazine.html', magazine = magazine)

@app.route('/magazines/delete/<int:id>')
def delete_magazine(id):
    data = {"id":id}
    Magazine.delete_magazine(data)
    return redirect('/user/account')