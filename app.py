from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):   # ✅ Capitalized class name
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) 
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        new_todo = Todo(title=title, desc=desc)   # ✅ avoid shadowing
        db.session.add(new_todo)
        db.session.commit()
        
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')   # ✅ correct route
def delete(sno):
    todo = Todo.query.get_or_404(sno)   # safer than filter_by
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))   # ✅ function name

@app.route('/update/<int:sno>', methods=['GET', 'POST'])   # ✅ correct route
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.get_or_404(sno)   # safer than filter_by
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
        
    todo = Todo.query.get_or_404(sno)   # safer than filter_by
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Create database tables
    app.run(debug=True)
