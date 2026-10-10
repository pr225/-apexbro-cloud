import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Groq setup
from groq import Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# HTML - Mic Left me hai
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ApexBro AI</title>
<style>
body{margin:0;font-family:Arial;background:#fff;display:flex;flex-direction:column;height:100vh}
.header{padding:14px;border-bottom:1px solid #eee;display:flex;gap:10px;align-items:center}
.logo{width:36px;height:36px;background:#16a34a;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow:auto;padding:15px;padding-bottom:90px}
.bubble{padding:12px 14px;border-radius:18px;margin:8px 0;max-width:80%;line-height:1.4}
.user{margin-left:auto;background:#000;color:#fff}
.bot{background:#f1f1f1;color:#000}
.bar{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #eee;display:flex;gap:8px;padding:10px;align-items:center}
.bar input{flex:1;padding:12px 16px;border-radius:24px;border:none;background:#f1f1f1;outline:none}
.btn{width:44px;height:44px;border-radius:50%;border:none;cursor:pointer}
.send{background:#000;color:#fff}
.mic{background:#eee}
</style>
</head>
<body>
<div class="header">
<div class="logo">P</div>
<div><b>ApexBro AI</b><div style="font-size:12px;color:#666">by Potenza Group - White ChatGPT Theme</div></div>
</div>
<div class="chat" id="chat">
<div class="bubble bot">Hi! Mai ApexBro hu, Potenza Group ne banaya hai. Ab white ChatGPT theme me hu. Pucho kuch bhi! 👋</div>
</div>
<div class="bar">
<button class="btn mic" onclick="voice()">🎤</button>
<input id="msg" placeholder="Message ApexBro..." onkeypress="if(event.key==='Enter')send()">
<button class="btn send" onclick="send()">↑</button>
</div>
<script>
async function send(){
 let inp=document.getElementById('msg');
 let t=inp.value.trim(); if(!t) return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=`<div class='bubble user'>${t}</div>`;
 inp.value=''; chat.scrollTop=chat.scrollHeight;
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({m:t})});
 let data=await res.json();
 chat.innerHTML+=`<div class='bubble bot'>${data.r}</div>`;
 chat.scrollTop=chat.scrollHeight;
}
function voice(){
 let R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Mic support nahi hai');return}
 let r=new R(); r.lang='hi-IN'; r.start();
 r.onresult=e=>{document.getElementById('msg').value=e.results[0][0].transcript}
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        m = request.json.get("m", "")
        comp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are ApexBro AI, made by Potenza Group. Helpful, friendly, Hindi+English."},
                {"role": "user", "content": m}
            ]
        )
        return jsonify({"r": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"r": f"Error: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
