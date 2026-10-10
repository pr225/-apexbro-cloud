import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui;background:#0f0f0f;color:#fff;height:100dvh;display:flex;flex-direction:column}
.header{padding:14px;text-align:center;border-bottom:1px solid #222;font-weight:bold}
#chat{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:11px 15px;border-radius:18px;font-size:15px;white-space:pre-wrap}
.user{align-self:flex-end;background:#0084ff}
.bot{align-self:flex-start;background:#222}
.bar{display:flex;gap:6px;padding:10px;background:#151515;border-top:1px solid #222;align-items:center}
input{flex:1;padding:12px 15px;border-radius:25px;border:none;background:#222;color:#fff;outline:none}
button{width:44px;height:44px;border-radius:50%;border:none;font-size:18px;cursor:pointer}
.send{background:#00ff88}
.mic{background:#333;color:#fff}
</style></head>
<body>
<div class="header">🤖 ApexBro AI - Potenza Group</div>
<div id="chat"><div class="msg bot">Ab type karoge to nahi bolunga, mic se bologe tabhi bolunga!</div></div>
<div class="bar">
<button class="mic" id="micBtn">🎤</button>
<input id="q" placeholder="Type karo...">
<button class="send" id="sendBtn">➤</button>
</div>
<script>
let selectedVoice=null;
function loadVoices(){ let v=speechSynthesis.getVoices(); selectedVoice=v.find(x=>x.name.includes('Male'))||v[0]; }
speechSynthesis.onvoiceschanged=loadVoices; loadVoices();
speechSynthesis.cancel();

const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
let rec;
if(SR){ rec=new SR(); rec.lang='en-IN'; rec.continuous=false; }

document.getElementById('micBtn').onclick=()=>{
  if(!rec){alert('Chrome me kholo');return;}
  rec.start();
  document.getElementById('micBtn').innerText='🔴';
  rec.onresult=(e)=>{
    let text=e.results[0][0].transcript;
    addMsg(text,'user');
    document.getElementById('micBtn').innerText='🎤';
    fetchAnswer(text,true);
  };
  rec.onend=()=>{document.getElementById('micBtn').innerText='🎤';};
};

document.getElementById('sendBtn').onclick=sendText;
document.getElementById('q').onkeypress=(e)=>{if(e.key==='Enter')sendText()};

function addMsg(t,c){ let ch=document.getElementById('chat'); ch.innerHTML+=`<div class='msg ${c}'>${t}</div>`; ch.scrollTop=ch.scrollHeight; }

function sendText(){
  let i=document.getElementById('q'), t=i.value.trim(); if(!t)return;
  speechSynthesis.cancel();
  addMsg(t,'user'); i.value='';
  fetchAnswer(t,false);
}

async function fetchAnswer(text, speak){
  let ch=document.getElementById('chat'); ch.innerHTML+=`<div class='msg bot' id='tmp'>...</div>`;
  let r=await fetch('/ask?q='+encodeURIComponent(text));
  let d=await r.json();
  document.getElementById('tmp').remove();
  addMsg(d.answer||'Error','bot');
  if(speak){
    let u=new SpeechSynthesisUtterance(d.answer);
    if(selectedVoice) u.voice=selectedVoice;
    u.rate=0.92; u.pitch=0.9;
    speechSynthesis.speak(u);
  }else{
    speechSynthesis.cancel();
  }
}
</script></body></html>
"""
@app.route("/ask")
def ask():
    q=request.args.get("q","")
    try:
        resp=client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role":"system","content":"You are ApexBro AI built by Potenza Group. Friendly helpful assistant. Reply short. Same language as user."},{"role":"user","content":q}])
        return jsonify({"answer": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": str(e)})
if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
