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
.header{padding:14px;text-align:center;border-bottom:1px solid #222;font-weight:bold}
#chat{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:11px 15px;border-radius:18px;font-size:15px;white-space:pre-wrap;line-height:1.4}
.user{align-self:flex-end;background:#0084ff}
.bot{align-self:flex-start;background:#222}
.bar{display:flex;gap:6px;padding:10px;background:#151515;border-top:1px solid #222;align-items:center}
input{flex:1;padding:12px 15px;border-radius:25px;border:none;background:#222;color:#fff;outline:none}
button{width:44px;height:44px;border-radius:50%;border:none;font-size:18px;cursor:pointer}
.send{background:#00ff88}
.mic{background:#333;color:#fff}
.mic.on{background:#ff0040;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
</style></head>
<body>
<div class="header">🤖 ApexBro AI - Potenza Group</div>
<div id="chat"><div class="msg bot">Hi! Type karo to mai text me jawab dunga, Mic se bolo to bolke jawab dunga!</div></div>
<div class="bar">
<button class="mic" id="micBtn" onclick="startVoice()">🎤</button>
<input id="q" placeholder="Type here..." onkeypress="if(event.key==='Enter')sendText()">
<button class="send" onclick="sendText()">➤</button>
</div>
<script>
let recognition;
let selectedVoice=null;
function loadVoices(){ let v=speechSynthesis.getVoices(); selectedVoice=v.find(x=>x.name.includes('Google UK English Male'))||v.find(x=>x.name.includes('Male'))||v.find(x=>x.lang=='en-IN')||v[0]; }
speechSynthesis.onvoiceschanged=loadVoices; loadVoices();

const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SR){
  recognition=new SR(); recognition.lang='en-IN'; recognition.continuous=false;
  recognition.onstart=()=>{document.getElementById('micBtn').classList.add('on'); document.getElementById('micBtn').innerText='🔴';}
  recognition.onend=()=>{document.getElementById('micBtn').classList.remove('on'); document.getElementById('micBtn').innerText='🎤';}
  recognition.onresult=(e)=>{
    let text=e.results[0][0].transcript;
    addMsg(text,'user');
    callAI(text,true);
  };
}

function addMsg(t,c){ let ch=document.getElementById('chat'); ch.innerHTML+=`<div class='msg ${c}'>${t}</div>`; ch.scrollTop=ch.scrollHeight; }

function startVoice(){ if(!recognition){alert('Chrome use karo');return;} try{recognition.start();}catch{} }

async function sendText(){
  let i=document.getElementById('q'), t=i.value.trim(); if(!t)return;
  addMsg(t,'user'); i.value='';
  callAI(t,false);
}

async function callAI(text, shouldSpeak){
  addMsg('...','bot'); let tmp=document.querySelectorAll('.msg.bot'); let last=tmp[tmp.length-1]; last.id='tmp';
  try{
    let r=await fetch('/ask?q='+encodeURIComponent(text));
    let d=await r.json();
    let ans=d.answer||'Error';
    document.getElementById('tmp').remove();
    addMsg(ans,'bot');
    if(shouldSpeak){
      speechSynthesis.cancel();
      let u=new SpeechSynthesisUtterance(ans);
      if(selectedVoice) u.voice=selectedVoice;
      u.rate=0.93; u.pitch=0.9;
      speechSynthesis.speak(u);
    }
  }catch(e){ document.getElementById('tmp').remove(); addMsg('Error: '+e,'bot'); }
}
</script></body></html>
"""

@app.route("/ask")
def ask():
    q=request.args.get("q","")
    try:
        resp=client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system","content":"You are ApexBro AI built by Potenza Group. Friendly, ChatGPT-like, natural male. Keep answers short and helpful. Reply in user's language. If asked who built you, say Potenza Group."},
                {"role":"user","content":q}
            ]
        )
        return jsonify({"answer": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer":"Error: "+str(e)})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
