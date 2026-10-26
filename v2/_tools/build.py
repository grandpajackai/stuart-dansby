import os
import os.path as _p; R=_p.dirname(_p.dirname(_p.abspath(__file__)))
def head(p,title,desc,path):
    return f'''<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#0E0E0E">
<meta name="robots" content="noindex"><link rel="canonical" href="https://grandpajackai.github.io/stuart-dansby/v2/{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://grandpajackai.github.io/stuart-dansby/assets/social.jpg"><meta property="og:type" content="website">
<link rel="icon" href="{p}../assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}../assets/barlow-condensed-bold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{p}v2.css"></head><body>
<a class="skip" href="#main">Skip to content</a>'''
def hdr(p,cur):
    def a(h,l,k): return f'<a href="{p}{h}"'+(' aria-current="page"' if k==cur else '')+f'>{l}</a>'
    return f'''<header class="hdr"><div class="wrap"><a class="brand" href="{p or "./"}" aria-label="Taking the Fight home"><img src="{p}img/fist.webp" width="40" height="40" alt=""><span>Taking <b>the</b> Fight</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span></button>
<nav class="nav" id="nav" aria-label="Main">{a("" if p else "./","Corporate","corp")}{a("education/","Students &amp; Education","edu")}{a("course/","Online Course","course")}<a class="btn btn-red btn-sm" data-book="{"edu" if cur=="edu" else "corp"}" href="mailto:info@takingthefight.com">Book a discovery call</a></nav></div></header>'''
def ftr(p):
    return f'''<footer class="ftr"><div class="wrap"><div><a class="brand" href="{p or "./"}"><img src="{p}img/fist.webp" width="40" height="40" alt=""><span>Taking <b>the</b> Fight</span></a><p style="margin-top:1rem;max-width:36ch">Stuart Warren Dansby. Thirty years of building people and businesses. A championship at 62. Five pillars you can use Monday morning.</p></div>
<div><h4>Work with Stuart</h4><ul><li><a href="{p or "./"}">Corporate speaking</a></li><li><a href="{p}education/">Students &amp; education</a></li><li><a href="{p}course/">The Five Pillars online course</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a data-email href="mailto:info@takingthefight.com">info@takingthefight.com</a></li><li><a data-book="corp" href="mailto:info@takingthefight.com">Book a discovery call</a></li><li><a href="{p}../privacy/">Privacy</a></li></ul></div>
<div class="legal"><span>© <span id="yr">2026</span> Taking the Fight · Stuart Warren Dansby</span><span>“We all have a fight.”</span></div></div></footer>
<dialog class="video" id="video" aria-label="Speaker reel"><button class="x" type="button">Close ✕</button><div class="frame"></div></dialog>
<script src="{p}config.js"></script><script src="{p}v2.js" defer></script></body></html>'''
def img(p,n,alt,cls='',lazy=True,sizes='(max-width:860px) 100vw, 50vw',pos=''):
    return f'<img src="{p}img/{n}.webp" srcset="{p}img/{n}-sm.webp 800w, {p}img/{n}.webp 1600w" sizes="{sizes}" alt="{alt}"'+(' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"')+(f' style="object-position:{pos}"' if pos else '')+'>'
