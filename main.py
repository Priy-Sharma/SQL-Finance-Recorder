from flask import Flask, render_template, request, redirect, url_for, flash
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
import os

# Creating the flask app
app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)  # Use a random secret key

# Creating SQLAlchemy instance
db = SQLAlchemy()

user = 'root'
pin = urllib.parse.quote("Root@123")  # URL-encode the password
host = "localhost"
db_name = 'finance_db'

# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"

# Initializing Flask app with SQLAlchemy
db.init_app(app)

# Creating Models
class Money(db.Model):
    __tablename__ = "money"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), nullable=False, unique=True)
    salary = db.Column(db.Float, nullable=False)
    house_rent = db.Column(db.Float)
    other_monthly_expenses = db.Column(db.Float)

    @property
    def savings(self):
        return self.salary - (self.house_rent or 0) - (self.other_monthly_expenses or 0)

    @property
    def savings_in_percentage(self):
        if self.salary > 0:
            return (self.savings * 100) / self.salary
        return 0

# Function to create the database
def create_db():
    with app.app_context():
        db.create_all()


@app.route("/")
def home():
    details = Money.query.all()
    return render_template("home.html", details=details)


@app.route("/add", methods=['GET', 'POST'])
def add_records():
    if request.method == 'POST':
        per_email = request.form.get('email')
        per_salary = float(request.form.get('salary'))
        per_house_rent = float(request.form.get('house_rent') or 0)
        per_other_monthly_expenses = float(request.form.get('other_monthly_expenses') or 0)

        # Check if the email already exists in the database
        existing_record = Money.query.filter_by(email=per_email).first()

        if existing_record:
            # If email exists, inform the user with an error message
            flash(f'Record with email {per_email} already exists!', 'error')
        else:
            # If email does not exist, add the new record
            add_detail = Money(
                email=per_email,
                salary=per_salary,
                house_rent=per_house_rent,
                other_monthly_expenses=per_other_monthly_expenses
            )
            db.session.add(add_detail)
            db.session.commit()

            # Flash success message
            flash('Record added successfully!', 'success')

        return redirect(url_for('home'))

    return render_template('add_records.html')


@app.route("/search", methods=['GET'])
def search_records():
    return render_template('search_records.html')


@app.route("/show", methods=['POST'])
def show_records():
    if request.method == 'POST':
        email = request.form.get('email')
        user_record = Money.query.filter_by(email=email).first()

        if user_record:
            return render_template('show_records.html', record=user_record)
        else:
            flash('No record found for the given email.', 'error')  # Use 'error' for the not found message
            return redirect(url_for('home'))

    return redirect(url_for('home'))


# For creating the database
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
