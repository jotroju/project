from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)




class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, )
    ra = db.Column(db.Integer, )
    date = db.Column(db.String )
    color = db.Column(db.String, )
    style = db.Column(db.String, )
    size = db.Column(db.String, )
    reason = db.Column(db.String,)

def __init__(self, name, ra,date, color, style, size, reason):
    self.name = customer
    self.ra = email
    self.date = date
    self.color = color
    self.style = style
    self.size = size
    self.reason = reason


@app.route('/submit', methods=['POST'])
def home():
    if request.method == 'POST':
        name = request.form['cname']
        ra = request.form['number']
        date = request.form['rdate']
        color = request.form['color']
        style = request.form['style']
        size = request.form['size']
        reason = request.form['reason']
        # data = Return(name, ra, date, color, style, size, reason)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')

@app.route('/')
def index():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)