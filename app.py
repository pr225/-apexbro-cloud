import os
import json
import datetime
from flask import Flask
from flask import request
from flask import jsonify
from groq import Groq

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

CONFIG_FILE = "config.json"
LOG_FILE = "logs.json"

DEFAULT_CONFIG = {
    "app_name": "ApexBro AI",
    "system_prompt": "You are ApexBro AI. Be helpful, friendly, premium quality. Answer in same language as user. Use tables with | header | for data.",
    "model": "llama-3.3-70b-versatile",
    "admin_pass": "potenza123"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            f = open(CONFIG_FILE, "r")
            cfg = json.load(f)
            f.close()
            if "gpt-oss" in cfg.get("model","") or "llama-3.1-8b-instant" in cfg.get("model",""):
                cfg["model"] = "llama-3.3-70b-versatile"
                save_config(cfg)
            return cfg
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(cfg):
    f = open(CONFIG_FILE, "w")
    json.dump(cfg, f, indent=2)
    f.close()

def log_query(q, ans):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            logs = json.load(open(LOG_FILE))
        except:
            logs = []
    logs.insert(0, {
        "time": datetime.datetime.now().strftime("%d-%m %H:%M"),
        "q": q[:150],
        "date": datetime.datetime.now().strftime("%d-%m-%Y")
    })
    json.dump(logs[:100], open(LOG_FILE, "w"), indent=2)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>APP_NAME</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:system-ui,Arial;
  background:#fff;
  color:#111;
  height:100dvh;
  display:flex;
  flex-direction:column;
  overflow:hidden
}
.header{
  padding:12px 16px;
  border-bottom:1px solid #e5e5e5;
  display:flex;
  align-items:center;
  gap:10px;
  background:#fff
}
.logo{
  width:34px;
  height:34px;
  background:#00c950;
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-weight:900
}
#chat{
  flex:1;
  overflow-y:auto;
  padding:20px 16px;
  display:flex;
  flex-direction:column;
  gap:18px;
  padding-bottom:120px
}
.msg{
  max-width:92%;
  font-size:15px;
  line-height:1.7;
  white-space:pre-wrap
}
.user{
  align-self:flex-end;
  background:#f1f1f1;
  padding:10px 16px;
  border-radius:18px 18px 4px 18px
}
.bot{
  align-self:flex-start;
  width:100%
}
.bot table{
  width:100%;
  border-collapse:collapse;
  margin:12px 0;
  font-size:13.5px;
  border:1px solid #e5e5e5;
  border-radius:10px;
  overflow:hidden
}
.bot th{background:#f8f8f8;padding:9px;text-align:left}
.bot td{padding:8px;border-top:1px solid #eee}
.bar{
  padding:12px;
  border-top:1px solid #e5e5e5;
  display:flex;
  gap:10px;
  background:#fff;
  align-items:center
}
.inp{
  flex:1;
  background:#f4f4f4;
  border:1px solid #e5e5e5;
  border-radius:26px;
  display:flex;
  align-items:center;
  padding:4px 6px 4px 14px
}
.inp input{
  flex:1;
  border:none;
  background:transparent;
  outline:none;
  font-size:15px;
  padding:8px 0
}
.btn-send{
  width:36px;
  height:36px;
  border-radius:50%;
  border:none;
  background:#000;
  color:#fff;
  cursor:pointer
}
.btn-mic{
  width:42px;
  height:42px;
  border-radius:50%;
  border:1px solid #e5e5e5;
  background:#fff;
  font-size:18px;
  cursor:pointer
}
.btn-mic.on{background:red;color:#fff;border-color:red}
</style>
</head>
<body>

<div class="header">
  <div class="logo">P</div>
  <div style="font-weight:800">APP_NAME</div>
  <a href="/admin" style="margin-left:auto;font-size:12px;text-decoration:none;color:#333;border:1px solid #ddd;padding:6px 12px;border-radius:20px">Admin</a>
</div>

<div id="chat">
  <div class="msg bot">Hello! How can I help you today?</div>
</div>

<div class="bar">
  <button class="btn-mic" id="micBtn">🎤</button>
  <div class="inp">
    <input id="q" placeholder="Message...">
    <button class="btn-send" id="sendBtn">↑</button>
  </div>
</div>

<script>
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec = null;
if(SR){ rec = new SR(); rec.lang='hi-IN'; }
let mic = document.getElementById('micBtn');
let chat = document.getElementById('chat');

mic.onclick = () => {
  if(!rec){ alert('Chrome me kholo'); return; }
  rec.start(); mic.classList.add('on');
  rec.onresult = (e) => {
    let t = e.results[0][0].transcript;
    addUser(t); getAns(t);
  };
  rec.onend = () => { mic.classList.remove('on'); };
};

document.getElementById('sendBtn').onclick = sendMsg;
document.getElementById('q').onkeypress = (e) => { if(e.key==='Enter') sendMsg(); };

function addUser(t){
  chat.innerHTML += `<div class="msg user">${t}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function sendMsg(){
  let i = document.getElementById('q');
  let t = i.value.trim();
  if(!t) return;
  addUser(t);
  i.value = '';
  getAns(t);
}

async function getAns(text){
  let id = 'a'+Date.now();
  chat.innerHTML += `<div class="msg bot" id="${id}">● ● ●</div>`;
  chat.scrollTop = chat.scrollHeight;
  try{
    let r = await fetch('/ask?q='+encodeURIComponent(text));
    let d = await r.json();
    document.getElementById(id).innerHTML = marked.parse(d.answer||'');
    chat.scrollTop = chat.scrollHeight;
  }catch(e){
    document.getElementById(id).innerText = 'Error: '+e;
  }
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    cfg = load_config()
    return HTML_PAGE.replace("APP_NAME", cfg["app_name"])

@app.route("/ask")
def ask():
    q = request.args.get("q","").strip()
    if not q:
        return jsonify({"answer": "Please ask something?"})
    cfg = load_config()
    try:
        r = client.chat.completions.create(
            model=cfg["model"],
            messages=[
                {"role": "system", "content": cfg["system_prompt"]},
                {"role": "user", "content": q}
            ],
            temperature=0.6,
            max_tokens=2000
        )
        ans = r.choices[0].message.content
        log_query(q, ans)
        return jsonify({"answer": ans})
    except Exception as e:
        return jsonify({"answer": f"Error: {e}"})

@app.route("/admin")
def admin():
    return """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:system-ui;padding:20px;background:#f5f5f7}
input,textarea,select{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #ccc}
button{padding:12px;background:#000;color:#fff;border:none;border-radius:10px;width:100%;font-weight:700;margin-top:8px}
.card{background:#fff;padding:18px;border-radius:14px;margin:14px 0}
</style></head><body>
<h2>ApexBro Admin</h2>
<div class="card"><input id="pass" type="password" placeholder="potenza123"><button onclick="login()">Login</button></div>
<div id="panel" style="display:none">
<div class="card"><h3>Change Password</h3><input id="curPass" disabled><input id="newPass" type="password" placeholder="New Password"><input id="cnfPass" type="password" placeholder="Confirm"><button onclick="changePass()" style="background:#16a34a">Change</button></div>
<div class="card"><h3>Settings</h3><input id="app_name" placeholder="App Name"><textarea id="sp" rows="6"></textarea><button onclick="saveAll()">Save</button><button onclick="resetCfg()" style="background:#ef4444">Reset</button></div>
</div>
<script>
let cur='';
async function login(){let p=document.getElementById('pass').value;let r=await fetch('/admin/api?pass='+p+'&action=get');let d=await r.json();if(d.error){alert(d.error);return;}cur=p;document.getElementById('panel').style.display='block';document.getElementById('curPass').value=p;document.getElementById('app_name').value=d.config.app_name;document.getElementById('sp').value=d.config.system_prompt;}
async function changePass(){let np=document.getElementById('newPass').value.trim();let cp=document.getElementById('cnfPass').value.trim();if(np.length<4){alert('4+');return;}if(np!=cp){alert('Match nahi');return;}let r=await fetch('/admin/api?pass='+cur+'&action=changepass',{method:'POST',body:JSON.stringify({new_pass:np}),headers:{'Content-Type':'application/json'}});alert((await r.json()).msg);cur=np;}
async function saveAll(){let cfg={app_name:document.getElementById('app_name').value,system_prompt:document.getElementById('sp').value,model:'llama-3.3-70b-versatile',admin_pass:cur};let r=await fetch('/admin/api?pass='+cur+'&action=save',{method:'POST',body:JSON.stringify(cfg),headers:{'Content-Type':'application/json'}});alert((await r.json()).msg);}
async function resetCfg(){let r=await fetch('/admin/api?pass='+cur+'&action=reset');alert((await r.json()).msg);}
</script></body></html>
"""

@app.route("/admin/api")
def admin_api():
    cfg = load_config()
    p = request.args.get("pass","")
    if p!=cfg["admin_pass"]:
        return jsonify({"error":"Wrong Password"})
    a = request.args.get("action","")
    if a=="get":
        return jsonify({"config":cfg})
    if a=="reset":
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return jsonify({"msg":"Reset ho gaya"})
    return jsonify({"error":"bad"})

@app.route("/admin/api", methods=["POST"])
def admin_save():
    cfg = load_config()
    p = request.args.get("pass","")
    if p!=cfg["admin_pass"]:
        return jsonify({"error":"Wrong"})
    a = request.args.get("action","")
    data = request.get_json() or {}
    if a=="changepass":
        np=data.get("new_pass","").strip()
        if len(np)<4:
            return jsonify({"error":"Chota"})
        cfg["admin_pass"]=np
        save_config(cfg)
        return jsonify({"msg":f"Password changed: {np}"})
    if a=="save":
        data["admin_pass"]=cfg["admin_pass"]
        save_config(data)
        return jsonify({"msg":"Saved!"})
    return jsonify({"error":"bad"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