ENDORSE=[("Stuart is a passionate and driven leader with tremendous EQ, commercial acumen, and organizational agility. He's an asset and a force multiplier.","Jonathan Thompson","Chief Executive Officer, Nielsen-Massey Vanillas"),
("A visionary executive who builds high-performing business models, develops exceptional teams, and consistently delivers results with integrity and character.","David Stis","Chief Commercial Officer, Del Monte Foods"),
("One of the most passionate and motivating leaders I've ever met. Stuart consistently rallies organizations to deliver beyond expectations.","David Klavsons","Chief Executive Officer, King Juice"),
("A strategic executive who combines vision, innovation, and disciplined execution while inspiring teams and driving measurable business growth.","Sheila Rondeau","CEO, MOGXP"),
("Stuart saw strengths in me I didn't yet recognize. His mentorship shaped both my career and the leader I've become.","John Albert III","Chief Executive Officer, Unified Building Group"),
("A high-performing commercial leader whose passion, strategic thinking, and ability to build new capabilities consistently drive growth and innovation.","Saverio Spontella","Chief Commercial &amp; Marketing Officer")]
PILLARS=[("Perspective","“The difference between stress and challenge is perspective.”","Name It. Perspective-ize It. Find A Way. Build the Checklist."),
("Discipline","“Successful people do what unsuccessful people don’t want to do.”","Find the Fight. Weigh It. Take It First. Sign It."),
("Your Real Competition Is You","“Your real competition is not the person across from you. It is who you were yesterday.”","Pick Your Opponent. Watch the Film. Corner Talk. Win the Round."),
("Servant Leadership &amp; the Power of the Team","“Judge people by the full body of their work, not their worst five minutes.”","Build Your Corner. Resource Them. Listen Without Ego. Let Them Own the Fix."),
("Championship Performance","“Three things happen every day: excuses, apologies and results. Only one of them matters.”","The Daily Fight Card: a three-minute morning routine.")]
def pillars_html():
    return '<div class="pillars">'+''.join(f'<div class="pillar rv"><span class="n" aria-hidden="true">0{i+1}</span><div><h3>{t}</h3><p class="tool"><b>The tool:</b> {tool}</p></div><blockquote>{q}</blockquote></div>' for i,(t,q,tool) in enumerate(PILLARS))+'</div>'
def reel(p):
    return f'<a class="reel rv" href="https://www.youtube.com/watch?v=5sc7bOOXswY" data-video="5sc7bOOXswY" target="_blank" rel="noopener" aria-label="Play Stuart Warren Dansby speaker reel (opens video)">{img(p,"keynote","",sizes="(max-width:860px) 100vw, 1240px",pos="50% 45%")}<span class="play" aria-hidden="true"><i></i></span><span class="lbl">Speaker reel · Watch Stuart on stage</span></a>'
def field(id,label,typ='text',req=True,full=False,opts=None,auto='',ph=''):
    r=' required aria-required="true"' if req else ''
    o='' if req else ' <span class="opt">(optional)</span>'
    ad=f' aria-describedby="{id}-err"' if req else ''
    a=f' autocomplete="{auto}"' if auto else ''
    lab=label.replace('&amp;','&')
    if opts: ctl=f'<select id="{id}" name="{id}" data-label="{lab}"{r}{ad}><option value="">Select one</option>'+''.join(f'<option>{x}</option>' for x in opts)+'</select>'
    elif typ=='area': ctl=f'<textarea id="{id}" name="{id}" data-label="{lab}"{r}{ad} placeholder="{ph}"></textarea>'
    else: ctl=f'<input id="{id}" name="{id}" type="{typ}" data-label="{lab}"{r}{ad}{a}>'
    return f'<div class="field{" full" if full else ""}"><label for="{id}">{label}{o}</label>{ctl}'+(f'<span class="err" id="{id}-err" aria-live="polite"></span>' if req else '')+'</div>'
def w(path,html):
    os.makedirs(os.path.dirname(R+'/'+path),exist_ok=True); open(R+'/'+path,'w').write(html)

