from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

QUESTIONS = [
    {"id":1,"level":"PCEP","topic":"Operators","question":"What is the result of print(2 ** 3 ** 2)?","options":["64","512","256","Error"],"answer":1,"why":"Exponentiation is right-associative: 2 ** (3 ** 2) = 512."},
    {"id":2,"level":"PCEP","topic":"Control flow","question":"What does list(range(2, 8, 2)) return?","options":["[2, 4, 6]","[2, 4, 6, 8]","[2, 3, 4, 5, 6, 7]","[4, 6, 8]"],"answer":0,"why":"The stop value is excluded, so the values are 2, 4 and 6."},
    {"id":3,"level":"PCEP","topic":"Collections","question":"What does len({1, 1, 2, 3}) return?","options":["4","2","3","Error"],"answer":2,"why":"A set removes duplicates, leaving 1, 2, and 3."},
    {"id":4,"level":"PCEP","topic":"Functions","question":"What is printed by print(bool('False'))?","options":["False","True","None","Error"],"answer":1,"why":"Any nonempty string is truthy, including the text 'False'."},
    {"id":5,"level":"PCEP","topic":"Exceptions","question":"Which block executes regardless of whether an exception occurs?","options":["except","else","finally","raise"],"answer":2,"why":"The finally suite executes on normal completion and during exception handling."},
    {"id":6,"level":"PCEP","topic":"Strings","question":"What is 'python'[::-1]?","options":["python","nohtyp","ptyhon","Error"],"answer":1,"why":"A slice with step -1 reverses the string."},
    {"id":7,"level":"PCAP","topic":"OOP","question":"What does super() commonly help you access?","options":["A global variable","A parent-class implementation","An imported package","A class decorator"],"answer":1,"why":"super() provides a proxy used to call methods following the method resolution order."},
    {"id":8,"level":"PCAP","topic":"OOP","question":"Which special method is called when an object is initialized?","options":["__str__","__call__","__init__","__iter__"],"answer":2,"why":"__init__ initializes an instance after it is created."},
    {"id":9,"level":"PCAP","topic":"Generators","question":"What does yield do inside a function?","options":["Immediately exits the program","Creates a generator function","Imports a module","Raises StopIteration immediately"],"answer":1,"why":"A function containing yield produces a generator iterator."},
    {"id":10,"level":"PCAP","topic":"Exceptions","question":"Which clause runs if no exception is raised in the try suite?","options":["except","raise","else","finally only"],"answer":2,"why":"The else suite runs when the try block completes without an exception."},
    {"id":11,"level":"PCAP","topic":"Modules","question":"What is the conventional entry-point check?","options":["if name == 'main':","if __name__ == '__main__':","if __main__():","if main is True:"],"answer":1,"why":"__name__ is '__main__' when the module is run as the main program."},
    {"id":12,"level":"PCAP","topic":"OOP","question":"If class Dog(Animal) is defined, Dog is a...","options":["Base class","Superclass","Subclass","Module"],"answer":2,"why":"Dog inherits from Animal, so Dog is its subclass."}
]

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101827">
<title>PyCert Academy — PCEP & PCAP Practice</title>
<style>
:root{--bg:#0a0f1c;--card:#131d30;--edge:#293652;--text:#eef4ff;--muted:#9aabc5;--a:#55dfbb;--b:#6d8fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse at 80% 0%,#182852 0%,transparent 45%),var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.55}
.container{max-width:1080px;margin:auto;padding:0 22px}nav{display:flex;align-items:center;justify-content:space-between;padding:24px 0;gap:12px}nav a{color:var(--muted);text-decoration:none;margin-left:18px}nav a:hover{color:var(--text)}
.logo{font-weight:850;font-size:21px;letter-spacing:-.7px}.logo span{color:var(--a)}.tag{display:inline-block;color:var(--a);background:#173b3a;border:1px solid #2a6d64;border-radius:30px;padding:7px 13px;font-size:12px;font-weight:750;letter-spacing:1px}
.hero{padding:72px 0 54px;display:grid;grid-template-columns:1.2fr .8fr;gap:30px;align-items:center}h1{font-size:clamp(42px,6vw,72px);line-height:1.07;letter-spacing:-2.5px;margin:20px 0}h1 em{font-style:normal;color:var(--a)}.lead{font-size:18px;max-width:580px;color:var(--muted)}
.btn{border:none;background:var(--a);color:#08151b;padding:13px 22px;border-radius:11px;font-weight:800;cursor:pointer;font-size:15px}.btn:hover{filter:brightness(1.09)}.btn.secondary{background:#263551;color:#fff}.buttons{display:flex;gap:12px;flex-wrap:wrap;margin:25px 0}.illustration{padding:25px;background:linear-gradient(145deg,#162440,#101727);border:1px solid var(--edge);border-radius:22px;box-shadow:0 18px 60px #0004}.terminal{background:#090f19;border-radius:13px;padding:20px;font:15px/1.9 Consolas,monospace;overflow:auto}.green{color:var(--a)}.purple{color:#a5a9ff}.yellow{color:#ffd47d}
section{padding:30px 0}h2{font-size:30px;letter-spacing:-1px;margin-bottom:8px}.sub{color:var(--muted);margin-top:0}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:25px 0}.card,.quiz{background:var(--card);border:1px solid var(--edge);border-radius:17px;padding:24px}.card h3{margin:8px 0}.card p{color:var(--muted)}.metric{font-size:30px;font-weight:850;color:var(--a)}
.controls{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}.select{background:#10192b;color:var(--text);border:1px solid var(--edge);padding:12px 14px;border-radius:10px;font-size:15px}
.quiz{max-width:790px}.progress{height:8px;background:#293650;border-radius:9px;overflow:hidden;margin:18px 0}.fill{height:100%;background:linear-gradient(90deg,var(--b),var(--a));width:0;transition:width .2s}.meta{color:var(--a);font-size:13px;font-weight:750}.question{font-size:22px;font-weight:750;margin:16px 0;white-space:pre-wrap}
.option{display:block;width:100%;text-align:left;background:#101b2f;color:var(--text);border:1px solid #34435d;border-radius:11px;padding:14px 16px;margin:10px 0;font-size:15px;cursor:pointer}.option:hover:not(:disabled){border-color:var(--a)}.option.correct{background:#163d36;border-color:var(--a)}.option.wrong{background:#422532;border-color:#ff8494}.option:disabled{cursor:default}.feedback{min-height:48px;color:var(--muted);margin:14px 0}.hidden{display:none}.score{font-size:48px;color:var(--a);font-weight:850}footer{border-top:1px solid var(--edge);color:var(--muted);padding:28px 0;margin-top:55px}
@media(max-width:760px){.hero{grid-template-columns:1fr;padding:36px 0}.cards{grid-template-columns:1fr}nav a{margin-left:8px;font-size:13px}h1{letter-spacing:-1px}}
</style>
</head>
<body>
<div class="container">
<nav><div class="logo">Py<span>Cert</span> Academy</div><div><a href="#tracks">Tracks</a><a href="#practice">Practice</a></div></nav>
<header class="hero"><div><div class="tag">PYTHON CERTIFICATION PREP</div><h1>Master Python.<br><em>Pass with confidence.</em></h1><p class="lead">Focused PCEP and PCAP practice, instant answer explanations, and progress you can track. Built for hands-on learners.</p><div class="buttons"><a href="#practice"><button class="btn">Start practice →</button></a><a href="#tracks"><button class="btn secondary">Explore tracks</button></a></div><p class="sub">12 original practice questions · Free · No account required</p></div>
<div class="illustration"><div class="terminal"><span class="purple">class</span> PythonLearner:<br> &nbsp;<span class="purple">def</span> __init__(self):<br> &nbsp;&nbsp;self.goal = <span class="yellow">"PCAP"</span><br> &nbsp;&nbsp;self.ready = <span class="purple">True</span><br><br><span class="green">>>> learner = PythonLearner()</span><br><span class="green">>>> learner.ready</span><br>True 🐍</div></div></header>
<section id="tracks"><h2>Choose your certification track</h2><p class="sub">Learn from fundamentals to object-oriented programming.</p><div class="cards">
<div class="card"><div class="metric">01</div><h3>PCEP — Entry Level</h3><p>Operators, control flow, collections, functions, and exceptions.</p><button class="btn secondary" onclick="choose('PCEP')">Practice PCEP</button></div>
<div class="card"><div class="metric">02</div><h3>PCAP — Associate</h3><p>Object-oriented programming, modules, iterators, generators, and exceptions.</p><button class="btn secondary" onclick="choose('PCAP')">Practice PCAP</button></div>
<div class="card"><div class="metric">∞</div><h3>Practice at your pace</h3><p>Get immediate explanations and review your score after every quiz.</p><button class="btn secondary" onclick="choose('ALL')">Mixed practice</button></div>
</div></section>
<section id="practice"><h2>Certification quiz</h2><p class="sub">Select your track and answer the questions. One answer per question.</p>
<div class="controls"><select id="level" class="select" aria-label="Certification track"><option value="ALL">Mixed · PCEP + PCAP</option><option value="PCEP">PCEP only</option><option value="PCAP">PCAP only</option></select><button class="btn" id="restart">Restart quiz</button></div>
<div class="quiz"><div id="game"><div class="meta" id="counter">QUESTION 1</div><div class="progress"><div class="fill" id="fill"></div></div><div class="question" id="question">Loading...</div><div id="options"></div><p class="feedback" id="feedback" aria-live="polite"></p><button class="btn hidden" id="next">Next question →</button></div><div id="result" class="hidden"><p class="meta">PRACTICE COMPLETE</p><div class="score" id="score"></div><h2>Great work!</h2><p class="sub" id="summary"></p><button class="btn" id="again">Try again</button></div></div>
</section><footer>PyCert Academy · Independent educational practice tool. Not affiliated with Python Institute or OpenEDG. Questions are original practice examples, not real exam questions.</footer></div>
<script>
let bank=[],index=0,correct=0,locked=false;
const $=id=>document.getElementById(id);
function choose(level){$('level').value=level;start();location.hash='practice'}
async function start(){
  try {const res=await fetch('/api/questions?level='+encodeURIComponent($('level').value));if(!res.ok)throw Error('Server error');bank=await res.json();}
  catch(e){$('question').textContent='Could not load questions. Please refresh the page.';return}
  index=0;correct=0;$('game').classList.remove('hidden');$('result').classList.add('hidden');show();
}
function show(){
  locked=false;$('feedback').textContent='';$('next').classList.add('hidden');$('options').replaceChildren();
  const q=bank[index];if(!q)return;
  $('counter').textContent=q.level+' · '+q.topic.toUpperCase()+' · QUESTION '+(index+1)+' OF '+bank.length;
  $('fill').style.width=(100*index/bank.length)+'%';$('question').textContent=q.question;
  q.options.forEach((o,i)=>{const b=document.createElement('button');b.className='option';b.textContent=String.fromCharCode(65+i)+'. '+o;b.onclick=()=>answer(i);$('options').appendChild(b)});
}
async function answer(choice){
  if(locked)return;locked=true;
  const q=bank[index];
  try{
    const res=await fetch('/api/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:q.id,choice})});
    if(!res.ok)throw Error('Validation error');
    const data=await res.json();
    if(data.correct)correct++;
    [...$('options').children].forEach((b,i)=>{b.disabled=true;if(i===data.answer)b.classList.add('correct');else if(i===choice)b.classList.add('wrong')});
    $('feedback').textContent=(data.correct?'✓ Correct! ':'✕ Not quite. ')+data.explanation;
    $('next').textContent=index===bank.length-1?'Show results →':'Next question →';$('next').classList.remove('hidden');
  }catch(e){locked=false;$('feedback').textContent='Connection issue. Please try again.'}
}
function next(){index++;if(index<bank.length){show();return}$('game').classList.add('hidden');$('result').classList.remove('hidden');$('score').textContent=Math.round(correct/bank.length*100)+'%';$('summary').textContent='You answered '+correct+' out of '+bank.length+' questions correctly. This is a practice score, not an official exam prediction.'}
$('restart').onclick=start;$('again').onclick=start;$('next').onclick=next;$('level').onchange=start;start();
</script>
</body></html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.get("/api/questions")
def questions():
    level = request.args.get("level", "ALL").upper()
    if level not in {"ALL", "PCEP", "PCAP"}:
        return jsonify({"error": "Invalid level"}), 400
    # Never expose correct answers through the public question endpoint.
    return jsonify([
        {key: value for key, value in item.items() if key not in {"answer", "why"}}
        for item in QUESTIONS if level == "ALL" or item["level"] == level
    ])

@app.post("/api/check")
def check():
    data = request.get_json(silent=True) or {}
    question_id = data.get("id")
    choice = data.get("choice")
    item = next((q for q in QUESTIONS if q["id"] == question_id), None)
    if item is None or type(choice) is not int or not 0 <= choice < len(item["options"]):
        return jsonify({"error": "Invalid question or choice"}), 400
    return jsonify({"correct": choice == item["answer"], "answer": item["answer"], "explanation": item["why"]})

if __name__ == "__main__":
    app.run(debug=False)
