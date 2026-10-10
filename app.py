import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Groq - safe import
try:
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    client = None
    print("Groq Error:", e)

HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro PRO</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial;display:flex;height:100vh;background:#fff;overflow:hidden}
.side{width:260px;background:#171717;color:#fff;display:flex;flex-direction:column;padding:10px}
.new{background:#fff;color:#000;padding:12px;border-radius:10px;text-align:center;cursor:pointer;font-weight:bold;margin-bottom:10px}
.list{flex:1;overflow:auto}.item{padding:10px;border-radius:8px;cursor:pointer;font-size:14px;color:#ddd;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.item:hover{background:#2f2f2f}
.main{flex:1;display:flex;flex-direction:column}
.top{padding:12px;border-bottom:1px solid #eee;display:flex;gap:10px;align-items:center}
.logo{width:36px;height:36px;background:#16a34a;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow:auto;padding:16px;padding-bottom:110px}
.row{display:flex;gap:10px;margin:14px auto;max-width:800px}
.av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;flex-shrink:0}
.u{background:#000;color:#fff}.b{background:#16a34a;color:#fff}
.bub{flex:1;line-height:1.5;padding-top:4px;white-space:pre-wrap}
.bar{position:absolute;bottom:0;left:0;right:0;background:#fff;padding:15px;display:flex;justify-content:center}
.box{width:100%;max-width:800px;background:#f1f1f1;border-radius:28px;display:flex;gap:6px;padding:8px;align-items:center}
.box input{flex:1;background:transparent;border:none;outline:none;padding:10px;font-size:16px}
.box button{width:42px;height:42px;border-radius:50%;border:none;cursor:pointer}
.send{background:#000;color:#fff}
</style></head>
<body>
<div class="side">
<div class="new" onclick="newC()">+ New Chat</div>
<div class="list" id="list"></div>
<div style="font-size:11px;color:#888;padding:10px">by Potenza Group - PRO</div>
</div>
<div class="main" style="position:relative">
<div class="top"><div class="logo">P</div><div><b>ApexBro AI PRO</b><div style="font-size:12px;color:gray">by Potenza Group</div></div></div>
<div class="chat" id="chat"></div>
<div class="bar"><div class="box">
<button onclick="voice()" style="background:transparent">🎤</button>
<input id="inp" placeholder="Message ApexBro..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()" class="send">↑</button>
</div></div>
</div>
<script>
let chats=JSON.parse(localStorage.getItem('apex')||'[]');let cur=null;
function render(){let l=document.getElementById('list');l.innerHTML='';chats.slice().reverse().forEach(c=>{let d=document.createElement('div');d.className='item';d.innerText=c.title;d.onclick=()=>load(c.id);l.appendChild(d)})}
function newC(){cur=Date.now()+'';chats.push({id:cur,title:'New Chat',msgs:[{r:'bot',t:'Hi! Mai ApexBro PRO hu 👋 Left me history hai.'}]});save();render();load(cur)}
function load(id){cur=id;let c=chats.find(x=>x.id==id);let ch=document.getElementById('chat');ch.innerHTML='';c.msgs.forEach(m=>add(m.t,m.r,false));ch.scrollTop=ch.scrollHeight}
function add(t,r,s=true){let ch=document.getElementById('chat');let row=document.createElement('div');row.className='row';row.innerHTML=`<div class="av ${r=='user'?'u':'b'}">${r=='user'?'U':'P'}</div><div class="bub">${t}</div>`;ch.appendChild(row);ch.scrollTop=ch.scrollHeight;if(s&&cur){let c=chats.find(x=>x.id==cur);c.msgs.push({r:r,t:t});if(c.msgs.length==2)c.title=t.slice(0,28);save();render()}}
async function send(){let i=document.getElementById('inp');let t=i.value.trim();if(!t)return;if(!cur)newC();add(t,'user');i.value='';let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({m:t})});let d=await res.json();add(d.r,'bot')}
function save(){localStorage.setItem('apex',JSON.stringify(chats))}
function voice(){let R=window.SpeechRecognition||window.webkitSpeechRecognition;if(!R){alert('Mic support nahi');return}let rec=new R();rec.lang='hi-IN';rec.start();rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript}}
if(chats.length==0)newC();else{render();load(chats[chats.length-1].id)}
</script>
</body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        if not client:
            return jsonify({"r": "GROQ_API_KEY Render me set nahi hai! Render > Environment me jao."})
        m = request.json.get("m","")
        comp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":m}]
        )
        return jsonify({"r": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"r": f"Error aaya: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
