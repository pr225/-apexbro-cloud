import os, sqlite3, uuid
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from groq import Groq

app=Flask(__name__)

# Key check
api_key = os.environ.get("GROQ_API_KEY")
print(f"KEY LOADED: {bool(api_key)}")
client=Groq(api_key=api_key) if api_key else None

DB="apexbro.db"

def init_db():
    con=sqlite3.connect(DB, check_same_thread=False)
    con.execute('CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, q TEXT, s TEXT, r TEXT)')
    con.commit()
    con.close()

init_db()

def do_work(tid):
    print(f"WORK START for {tid}")
    con=sqlite3.connect(DB, check_same_thread=False)
    row=con.execute("SELECT q FROM tasks WHERE id=?",(tid,)).fetchone()
    if not row:
        con.close()
        return
    q=row[0]
    try:
        if not client:
            raise Exception("GROQ_API_KEY missing in Render Environment")
        # NEW MODEL - ye ab kaam karta hai
        resp=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":q}]
        )
        ans=resp.choices[0].message.content
        print(f"ANSWER: {ans[:50]}")
        con.execute("UPDATE tasks SET s='done',r=? WHERE id=?",(ans,tid))
    except Exception as e:
        print(f"ERROR: {e}")
        con.execute("UPDATE tasks SET s='error',r=? WHERE id=?",(str(e),tid))
    con.commit()
    con.close()

sched=BackgroundScheduler()
sched.start()

@app.route("/")
def home():
    return """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>ApexBro AI</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#101010;color:#fff;height:100dvh;display:flex;flex-direction:column}.header{padding:16px;text-align:center;border-bottom:1px solid #222;font-weight:700;font-size:18px}#chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}.msg{max-width:80%;padding:12px 14px;border-radius:18px;line-height:1.4;font-size:15px;white-space:pre-wrap}.user{align-self:flex-end;background:#0084ff;border-bottom-right-radius:4px}.bot{align-self:flex-start;background:#222;border-bottom-left-radius:4px}.bar{display:flex;gap:8px;padding:12px;border-top:1px solid #222;background:#151515}input{flex:1;padding:14px 16px;border-radius:25px;border:none;background:#222;color:#fff;outline:none;font-size:16px}button{width:48px;height:48px;border-radius:50%;border:none;background:#00ff88;font-size:20px}.typing{opacity:0.6;font-style:italic}</style></head><body><div class="header">🤖 ApexBro AI - 24/7 Online</div><div id="chat"><div class='msg bot'>Hi! Main ApexBro hu. Bolo kya help chahiye?</div></div><div class="bar"><input id="q" placeholder="Kuch likho..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">➤</button></div><script>async function send(){let input=document.getElementById('q');let text=input.value.trim();if(!text)return;let chat=document.getElementById('chat');chat.innerHTML+=`<div class='msg user'>${text}</div>`;input.value='';chat.scrollTop=chat.scrollHeight;let typingId='t'+Date.now();chat.innerHTML+=`<div id="${typingId}" class='msg bot typing'>Soch raha hu...</div>`;try{let r1=await fetch('/api/task?q='+encodeURIComponent(text));let d1=await r1.json();let tid=d1.id;let ans=null;for(let i=0;i<30;i++){await new Promise(r=>setTimeout(r,1000));let r2=await fetch('/api/task/'+tid);let d2=await r2.json();if(d2.status==='done'){ans=d2.res||d2.r;break;}if(d2.status==='error'){ans='Error: '+d2.res;break;}}document.getElementById(typingId).remove();if(!ans)ans='Time out, phir se try karo';chat.innerHTML+=`<div class='msg bot'>${ans.replace(/\\n/g,'<br>')}</div>`;}catch(e){document.getElementById(typingId).remove();chat.innerHTML+=`<div class='msg bot'>Network error: ${e}</div>`;}chat.scrollTop=chat.scrollHeight;}</script></body></html>"""

@app.route("/api/task")
def create():
    q=request.args.get("q","")
    if not q: return jsonify({"error":"q missing"})
    tid=str(uuid.uuid4())[:6]
    con=sqlite3.connect(DB, check_same_thread=False)
    con.execute("INSERT INTO tasks VALUES (?,?,?,?)",(tid,q,'pending',''))
    con.commit()
    con.close()
    sched.add_job(lambda:do_work(tid),'date')
    return jsonify({"id":tid})

@app.route("/api/task/<tid>")
def get(tid):
    con=sqlite3.connect(DB, check_same_thread=False)
    row=con.execute("SELECT s,r FROM tasks WHERE id=?",(tid,)).fetchone()
    con.close()
    if row: return jsonify({"status":row[0],"res":row[1],"r":row[1]})
    return jsonify({"error":"not found"})

if __name__=="__main__":
    app.run(host='0.0.0.0',port=10000)
