import os
import json
import datetime
import traceback
from flask import Flask
from flask import request
from flask import jsonify
from groq import Groq

# =====================================================
# ApexBro AI - Potenza Group - Premium 600+ Lines
# White ChatGPT Theme - All Qualities Fixed
# =====================================================

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

CONFIG_FILE = "config.json"
LOG_FILE = "logs.json"

DEFAULT_CONFIG = {
    "app_name": "ApexBro AI",
    "sub_title": "by Potenza Group - White ChatGPT Theme",
    "system_prompt": "You are ApexBro AI, built by Potenza Group. Premium ChatGPT quality. Use markdown tables with | header |. For business give Investment, Production, Expense, Profit tables. Indian UP context. No ** in table cells. Reply same language as user. Never say OpenAI. Be premium detailed.",
    "model": "llama-3.3-70b-versatile",
    "admin_pass": "potenza123"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            f = open(CONFIG_FILE, "r")
            cfg = json.load(f)
            f.close()
            for w in ["gpt-oss", "llama-3.1-8b-instant"]:
                if w in cfg.get("model",""):
                    cfg["model"] = "llama-3.3-70b-versatile"
                    save_config(cfg)
                    break
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
            f = open(LOG_FILE, "r")
            logs = json.load(f)
            f.close()
        except:
            logs = []
    new_entry = {
        "time": datetime.datetime.now().strftime("%d-%m %H:%M:%S"),
        "short_time": datetime.datetime.now().strftime("%d-%m %H:%M"),
        "q": q[:150],
        "ans": ans[:500],
        "date": datetime.datetime.now().strftime("%d-%m-%Y")
    }
    logs.insert(0, new_entry)
    logs = logs[:150]
    f = open(LOG_FILE, "w")
    json.dump(logs, f, indent=2)
    f.close()

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
  background:#fff;
  flex-shrink:0
}
.logo{
  width:36px;
  height:36px;
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
  padding:18px 16px;
  display:flex;
  flex-direction:column;
  gap:20px;
  padding-bottom:140px
}
.msg{
  max-width:96%;
  font-size:14.8px;
  line-height:1.75;
  white-space:pre-wrap;
  word-break:break-word;
  animation:fade 0.2s
}
@keyframes fade{
  from{opacity:0;transform:translateY(6px)}
  to{opacity:1;transform:translateY(0)}
}
.user{
  align-self:flex-end;
  background:#f1f1f1;
  padding:11px 16px;
  border-radius:18px 18px 4px 18px;
  max-width:85%;
  color:#111
}
.bot{
  align-self:flex-start;
  width:100%;
  line-height:1.75
}
.bot-actions{
  margin-top:10px;
  display:flex;
  gap:8px;
  flex-wrap:wrap
}
.btn-small{
  font-size:11px;
  padding:5px 10px;
  border-radius:14px;
  border:1px solid #e5e5e5;
  background:#fff;
  cursor:pointer;
  color:#333;
  font-weight:600
}
.bot table{
  width:100%;
  border-collapse:collapse;
  margin:14px 0;
  font-size:13.5px;
  border:1px solid #e5e5e5;
  border-radius:12px;
  overflow:hidden
}
.bot th{
  background:#f8f8f8;
  padding:10px;
  text-align:left;
  border-bottom:1px solid #e5e5e5
}
.bot td{
  padding:9px 10px;
  border-top:1px solid #f0f0f0
}
.src{
  margin-top:12px;
  font-size:11px;
  color:#666;
  border-top:1px solid #eee;
  padding-top:8px;
  display:flex;
  gap:6px;
  flex-wrap:wrap
}
.src span{
  background:#eef2ff;
  color:#4f46e5;
  padding:4px 10px;
  border-radius:12px;
  font-weight:600
}
.bar-wrap{
  position:sticky;
  bottom:0;
  background:#fff;
  border-top:1px solid #e5e5e5;
  padding:10px 12px
}
.bar-top{
  display:flex;
  justify-content:space-between;
  padding:0 4px 8px;
  font-size:11px;
  color:#888
}
.bar{
  display:flex;
  gap:10px;
  align-items:center
}
.inp{
  flex:1;
  background:#f4f4f4;
  border:1px solid #e5e5e5;
  border-radius:28px;
  display:flex;
  align-items:center;
  padding:5px 6px 5px 16px
}
.inp:focus-within{
  background:#fff;
  border-color:#000
}
.inp input{
  flex:1;
  border:none;
  background:transparent;
  outline:none;
  font-size:15px;
  padding:10px 0
}
.btn-send{
  width:36px;
  height:36px;
  border-radius:50%;
  border:none;
  background:#000;
  color:#fff;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center
}
.btn-mic{
  width:44px;
  height:44px;
  border-radius:50%;
  border:1px solid #e5e5e5;
  background:#fff;
  font-size:19px;
  cursor:pointer
}
.btn-mic.on{
  background:red;
  color:#fff;
  border-color:red
}
.footer-note{
  text-align:center;
  font-size:10px;
  color:#aaa;
  padding:8px
}
.typing{
  display:flex;
  gap:4px;
  padding:8px
}
.typing span{
  width:6px;
  height:6px;
  background:#999;
  border-radius:50%;
  animation:bounce 1s infinite
}
@keyframes bounce{
  0%,80%,100%{transform:scale(0.8);opacity:0.5}
  40%{transform:scale(1.2);opacity:1}
}
</style>
</head>
<body>

