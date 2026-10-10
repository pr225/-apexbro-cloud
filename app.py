import os
import json
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

# --- CONFIG ---
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "app_name": "ApexBro AI",
    "by_text": "by Potenza Group - White ChatGPT Theme",
    "welcome_msg": "Hi! Mai ApexBro hu, Potenza Group ne banaya hai. Ab white ChatGPT theme me hu. Pucho kuch bhi! 👋",
    "system_prompt": "You are ApexBro AI, created by Potenza Group. Be helpful, friendly, answer in Hindi + English mix.",
    "model": "llama-3.1-8b-instant"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(cfg):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(f, cfg, indent=2)
    except:
        pass

# Groq Client
groq_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_key) if groq_key else None

# --- MAIN UI ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{app_name}}</title>
<style>
body{margin:0;font-family:system-ui;background:white;color:#111;display:flex;flex-direction:column;height:100vh}
.header{padding:12px 16px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:12px;background:white}
.logo{width:40px;height:40px;background:#16a34a;border-radius:50%;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:20px}
.title{font-weight:700;font-size:16px}
.subtitle{font-size:12px;color:#666}
.chat{flex:1;overflow-y:auto;padding:20px 16px;padding-bottom:90px}
.msg{max-width:85%;padding:12px 14px;border-radius:18px;margin:10px 0;line-height:1.5;word-wrap:break-word}
.user{margin-left:auto;background:#111;color:white;border-bottom-right-radius:4px}
.bot{background:#f3f3f3;color:#111;border-bottom-left-radius:4px}
.input-bar{position:fixed;bottom:0;left:0;right:0;background:white;border-top:1px solid #eee;padding:10px 12px;display:flex;align-items:center;gap:8px}
.input-bar input{flex:1;background:#f3f3f3;border:none;padding:12px 16px;border-radius:25px;outline:none;font-size:15px}
.icon-btn{width:42px;height:42px;border-radius:50%;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;flex-shrink:0}
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
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  c.innerHTML+=`<div class='msg bot'>${d.reply}</div>`;
 }catch(e){
  c.innerHTML+=`<div class='msg bot'>Error: Server se connect nahi ho paya</div>`;
 }
 c.scrollTop=c.scrollHeight;
}
function startVoice(){
 let SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){alert('Voice not supported in this browser');return}
 let rec=new SR();rec.lang='hi-IN';rec.start();
 rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript}
}
</script>
</body>
</html>
"""

ADMIN_PAGE = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:system-ui;padding:20px;max-width:600px;margin:auto}input,textarea,select{width:100%;padding:10px;margin:6px 0 12px;border:1px solid #ccc;border-radius:8px;box-sizing:border-box}button{padding:12px 20px;background:#16a34a;color:white;border:none;border-radius:8px;cursor:pointer;width:100%;font-weight:bold}</style>
</head><body>
<h2>ApexBro Admin - Potenza Group</h2>
<form method="POST">
<label>App Name</label><input name="app_name" value="{{c.app_name}}">
<label>By Text (Upar wala)</label><input name="by_text" value="{{c.by_text}}">
<label>Welcome Message</label><textarea name="welcome_msg" rows
