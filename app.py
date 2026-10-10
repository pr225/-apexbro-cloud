import os, json, datetime
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

CONFIG_FILE = "config.json"
LOG_FILE = "logs.json"

DEFAULT_CONFIG = {
    "app_name": "ApexBro AI",
    "sub_title": "by Potenza Group - White ChatGPT Theme",
    "system_prompt": "You are ApexBro AI, built by Potenza Group. You answer like ChatGPT. Use markdown tables with | header |. For business questions give Investment, Production, Expense, Profit tables. Indian context UP. No ** inside table cells. Reply in same language as user. Never say you are OpenAI. Be premium quality.",
    "model": "llama-3.1-8b-instant",
    "admin_pass": "potenza123"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try: return json.load(open(CONFIG_FILE))
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(cfg):
    json.dump(cfg, open(CONFIG_FILE,"w"))

def log_query(q, ans):
    logs=[]
    if os.path.exists(LOG_FILE):
        try: logs=json.load(open(LOG_FILE))
        except: logs=[]
    logs.insert(0,{"time":datetime.datetime.now().strftime("%d-%m %H:%M"), "q":q[:120], "ans":ans[:200]})
    logs=logs[:100]
    json.dump(logs, open(LOG_FILE,"w"))

config = load_config()

HTML_PAGE = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>APP_NAME</title><script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#fff;color:#111;height:100dvh;display:flex;flex-direction:column}
.header{padding:12px 14px;border-bottom:1px solid #e5e5e5;display:flex;align-items:center;gap:10px;background:#fff}
.logo{width:34px;height:34px;background:#00c950;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900}
#chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:16px;padding-bottom:100px}
.msg{max-width:96%;font-size:14.5px;line-height:1.6;white-space:pre-wrap}
/* ChatGPT jaisa User Message - Grey, Right me */
.user{align-self:flex-end;background:#f1f1f1;padding:10px 16px;border-radius:18px;max-width:85%;color:#000}
.bot{align-self:flex-start;width:100%}
.bot table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden}
.bot th{background:#f5f5f5;padding:8px;text-align:left;border-bottom:1px solid #e5e5e5}
.bot td{padding:8px;border-top:1px solid #eee}
.src{margin-top:10px;font-size:11px;color:#666;border-top:1px solid #eee;padding-top:8px}
.src span{background:#eef2ff;color:#4f46e5;padding:2px 7px;border-radius:10px;margin-right:4px;display:inline-block}

/* Bottom - Mic Left, Send Right - ChatGPT Style */
.bar{padding:10px 12px;border-top:1px solid #e5e5e5;display:flex;gap:8px;background:#fff;align-items:center}
.inp{flex:1;background:#f4f4f4;border:1px solid #e5e5e5;border-radius:28px;display:flex;align-items:center;padding:4px 6px 4px 12px}
.inp input{flex:1;border:none;background:transparent;outline:none;font-size:15px}
.btn-send{width:36px;height:36px;border-radius:50%;border:none;background:#000;color:#fff;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.btn-mic{width:40px;height:40px;border-radius:50%;border:none;background:transparent;font-size:20px;cursor:pointer;flex-shrink:0}
.btn-mic.on{background:red;color:#fff}
</style></head><body>
<div class="header"><div class="logo">P</div><div><div style="font-weight:700;font-size:15px">APP_NAME</div><div style="font-size:11px;color:#666">SUB_TITLE</div></div>
<div style="margin-left:auto"><a href="/admin" style="font-size:12px;text-decoration:none;color:#666">⚙️ Admin</a></div>
</div>
<div id="chat"><div class="msg bot">Hi! Mai APP_NAME hu, Potenza Group ne banaya hai. Jo puchna ho pucho! 👋</div></div>
<div class="bar">
<button class="btn-mic" id="micBtn">🎤</button>
<div class="inp"><input id="q" placeholder="Jo puchna ho pucho..."><button class="btn-send" id="sendBtn">↑</button></div>
</div>
<script>
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;let rec=null;if(SR){rec=new SR();rec.lang='hi-IN';}
let mic=document.getElementById('micBtn');let chat=document.getElementById('chat');let voice=null;
function loadV(){let v=speechSynthesis.getVoices();voice=v[0];}speechSynthesis.onvoiceschanged=loadV;loadV();
mic.onclick=()=>{if(!rec){alert('Chrome me kholo');return;}speechSynthesis.cancel();rec.start();mic.classList.add('on');mic.innerText='●';rec.onresult=(e)=>{let t=e.results[0][0].transcript;addUser(t);getAns(t,true);};rec.onend=()=>{mic.classList.remove('on');mic.innerText='🎤';};};
document.getElementById('sendBtn').onclick=sendText;document.getElementById('q').onkeypress=(e)=>{if(e.key==='Enter')sendText()};
function addUser(t){chat.innerHTML+=`<div class="msg user">${t}</div>`;chat.scrollTop=chat.scrollHeight;}
function sendText(){let i=document.getElementById('q');let t=i.value.trim();if(!t)return;speechSynthesis.cancel();addUser(t);i.value='';getAns(t,false);}
async function getAns(text,sp){let id='t'+Date.now();chat.innerHTML+=`<div class="msg bot" id="${id}">● ● ●</div>`;chat.scrollTop=chat.scrollHeight;try{let r=await fetch('/ask?q='+encodeURIComponent(text));let d=await r.json();document.getElementById(id).remove();let html=marked.parse(d.answer||'');let src=`<div class="src">🔍 Sources: <span>UP Dairy</span> <span>NDDB</span> <span>Market</span></div>`;chat.innerHTML+=`<div class="msg bot">${html}${src}</div>`;if(sp){let c=(d.answer||'').replace(/[#*|_`]/g,'').substring(0,500);let u=new SpeechSynthesisUtterance(c);if(voice)u.voice=voice;speechSynthesis.speak(u);}chat.scrollTop=chat.scrollHeight;}catch(e){document.getElementById(id).remove();chat.innerHTML+=`<div class="msg bot">Error: ${e}</div>`;}}
</script></body></html>
"""

@app.route("/")
def home():
    cfg = load_config()
    page = HTML_PAGE.replace("APP_NAME", cfg["app_name"]).replace("SUB_TITLE", cfg["sub_title"])
    return page

@app.route("/ask")
def ask():
    q = request.args.get("q","").strip()
    if not q: return jsonify({"answer":"Pucho?"})
    cfg = load_config()
    try:
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role":"system","content":cfg["system_prompt"]},{"role":"user","content":q}],
            temperature=0.6, max_tokens=1800
        )
        ans = resp.choices[0].message.content
        log_query(q, ans)
        return jsonify({"answer":ans})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)} - GROQ_API_KEY check karo Render me"})

@app.route("/admin")
def admin():
    return """
    <html><head><meta name="viewport" content="width=device-width,initial-scale=1">
    <style>body{font-family:system-ui;padding:20px;background:#f6f6f6}input,textarea,select{width:100%;padding:10px;margin:6px 0;border:1px solid #ccc;border-radius:8px}button{padding:12px 20px;background:#000;color:#fff;border:none;border-radius:8px;cursor:pointer;width:100%}.card{background:#fff;padding:16px;border-radius:12px;margin:12px 0;box-shadow:0 2px 8px #0001}</style>
    </head><body>
    <h2>⚙️ ApexBro Admin - Potenza Group</h2>
    <div class="card"><h3>Login</h3><input id="pass" type="password" placeholder="Admin Password (potenza123)"><button onclick="login()">Login</button></div>
    <div id="panel" style="display:none">
    <div class="card"><h3>App Control</h3>
    App Name: <input id="app_name"><br>
    Sub Title: <input id="sub_title"><br>
    Model: <select id="model"><option>llama-3.1-8b-instant</option><option>openai/gpt-oss-20b</option><option>qwen/qwen3-32b</option></select><br>
    System Prompt:<br><textarea id="sp" rows="8"></textarea><br>
    <button onclick="save()">💾 Save Changes</button>
    </div>
    <div class="card"><h3>📊 Stats</h3><div id="stats"></div></div>
    <div class="card"><h3>📝 Recent 100 Queries</h3><div id="logs" style="font-size:13px;max-height:400px;overflow:auto"></div></div>
    </div>
    <script>
    let cfg={};
    async function login(){
      let p=document.getElementById('pass').value;
      let r=await fetch('/admin/api?pass='+p+'&action=get');
      let d=await r.json();
      if(d.error){alert(d.error);return;}
      cfg=d.config; document.getElementById('panel').style.display='block';
      document.getElementById('app_name').value=cfg.app_name;
      document.getElementById('sub_title').value=cfg.sub_title;
      document.getElementById('model').value=cfg.model;
      document.getElementById('sp').value=cfg.system_prompt;
      loadLogs(p);
    }
    async function save(){
      let p=document.getElementById('pass').value;
      cfg.app_name=document.getElementById('app_name').value;
      cfg.sub_title=document.getElementById('sub_title').value;
      cfg.model=document.getElementById('model').value;
      cfg.system_prompt=document.getElementById('sp').value;
      let r=await fetch('/admin/api?pass='+p+'&action=save',{method:'POST',body:JSON.stringify(cfg),headers:{'Content-Type':'application/json'}});
      let d=await r.json(); alert(d.msg);
    }
    async function loadLogs(p){
      let r=await fetch('/admin/api?pass='+p+'&action=logs'); let d=await r.json();
      document.getElementById('stats').innerHTML='Total Queries: '+d.total+'<br>Today: '+d.today;
      let h=''; d.logs.forEach(l=>{h+=`<div style="border-bottom:1px solid #eee;padding:6px 0"><b>${l.time}</b> - ${l.q}</div>`}); document.getElementById('logs').innerHTML=h;
    }
    </script></body></html>
    """

@app.route("/admin/api")
def admin_api():
    cfg = load_config()
    p = request.args.get("pass","")
    if p!= cfg["admin_pass"]:
        return jsonify({"error":"Wrong Password! Default is potenza123"})
    action = request.args.get("action","")
    if action=="get":
        return jsonify({"config":cfg})
    if action=="logs":
        logs=[]
        if os.path.exists(LOG_FILE):
            try: logs=json.load(open(LOG_FILE))
            except: pass
        today = datetime.datetime.now().strftime("%d-%m")
        today_count = len([l for l in logs if today in l["time"]])
        return jsonify({"total":len(logs),"today":today_count,"logs":logs})
    return jsonify({"error":"bad action"})

@app.route("/admin/api", methods=["POST"])
def admin_save():
    cfg = load_config()
    p = request.args.get("pass","")
    if p!= cfg["admin_pass"]:
        return jsonify({"error":"Wrong Password"})
    action = request.args.get("action","")
    if action=="save":
        new_cfg = request.get_json()
        save_config(new_cfg)
        return jsonify({"msg":"✅ Saved! Ab home page reload karo, changes live hai!"})
    return jsonify({"error":"bad"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
