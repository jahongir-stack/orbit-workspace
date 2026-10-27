from flask import Flask,render_template,request,session,redirect,url_for,flash,abort
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from pathlib import Path
import os,sqlite3
app=Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','local-development-only')
DB=Path(__file__).parent/'instance'/'app.db'
DB.parent.mkdir(exist_ok=True)
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def login_required(fn):
 @wraps(fn)
 def wrapped(*args,**kwargs):
  if 'user' not in session:return redirect(url_for('login'))
  return fn(*args,**kwargs)
 return wrapped
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  email=request.form.get('email','').strip().lower();pw=request.form.get('password','')
  with connect() as c:
   if request.form.get('action')=='register':
    if len(pw)<8 or not email:flash('Use a valid email and 8+ character password.');return redirect(url_for('login'))
    try:c.execute('INSERT INTO users(email,password) VALUES(?,?)',(email,generate_password_hash(pw)))
    except sqlite3.IntegrityError:flash('Account exists.');return redirect(url_for('login'))
   row=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
   if row and check_password_hash(row['password'],pw):session.clear();session['user']=row['id'];return redirect(url_for('index'))
  flash('Invalid credentials.')
 return render_template('login.html')
@app.route('/logout',methods=['POST'])
def logout():session.clear();return redirect(url_for('index'))

def init_db():
 with connect() as c:
  c.executescript("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL); CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY,name TEXT,price INTEGER,category TEXT,user_id INTEGER);")
  if not c.execute("SELECT 1 FROM tasks LIMIT 1").fetchone():c.execute("INSERT INTO tasks(name,price,category) VALUES ('Plan roadmap',1,'todo'),('Design system',2,'progress'),('Launch beta',3,'done')")
@app.route('/')
def index():
 with connect() as c:
  tasks=c.execute('SELECT * FROM tasks WHERE user_id=? OR user_id IS NULL',(session.get('user'),)).fetchall();return render_template('index.html',items=tasks)
@app.route('/task',methods=['POST'])
@login_required
def task():
 name=request.form.get('name','').strip()
 if not name or len(name)>120:abort(400)
 with connect() as c:c.execute('INSERT INTO tasks(name,price,category,user_id) VALUES(?,?,?,?)',(name,2,'todo',session['user']))
 return redirect(url_for('index'))
@app.route('/task/<int:item>',methods=['POST'])
@login_required
def move(item):
 status=request.form.get('status','todo')
 if status not in ('todo','progress','done'):abort(400)
 with connect() as c:c.execute('UPDATE tasks SET category=? WHERE id=? AND user_id=?',(status,item,session['user']))
 return redirect(url_for('index'))

if __name__=='__main__':
 init_db()
 app.run(debug=os.getenv('FLASK_DEBUG')=='1')
