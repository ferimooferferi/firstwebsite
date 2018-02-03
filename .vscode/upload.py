from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.utils import secure_filename
import sqlite3 as sql
import os
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='C:\Users\Asus\Desktop\hgf'

@app.route('/signup',methods=['POST','GET'])
def signing_up():
   return render_template('secondhtml.html')

@app.route('/adduser',methods=['POST','GET'])
def addusers():
    user=request.form['user']
    password=hashlib.md5(request.form['pass'].encode()).hexdigest()
    first=request.form['first']
    last=request.form['last']
    email=request.form['email']
    age=request.form['age']
    phone=request.form['tel']
    con=sql.connect('users.db')
    cur=con.cursor()
    cur.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?);',(first,last,email,age,phone,user,password))
    con.commit()
    con.close()
    return redirect(url_for('.homepage'))

@app.route('/signout',methods=['POST','GET'])
def signing_out():
    session['logged_in']=False
    if session['logged_in']==False:
        flash('Successfully logged out!')
        session.pop('username',None)
        return redirect(url_for('.homepage'))
    else:
        flash('There was an error in logging out from your account!')

@app.route('/login',methods=['GET','POST'])
def signing_in():
    return render_template('fifthhtml.html')

@app.route('/acclogin',methods=['POST'])
def logins():
    user=request.form['user']
    password=request.form['pass']
    email=request.form['email']
    con=sql.connect("users.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM users;")
    rows=cur.fetchall()
    con.commit()
    con.close()
    for row in rows:
        if user==row[-2]:
            if row[-1]==hashlib.md5(password.encode()).hexdigest():
                session['logged_in']=True
                session['username']=user
                return redirect(url_for('.homepage'))
            
    return redirect(url_for('.signing_in'))            

@app.route('/post',methods=['POST','GET'])
def posting():
    return render_template('ninthhtml.html')

@app.route('/postdata',methods=['POST'])
def dat():
    subject=request.form['subj']
    post=request.form['post']
    conn=sql.connect("datas.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO posts (subject,post) VALUES (?,?)",(subject,post))
    conn.commit()    
    conn.close() 
    return redirect('/post')

@app.route('/profile/completition',methods=['POST','GET'])
def comp():
    return render_template('eighthhtml.html')

@app.route('/profile')
def prof():
    user=session['username']
    return render_template('newprofile.html',user=user)

@app.route('/home')
def homepage():
    con=sql.connect('datas.db')
    cur=con.cursor()
    cur.execute("SELECT * FROM posts ORDER BY ROWID DESC LIMIT 1;")
    posts=cur.fetchone()
    con.commit()
    con.close()
    return render_template('newhome2.html',posts=posts)

@app.route('/deletepost',methods=['POST'])
def delete(subz):
    con=sql.connect('datas.db')
    cur=con.cursor()
    cur.execute("DELETE FROM posts WHERE subject=?",(subz))
    con.commit()
    con.close()

if __name__ == '__main__':
   app.secret_key=os.urandom(12) 
   app.run(debug = True) 