<div class="header">
  <div class="logo">P</div>
  <div>
    <b style="font-size:15px">APP_NAME</b>
    <div style="font-size:11px;color:#666">SUB_TITLE</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px">
    <button onclick="clearChat()" class="btn-small">Clear</button>
    <a href="/admin" style="font-size:12px;text-decoration:none;color:#333;border:1px solid #ddd;padding:6px 12px;border-radius:20px">Admin</a>
  </div>
</div>

<div id="chat">
  <div class="msg bot">
    <b>Hi! Mai APP_NAME hu</b><br>
    Potenza Group ka Premium AI hu.<br><br>
    Copy, Regenerate, Voice sab hai!<br><br>
    <span style="font-size:12px;color:#666">Jo puchna ho pucho...</span>
  </div>
</div>

<div class="bar-wrap">
  <div class="bar-top">
    <span>Mic Left | Send | Copy | Regenerate</span>
    <span id="status">Ready</span>
  </div>
  <div class="bar">
    <button class="btn-mic" id="micBtn">Mic</button>
    <div class="inp">
      <input id="q" placeholder="Jo puchna ho pucho...">
      <button class="btn-send" id="sendBtn">Up</button>
    </div>
  </div>
</div>

<div class="footer-note">
  ApexBro AI | Potenza Group | 600+ Lines Premium
</div>

<script>
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec = null;
if(SR){
  rec = new SR();
  rec.lang = 'hi-IN';
}
let mic = document.getElementById('micBtn');
let chat = document.getElementById('chat');
let lastQ = '';

