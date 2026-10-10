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
<title>ApexBro LIVE - Potenza Group</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui;background:#0a0a0a;color:#fff;height:100dvh;display:flex;flex-direction:column}
.header{padding:14px;text-align:center;border-bottom:1px solid #222;font-weight:bold;display:flex;justify-content:space-between;align-items:center}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:12px 16px;border-radius:18px;font-size:15px;white-space:pre-wrap;line-height:1.4}
.user{align-self:flex-end;background:#0084ff}
.bot{align-self:flex-start;background:#222}
.bar{display:flex;gap:8px;padding:12px;background:#151515;border-top:1px solid #222;align-items:center;justify-content:center}
.live-btn{padding:14px 28px;border-radius:30px;border:none;font-size:16px;font-weight:bold;cursor:pointer;transition:0.3s}
.live-off{background:#222;color:#fff;border:2px solid #333}
.live-on{background:#00ff88;color:#000;box-shadow:0 0 20px #00ff88;animation:pulse 1.5s infinite}
.small{font-size:12px;opacity:0.6;text-align:center;padding:5px}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.05)}100%{transform:scale(1)}}
</style></head>
<body>
<div class="header"><span>🤖 ApexBro LIVE</span><span style="font-size:11px;opacity:0.6">Potenza Group</span></div>
<div id="chat"><div class="msg bot">Live Mode ON karo, fir bas bolte jao... mai sununga aur bolunga. ChatGPT jaisa!</div></div>
<div class="small" id="status">Live OFF hai - button dabao</div>
<div class="bar">
<button id="liveBtn" class="live-btn live-off" onclick="toggleLive()">🎤 START LIVE</button>
</div>
<script>
let recognition;
let isLive=false;
let selectedVoice=null;
let isSpeaking=false;

function loadVoices(){
  let v = speechSynthesis.getVoices();
  selectedVoice = v.find(x=>x.name.includes('Google UK English Male')) || v.find(x=>x.name.includes('Male')) || v.find(x=>x.lang=='en-IN') || v[0];
}
speechSynthesis.onvoiceschanged=loadVoices; loadVoices();

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
if(SR){
  recognition = new SR();
  recognition.lang='en-IN';
  recognition.continuous=false;
  recognition.interimResults=false;
  recognition.onresult = (e)=>{
    let text = e.results[0][0].transcript;
    if(!text) return;
    addMsg(text,'user');
    callAI(text);
  };
  recognition.onend = ()=>{
    if(isLive &&!isSpeaking){ recognition.start(); document.getElementById('status').innerText='☀️ Sun raha hu... bolo'; }
  };
  recognition.onerror = (e)=>{ if(isLive) setTimeout(()=>{try{recognition.start()}catch{}},1000); };
}

function addMsg(t,cls){ let c=document.getElementById('chat'); c.innerHTML+=`<div class='msg ${cls}'>${t}</div>`; c.scrollTop=c.scrollHeight; }

function toggleLive(){
  let btn=document.getElementById('liveBtn');
  if(!isLive){
    isLive=true; btn.innerText='🔴 STOP LIVE'; btn.className='live-btn live-on';
    document.getElementById('status').innerText='🎧 Live ON - bolo kuch bhi';
    try{recognition.start()}catch{}
  }else{
    isLive=false; btn.innerText='🎤 START LIVE'; btn.className='live-btn live-off';
    document.getElementById('status').innerText='Live OFF hai';
    try{recognition.stop(); speechSynthesis.cancel();}catch{}
  }
}

async function callAI(text){
  isSpeaking=true;
  try{recognition.stop()}catch{}
  document.getElementById('status').innerText='🤔 Soch raha hu...';
  let r=await fetch('/ask?q='+encodeURIComponent(text));
  let d=await r.json();
  let ans=d.answer||'Sorry sun nahi paya';
  addMsg(ans,'bot');
  document.getElementById('status').innerText='🔊 Bol raha hu...';
  let utter = new SpeechSynthesisUtterance(ans);
  if(selectedVoice) utter.voice=selectedVoice;
  utter.rate=0.92; utter.pitch=0.9;
  utter.onend=()=>{
    isSpeaking=false;
    if(isLive){ document.getElementById('status').innerText='☀️ Sun raha hu... bolo'; try{recognition.start()}catch{} }
    else{ document.getElementById('status').innerText='Live OFF hai'; }
  };
  speechSynthesis.speak(utter);
}
</script></body></html>
"""

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are ApexBro LIVE, built by Potenza Group. You are in LIVE voice call mode. Talk like ChatGPT Advanced Voice - super friendly, natural, human-like male friend. Keep answers VERY short - 1 or 2 sentences max, because it's voice chat. No long paragraphs. No 'yaar' in every sentence, be natural. If user says hi, say hi back warmly."},
                {"role":"user","content":q}
            ]
        )
        return jsonify({"answer": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": "Thoda network issue hai, fir se bolo?"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