# ================= CORPORATE =================
p=''
corp=head(p,'Stuart Warren Dansby | Corporate Keynotes &amp; Workshops | Taking the Fight','Not motivational speaking. Stuart Warren Dansby brings 30 years of building people and businesses, and a championship at 62, into five practical pillars your team can use Monday morning.','')+hdr(p,'corp')+f'''
<main id="main">
<section class="hero"><div class="hero-media"><img src="{p}../assets/stuart-stage.webp" srcset="{p}../assets/stuart-stage-small.webp 800w, {p}../assets/stuart-stage.webp 1920w" sizes="100vw" alt="" fetchpriority="high" style="object-position:80% 30%"></div><div class="wrap">
<span class="eyebrow">Keynotes · Workshops · Follow-through</span>
<h1>Inspiration fades by Monday. <span class="red">Behavior doesn’t.</span></h1>
<p class="lede">Stuart Warren Dansby spent 30 years building people and businesses, then started fighting at 48 and won a championship at 62. He turns both into five practical pillars your team can put to work the next morning.</p>
<div class="actions"><a class="btn btn-red" data-book="corp" href="#contact">Book a 20-minute discovery call <span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="https://www.youtube.com/watch?v=5sc7bOOXswY" data-video="5sc7bOOXswY" target="_blank" rel="noopener">▶ Watch the reel</a></div>
<div class="hero-meta"><div><b>30+ yrs</b>Building businesses &amp; leaders</div><div><b>62</b>Championship belt, vs. a 32-year-old</div><div><b>30+</b>Awards for the documentary</div><div><b>2025</b>MMAM Hall of Fame</div></div>
</div></section>

<div class="marquee" aria-hidden="true"><div><span>Perspective</span><span>Discipline</span><span>Your Real Competition Is You</span><span>Servant Leadership</span><span>Championship Performance</span><span>Perspective</span><span>Discipline</span><span>Your Real Competition Is You</span><span>Servant Leadership</span><span>Championship Performance</span></div></div>

<section class="sec cream" id="different"><div class="wrap">
<div class="split top"><div class="rv"><span class="eyebrow">This isn’t motivational speaking</span><h2>The story opens the door. The system changes the work.</h2></div>
<div class="rv"><p class="lede">Most keynotes leave a room energized and unchanged. Stuart’s story connects with people, and the Five Pillars give them something to do with that feeling: one tool per pillar, built to be used the next day without thinking about it.</p><p>“This isn’t about fighting. Fighting is just where I learned these lessons. You’ll never have to throw a punch. But you already have a fight.”</p></div></div>
<div class="versus rv" role="table" aria-label="Taking the Fight compared with generic motivational speaking">
<div class="h" role="columnheader">Generic motivational talk</div><div class="h" role="columnheader">Taking the Fight</div>
<div class="no" role="cell">A highlight-reel life story</div><div class="yes" role="cell">A ring story paired with a business story, every time</div>
<div class="no" role="cell">Energy that fades by Monday</div><div class="yes" role="cell">A four-step tool for each pillar, used the next day</div>
<div class="no" role="cell">Speaker who has never run a P&amp;L</div><div class="yes" role="cell">30 years leading teams, budgets and turnarounds</div>
<div class="no" role="cell">One event, then nothing</div><div class="yes" role="cell">30- and 60-day follow-through that drives it into action</div>
</div></div></section>

<section class="sec" id="pillars"><div class="wrap">
<div class="split top"><div class="rv"><span class="eyebrow">The operating system</span><h2>The Five Pillars of Taking the Fight</h2></div><p class="lede rv">Each pillar pairs a true story from the ring with a true story from business, is backed by published research, and ends with one simple tool. The test for every one: can someone use it Monday morning?</p></div>
{pillars_html()}
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">{reel(p)}</div></section>

<section class="sec cream" id="credibility"><div class="wrap">
<div class="split"><div class="rv"><span class="eyebrow">Credibility</span><h2>Tested where payroll is real.</h2><p class="lede">Stuart’s defining strength is developing people, then building the process and execution around them. That’s why Taking the Fight starts with people: sustainable performance does too.</p>
<p>John Albert started as a young gym-membership salesperson who struggled to sell. Under Stuart’s coaching he became owner and CEO of a company generating roughly $85M and growing.</p></div>
<figure class="photo tall rv">{img(p,"stage","Stuart Warren Dansby speaking on stage in front of the Taking the Fight logo",pos="50% 20%")}<figcaption>On stage · Taking the Fight</figcaption></figure></div>
<div class="stats rv"><div class="stat"><b>5×+</b><span>Revenue growth helping build a multi-club fitness business</span><small>World Gym</small></div>
<div class="stat"><b>1 → 5</b><span>Offices, with annual revenue grown from ~$2.5M to $9.5M by 2007</span><small>Mortgage &amp; real estate finance</small></div>
<div class="stat"><b>$75M</b><span>Trade investment governed; a 12-person team supporting ~$120M revenue</span><small>BSN / Glanbia</small></div>
<div class="stat"><b>$85M</b><span>Company now led by a CEO Stuart developed from entry level</span><small>People development</small></div></div>
</div></section>

<section class="sec" id="offers"><div class="wrap">
<div class="split top"><div class="rv"><span class="eyebrow">Ways to work with Stuart</span><h2>Inspire. Apply. Develop. Reinforce.</h2></div><p class="lede rv">Meet your people at the level the moment requires, from a single keynote to a full curriculum with follow-through. Every engagement is scoped on a discovery call.</p></div>
<div class="ladder">
<article class="rung rv"><span class="step">01 · Keynote</span><span class="dur">45–60 minutes</span><h3>The Keynote</h3><p>The story creates connection and introduces the Five Pillars.</p><span class="verb">Inspire</span></article>
<article class="rung feature rv"><span class="step">02 · Breakout workshop</span><span class="dur">90 minutes</span><h3>Keynote + Breakout</h3><p>Teams apply the Five Pillars to their own real performance challenges and leave with a plan.</p><span class="verb">Apply</span></article>
<article class="rung rv"><span class="step">03 · Full course</span><span class="dur">~8 hours over 2–3 days</span><h3>The Full Course</h3><p>A deeper curriculum on all five pillars, from understanding to application and sustained performance.</p><span class="verb">Develop</span></article>
<article class="rung rv"><span class="step">04 · Coaching</span><span class="dur">Ongoing</span><h3>Coaching &amp; Mentoring</h3><p>The principles move from an event into continued personal and professional development.</p><span class="verb">Develop</span></article>
<article class="rung rv"><span class="step">05 · Follow-through</span><span class="dur">30 and 60 days</span><h3>Follow-Through</h3><p>Reinforcement that helps leaders and teams drive the pillars into action.</p><span class="verb">Reinforce</span></article>
</div>
<p class="muted rv" style="margin-top:1.5rem;font-size:.95rem">Built for people &amp; culture development, operational excellence, organizational leadership, commercial growth, and strategy &amp; execution.</p>
</div></section>

<section class="sec char" id="story"><div class="wrap">
<div class="split"><figure class="photo tall rv">{img(p,"faceoff","Stuart Warren Dansby facing off with his opponent before a fight",pos="50% 30%")}<figcaption>Started at 48 · Champion at 62</figcaption></figure>
<div class="rv"><span class="eyebrow">The fight behind the framework</span><h2>Started at 48. Champion at 62.</h2>
<p class="lede">With no fighting background, grade 4 arthritis in both knees and life-altering injuries, Stuart could understand a technique in a session but needed weeks of repetition before his body could use it under pressure.</p>
<p>He lost 20 rounds in sparring to win one. He kept showing up. At 62 he won a championship against a 32-year-old, and the award-winning documentary <em>Taking the Fight</em> chronicles his six-year saga.</p>
<p class="muted">The limitation was never comprehension. It was physical adaptation. That is the lesson your team needs most.</p></div></div>
<div class="stories">
<article class="story rv"><b>Ego</b><p>After about ten festival rejections, Stuart removed his own executive producer credit from the festival version. No one asked him to. Two weeks later, the film won its first festival.</p><span class="lesson">Mission before ego</span></article>
<article class="story rv"><b>24 hrs</b><p>No graphics budget, no graphics person. A professional who believed in the mission said “give it to me” and created the Taking the Fight logo in about a day.</p><span class="lesson">Ownership &amp; the tribe</span></article>
<article class="story rv"><b>16</b><p>Nico, once a fearful young karate student, asked to score the film. Given ten minutes of footage, he earned the rest, and won four awards for Best Original Music Score.</p><span class="lesson">Courage over comfort</span></article>
<article class="story rv"><b>85</b><p>Festival submissions. 26 selections. 30+ awards. Absorb rejection, learn, adjust, continue: the same willingness to lose 20 rounds to win one.</p><span class="lesson">Keep going</span></article>
</div></div></section>

<section class="sec" id="standard"><div class="wrap">
<span class="eyebrow rv">The personal standard</span><h2 class="rv" style="max-width:16ch">Three pillars Stuart has lived by for decades.</h2>
<div class="pp">
<article class="rv"><span class="num">01</span><h3>You can’t outwork me. Period.</h3><p>Effort, preparation and showing up again tomorrow are controllable. It’s a refusal to be outworked in pursuit of the goal in front of him.</p></article>
<article class="rv"><span class="num">02</span><h3>You can’t have a stronger desire to learn.</h3><p>Learning is a daily discipline, not a phase of life. There is always something to improve, question or understand more deeply.</p></article>
<article class="rv"><span class="num">03</span><h3>You can’t have a more positive attitude.</h3><p>Positivity doesn’t ignore reality. It chooses the perspective and energy that allow productive action instead of surrendering to the obstacle.</p></article>
</div></div></section>

<section class="sec cream" id="endorsements"><div class="wrap">
<span class="eyebrow rv">What leaders say</span><h2 class="rv" style="max-width:14ch">A force multiplier for teams.</h2>
<div class="endorse">'''+''.join(f'<blockquote class="rv"><p>{q}</p><footer><strong>{n}</strong>{t}</footer></blockquote>' for q,n,t in ENDORSE)+f'''</div></div></section>

<section class="sec" id="quote" style="text-align:left"><div class="wrap"><blockquote class="big-quote rv">“Everything you do in life has <em>your signature</em> on it. Everything.”</blockquote><p class="attrib rv">— Stuart Warren Dansby</p></div></section>

<section class="cta" id="contact" aria-labelledby="cta-h"><div class="wrap">
<div class="split top"><div class="rv"><span class="eyebrow" style="color:#FFE3DF">Start with a conversation</span><h2 id="cta-h">Tell Stuart what your team is up against.</h2>
<p class="lede">Twenty minutes, directly with Stuart. No pitch deck. He’ll ask about your people, your event and the fight in front of you, and tell you honestly whether Taking the Fight is the right fit.</p>
<div class="actions"><a class="btn btn-dark" data-book="corp" href="mailto:info@takingthefight.com">Book a discovery call with Stuart <span class="arr" aria-hidden="true">→</span></a></div>
<p class="cta-note">Booking for Florida teams and organizations nationwide. Prefer to send details first? Use the form.</p></div>
<div class="panel rv" style="background:var(--cream);color:var(--char);border:0"><h3 style="margin-bottom:1.2rem">Send an inquiry</h3>
<form class="form" data-mail="Speaking inquiry: Stuart Warren Dansby" action="mailto:info@takingthefight.com" method="post" enctype="text/plain" novalidate>
{field("name","Your name",auto="name")}{field("org","Organization",auto="organization")}{field("email","Work email","email",auto="email")}{field("phone","Phone","tel",False,auto="tel")}
{field("format","What are you considering?",opts=["Keynote (45–60 min)","Keynote + 90-min breakout","Full course (2–3 days)","Coaching & mentoring","Not sure yet"],full=True)}
{field("when","Event date or timeframe",req=False)}{field("size","Audience size",req=False)}
{field("msg","What’s the fight your team is facing?","area",False,True,ph="A few sentences about your audience and goals")}
<div class="full"><button class="btn btn-red" type="submit" style="width:100%">Send inquiry <span class="arr" aria-hidden="true">→</span></button></div>
<p class="form-status" role="status" aria-live="polite"></p></form></div></div></div></section>
</main>'''+ftr(p)
w('index.html',corp)