function addUser(t){
  lastQ = t;
  chat.innerHTML += `<div class="msg user">${t}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function addBotActions(id){
  let el = document.getElementById(id);
  if(!el) return;
  let actions = `<div class="bot-actions">
    <button class="btn-small" onclick="copyText('${id}')">Copy</button>
    <button class="btn-small" onclick="speakText('${id}')">Speak</button>
    <button class="btn-small" onclick="regenerate()">Regenerate</button>
  </div>`;
  el.innerHTML += actions;
}

async function copyText(id){
  let el = document.getElementById(id);
  let txt = el.innerText;
  await navigator.clipboard.writeText(txt);
  alert('Copy ho gaya!');
}

function speakText(id){
  let el = document.getElementById(id);
  let txt = el.innerText.substring(0,600);
  let u = new SpeechSynthesisUtterance(txt);
  u.lang = 'hi-IN';
  speechSynthesis.speak(u);
}

function regenerate(){
  if(!lastQ){
    alert('Pehle kuch pucho');
    return;
  }
  getAns(lastQ);
}

function clearChat(){
  if(!confirm('Clear?')) return;
  chat.innerHTML = `<div class="msg bot"><b>Chat Cleared!</b></div>`;
}

mic.onclick = () => {
  if(!rec){
    alert('Chrome me kholo');
    return;
  }
  rec.start();
  mic.classList.add('on');
  mic.innerText = '...';
  rec.onresult = (e) => {
    let t = e.results[0][0].transcript;
    addUser(t);
    getAns(t);
  };
  rec.onend = () => {
    mic.classList.remove('on');
    mic.innerText = 'Mic';
  };
};

document.getElementById('sendBtn').onclick = () => {
  let i = document.getElementById('q');
  let t = i.value.trim();
  if(!t) return;
  addUser(t);
  i.value = '';
  getAns(t);
};

document.getElementById('q').onkeypress = (e) => {
  if(e.key === 'Enter'){
    document.getElementById('sendBtn').click();
  }
};

async function getAns(text){
  let id = 'b' + Date.now();
  chat.innerHTML += `<div class="msg bot" id="${id}">
    <div class="typing"><span></span><span></span><span></span></div>
  </div>`;
  chat.scrollTop = chat.scrollHeight;
  document.getElementById('status').innerText = 'Thinking...';
  try{
    let r = await fetch('/ask?q=' + encodeURIComponent(text));
    let d = await r.json();
    document.getElementById(id).innerHTML = marked.parse(d.answer || 'Error') + `<div class="src"><span>UP Dairy</span><span>NDDB</span><span>Market</span></div>`;
    addBotActions(id);
    document.getElementById('status').innerText = 'Ready';
    chat.scrollTop = chat.scrollHeight;
  }catch(e){
    document.getElementById(id).innerText = 'Error: ' + e;
  }
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    cfg = load_config()
    p = HTML_PAGE.replace("APP_NAME", cfg["app_name"])
    p = p.replace("SUB_TITLE", cfg["sub_title"])
    p = p.replace("APP_NAME", cfg["app_name"])
    return p

@app.route("/ask")
def ask():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"answer": "Pucho?"})
    cfg = load_config()
    m = cfg["model"]
    if "gpt-oss" in m or "llama-3.1-8b-instant" in m:
        m = "llama-3.3-70b-versatile"
    try:
        r = client.chat.completions.create(
            model=m,
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
    except:
        try:
            r2 = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "user", "content": q}
                ]
            )
            return jsonify({"answer": r2.choices[0].message.content})
        except Exception as e:
            return jsonify({"answer": f"Error: {e}"})

@app.route("/admin")
def admin():
    return """
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:system-ui;padding:20px;background:#f5f5f7}
input,textarea,select{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #ccc}
button{padding:13px;background:#000;color:#fff;border:none;border-radius:10px;width:100%;font-weight:700;margin-top:8px;cursor:pointer}
.card{background:#fff;padding:20px;border-radius:16px;margin:16px 0;box-shadow:0 4px 20px #0001}
</style>
</head>
<body>
<h2>ApexBro Admin - Ultimate</h2>
<div class="card">
<input id="pass" type="password" placeholder="potenza123">
<button onclick="login()">Login</button>
</div>
<div id="panel" style="display:none">
<div class="card" style="border:2px solid #16a34a">
<h3>Password Change</h3>
<input id="curPass" disabled>
<input id="newPass" type="password" placeholder="Naya password">
<input id="cnfPass" type="password" placeholder="Confirm">
<button onclick="changePass()" style="background:#16a34a">Change Password</button>
</div>
<div class="card">
<h3>App Control</h3>
<input id="app_name">
<input id="sub_title">
<select id="model">
<option>llama-3.3-70b-versatile</option>
<option>llama3-8b-8192</option>
</select>
<textarea id="sp" rows="8"></textarea>
<button onclick="saveAll()">Save All</button>
</div>
<div class="card">
<h3>Logs & Export</h3>
<div id="stats"></div>
<div id="logs" style="font-size:12px;max-height:400px;overflow:auto;border:1px solid #eee;padding:10px"></div>
<button onclick="exportLogs()" style="background:#4f46e5">Export Logs</button>
<button onclick="resetCfg()" style="background:#ef4444">Reset</button>
</div>
</div>
<script>
let cur='';
async function login(){
  let p=document.getElementById('pass').value;
  let r=await fetch('/admin/api?pass='+p+'&action=get');
  let d=await r.json();
  if(d.error){alert(d.error);return;}
  cur=p;
  document.getElementById('panel').style.display='block';
  document.getElementById('curPass').value=p;
  document.getElementById('app_name').value=d.config.app_name;
  document.getElementById('sub_title').value=d.config.sub_title;
  document.getElementById('model').value=d.config.model;
  document.getElementById('sp').value=d.config.system_prompt;
  loadLogs();
}
async function changePass(){
  let np=document.getElementById('newPass').value.trim();
  let cp=document.getElementById('cnfPass').value.trim();
  if(np.length<4){alert('4+');return;}
  if(np!=cp){alert('Match nahi');return;}
  let r=await fetch('/admin/api?pass='+cur+'&action=changepass',{
    method:'POST',
    body:JSON.stringify({new_pass:np}),
    headers:{'Content-Type':'application/json'}
  });
  let d=await r.json();
  alert(d.msg);
  cur=np;
}
async function saveAll(){
  let cfg={
    app_name:document.getElementById('app_name').value,
    sub_title:document.getElementById('sub_title').value,
    model:document.getElementById('model').value,
    system_prompt:document.getElementById('sp').value,
    admin_pass:cur
  };
  let r=await fetch('/admin/api?pass='+cur+'&action=save',{
    method:'POST',
    body:JSON.stringify(cfg),
    headers:{'Content-Type':'application/json'}
  });
  alert((await r.json()).msg);
}
async function loadLogs(){
  let r=await fetch('/admin/api?pass='+cur+'&action=logs');
  let d=await r.json();
  document.getElementById('stats').innerHTML='Total: '+d.total+' | Today: '+d.today;
  let h='';
  d.logs.forEach(l=>{
    h+=`<div style="padding:6px 0;border-bottom:1px solid #f0f0f0"><b>${l.short_time}</b> - ${l.q}</div>`;
  });
  document.getElementById('logs').innerHTML=h;
}
function exportLogs(){
  let txt=document.getElementById('logs').innerText;
  let blob=new Blob([txt],{type:'application/json'});
  let a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='logs.json';
  a.click();
}
async function resetCfg(){
  if(!confirm('Reset?')) return;
  let r=await fetch('/admin/api?pass='+cur+'&action=reset');
  alert((await r.json()).msg);
}
</script>
</body>
</html>
"""

@app.route("/admin/api")
def admin_api():
    cfg = load_config()
    p = request.args.get("pass", "")
    if p!= cfg["admin_pass"]:
        return jsonify({"error": "Wrong! Default potenza123"})
    a = request.args.get("action", "")
    if a == "get":
        return jsonify({"config": cfg})
    if a == "logs":
        logs = []
        if os.path.exists(LOG_FILE):
            try:
                logs = json.load(open(LOG_FILE))
            except:
                logs = []
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        today_c = len([l for l in logs if l.get("date") == today])
        return jsonify({"total": len(logs), "today": today_c, "logs": logs})
    if a == "reset":
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return jsonify({"msg": "Reset ho gaya"})
    return jsonify({"error": "bad"})

@app.route("/admin/api", methods=["POST"])
def admin_save():
    cfg = load_config()
    p = request.args.get("pass", "")
    if p!= cfg["admin_pass"]:
        return jsonify({"error": "Wrong"})
    a = request.args.get("action", "")
    data = request.get_json() or {}
    if a == "changepass":
        np = data.get("new_pass", "").strip()
        if len(np) < 4:
            return jsonify({"error": "Chota"})
        cfg["admin_pass"] = np
        save_config(cfg)
        return jsonify({"msg": f"Password change: {np}"})
    if a == "save":
        data["admin_pass"] = cfg["admin_pass"]
        save_config(data)
        return jsonify({"msg": "Saved! Premium live!"})
    return jsonify({"error": "bad"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
