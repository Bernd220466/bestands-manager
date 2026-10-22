import re, json, html, sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from terms import TERMS
def slug(t):
    t=t.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
names={t[0] for t in TERMS}
for t in TERMS:
    for r in t[4]: assert r in names,(t[0],r)
T=sorted(TERMS,key=lambda x:x[0].lower().replace('ä','a').replace('ö','o').replace('ü','u'))
letters=[]; body=[]
cur=None
for name,cat,defi,form,rel in T:
    L=name[0].upper()
    if L!=cur:
        if cur: body.append('</div>')
        cur=L; letters.append(L)
        body.append(f'<h2 class="g-letter" id="buchstabe-{L.lower()}">{L}</h2><div class="g-group">')
    rels=' · '.join(f'<a href="#{slug(r)}">{html.escape(r)}</a>' for r in rel)
    fh=f'<p class="g-formula"><span>Formel</span>{html.escape(form)}</p>' if form else ''
    body.append(f'''<article class="g-term" id="{slug(name)}" data-cat="{cat}" data-text="{html.escape((name+' '+defi).lower())}">
<h3>{html.escape(name)} <span class="g-cat">{cat}</span></h3>
<p>{html.escape(defi)}</p>{fh}
<p class="g-rel">Siehe auch: {rels}</p></article>''')
body.append('</div>')
cats=sorted({t[1] for t in TERMS})
ld={"@context":"https://schema.org","@type":"DefinedTermSet","name":"Glossar Bestandsmanagement","url":"https://bestands-manager.com/glossar.html",
    "hasDefinedTerm":[{"@type":"DefinedTerm","name":t[0],"description":t[2],"url":"https://bestands-manager.com/glossar.html#"+slug(t[0])} for t in T]}
