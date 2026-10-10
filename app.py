import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML = """
<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>ApexBro AI PRO - by Potenza Group</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial;height:100vh;height:100dvh;display:flex;background:#fff;color:#0d0d0d;overflow:hidden}
.side{width:260px;background:#171717;color:#fff;display:flex;flex-direction:column;flex-shrink:0;z-index:5}
.brand{padding:14px 14px 8px 14px;display:flex;align-items:center;gap:10px}
.p-logo{width:32px;height:32px;background:#19c37d;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800}
.new{margin:8px 10px;background:#fff;color:#000;padding:11px;border-radius:10px;text-align:center;cursor:pointer;font-weight:700;font-size:14px}
.new:hover{background:#ececec}
.list{flex:1;overflow-y:auto;padding:6px}
.item{padding:10px 10px;border-radius:8px;font-size:14px;color:#ececec;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.2}
.item:hover{background:#2f2f2f}
.small{font-size:11px;color:#7a7a7a;padding:12px}
.main{flex:1;display:flex;flex-direction:column;min-width:0;position:relative;background:#fff}
.top{height:56px;display:flex;align-items:center;gap:12px;padding:0 14px;border-bottom:1px solid #efefef;flex-shrink:0}
.top b{font-size:15px}.top span{font-size:12px;color:#666}
.hamburger{display:none;border:none;background:transparent;font-size:22px;cursor:pointer}
.chat{flex:1;overflow-y:auto;padding:10px 0 160px 0}
.row{max-width:760px;width:100%;margin:0 auto;padding:18px 20px;display:flex;gap:14px}
.av{width:30px;height:30px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.av.u{background:#000;color:#fff}.av.b{background:#19c37d;color:#fff}
.bub{flex:1;white-space:pre-wrap;line-height:1.65;font-size:15px;padding-top:1px;word-break:break-word}
.bottom{position:absolute;left:0;right:0;bottom:0;padding:12px 12px 18px 12px;background:linear-gradient(to top, #fff 65%, rgba(255,255,255,0) 100%)}
.box{max-width:760px;margin:0 auto;background:#f4f4f4;border-radius:28px;display:flex;align-items:center;padding:6px 8px;gap:4px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.box input{flex:1;background:transparent;border:none;outline:none;padding:12px 8px;font-size:16px}
.icon{width:40px;height:40px;border-radius:50%;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px}
.mic{background:transparent}
.mic:hover{background:#e9e9e9}
.send{background:#000;color:#fff}
.send:disabled{opacity:0.3}
.overlay{display:none}
@media(max-width:820px){
.hamburger{display:block}
.side{position:fixed;left:-100%;top:0;bottom:0;width:280px;transition:0.25s ease;box-shadow:20px 0 60px rgba(0,0,0,0.3)}
.side.open{left:0}
.overlay.open{display:block;position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:4}
}
</style></head>
<body>
<div class="overlay" id="over" onclick="toggleSide()"></div>
<div class="side" id="side">
<div class="brand"><div class="p-logo">P</div><div><div style="font-weight:700;font-size:14px">Potenza Group</div><div style="font-size:11px;color:#aaa">White ChatGPT Theme</div></div></div>
<div class="new" onclick="createChat()">+ New Chat</div>
<div class="list" id="list"></div>
<div class="small">ApexBro AI PRO • Mic left me hai</div>
</div>

<div class="main">
<div class="top">
<button class="hamburger" onclick="toggleSide()">☰</button>
<div class="p-logo" style="width:30px;height:30px">P</div>
<div><b>ApexBro AI PRO</b> <span>by Potenza Group</span></div>
</div>
<div class="chat" id="chat"></div>
<div class="bottom">
<div class="box">
<button class="icon mic" onclick="startVoice()" title="Voice">🎤</button>
<input id="inp" placeholder="Message ApexBro..." autocomplete="off" onkeydown="if(event.key==='Enter') doSend()">
<button class="icon send" id="sendBtn" onclick="doSend()">↑</button>
</div>
<div style="text-align:center;font-size:11px;color:#999;margin-top:8px">ApexBro can make mistakes. Check important info.</div>
</div>
</div>

<script>
let chats = JSON.parse(localStorage.getItem('apex_pro_final_v3') || '[]');
let cur = null;

function toggleSide(){
 document.getElementById('side').classList.toggle('open');
 document.getElementById('over').classList.toggle('open');
}

function save(){ localStorage.setItem('apex_pro_final_v3', JSON.stringify(chats)); }

function renderList(){
 const el = document.getElementById('list');
 el.innerHTML =