# ================= EDUCATION =================
p='../'
edu=head(p,'Taking the Fight for Students &amp; Schools | Stuart Warren Dansby','Workplace readiness built on five practical pillars. Stuart Warren Dansby helps students build the discipline, accountability and resilience employers expect.','education/')+hdr(p,'edu')+f'''
<main id="main">
<section class="hero"><div class="hero-media"><img src="{p}../assets/stuart-bio.webp" srcset="{p}../assets/stuart-bio-small.webp 800w, {p}../assets/stuart-bio.webp 1920w" sizes="100vw" alt="" fetchpriority="high" style="object-position:72% 25%"></div><div class="wrap">
<span class="eyebrow">Students · Schools · Colleges · Youth programs</span>
<h1>Ready for what <span class="red">comes next.</span></h1>
<p class="lede">Students leave school with knowledge. Employers want discipline, accountability, resilience and ownership. Taking the Fight gives students a practical framework for both, from a man who started fighting at 48 and became a champion at 62.</p>
<div class="actions"><a class="btn btn-red" data-book="edu" href="#contact">Talk with Stuart about your students <span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="https://www.youtube.com/watch?v=5sc7bOOXswY" data-video="5sc7bOOXswY" target="_blank" rel="noopener">▶ Watch the reel</a></div>
</div></section>

<section class="sec cream"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow">The gap</span><h2>The skills nobody grades, and every employer hires for.</h2></div>
<div class="rv"><p class="lede">Many students enter the workplace without enough preparation in the human skills and performance mindset employers expect. Taking the Fight connects real human challenges to practical skills and ownership.</p>
<div class="skills" aria-label="Skills students build"><span>Discipline</span><span>Accountability</span><span>Resilience</span><span>Communication</span><span>Ownership</span><span>Teamwork</span><span>Responding to challenge</span></div>
<p>The Five Pillars become a framework for workplace readiness, self-improvement and championship performance, in class, on a team, in a first job and in life.</p></div></div></div></section>

<section class="sec"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow">Five pillars, student-sized</span><h2>Lessons from the ring. Tools for Monday.</h2></div><p class="lede rv">Same core framework, with examples drawn from academics, campus jobs, athletics, student organizations, career prep and family.</p></div>
{pillars_html()}</div></section>

<section class="sec char"><div class="wrap"><div class="split"><figure class="photo wide rv">{img(p,"belt","Stuart Warren Dansby holding his championship belt",pos="50% 30%")}<figcaption>Champion at 62</figcaption></figure>
<div class="rv"><span class="eyebrow">Why students listen</span><h2>Courage starts with fear.</h2><p class="lede">Nico was a young karate student who was afraid. Stuart talked with him about courage and living outside his comfort zone. Nico became a Junior National Karate Champion, then, at 16, scored the entire <em>Taking the Fight</em> documentary and won four awards for Best Original Music Score.</p><p class="muted">“The foundation of courage is fear.”</p></div></div></div></section>

<section class="sec"><div class="wrap"><span class="eyebrow rv">Formats for schools</span><h2 class="rv" style="max-width:15ch">From one assembly to a semester of follow-through.</h2>
<div class="ladder four">
<article class="rung rv"><span class="step">Assembly or keynote</span><span class="dur">45–60 minutes</span><h3>The Story</h3><p>Connection first. The Five Pillars introduced through the fight and the film.</p><span class="verb">Inspire</span></article>
<article class="rung feature rv"><span class="step">Classroom workshop</span><span class="dur">90 minutes</span><h3>Apply It</h3><p>Students apply the pillars to their own challenges with worksheets and a daily practice.</p><span class="verb">Apply</span></article>
<article class="rung rv"><span class="step">Multi-day program</span><span class="dur">2–3 days</span><h3>Go Deep</h3><p>The full curriculum for leadership programs, athletics and career-readiness tracks.</p><span class="verb">Develop</span></article>
<article class="rung rv"><span class="step">Follow-through</span><span class="dur">30 and 60 days</span><h3>Make It Stick</h3><p>Weekly reinforcement, with a teacher or advisor update each week.</p><span class="verb">Reinforce</span></article>
</div></div></section>

<section class="sec cream"><div class="wrap"><blockquote class="big-quote rv" style="color:var(--char)">“Your real competition is not the person across from you. It is <em style="color:var(--red)">who you were yesterday.</em>”</blockquote><p class="attrib rv" style="color:#6E6A64">— Stuart Warren Dansby</p></div></section>

<section class="cta" id="contact" aria-labelledby="cta-h"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow" style="color:#FFE3DF">For educators &amp; program leaders</span><h2 id="cta-h">Give your students a fight worth taking.</h2>
<p class="lede">Start with a short call with Stuart about your students, your calendar and what you want them to walk away with.</p>
<div class="actions"><a class="btn btn-dark" data-book="edu" href="mailto:info@takingthefight.com">Book a call with Stuart <span class="arr" aria-hidden="true">→</span></a></div></div>
<div class="panel rv" style="background:var(--cream);color:var(--char);border:0"><h3 style="margin-bottom:1.2rem">Tell us about your school</h3>
<form class="form" data-mail="Education inquiry: Taking the Fight" action="mailto:info@takingthefight.com" method="post" enctype="text/plain" novalidate>
{field("name","Your name",auto="name")}{field("school","School or organization",auto="organization")}{field("email","Email","email",auto="email")}{field("role","Your role",req=False)}
{field("level","Student level",opts=["High school","College / university","Career or technical program","Youth or athletics program","Other"],full=True)}
{field("msg","What would you like students to walk away with?","area",False,True)}
<div class="full"><button class="btn btn-red" type="submit" style="width:100%">Send inquiry <span class="arr" aria-hidden="true">→</span></button></div>
<p class="form-status" role="status" aria-live="polite"></p></form></div></div></div></section>
</main>'''+ftr(p)
w('education/index.html',edu)

