import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI - Potenza Group</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui;background:#0f0f0f;color:#fff;height:100dvh;display:flex;flex-direction:column}
.header{padding:15px;text-align:center;border-bottom:1px solid #222;font-weight:bold;display:flex;justify-content:center;align-items:center;gap:8px}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:10px 14px;border-radius:18px;font-size:15px;white-space:pre-wrap;position:relative}
.user{align-self:flex-end;background:#0084ff}
.bot{align-self:flex-start;background:#222;padding-right:40px}
.bar{display:flex;gap:6px;padding:10px;background:#151515;border-top:1px solid #222;align-items:center}
input{flex:1;padding:12px 15px;border-radius:25px;border:none;background:#222;color:#fff;outline:none}
button{width:45px;height:45px;border-radius:50%;border:none;font-size:18px;cursor:pointer}
.send{background:#00ff88}
.mic{background:#333;color:#fff}
.mic.listening{background:#ff0040;animation:pulse 1s infinite}
.speak{position:absolute;right:5px;bottom:5px;background:none;border:none;font-size:16px;cursor:pointer;width:30px;height:30px}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
</style></head>
<body>
<div class="header">🤖 ApexBro AI - by Potenza Group 🎙️</div>
<div id="chat"><div class="msg bot">Hi! Main ApexBro hu, built by Potenza Group. Bolo ya mic dabake bolo! <button class='speak' onclick="speakText(this)">🔊</button></div></div>
<div class="bar">
<button class="mic" id="micBtn" onclick="toggleMic()">🎤</button>
<input id="q" placeholder="Message or mic dabao..." onkeypress="if(event.key==='Enter')send()">
<button class="send" onclick="send()">➤</button>
</div>
<script>
let recognition;
let isListening=false;

if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang='hi-IN';
  recognition.continuous=false;
  recognition.interimResults=false;
  recognition.onstart=()=>{isListening=true; document.getElementById('micBtn').classList.add('listening'); document.getElementById('micBtn').innerText='🔴';}
  recognition.onend=()=>{isListening=false; document.getElementById('micBtn').classList.remove('listening'); document.getElementById('micBtn').innerText='🎤';}
  recognition.onresult=(e)=>{
    let text=e.results[0][0].transcript;
    document.getElementById('q').value=text;
    send();
  }
  recognition.onerror=(e)=>{alert('Mic error: '+e.error); isListening=false; document.getElementById('micBtn').classList.remove('listening'); document.getElementById('micBtn').innerText='🎤';}
}

function toggleMic(){
  if(!recognition){alert('Mic support nahi hai is browser me, Chrome use karo'); return;}
  if(isListening){recognition.stop();}else{recognition.start();}
}

function speakText(btn){
  let text = btn.parentElement.innerText.replace('🔊','').trim();
  let utter = new SpeechSynthesisUtterance(text);
  utter.lang='hi-IN';
  utter.rate=0.9;
  speechSynthesis.speak(utter);
}

async function send(){
 let i=document.getElementById('q'),t=i.value.trim(); if(!t)return;
 let c=document.getElementById('chat'); c.innerHTML+=`<div class='msg user'>${t}</div>`; i.value=''; c.scrollTop=c.scrollHeight;
 c.innerHTML+=`<div id='tmp' class='msg bot'>Soch raha hu...</div>`;
 try{
  let r=await fetch('/ask?q='+encodeURIComponent(t));
  let d=await r.json();
  let ans = d.answer||d.error||'No reply';
  document.getElementById('tmp').remove();
  c.innerHTML+=`<div class='msg bot'>${ans.replace(/\\n/g,'<br>')}<button class='speak' onclick="speakText(this)">🔊</button></div>`;
  // Auto speak
  let utter = new SpeechSynthesisUtterance(ans);
  utter.lang = /[\\u0900-\\u097F]/.test(ans)? 'hi-IN' : 'en-IN';
  utter.rate=0.9;
  speechSynthesis.speak(utter);
 }catch(e){document.getElementById('tmp').remove(); c.innerHTML+=`<div class='msg bot'>Error: ${e}</div>`;}
 c.scrollTop=c.scrollHeight;
}
</script></body></html>
"""

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    if not q:
        return jsonify({"error":"q missing"})
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are ApexBro AI, created by Potenza Group. You are a helpful, friendly AI assistant built by Potenza Group. Never say you are OpenAI or ChatGPT. If someone asks who built you, always say 'I was built by Potenza Group - ApexBro AI'. Keep answers short for voice. Always reply in same language user uses."},
                {"role":"user","content":q}
            ]
        )
        return jsonify({"answer": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
