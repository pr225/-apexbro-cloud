import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML = """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI</title>
<style>
body{margin:0;font-family:system-ui,Arial;background:#fff;height:100vh;display:flex;flex-direction:column}
.top{padding:12px 16px;border-bottom:1px solid #eee;display:flex;gap:10px;align-items:center;flex-shrink:0}
.logo{width:36px;height:36px;background:#16a34a;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px}
.chat{flex:1;overflow:auto;padding:16px;padding-bottom:110px}
.msg{padding:12px 16px;border-radius:18px;margin:10px 0;max-width:85%;line-height:1.6;white-space:pre-wrap;font-size:15px}
.user{background:#000;color:#fff;margin-left:auto;border-bottom-right-radius:4px}
.bot{background:#f3f3f3;color:#000;border-bottom-left-radius:4px}

/* ChatGPT wala bottom bar - FINAL */
.bar{position:fixed;bottom:0;left:0;right:0;padding:12px;background:#fff;display:flex;justify-content:center}
.box{width:100%;max-width:750px;display:flex;align-items:center;gap:8px;background:#f4f4f4;border-radius:28px;padding:6px 8px 6px 8px;box-shadow:0 1px 8px rgba(0,0,0,0.06)}
.mic{width:40px;height:40px;border-radius:50%;border:none;background:transparent;font-size:18px;cursor:pointer;flex-shrink:0}
.mic:hover{background:#e8e8e8}
.box input{flex:1;background:transparent;border:none;outline:none;padding:12px 4px;font-size:16px}
.send{width:36px;height:36px;border-radius:50%;border:none;background:#000;color:#fff;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
</style></head>
<body>
<div class="top"><div class="logo">P</div><div><b>ApexBro AI</b><div style="font-size:12px;color:gray">by Potenza Group - White ChatGPT Theme</div></div></div>

<div class="chat" id="c"><div class="msg bot">Hi! Main ApexBro hu 👋 Jo puchna ho pucho!</div></div>

<div class="bar">
<div class="box">
<button class="mic" onclick="voice()" title="Bolke pucho">🎤</button>
<input id="i" placeholder="Jo puchna ho pucho..." onkeydown="if(event.key==='Enter')send()">
<button class="send" onclick="send()">↑</button>
</div>
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
 if(!R){alert('Is browser me mic nahi');return}
 let rec=new R();rec.lang='hi-IN';rec.start();
 rec.onresult=e=>{document.getElementById('i').value=e.results[0][0].transcript}
}
</script>
</body></html>"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    m=request.json.get("m","")
    comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":m}])
    return jsonify({"r":comp.choices[0].message.content})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
