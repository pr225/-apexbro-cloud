from flask import Flask, request, jsonify
import os, sqlite3, uuid, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from groq import Groq
app=Flask(__name__)
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
DB="apexbro.db"
def init_db():
 con=sqlite3.connect(DB)
 con.execute('CREATE TABLE IF NOT EXISTS tasks(id TEXT,q TEXT,s TEXT,r TEXT)')
 con.commit()
init_db()
def do_work(tid):
 con=sqlite3.connect(DB)
 row=con.execute("SELECT q FROM tasks WHERE id=?",(tid,)).fetchone()
 if not row: return
 q=row[0]
 try:
  resp=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"user","content":q}])
  ans=resp.choices[0].message.content
  con.execute("UPDATE tasks SET s='done',r=? WHERE id=?",(ans,tid))
 except Exception as e:
  con.execute("UPDATE tasks SET s='error',r=? WHERE id=?",(str(e),tid))
 con.commit()
sched=BackgroundScheduler()
sched.start()
@app.route("/")
def home():return "APEXBRO 24/7 ONLINE"
@app.route("/api/task")
def create():
 q=request.args.get("q","")
 tid=str(uuid.uuid4())[:6]
 con=sqlite3.connect(DB)
 con.execute("INSERT INTO tasks VALUES (?,?,?,?)",(tid,q,"wait",""))
 con.commit()
 sched.add_job(lambda:do_work(tid),'date',run_date=datetime.datetime.now()+datetime.timedelta(seconds=2),id=tid)
 return jsonify({"id":tid})
@app.route("/api/task/<tid>")
def get(tid):
 con=sqlite3.connect(DB)
 row=con.execute("SELECT s,r FROM tasks WHERE id=?",(tid,)).fetchone()
 if row:return jsonify({"status":row[0],"result":row[1]})
 return jsonify({"error":"not found"})
if __name__=="__main__":
 app.run(host='0.0.0.0',port=10000)
