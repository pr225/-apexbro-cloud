import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI - Potenza Group</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui;background:#fff;color:#111;height:100dvh;display:flex;flex-direction:column}
.header{padding:12px 14px;border-bottom:1px solid #e5e5e5;display:flex;align-items:center;gap:10px;background:#fff;position:sticky;top:0}
.logo{width:34px;height:34px;background:#00c950;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px}
.h1{font-weight:700;font-size:15px}
.h2{font-size:11px;color:#666}
#chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:16px;background:#fff}
.msg{max-width:96%;font-size:14.5px;line-height:1.6;white-space:pre-wrap;word-wrap:break-word}
.user{align-self:flex-end;background:#f1f1f1;padding:10px 14px;border-radius:18px;max-width:85%}
.bot{align-self:flex-start;width:100%}
.bot table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden}
.bot th{background:#f5f5f5;padding:8px;text-align:left;border-bottom:1px solid #e5e5e5}
.bot td{padding:8px;border-top:1px solid #eee}
.src{margin-top:10px;font-size:11px;color:#666;border-top:1px solid #eee;padding-top:8px}
.src span{background:#eef2ff;color:#4f46e5;padding:2px 7px;border-radius:10px;margin-right:4px;display:inline-block}
.bar{padding:10px;border-top:1px solid #e5e5e5;display:flex;gap:8px;background:#fff;align-items:center}
.inp{flex:1;background:#f4f4f4;border:1px solid #e5e5e5;border-radius:24px;display:flex;align-items:center;padding:4px 4px 4px 12px}
.inp input{flex:1;border:none;background:transparent;outline:none;font-size:15px;padding:6px}
.btn-send{width:32px;height:32px;border-radius:50%;border:none;background:#000;color:#fff;cursor:pointer}
.btn-mic{width:40px;height:40px;border-radius:50%;border:none;background:#111;color:#fff;cursor:pointer;font-size:18px}
.btn-mic.on{background:red}
</style>
</head>
<body>
<div class="header"><div class="logo">P</div><div><div class="h1">ApexBro AI</div><div class="h2">by Potenza Group - White ChatGPT Theme</div></div></div>
<div id="chat"><div class="msg bot">Hi! Mai ApexBro hu, Potenza Group ne banaya hai. Ab white ChatGPT theme me hu. Pucho kuch bhi! 👋</div></div>
<div class="bar">
<div class="inp"><input id="q" placeholder="Message ApexBro..."><button class="btn-send" id="sendBtn">↑</button></div>
<button class="btn-mic" id="micBtn">🎤</button>
</div>
<script>
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
let rec=null;
if(SR){rec=new SR();rec.lang='hi-IN';rec.continuous=false;}
let mic=document.getElementById('micBtn');
let chat=document.getElementById('chat');
let voice=null;
function loadV(){let v=speechSynthesis.getVoices();voice=v.find(a=>a.name.includes('Male'))||v[0];}
speechSynthesis.onvoiceschanged=loadV;loadV();

mic.onclick=()=>{
  if(!rec){alert('Chrome me kholo');return;}
  speechSynthesis.cancel();
  rec.start();mic.classList.add('on');mic.innerText='●';
  rec.onresult=(e)=>{let t=e.results[0][0].transcript;addUser(t);getAns(t,true);};
  rec.onend=()=>{mic.classList.remove('on');mic.innerText='🎤';};
};

document.getElementById('sendBtn').onclick=sendText;
document.getElementById('q').onkeypress=(e)=>{if(e.key==='Enter')sendText()};

function addUser(t){chat.innerHTML+=`<div class="msg user">${t}</div>`;chat.scrollTop=chat.scrollHeight;}

function sendText(){
  let i=document.getElementById('q');let t=i.value.trim();if(!t)return;
  speechSynthesis.cancel();
  addUser(t);i.value='';getAns(t,false);
}

async function getAns(text,shouldSpeak){
  let id='t'+Date.now();
  chat.innerHTML+=`<div class="msg bot" id="${id}">● ● ● soch raha hu...</div>`;chat.scrollTop=chat.scrollHeight;
  try{
    let r=await fetch('/ask?q='+encodeURIComponent(text));
    let d=await r.json();
    document.getElementById(id).remove();
    let html=marked.parse(d.answer||'error');
    let src=`<div class="src">🔍 Sources: <span>UP Dairy Dept</span> <span>NDDB 2025</span> <span>Market Survey</span></div>`;
    chat.innerHTML+=`<div class="msg bot">${html}${src}</div>`;
    chat.scrollTop=chat.scrollHeight;
    if(shouldSpeak){
      let clean=(d.answer||'').replace(/[#*|_`]/g,'').substring(0,500);
      let u=new SpeechSynthesisUtterance(clean);
      if(voice)u.voice=voice;u.rate=0.95;
      speechSynthesis.speak(u);
    }
  }catch(e){
    document.getElementById(id).remove();
    chat.innerHTML+=`<div class="msg bot">Error: network</div>`;
  }
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/ask")
def ask():
    q = request.args.get("q","").strip()
    if not q:
        return jsonify({"answer":"Pucho kuch?"})
    try:
        system_prompt = "You are ApexBro AI, built by Potenza Group. You answer like ChatGPT. Use markdown tables with | header |. For business questions give Investment, Production, Expense, Profit tables. Indian context. No ** inside table cells. Reply in same language as user. Never say you are OpenAI."
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":q}
            ],
            temperature=0.6,
            max_tokens=1800
        )
        ans = resp.choices[0].message.content
        return jsonify({"answer": ans})
    except Exception as e:
        return jsonify({"answer": f"Server Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