page=f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Glossar Bestandsmanagement · Bestands-Manager.com</title>
<meta name="description" content="Glossar Bestandsmanagement: {len(T)} Begriffe von ABC-Analyse bis Ziel-Reichweite – verständlich erklärt, mit Formeln. Für Händler, Einkäufer und Disponenten.">
<link rel="canonical" href="https://bestands-manager.com/glossar.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0F1E38">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>
.glossar{{max-width:860px;margin:0 auto;padding-block:48px 72px}}
.glossar h1{{font-size:clamp(2.4rem,6vw,3.4rem);margin-bottom:14px}}
.g-lead{{color:var(--muted);font-size:1.1rem;max-width:62ch;margin:0 0 28px}}
.g-tools{{position:static;z-index:5;background:var(--bg);padding:14px 0 12px;border-bottom:1px solid var(--line);margin-bottom:8px}}
@media (min-width:760px){{.g-tools{{position:sticky;top:0;z-index:5}}}}
.g-search{{width:100%;font:inherit;font-size:1.05rem;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}}
.g-search:focus{{outline:3px solid var(--orange);outline-offset:1px}}
.g-chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}}
.g-chips button{{font:inherit;font-size:.9rem;padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}}
.g-chips button[aria-pressed="true"]{{background:var(--navy);color:var(--on-navy);border-color:var(--navy)}}
.g-az{{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:10px;font-family:var(--display);font-weight:700;font-size:1.1rem}}
.g-az a{{text-decoration:none;color:var(--orange-ink)}}
.g-letter{{font-size:2rem;color:var(--orange-ink);margin:34px 0 6px;scroll-margin-top:170px}}
.g-term{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:12px 0;scroll-margin-top:170px}}
.g-term:target{{border-color:var(--orange);box-shadow:0 0 0 3px var(--orange-soft)}}
.g-term h3{{font-size:1.45rem;margin:0 0 6px;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px}}
.g-term p{{margin:0 0 8px}}
.g-cat{{font-family:var(--body);font-weight:600;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.g-formula{{font-size:.95rem;background:var(--bg);border-left:3px solid var(--orange);padding:8px 12px;border-radius:4px}}
.g-formula span{{display:block;font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--orange-ink)}}
.g-rel{{font-size:.92rem;color:var(--muted)}}
.g-empty{{display:none;color:var(--muted);margin-top:24px}}
.g-cta{{margin-top:48px;background:var(--navy);color:var(--on-navy);border-radius:12px;padding:28px}}
.g-cta h2{{color:var(--on-navy);font-size:1.9rem;margin-bottom:8px}}
.g-cta p{{color:var(--on-navy-muted);margin:0 0 16px}}
.g-cta a.btn{{display:inline-block;background:var(--orange);color:#fff;text-decoration:none;font-weight:700;padding:11px 18px;border-radius:8px;margin:4px 8px 4px 0}}
.g-cta a.btn.ghost{{background:transparent;border:1px solid var(--on-navy-muted);color:var(--on-navy)}}
</style>
</head>
<body>
<header class="top">
  <div class="wrap subnav">
    <a class="logo" href="index.html">Bestands-Manager<span>.com</span></a>
    <a class="back" href="index.html">Zur Startseite</a>
  </div>
</header>
<main class="wrap glossar">
<p class="eyebrow">Glossar</p>
<h1>Bestandsmanagement von A bis Z</h1>
<p class="g-lead">Die wichtigsten Begriffe rund um Lager, Bestand und Disposition – kurz und verständlich erklärt, mit Formeln zum Nachrechnen. Das Glossar wächst laufend.</p>
<div class="g-tools">
  <input class="g-search" id="q" type="search" placeholder="Begriff suchen, z. B. Reichweite" aria-label="Glossar durchsuchen">
  <div class="g-chips" role="group" aria-label="Nach Thema filtern">
    <button type="button" data-cat="" aria-pressed="true">Alle</button>
    {''.join(f'<button type="button" data-cat="{c}" aria-pressed="false">{c}</button>' for c in cats)}
  </div>
  <nav class="g-az" aria-label="Alphabet">{''.join(f'<a href="#buchstabe-{l.lower()}">{l}</a>' for l in letters)}</nav>
</div>
{chr(10).join(body)}
<p class="g-empty" id="empty">Kein Begriff gefunden. Fehlt Ihnen etwas? Schreiben Sie an info@bestands-manager.com.</p>
<section class="g-cta">
  <h2>Wie viel Geld steckt in Ihrem Lager?</h2>
  <p>Wenden Sie die Begriffe direkt auf Ihre Zahlen an – kostenlos und ohne Anmeldung.</p>
  <a class="btn" href="rechner.html">Lagerkosten-Rechner</a><a class="btn ghost" href="index.html#check">Gratis-Bestands-Check</a>
</section>
<p class="small" style="margin-top:24px;color:var(--muted)">Stand: Oktober 2026 · {len(T)} Begriffe · Alle Erklärungen sind eigene Texte von Bestands-Manager.com.</p>
</main>
<footer>
  <div class="wrap">
    <div><strong>Bestands-Manager.com</strong><br>Bernd Schäfer · Thomas-Mann-Straße 12 · 67574 Osthofen</div>
    <div><a href="https://www.linkedin.com/in/bernd-schaefer-bestandsmanager" target="_blank" rel="noopener">LinkedIn</a> · <a href="glossar.html">Glossar</a> · <a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></div>
  </div>
</footer>
<script>
(function(){{
  const q=document.getElementById('q'), terms=[...document.querySelectorAll('.g-term')], groups=[...document.querySelectorAll('.g-group')], btns=[...document.querySelectorAll('.g-chips button')], empty=document.getElementById('empty');
  let cat='';
  function apply(){{
    const s=q.value.trim().toLowerCase(); let n=0;
    terms.forEach(t=>{{const ok=(!cat||t.dataset.cat===cat)&&(!s||t.dataset.text.includes(s)); t.hidden=!ok; if(ok)n++;}});
    groups.forEach(g=>{{const vis=[...g.children].some(c=>!c.hidden); g.hidden=!vis; g.previousElementSibling.hidden=!vis;}});
    empty.style.display=n?'none':'block';
  }}
  q.addEventListener('input',apply);
  btns.forEach(b=>b.addEventListener('click',()=>{{cat=b.dataset.cat; btns.forEach(x=>x.setAttribute('aria-pressed',x===b)); apply();}}));
}})();
</script>
</body>
</html>
'''
import os
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','glossar.html'),'w',encoding='utf-8').write(page)
print(len(T),letters)