# ================= COURSE =================
LES=[("Perspective","“Stress is what happens to you. Challenge is what you decide to do about it.”","At 62, the state licensing body tried to keep Stuart out of his title fight with test after test. He turned the stress into a challenge.","Name It. Perspective-ize It. F.A.W. (Find A Way). Build the Checklist.","18–20 min"),
("Discipline","“Successful people do what unsuccessful people don’t want to do.”","Training twice a day for his first fight in a ring while running a major budget as a new Director of Sales Operations.","Find the Fight. Weigh It. Take It First. Sign It.","19–21 min"),
("Your Real Competition Is You","“Your real competition is not the person across from you. It is who you were yesterday.”","A world champion’s challenge, the worst sparring day of camp, and the next morning across from a top-ranked UFC middleweight.","Pick Your Opponent. Watch the Film. Corner Talk. Win the Round.","21–23 min"),
("Servant Leadership &amp; the Power of the Team","“Good people will put more pressure on themselves than you ever can. So don’t put pressure on them.”","Two rival coaches who only came together to corner Stuart, and a VP who owned a budget miss with “we.”","Build Your Corner. Resource Them. Listen Without Ego. Let Them Own the Fix.","18–20 min"),
("Championship Performance","“Three things happen every day: excuses, apologies and results. Only one of them matters.”","The title fight at 62: moved to the main event, walking out in complete peace, and every pillar inside one night.","The Daily Fight Card: a three-minute morning routine.","14–16 min")]
p='../'
course=head(p,'The Five Pillars of Taking the Fight | Online Course | Stuart Warren Dansby','An online course from Stuart Warren Dansby: five video lessons, worksheets and a 5-week follow-through camp. Join the early-access list.','course/')+hdr(p,'course')+f'''
<main id="main">
<section class="hero course-hero"><div class="hero-media">{img(p,"spar","",sizes="100vw")}</div><div class="wrap ch-grid"><div>
<span class="badge">Coming soon · Early access open</span>
<h1>We all have <span class="red">a fight.</span></h1>
<p class="lede">The Five Pillars of Taking the Fight: the five principles that took Stuart Warren Dansby from no fighting background in his late 40s to a championship belt at 62, built to use at work, in school and in life, starting the Monday after you finish.</p>
<div class="actions"><a class="btn btn-red" href="#early-access">Get early access <span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="#lessons">See what’s inside</a></div>
<div class="hero-meta"><div><b>5</b>Video lessons + intro</div><div><b>~1h 40m</b>Total video</div><div><b>5</b>Worksheets &amp; process cards</div><div><b>5 weeks</b>Follow-through camp</div></div>
</div><figure class="cover"><img src="{p}img/cover.webp" srcset="{p}img/cover-sm.webp 527w, {p}img/cover.webp 1054w" sizes="(max-width:860px) 70vw, 420px" width="1054" height="1492" fetchpriority="high" alt="Taking the Fight poster: Stuart Warren Dansby with his championship belt"></figure></div></section>

<section class="sec cream"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow">Not a course about fighting</span><h2>You’ll never throw a punch. You already have a fight.</h2></div>
<div class="rv"><p class="lede">Every lesson pairs a true story from the ring with a true story from business, backs it with published research, and ends with one simple tool you can use the next day.</p>
<ul class="includes"><li>A 14–23 minute video lesson built around one true story and a four-step tool</li><li>A downloadable worksheet with write-in space and a 6-day daily practice</li><li>A one-page process card for your desk or phone</li><li>A 5-week email camp, one pillar per week, so it actually sticks</li></ul></div></div></div></section>

<section class="sec" id="lessons"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow">The curriculum</span><h2>Five lessons. Five tools.</h2></div><p class="lede rv">Starts with a welcome from Stuart at his desk: why a fighter is teaching business and life, and how to get the most from the course.</p></div>
<div class="lessons">'''+''.join(f'<article class="lesson rv"><span class="n" aria-hidden="true">0{i+1}</span><div><span class="eyebrow" style="margin-bottom:.8rem">Lesson {i+1}</span><h3>{t}</h3><p class="q">{q}</p></div><div><p class="muted" style="margin:0;font-size:.95rem">{s}</p><p class="tool"><b>Tool:</b> {tool}</p></div><span class="rt">{rt}</span></article>' for i,(t,q,s,tool,rt) in enumerate(LES))+f'''</div></div></section>

<section class="sec cream"><div class="wrap"><span class="eyebrow rv">The follow-through camp</span><h2 class="rv" style="max-width:15ch">The course doesn’t end when the videos do.</h2>
<p class="lede rv">Five weeks, one pillar per week, matched to each lesson’s daily practice. Real emails from a real inbox, with replies welcome.</p>
<div class="weeks">
<div class="week rv"><b>Week 1</b><h3>Perspective</h3><p>Monday kickoff, Thursday nudge</p></div>
<div class="week rv"><b>Week 2</b><h3>Discipline</h3><p>Monday kickoff, Thursday nudge</p></div>
<div class="week rv"><b>Week 3</b><h3>Real Competition</h3><p>Kickoff, nudge and a checkpoint video from Stuart</p></div>
<div class="week rv"><b>Week 4</b><h3>Servant Leadership</h3><p>Monday kickoff, Thursday nudge</p></div>
<div class="week rv"><b>Week 5</b><h3>Championship</h3><p>The Daily Fight Card all week, then graduation</p></div>
</div></div></section>

<section class="sec char"><div class="wrap"><div class="split"><figure class="photo tall rv">{img(p,"ring","Stuart Warren Dansby in the ring during a fight",pos="50% 40%")}<figcaption>Started at 48 · Champion at 62</figcaption></figure>
<div class="rv"><span class="eyebrow">Your instructor</span><h2>Stuart Warren Dansby</h2><p class="lede">Thirty years building and contributing to businesses as a commercial growth executive. A seven-year fighting career, a championship at 62 against a 32-year-old, and induction into the MMAM Hall of Fame in 2025.</p><p>Co-executive producer of the award-winning documentary <em>Taking the Fight</em>, selected by 26 festivals with 30+ awards.</p><p class="muted">“I am simply the conduit to deliver the message.”</p></div></div></div></section>

<section class="cta" id="early-access" aria-labelledby="ea-h"><div class="wrap"><div class="split top"><div class="rv"><span class="eyebrow" style="color:#FFE3DF">Early access</span><h2 id="ea-h">Be first in line.</h2>
<p class="price" data-price></p>
<p class="lede">Join the early-access list and you’ll hear first when the course opens, including any launch offer. No spam, just the date and the door.</p>
<div class="actions"><a class="btn btn-dark" data-checkout href="#early-access" hidden>Enroll now <span class="arr" aria-hidden="true">→</span></a></div>
<p class="cta-note">Buying for a team or a school? Corporate and education groups get the same camp plus a weekly manager or teacher update. Note it in the form.</p></div>
<div class="panel rv" style="background:var(--cream);color:var(--char);border:0"><h3 style="margin-bottom:1.2rem">Join the early-access list</h3>
<form class="form" data-mail="Early access: The Five Pillars of Taking the Fight" action="mailto:info@takingthefight.com" method="post" enctype="text/plain" novalidate>
{field("name","First name",auto="given-name")}{field("email","Email","email",auto="email")}
{field("for","Who is this for?",opts=["Just me","My team or company","My school or students"],full=True)}
{field("msg","Anything you want Stuart to know?","area",False,True,ph="Optional")}
<div class="full"><button class="btn btn-red" type="submit" style="width:100%">Request early access <span class="arr" aria-hidden="true">→</span></button></div>
<p class="form-status" role="status" aria-live="polite"></p></form></div></div></div></section>

<section class="sec cream"><div class="wrap" style="max-width:860px"><span class="eyebrow">Questions</span><h2>Good to know</h2><div class="faq">
<details><summary>Do I need any fighting or fitness background?</summary><p>No. Fighting is just where Stuart learned these lessons. Every tool is built for work, school and everyday life.</p></details>
<details><summary>How long does it take?</summary><p>About 1 hour 40 minutes of video across the intro and five lessons, paced one pillar per week alongside the 5-week follow-through camp.</p></details>
<details><summary>Can I buy it for my team or school?</summary><p>Yes. Group buyers get the same camp plus a weekly email for the manager or teacher. Mention it in the early-access form or email <a data-email href="mailto:info@takingthefight.com">info@takingthefight.com</a>.</p></details>
<details><summary>When does it open?</summary><p>Filming is underway. Early-access members hear the launch date first.</p></details>
</div></div></section>
</main>'''+ftr(p)
w('course/index.html',course)
print('ok')
