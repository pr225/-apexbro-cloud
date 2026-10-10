import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

PRO_HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ApexBro AI - PRO</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui;display:flex;height:100vh;background:#fff;overflow:hidden}
.sidebar{width:260px;background:#171717;color:#fff;display:flex;flex-direction:column;padding:10px;transition:0.3s}
.newchat{background:#fff;color:#000;padding:12px;border-radius:10px;text-align:center;cursor:pointer;font-weight:600;margin-bottom:12px}
.newchat:hover{background:#ececec}
.hist{flex:1;overflow:auto}
.hist-item{padding:10px;border-radius:8px;cursor:pointer;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#ececec}
.hist-item:hover{background:#2f2f2f}
.main{flex:1;display:flex;flex-direction:column;background:#fff;position:relative}
.top{padding:14px 20px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:12px}
.logo{width:36px;height:36px;background:#16a34a;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow:auto;padding:20px;padding-bottom:120px}
.msg-row{display:flex;gap:12px;margin:18px auto;max-width:800px;width:100%}
.avatar{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;flex-shrink:0}
.user-av{background:#000;color:#fff}
.bot-av{background:#16a34a;color:#fff}
.bubble{flex:1;line-height:1.6;padding-top:4px;white-space:pre-wrap}
.input-wrap{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent, #fff 20%);padding:20px;display:flex;justify-content:center}
.input-box{width:100%;max-width:800px;background:#f4f4f4;border-radius:28px;display:flex;align-items:center;padding:8px 12px;gap:8px;box-shadow:0 0 10px rgba(0,0,0,0.05)}
.input-box input{flex:1;background:transparent;border:none;outline:none;padding:10px;font-size:16px}
.icon-btn{width:40px;height:40px;border-radius:50%;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
.mic-btn{background:transparent}
.send-btn{background:#000;color:#fff}
.menu-btn{display:none;background:none;color:#000;font-size:20px}
@media(max-width:768px){.sidebar{position:absolute;left:-260px;z-index:10;height:100%}.sidebar.open{left:0}.menu-btn{display:block}}
</style>
</head>
<body>
<div class="sidebar" id="sidebar">
<div class="newchat" onclick="newChat()"><i class="fa-solid fa-plus"></i> New Chat</div>
<div class="hist" id="hist"></div>
<div style="padding:10px;font-size:12px;color:#888">by Potenza Group<br>White ChatGPT Theme PRO</div>
</div>
<div class="main">
<div class="top">
<button class="icon-btn menu-btn" onclick="toggle()"><i class="fa-solid fa-bars"></i></button>
<div class="logo">P</div>
<div><b>ApexBro AI PRO</b><div style="font-size:12px;color:#666">by Potenza Group</div></div>
</div>
<div class="chat" id="chat"></div>
<div class="input-wrap">
<div class="input-box">
<button class="icon-btn mic-btn" onclick="voice()" title="Voice"><i class="fa-solid fa-microphone"></i></button>
<input id="inp" placeholder="Message ApexBro..." onkeydown="if(event.key==='Enter')sendMsg()">
<button class="icon-btn send-btn" onclick="sendMsg()"><i class="fa-solid fa-arrow-up"></i></button>
</div>
</div>
</div>
<script>
let chats=JSON.parse(localStorage.getItem('apex_chats')||'[]');
let curId=null;
function renderHist(){
 let h=document.getElementById('hist');h.innerHTML='';
 chats.slice().reverse().forEach(c=>{
   let d=document.createElement('div');d.className='hist-item';d.innerText=c.title;
   d.onclick=()=>{loadChat(c.id)};h.appendChild(d);
 })
}
function newChat(){
 curId=Date.now().toString();
 chats.push({id:curId,title:'New Chat',msgs:[{r:'bot',t:'Hi! Mai ApexBro PRO hu. Potenza Group ne banaya hai. Ab left me history bhi hai. Pucho kuch bhi! 👋'}]});
 save();renderHist();loadChat(curId);
}
function loadChat(id){
 curId=id;let c=chats.find(x=>x.id==id);let chat=document.getElementById('chat');chat.innerHTML='';
 c.msgs.forEach(m=>{addBubble(m.t,m.r,false)});
 chat.scrollTop=chat.scrollHeight;
 if(window.innerWidth<768)toggle();
}
function addBubble(text,role,saveMsg=true){
 let chat=document.getElementById('chat');
 let row=document.createElement('div');row.className='msg-row';
 let av=document.createElement('div');av.className='avatar '+(role=='user'?'user-av':'bot-av');av.innerText=role=='user'?'U':'P';
 let bub=document.createElement('div');bub.className='bubble';bub.innerText=text;
 row.appendChild(av);row.appendChild(bub);chat.appendChild(row);
 chat.scrollTop=chat.scrollHeight;
 if(saveMsg && curId){
   let c=chats.find(x=>x.id==curId);
   c.msgs.push({r:role,t:text});
   if(c.msgs.length==2)c.title=text.slice(0,30);
   save();renderHist();
 }
}
async function sendMsg(){
 let inp=document.getElementById('inp');let t=inp.value.trim();if(!t)return;
 if(!curId)newChat();
 addBubble(t,'user');inp.value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({m:t})});
 let d=await res.json();addBubble(d.r,'bot');
}
function save(){localStorage.setItem('apex_chats',JSON.stringify(chats))}
function toggle(){document.getElementById('sidebar').classList.toggle('open')}
function voice(){
 let R=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!R){alert('Mic not supported');return}
 let rec=new R();rec.lang='hi-IN';rec.start();
 rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript}
}
if(chats.length==0)newChat();else{renderHist();loadChat(chats[chats.length-1].id)}
</script>
</body></html>
"""

@app.route("/")
def home(): return PRO_HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        m = request.json.get("m","")
        comp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"You are ApexBro AI PRO, made by Potenza Group. You are helpful, smart, friendly. Answer in Hinglish mix."},
                {"role":"user","content":m}
            ]
        )
        return jsonify({"r": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"r": f"Error: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
