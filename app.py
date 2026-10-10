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
<title>ApexBro AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui;background:#0f0f0f;color:#fff;height:100dvh;display:flex;flex-direction:column}
.header{padding:15px;text-align:center;border-bottom:1px solid #222;font-weight:bold}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:80%;padding:10px 14px;border-radius:18px;font-size:15px;white-space:pre-wrap}
.user{align-self:flex-end;background:#0084ff}
.bot{align-self:flex-start;background:#222}
.bar{display:flex;gap:8px;padding:10px;background:#151515;border-top:1px solid #222}
input{flex:1;padding:12px 15px;border-radius:25px;border:none;background:#222;color:#fff;outline:none}
button{width:45px;height:45px;border-radius:50%;border:none;background:#00ff88}
</style></head>
<body>
<div class="header">🤖 ApexBro AI - by Potenza Group</div>
<div id="chat"><div class="msg bot">Hi! Main ApexBro hu, built by Potenza Group. Bolo kya help chahiye?</div></div>
<div class="bar"><input id="q" placeholder="Message..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">➤</button></div>
<script>
async function send(){
 let i=document.getElementById('q'),t=i.value.trim(); if(!t)return;
 let c=document.getElementById('chat'); c.innerHTML+=`<div class='msg user'>${t}</div>`; i.value=''; c.scrollTop=c.scrollHeight;
 c.innerHTML+=`<div id='tmp' class='msg bot'>Soch raha hu...</div>`;
 try{
  let r=await fetch('/ask?q='+encodeURIComponent(t));
  let d=await r.json();
  document.getElementById('tmp').remove();
  c.innerHTML+=`<div class='msg bot'>${(d.answer||d.error||'No reply').replace(/\\n/g,'<br>')}</div>`;
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
                {"role": "system", "content": "You are ApexBro AI, created by Potenza Group. You are a helpful, friendly AI assistant built by Potenza Group. Never say you are OpenAI or ChatGPT. If someone asks who built you, always say 'I was built by Potenza Group - ApexBro AI'. Always reply in same language user uses."},
                {"role":"user","content":q}
            ]
        )
        return jsonify({"answer": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
