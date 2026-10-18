from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HTML = r"""
<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#212121">
<title>My AI - Smart Assistant</title>

<style>
*{box-sizing:border-box}
:root{
 --bg:#212121;--panel:#171717;--text:#ececec;
 --muted:#a0a0a0;--border:#383838;--accent:#10a37f;
}
body{
 margin:0;background:var(--bg);color:var(--text);
 font-family:system-ui,-apple-system,Arial,sans-serif;
}
button,input,textarea,select{font:inherit}
button{cursor:pointer}
.app{display:flex;height:100dvh;overflow:hidden}
.sidebar{
 width:265px;background:var(--panel);padding:15px;
 display:flex;flex-direction:column;gap:12px;
 border-right:1px solid var(--border);flex-shrink:0;
}
.brand{font-size:21px;font-weight:750;padding:8px 4px}
.brand span{color:var(--accent)}
.new{
 background:transparent;color:white;border:1px solid #555;
 border-radius:10px;padding:12px;text-align:left;
}
.new:hover,.history-item:hover{background:#303030}
.history-title{font-size:12px;color:var(--muted);margin-top:12px}
.history{overflow:auto;flex:1}
.history-item{
 display:flex;align-items:center;gap:8px;padding:10px;
 border-radius:8px;cursor:pointer;font-size:14px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.history-item.active{background:#303030}
.sidebar-bottom{border-top:1px solid var(--border);padding-top:12px}
.model-label{font-size:12px;color:var(--muted);margin-bottom:7px}
#model{
 width:100%;background:#262626;color:white;
 border:1px solid #444;border-radius:9px;padding:10px;
}
.main{flex:1;min-width:0;display:flex;flex-direction:column}
.topbar{
 height:58px;display:flex;align-items:center;gap:12px;
 padding:0 18px;border-bottom:1px solid var(--border);
}
.menu{display:none}
.top-title{font-weight:650}
.top-right{margin-left:auto;color:var(--muted);font-size:12px}
.messages{
 flex:1;overflow-y:auto;padding:25px 18px 30px;
 scroll-behavior:smooth;
}
.welcome{
 max-width:720px;margin:12vh auto 0;text-align:center;
}
.logo{
 width:55px;height:55px;border-radius:18px;background:var(--accent);
 display:grid;place-items:center;font-size:29px;margin:0 auto 22px;
 color:white;font-weight:bold;
}
.welcome h1{font-size:29px;margin:0 0 12px}
.welcome p{color:var(--muted);margin:0 0 28px}
.suggestions{
 display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
 gap:10px;text-align:left;
}
.suggestion{
 border:1px solid var(--border);border-radius:13px;padding:14px;
 background:transparent;color:var(--text);line-height:1.5;
}
.suggestion small{display:block;color:var(--muted);margin-top:5px}
.suggestion:hover{background:#303030}
.message{max-width:800px;margin:0 auto 26px}
.message-row{display:flex;gap:12px;align-items:flex-start}
.avatar{
 flex-shrink:0;width:31px;height:31px;border-radius:50%;
 display:grid;place-items:center;background:#333;font-size:14px;
}
.message.user .avatar{background:#6a4a92}
.message.assistant .avatar{background:var(--accent)}
.content{min-width:0;flex:1;line-height:1.8;overflow-wrap:anywhere}
.content p{margin:0 0 12px}
.content pre{
 background:#111;padding:14px;border-radius:10px;overflow:auto;
 white-space:pre-wrap;overflow-wrap:anywhere;
}
.content code{background:#333;padding:2px 5px;border-radius:4px}
.content pre code{background:transparent;padding:0}
.actions{display:flex;gap:7px;margin-top:10px}
.action{
 color:#aaa;background:transparent;border:1px solid transparent;
 border-radius:7px;padding:5px 8px;font-size:12px;
}
.action:hover{border-color:#555;color:white}
.composer-wrap{padding:12px 16px 18px}
.composer{max-width:800px;margin:auto}
.inputbox{
 display:flex;align-items:flex-end;gap:10px;
 border:1px solid #505050;border-radius:18px;
 padding:10px 12px;background:#303030;
 box-shadow:0 3px 18px #0002;
}
#prompt{
 flex:1;min-width:0;max-height:180px;resize:none;
 background:transparent;border:0;outline:0;color:white;
 padding:8px 0;line-height:1.5;
}
#send{
 width:39px;height:39px;border:0;border-radius:12px;
 background:var(--accent);color:white;font-size:20px;
}
#send:disabled{opacity:.45}
.hint{text-align:center;color:#999;font-size:11px;margin-top:10px}
.typing{color:var(--muted);font-size:14px}
.error{color:#ff9c9c}
.overlay{display:none}
@media(max-width:650px){
 .sidebar{
  position:fixed;z-index:5;top:0;bottom:0;left:0;
  transform:translateX(-105%);transition:transform .2s;
  box-shadow:5px 0 25px #0005;
 }
 .sidebar.open{transform:translateX(0)}
 .overlay.show{
  display:block;position:fixed;inset:0;background:#0008;z-index:4;
 }
 .menu{display:block;background:transparent;color:white;border:0;font-size:23px}
 .topbar{padding:0 12px}
 .top-right{font-size:10px}
 .messages{padding:22px 14px}
 .composer-wrap{padding:10px 10px 14px}
 .welcome{margin:8vh auto 0}
 .welcome h1{font-size:24px}
 .suggestions{grid-template-columns:1fr}
 .suggestion{padding:12px}
}

/* PREMIUM_DESIGN_V1 */
:root{
 --bg:#0b1020;
 --panel:#101729;
 --text:#f1f5f9;
 --muted:#9ba9bd;
 --border:#26344b;
 --accent:#7c6cff;
}
body{
 background:
  radial-gradient(ellipse at 50% -20%,#29345c 0%,transparent 55%),
  var(--bg);
 color:var(--text);
}
.sidebar{
 background:rgba(12,18,33,.96);
 border-right:1px solid var(--border);
}
.brand{
 letter-spacing:.3px;
}
.brand span{
 color:#a99dff;
}
.new{
 border-color:#3b4760;
 background:linear-gradient(135deg,#1c2740,#151d30);
 transition:background .2s,border-color .2s;
}
.new:hover,.history-item:hover{
 background:#28334b;
}
.history-item.active{
 background:#292a4a;
 border:1px solid #494477;
}
#model{
 background:#151d30;
 border-color:#34415b;
}
.topbar{
 background:rgba(11,16,32,.72);
 border-bottom:1px solid var(--border);
 backdrop-filter:blur(14px);
}
.top-title{
 letter-spacing:.2px;
}
.logo{
 background:linear-gradient(135deg,#8b7bff,#5b8cff);
 box-shadow:0 8px 35px #7668ff40;
 border-radius:19px;
}
.welcome h1{
 letter-spacing:-.7px;
}
.welcome p{
 line-height:1.7;
}
.suggestion{
 background:rgba(22,31,51,.72);
 border-color:#2d3b55;
 transition:transform .18s,border-color .18s,background .18s;
}
.suggestion:hover{
 background:#1c2841;
 border-color:#7770d8;
 transform:translateY(-2px);
}
.avatar{
 background:#28334b;
}
.message.assistant .avatar{
 background:linear-gradient(135deg,#8b7bff,#5b8cff);
}
.message.user .avatar{
 background:#4f467d;
}
.content{
 line-height:1.85;
}
.content pre{
 border:1px solid #303c55;
 background:#090e19;
}
.content code{
 background:#27334b;
}
.action{
 transition:background .15s,color .15s;
}
.action:hover{
 background:#28334b;
}
.inputbox{
 background:#141d30;
 border-color:#35435e;
 border-radius:22px;
 box-shadow:0 8px 35px #0003;
 transition:border-color .2s,box-shadow .2s;
}
.inputbox:focus-within{
 border-color:#8175ff;
 box-shadow:0 0 0 3px #8175ff20,0 8px 35px #0003;
}
#prompt{
 color:var(--text);
}
#send{
 background:linear-gradient(135deg,#8b7bff,#5b8cff);
 box-shadow:0 3px 12px #7668ff40;
 transition:transform .15s,opacity .15s;
}
#send:hover{
 transform:scale(1.05);
}
.hint{
 color:#8997ad;
}
.typing{
 color:#b3bdd0;
}
@media(max-width:650px){
 .sidebar{
  background:#0e1526;
 }
 .welcome{
  margin-top:6vh;
 }
 .welcome h1{
  font-size:25px;
  line-height:1.35;
 }
 .suggestion:hover{
  transform:none;
 }
}

</style>
</head>

<body>
<div class="app">
<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

<aside class="sidebar" id="sidebar">
 <div class="brand">✳ My <span>AI</span></div>
 <button class="new" onclick="newChat()">＋ New Chat</button>
 <div class="history-title">RECENT CHATS</div>
 <div class="history" id="history"></div>
 <div class="sidebar-bottom">
  <div class="model-label">AI MODEL</div>
  <select id="model">
   <option value="openrouter/free">Free model (OpenRouter)</option>
  </select>
  <div style="font-size:11px;color:#888;margin-top:10px">
   AI Assistant · Powered by OpenRouter
  </div>
 </div>
</aside>

<main class="main">
 <header class="topbar">
  <button class="menu" onclick="toggleSidebar()">☰</button>
  <div class="top-title">My AI</div>
  <div class="top-right">Smart AI Assistant</div>
 </header>

 <section class="messages" id="messages">
  <div class="welcome" id="welcome">
   <div class="logo">✳</div>
   <h1>आज मैं आपकी क्या मदद करूँ?</h1>
   <p>कुछ भी पूछें, AI के साथ बातचीत शुरू करें।</p>
   <div class="suggestions">
    <button class="suggestion" onclick="suggest('Python को आसान हिंदी में समझाओ')">
     💻 Coding सीखें
     <small>प्रोग्रामिंग को आसान तरीके से समझें</small>
    </button>
    <button class="suggestion" onclick="suggest('मुझे एक अच्छी कहानी सुनाओ')">
     ✍️ कुछ नया लिखें
     <small>कहानी, लेख या आइडिया पाएँ</small>
    </button>
    <button class="suggestion" onclick="suggest('साइंस क्या है? आसान हिंदी में समझाओ')">
     🧠 कुछ नया सीखें
     <small>अपने सवालों के जवाब पाएँ</small>
    </button>
    <button class="suggestion" onclick="suggest('मुझे पढ़ाई का टाइम टेबल बनाकर दो')">
     📚 पढ़ाई में मदद
     <small>पढ़ाई और तैयारी में सहायता लें</small>
    </button>
   </div>
  </div>
  <div id="chat"></div>
 </section>

 <div class="composer-wrap">
  <div class="composer">
   <div class="inputbox">
    <textarea id="prompt" rows="1"
     placeholder="यहाँ अपना सवाल लिखें..."
     oninput="resizeInput(this)"
     onkeydown="handleKey(event)"></textarea>
    <button id="send" onclick="sendMessage()">↑</button>
   </div>
   <div class="hint">AI गलतियाँ कर सकता है। जरूरी जानकारी की जाँच करें।</div>
  </div>
 </div>
</main>
</div>

<script>
const $ = id => document.getElementById(id);
const STORAGE_KEY = "my_ai_chats_v1";
let chats = [];
let currentId = null;
let busy = false;

try {
 chats = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
 if (!Array.isArray(chats)) chats = [];
} catch(e) { chats = []; }

function saveChats(){
 try { localStorage.setItem(STORAGE_KEY, JSON.stringify(chats)); }
 catch(e) { alert("फोन की स्टोरेज भर गई है। कुछ पुरानी चैट हटाएँ।"); }
}

function makeId(){
 return Date.now().toString(36) + Math.random().toString(36).slice(2,8);
}

function newChat(){
 if(busy) return;
 currentId = makeId();
 chats.unshift({id:currentId,title:"New Chat",messages:[]});
 saveChats();
 renderChat();
 renderHistory();
 $("prompt").focus();
 closeSidebar();
}

function currentChat(){
 return chats.find(c => c.id === currentId);
}

function ensureChat(){
 if(!currentChat()){
  currentId = makeId();
  chats.unshift({id:currentId,title:"New Chat",messages:[]});
 }
 return currentChat();
}

function renderHistory(){
 const box = $("history");
 box.innerHTML = "";
 chats.forEach(c => {
  const row = document.createElement("div");
  row.className = "history-item" + (c.id === currentId ? " active" : "");
  const title = document.createElement("span");
  title.style.cssText = "overflow:hidden;text-overflow:ellipsis;flex:1";
  title.textContent = "▤ " + c.title;
  row.appendChild(title);

  const del = document.createElement("button");
  del.textContent = "×";
  del.title = "Delete chat";
  del.className = "action";
  del.onclick = e => {
   e.stopPropagation();
   chats = chats.filter(x => x.id !== c.id);
   if(currentId === c.id) currentId = null;
   saveChats();
   if(!currentId) newChat();
   else {renderHistory();renderChat();}
  };
  row.appendChild(del);
  row.onclick = () => {
   if(busy) return;
   currentId = c.id;
   renderHistory();
   renderChat();
   closeSidebar();
  };
  box.appendChild(row);
 });
}

function renderChat(){
 const c = currentChat();
 $("chat").innerHTML = "";
 $("welcome").style.display = c && c.messages.length ? "none" : "block";
 if(!c) { $("welcome").style.display="block"; return; }
 c.messages.forEach((m,i) => addMessage(m.role,m.content,i));
 $("messages").scrollTop = $("messages").scrollHeight;
}

function escapeHTML(s){
 return String(s).replace(/[&<>"']/g, ch => ({
  "&":"&amp;","<":"&lt;",">":"&gt;",
  '"':"&quot;","'":"&#39;"
 }[ch]));
}

function formatText(s){
 let safe = escapeHTML(s);
 safe = safe.replace(/```([\s\S]*?)```/g, (m,code) =>
  "<pre><code>"+code.trim()+"</code></pre>");
 safe = safe.replace(/`([^`\n]+)`/g,"<code>$1</code>");
 safe = safe.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>");
 safe = safe.replace(/\n/g,"<br>");
 return safe;
}

function addMessage(role,content,index){
 const row = document.createElement("div");
 row.className = "message " + role;
 const inner = document.createElement("div");
 inner.className = "message-row";
 const avatar = document.createElement("div");
 avatar.className = "avatar";
 avatar.textContent = role === "user" ? "🙂" : "✳";
 const body = document.createElement("div");
 body.className = "content";
 const text = document.createElement("div");
 text.innerHTML = formatText(content);
 body.appendChild(text);
 inner.append(avatar,body);
 row.appendChild(inner);

 if(role === "assistant"){
  const actions = document.createElement("div");
  actions.className = "actions";
  const copy = document.createElement("button");
  copy.className = "action";
  copy.textContent = "▢ Copy";
  copy.onclick = async () => {
   try {
    await navigator.clipboard.writeText(content);
    copy.textContent = "✓ Copied";
   } catch(e) {
    const ta=document.createElement("textarea");
    ta.value=content;document.body.appendChild(ta);
    ta.select();document.execCommand("copy");ta.remove();
    copy.textContent="✓ Copied";
   }
   setTimeout(()=>copy.textContent="▢ Copy",1500);
  };
  actions.appendChild(copy);

  const c = currentChat();
  if(c && index === c.messages.length-1){
   const regen = document.createElement("button");
   regen.className="action";
   regen.textContent="↻ Regenerate";
   regen.onclick=()=>regenerate();
   actions.appendChild(regen);
  }
  body.appendChild(actions);
 }
 $("chat").appendChild(row);
}

function resizeInput(el){
 el.style.height="auto";
 el.style.height=Math.min(el.scrollHeight,180)+"px";
}

function handleKey(e){
 if(e.key==="Enter" && !e.shiftKey){
  e.preventDefault();sendMessage();
 }
}

function suggest(text){
 $("prompt").value=text;
 resizeInput($("prompt"));
 sendMessage();
}

function toggleSidebar(){
 $("sidebar").classList.toggle("open");
 $("overlay").classList.toggle("show");
}
function closeSidebar(){
 $("sidebar").classList.remove("open");
 $("overlay").classList.remove("show");
}

async function sendMessage(){
 if(busy) return;
 const input=$("prompt");
 const text=input.value.trim();
 if(!text) return;

 const c=ensureChat();
 c.messages.push({role:"user",content:text});
 if(c.title==="New Chat") c.title=text.slice(0,35);
 input.value="";
 resizeInput(input);
 saveChats();
 renderChat();
 renderHistory();
 await askAI();
}

async function askAI(){
 const c=currentChat();
 if(!c) return;
 busy=true;
 $("send").disabled=true;
 const wait=document.createElement("div");
 wait.className="message assistant";
 wait.id="waiting";
 wait.innerHTML='<div class="message-row"><div class="avatar">✳</div><div class="content typing">AI जवाब तैयार कर रहा है…</div></div>';
 $("chat").appendChild(wait);
 $("welcome").style.display="none";
 $("messages").scrollTop=$("messages").scrollHeight;

 try{
  const res=await fetch("/api/chat",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({
    messages:c.messages,
    model:$("model").value
   })
  });
  const data=await res.json();
  if(!res.ok) throw new Error(data.error || "Request failed");
  c.messages.push({role:"assistant",content:data.reply});
 }catch(e){
  c.messages.push({
   role:"assistant",
   content:"माफ़ कीजिए, जवाब नहीं मिल पाया।\n\nकारण: "+e.message+
    "\n\nAPI Key, इंटरनेट कनेक्शन और चुने गए मॉडल की उपलब्धता जाँचें।"
  });
 }
 finally{
  busy=false;
  $("send").disabled=false;
  saveChats();
  renderChat();
  renderHistory();
  $("prompt").focus();
 }
}

async function regenerate(){
 if(busy) return;
 const c=currentChat();
 if(!c || !c.messages.length || c.messages[c.messages.length-1].role!=="assistant") return;
 c.messages.pop();
 saveChats();
 renderChat();
 await askAI();
}

if(chats.length){
 currentId=chats[0].id;
}
renderHistory();
renderChat();
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.post("/api/chat")
def chat():
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return jsonify({
            "error": "OPENROUTER_API_KEY set nahi hai. Termux mein API key set karein."
        }), 400

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    model = data.get("model", "openrouter/free")

    allowed_models = {
        "openrouter/free",
    }
    if model not in allowed_models:
        model = "openrouter/free"

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Pehle apna sawal likhein."}), 400

    clean_messages = [{
        "role": "system",
        "content": (
            "You are a helpful AI assistant. Answer the user's questions "
            "clearly and accurately. Reply in the language the user uses. "
            "If the user writes Hindi or Hinglish, respond in simple Hindi "
            "or Hinglish. If unsure, say so honestly."
        )
    }]

    for item in messages[-20:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in ("user", "assistant"):
            continue
        if not isinstance(content, str) or not content.strip():
            continue
        clean_messages.append({
            "role": role,
            "content": content[:12000]
        })

    # FREE_SEARCH_V2 - Free News API
    last_question = next(
        (m["content"] for m in reversed(clean_messages)
         if m.get("role") == "user"),
        ""
    )

    q_lower = last_question.lower()
    search_triggers = (
        "/search", "search:", "internet par search",
        "internet se search", "web par search",
        "online search", "google par search",
        "internet par dhundo", "internet se dhundo",
        "latest news", "aaj ki khabar"
    )

    if any(word in q_lower for word in search_triggers):
        search_query = last_question.strip()

        for prefix in ("/search", "search:"):
            if search_query.lower().startswith(prefix):
                search_query = search_query[len(prefix):].strip()
                break

        try:
            sr = requests.get(
                "https://freenewsapi.ai/v1/search",
                params={
                    "q": search_query[:300],
                    "country": "IN",
                    "lang": "en",
                    "size": 5
                },
                timeout=20
            )
            sr.raise_for_status()
            data = sr.json()
            results = data.get("results", [])

            source_text = []
            for i, item in enumerate(results[:5], 1):
                url = str(item.get("url", ""))
                if not url.startswith(("https://", "http://")):
                    continue

                title = str(item.get("title", ""))[:250]
                description = str(item.get("description", ""))[:800]
                published = str(item.get("published_at", "Date unavailable"))
                source = str(item.get("sitename", item.get("host", "News source")))

                source_text.append(
                    f"{i}. {title}\n"
                    f"Source: {source}\n"
                    f"Published: {published}\n"
                    f"Description: {description}\n"
                    f"URL: {url}"
                )

            if source_text:
                clean_messages.insert(1, {
                    "role": "system",
                    "content": (
                        "The user requested a news/web search. Use the "
                        "following live news results to answer in the user's "
                        "language. Prioritize relevant Indian news. Mention "
                        "publication dates when available. Do not invent "
                        "facts, dates, or details not supported by the results. "
                        "Include clickable source URLs in your answer. "
                        "If results are unrelated to the query, say so honestly.\n\n"
                        + "\n\n".join(source_text)
                    )
                })
            else:
                clean_messages.insert(1, {
                    "role": "system",
                    "content": (
                        "The news search returned no usable results. "
                        "Tell the user honestly and suggest trying different keywords."
                    )
                })

        except (requests.RequestException, ValueError) as e:
            print("News search error:", str(e))
            clean_messages.insert(1, {
                "role": "system",
                "content": (
                    "The news search failed. Do not pretend it succeeded. "
                    "Tell the user to try again later."
                )
            })

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-OpenRouter-Title": "My AI Chat"
            },
            json={
                "model": model,
                "messages": clean_messages,
                "temperature": 0.7
            },
            timeout=90
        )

        if not response.ok:
            try:
                detail = response.json().get("error", {}).get(
                    "message", "OpenRouter API request failed"
                )
            except Exception:
                detail = "OpenRouter API request failed"
            return jsonify({"error": str(detail)[:500]}), response.status_code

        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        if not isinstance(reply, str) or not reply.strip():
            return jsonify({"error": "AI se khaali jawab mila."}), 502

        return jsonify({"reply": reply})

    except requests.Timeout:
        return jsonify({
            "error": "Request timeout. Dobara koshish karein."
        }), 504
    except requests.RequestException:
        return jsonify({
            "error": "Internet connection ya API server mein dikkat hai."
        }), 502
    except (KeyError, IndexError, TypeError, ValueError):
        return jsonify({
            "error": "AI response ko samajhne mein dikkat hui."
        }), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
