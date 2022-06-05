from flask import render_template
from app import app


@app.route('/dashboard/home',methods=['GET'])
def dashboard_home():
    return render_template('/admin/home.html')

@app.route('/dashboard/users',methods=['GET'])
def dashboard_users():
    return render_template('/admin/users.html')
