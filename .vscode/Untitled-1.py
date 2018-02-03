from flask import Flask,redirect,url_for
import sqlite3 as sql
app=Flask(__name__)

@app.route('/hello',methods=['POST','GET'])
def hello_world():
    return 'hello world'

@app.route('/pip',methods=['GET'])
def ask():
    conn=sql.connect("datas.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO posts (POSTID,POST) VALUES (2,'sasa')")
    conn.commit()
    conn.close()
    return "Database closed!"
    
if __name__=='__main__':
    app.run(debug=True)