import os, json, time
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

# Config handling
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "app_name": "ApexBro AI",
    "by_text": "by Potenza Group - White ChatGPT Theme",
    "welcome_msg": "Hi! Mai ApexBro hu, Potenza Group ne banaya hai. Ab white ChatGPT theme me hu. Pucho kuch bhi! 👋",
    "system_prompt": "You are ApexBro AI, created by Potenza Group. Be helpful, friendly, answer in Hindi + English mix like user. You are in White ChatGPT theme.",
    "model": "llama-3.1-8b-instant"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(f, cfg, indent=2)

config = load_config()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{app_name}}</title>
<style>
body{margin:0;font-family:system-ui;background:white;color:#111;display:flex;flex-direction:column;height:100vh}
.header{padding:12px 16px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:12px;position:sticky;top:0;background:white;z-index:10}
.logo{width:40px;height:40px;background:#16a34a;border-radius:50%;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:20px}
.title{font-weight:700;font-size:16px}
.subtitle{font-size:12px;color:#666}
.chat{flex:1;overflow-y:auto;padding:20px 16px;padding-bottom:90px}
.msg{max-width:85%;padding:12px 14px;border-radius:18px;margin:10px 0;line-height:1.4}
.user{margin-left:auto;background:#111;color:white;border-bottom-right-radius:4px}
.bot{background:#f3f3f3;color:#111;border-bottom-left-radius:4px}
.input-bar{position:fixed;bottom:0;left:0;right:0;background:white;border-top:1px solid #eee;padding:10px 12px;display:flex;align-items:center;gap:8px}
.input-bar input{flex:1;background:#f3f3f3;border:none;padding:12px 16px;border-radius:25px;outline:none;font-size:15px}
.icon-btn{width:42px;height:42px;border-radius:50%;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
.send{background:#111;color:white}
.mic{background:#f3f3f3}
</style>
</head>
<body>
<div class="header">
<div class="logo">P</div>
<div>
<div class="title">{{app_name}}</div>
<div class="subtitle">{{by_text}}</div>
</div>
</div>
<div class="chat" id="chat">
<div class="msg bot">{{welcome_msg}}</div>
</div>
<div class="input-bar">
<button class="icon-btn mic" onclick="startVoice()">🎤</button>
<input id="inp" placeholder="Message {{app_name}}..." onkeydown="if(event.key==='Enter')send()">
<button class="icon-btn send" onclick="send()">↑</button>
</div>
<script>
async function send(){
let i=document.getElementById('inp');let t=i.value.trim();if(!t)return;
let c=document.getElementById('chat');
c.innerHTML+=`<div class='msg user'>${t}</div>`;i.value='';c.scrollTop=c.scrollHeight;
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
let d=await r.json();
c.innerHTML+=`<div class='msg bot'>${d.reply}</div>`;c.scrollTop=c.scrollHeight;
}
function startVoice(){
let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang='hi-IN';rec.start();
rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript}
}
</script>
</body>
</html>
"""

ADMIN_PAGE = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{font-family:system-ui;padding:20px;max-width:600px;margin:auto}input,textarea,select{width:100%;padding:10px;margin:6px 0 12px;border:1px solid #ccc;border-radius:8px}button{padding:12px 20px;background:#16a34a;color:white;border:none;border-radius:8px;cursor:pointer;width:100%}</style></head><body>
<h2>ApexBro Admin - Potenza Group</h2>
<form method="POST">
<label>App Name</label><input name="app_name" value="{{c.app_name}}">
<label>By Text (Upar wala)</label><input name="by_text" value="{{c.by_text}}">
<label>Welcome Message</label><textarea name="welcome_msg">{{c.welcome_msg}}</textarea>
<label>System Prompt (AI ka dimag)</label><textarea name="system_prompt">{{c.system_prompt}}</textarea>
<label>Model</label><select name="model"><option {{'selected' if c.model=='llama-3.1-8b-instant'}} >llama-3.1-8b-instant</option><option {{'selected' if c.model=='llama-3.3-70b-versatile'}}>llama-3.3-70b-versatile</option></select>
<button type="submit">Save</button>
</form>
<p><a href="/">Back to App</a></p></body></html>
"""

@app.route("/")
def home():
    cfg=load_config()
    return render_template_string(HTML_PAGE, app_name=cfg['app_name'], by_text=cfg['by_text'], welcome_msg=cfg['welcome_msg'])

@app.route("/chat", methods=["POST"])
def chat():
    cfg=load_config()
    user_msg=request.json.get("message","")
    try:
        chat_completion=client.chat.completions.create(
            messages=[{"role":"system","content":cfg['system_prompt']},{"role":"user","content":user_msg}],
            model=cfg['model']
        )
        reply=chat_completion.choices[0].message.content
    except Exception as e:
        reply=f"Error: {str(e)}"
    return jsonify({"reply":reply})

@app.route("/admin", methods=["GET","POST"])
def admin():
    cfg=load_config()
    if request.method=="POST":
        cfg['app_name']=request.form.get('app_name',cfg['app_name'])
        cfg['by_text']=request.form.get('by_text',cfg['by_text'])
        cfg['welcome_msg']=request.form.get('welcome_msg',cfg['welcome_msg'])
        cfg['system_prompt']=request.form.get('system_prompt',cfg['system_prompt'])
        cfg['model']=request.form.get('model',cfg['model'])
        save_config(cfg)
    return render_template_string(ADMIN_PAGE, c=cfg)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
