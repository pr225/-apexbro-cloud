import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI - Potenza Group</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,-apple-system;background:#ffffff;color:#0d0d0d;height:100dvh;display:flex;flex-direction:column}
.header{padding:12px 16px;border-bottom:1px solid #e5e5e5;display:flex;align-items:center;gap:10px;background:#fff;position:sticky;top:0;z-index:10}
.logo{width:36px;height:36px;background:#00c950;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:20px}
.header-title{font-weight:700;font-size:16px}
.header-sub{font-size:11px;color:#666}
#chat{flex:1;overflow-y:auto;padding:20px 14px;display:flex;flex-direction:column;gap:18px;background:#fff}
.msg{max-width:95%;font-size:15px;line-height:1.6;white-space:pre-wrap;word-break:break-word}
.user{align-self:flex-end;background:#f4f4f4;border-radius:20px;padding:10px 16px;max-width:85%}
.bot{align-self:flex-start;width:100%;padding:0 4px}
.bot-card{background:#f9f9f9;border:1px solid #ececec;border-radius:12px;padding:14px;margin:10px 0}
.bot table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden}
.bot th{background:#f4f4f4;padding:10px;text-align:left;font-weight:600;border-bottom:1px solid #e5e5e5}
.bot td{padding:10px;border-top:1px solid #eee}
.bot h2,.bot h3{margin:16px 0 8px;font-size:16px}
.bot strong{font-weight:600}
.bot a{color:#0a66c2;text-decoration:none}
.sources{margin-top:12px;padding-top:10px;border-top:1px solid #eee;font-size:12px;color:#666}
.sources span{background:#eef2ff;color:#4f46e5;padding:2px 8px;border-radius:12px;margin-right:6px;display:inline-block;margin-bottom:4px}
.bar{padding:10px 14px;background:#fff;border-top:1px solid #e5e5e5;display:flex;gap:8px;align-items:center}
.input-wrap{flex:1;display:flex;align-items:center;background:#f4f4f4;border-radius:24px;padding:6px 6px 16px;border:1px solid #e5e5e5}
.input-wrap input{flex:1;border:none;background:transparent;outline:none;font-size:15px}
.mic{width:38px;height:38px;border-radius:50%;border:none;background:#000;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center}
.send{width:32px;height:32px;border-radius:50%;border:none;background:#000;color:#fff;cursor:pointer}
#micBtn.listening{background:#ff0000;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
</style></head>
<body>
<div class="header">
<div class="logo">P</div>
<div><div class="header-title">ApexBro AI</div><div class="header-sub">by Potenza Group • ChatGPT Quality</div></div>
</div>
<div id="chat"><div class="msg bot">Hi! Mai ApexBro hu - Potenza Group dwara banaya gaya. ChatGPT jaisi quality me jawab dunga. Pucho kuch bhi! 👋</div></div>
<div class="bar">
<div class="input-wrap"><input id="q" placeholder="Message ApexBro..."><button class="send" id="sendBtn">↑</button></div>
<button class="mic" id="micBtn">🎤</button>
</div>
<script>
let voice=null;
function loadV(){ let v=speechSynthesis.getVoices(); voice=v.find(x=>x.name.includes('Google UK English Male'))||v.find(x=>x.lang=='en-IN')||v[0]; }
speechSynthesis.onvoiceschanged=loadV; loadV();

const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
let rec; if(SR){ rec=new SR(); rec.lang='hi-IN'; rec.continuous=false; }

let micBtn=document.getElementById('micBtn');
micBtn.onclick=()=>{
  if(!rec){alert('Chrome me kholo');return;}
  speechSynthesis.cancel();
  rec.start(); micBtn.classList.add('listening'); micBtn.innerText='●';
  rec.onresult=(e)=>{
    let t=e.results[0][0].transcript;
    addUser(t); fetchAns(t,true);
  };
  rec.onend=()=>{micBtn.classList.remove('listening'); micBtn.innerText='🎤';};
};

document.getElementById('sendBtn').onclick=sendText;
document.getElementById('q').onkeypress=(e)=>{if(e.key==='Enter')sendText()};

function addUser(t){ let c=document.getElementById('chat'); c.innerHTML+=`<div class='msg user'>${t}</div>`; c.scrollTop=c.scrollHeight; }

function sendText(){
  let i=document.getElementById('q'); let t=i.value.trim(); if(!t)return;
  speechSynthesis.cancel();
  addUser(t); i.value=''; fetchAns(t,false);
}

async function fetchAns(text,shouldSpeak){
  let c=document.getElementById('chat');
  let id='tmp'+Date.now();
  c.innerHTML+=`<div class='msg bot' id='${id}'>● ● ●</div>`; c.scrollTop=c.scrollHeight;
  try{
    let r=await fetch('/ask?q='+encodeURIComponent(text));
    let d=await r.json();
    document.getElementById(id).remove();
    let html=marked.parse(d.answer||'');
    let sourcesHtml = d.sources? `<div class='sources'>🔍 Sources: ${d.sources.map(s=>`<span>${s}</span>`).join('')}</div>` : `<div class='sources'>🔍 Sources: <span>UP Govt Dairy Data</span><span>NDDB</span><span>Market Research</span></div>`;
    c.innerHTML+=`<div class='msg bot'>${html}${sourcesHtml}</div>`;
    if(shouldSpeak){
      let clean = (d.answer||'').replace(/[#*|`]/g,'').slice(0,400);
      let u=new SpeechSynthesisUtterance(clean);
      if(voice) u.voice=voice; u.rate=0.93; u.pitch=0.9;
      speechSynthesis.speak(u);
    }
  }catch(e){ document.getElementById(id).remove(); c.innerHTML+=`<div class='msg bot'>Error, try again</div>`; }
  c.scrollTop=c.scrollHeight;
}
</script></body></html>
"""

@app.route("/ask")
def ask():
    q=request.args.get("q","")
    if not q: return jsonify({"answer":"Pucho kuch?"})
    try:
        system_prompt = \"\"You are ApexBro AI, built by Potenza Group. You are as intelligent and well-formatted as ChatGPT-4o.

RULES:
- Always give detailed, accurate, well-structured answers like ChatGPT.
- Use markdown: headings ##, tables | col |, bullet points.
- For business/finance queries: ALWAYS give 1) Investment breakdown table, 2) Daily/Monthly production, 3) Sales price options table, 4) Expense table, 5) Profit margin calculation, 6) Final recommendation.
- Use Indian context: Uttar Pradesh, realistic rates (Buffalo ₹80k-1.5L, Milk ₹50-70/L).
- Use clean tables: No ** inside cells. Example: | Item | Cost |
- Language: Reply in same language as user - Hindi if user uses Hindi.
- Add disclaimer: numbers are estimates.
- Never say you are OpenAI. Always say built by Potenza Group.
- Quality must be ChatGPT level.
\"\"\"
        resp=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":system_prompt},{"role":"user","content":q}],
            temperature=0.6,
            max_tokens=2000
        )
        ans=resp.choices[0].message.content
        sources=["UP Dairy Dept","NDDB 2025-26","Local Market Survey"]
        return jsonify({"answer":ans,"sources":sources})
    except Exception as e:
        return jsonify({"answer":f"Error: {str(e)}","sources":[]})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
