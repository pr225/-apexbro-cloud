import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML = """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI</title>
<style>
body{margin:0;font-family:system-ui;background:#fff;height:100vh;display:flex;flex-direction:column}
.top{padding:12px;border-bottom:1px solid #eee;display:flex;gap:10px;align-items:center}
.logo{width:36px;height:36px;background:#16a34a;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow:auto;padding:16px;padding-bottom:90px}
.msg{padding:12px 16px;border-radius:18px;margin:8px 0;max-width:80%;line-height:1.5;white-space:pre-wrap}
.user{background:#000;color:#fff;margin-left:auto}
.bot{background:#f3f3f3;color:#000}
.bar{position:fixed;bottom:0;left:0;right:0;display:flex;gap:8px;padding:12px;background:#fff;border-top:1px solid #eee}
.bar input{flex:1;padding:12px 16px;border-radius:24px;border:none;background:#eee;outline:none;font-size:15px}
.bar button{width:44px;height:44px;border-radius:50%;border:none;cursor:pointer;font-size:18px}
</style></head>
<body>
<div class="top"><div class="logo">P</div><div><b>ApexBro AI</b><div style="font-size:12px;color:gray">by Potenza Group - White Theme</div></div></div>
<div class="chat" id="c"><div class="msg bot">Hi! Mai ApexBro hu, pucho kuch bhi! 👋</div></div>
<div class="bar">
<button onclick="voice()" style="background:#f3f3f3">🎤</button>
<input id="i" placeholder="Message..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()" style="background:#000;color:#fff">↑</button>
</div>
<script>
async function send(){
 let inp=document.getElementById('i');let t=inp.value.trim();if(!t)return;
 let ch=document.getElementById('c');ch.innerHTML+=`<div class='msg user'>${t}</div>`;inp.value='';
 ch.scrollTop=ch.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({m:t})});
 let d=await r.json();ch.innerHTML+=`<div class='msg bot'>${d.r}</div>`;ch.scrollTop=ch.scrollHeight;
}
function voice(){
 let R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Mic support nahi');return}
 let rec=new R();rec.lang='hi-IN';rec.start();
 rec.onresult=e=>{document.getElementById('i').value=e.results[0][0].transcript}
}
</script>
</body></html>"""

@app.route("/")
def home(): return HTML

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        m=request.json.get("m","")
        comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":m}])
        return jsonify({"r":comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"r":f"Error: {e}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
