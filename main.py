# main.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tenants.db'
db = SQLAlchemy(app)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_number = db.Column(db.String(20))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))

@app.route('/')
def index():
    tenants = Tenant.query.all()
    return render_template('index.html', tenants=tenants)

@app.route('/add', methods=['POST'])
def add_tenant():
    name = request.form['name']
    id_number = request.form['id_number']
    age = request.form['age']
    email = request.form['email']
    address = request.form['address']
    phone_number = request.form['phone_number']
    new_tenant = Tenant(name=name, id_number=id_number, age=age, email=email, address=address, phone_number=phone_number)
    db.session.add(new_tenant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_tenant():
    id_number = request.form['id_number']
    tenant = Tenant.query.filter_by(id_number=id_number).first()
    return render_template('search_result.html', tenant=tenant)

@app.route('/delete/<int:id>')
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    if request.method == 'POST':
        tenant.name = request.form['name']
        tenant.id_number = request.form['id_number']
        tenant.age = request.form['age']
        tenant.email = request.form['email']
        tenant.address = request.form['address']
        tenant.phone_number = request.form['phone_number']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', tenant=tenant)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
