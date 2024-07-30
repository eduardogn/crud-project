from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sentence = db.Column(db.String(200), nullable=False)

# Ensure this code runs within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    friends = Friend.query.all()
    return render_template('index.html', friends=friends)

@app.route('/add', methods=['GET', 'POST'])
def add_friend():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        sentence = request.form['sentence']
        new_friend = Friend(name=name, age=age, email=email, sentence=sentence)
        db.session.add(new_friend)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_friend.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_friend(id):
    friend = Friend.query.get_or_404(id)
    if request.method == 'POST':
        friend.name = request.form['name']
        friend.age = request.form['age']
        friend.email = request.form['email']
        friend.sentence = request.form['sentence']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_friend.html', friend=friend)

@app.route('/view/<int:id>')
def view_friend(id):
    friend = Friend.query.get_or_404(id)
    return render_template('view_friend.html', friend=friend)

@app.route('/delete/<int:id>')
def delete_friend(id):
    friend = Friend.query.get_or_404(id)
    db.session.delete(friend)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
