# Erzeugt /wissen/*.html aus den Artikeln unten. Aufruf: python3 _wissen/build.py
import os, json, re, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'wissen'); os.makedirs(OUT, exist_ok=True)
BASE = 'https://bestands-manager.com/'
src = open(os.path.join(ROOT, 'geld-im-regal-check.html')).read()
LOGO = re.search(r'(<a class="logo".*?</a>)', src, re.S).group(1).replace('href="index.html"', 'href="../index.html"')
FOOT = src[src.index('<footer>'):src.index('</footer>') + 9].replace('href="', 'href="../').replace('href="../https://', 'href="https://')

from articles import ARTICLES

CSS = '''.pg{max-width:780px;margin:0 auto;padding-block:48px 80px}
.pg h1{font-size:clamp(2rem,4.6vw,2.8rem);margin-bottom:12px;line-height:1.1}
.pg h2{font-size:1.5rem;margin:36px 0 10px}
.pg h3{font-size:1.15rem;margin:22px 0 6px}
.pg p,.pg li{line-height:1.65}.pg p{margin:0 0 12px}
.pg ul,.pg ol{padding-left:1.2em}.pg li{margin:5px 0}
.meta{color:var(--muted);font-size:.92rem;margin-bottom:22px}
.kurz{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--orange);border-radius:8px;padding:16px 20px;margin:18px 0 8px}
.kurz b{display:block;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--orange);margin-bottom:4px}
.kurz p{margin:0}
.formel{font-family:"Barlow Condensed",sans-serif;font-size:1.35rem;background:var(--surface);border-radius:8px;padding:12px 16px;text-align:center;margin:12px 0}
.pg table{width:100%;border-collapse:collapse;font-size:.95rem;margin:10px 0}
.pg th{background:var(--navy,#0F1E38);color:#fff;text-align:left;padding:8px}
.pg td{border-top:1px solid var(--line);padding:8px;vertical-align:top}
.tw{overflow-x:auto}
.fig{margin:22px 0}.fig img{width:100%;height:auto;display:block;border-radius:10px}
.fig figcaption{font-size:.85rem;color:var(--muted);margin-top:6px}
.cta{background:var(--navy,#0F1E38);color:#EEF2F8;border-radius:10px;padding:22px 24px;margin-top:36px}
.cta h2{color:#fff;margin-top:0}.cta a:not(.btn){color:var(--orange)}.cta .btn{color:#fff}
.cta .btn{margin-top:8px}
.faq details{border-top:1px solid var(--line);padding:10px 0}.faq summary{font-weight:700;cursor:pointer}
.mehr{display:grid;gap:10px;margin-top:10px}.mehr a{display:block;border:1px solid var(--line);border-radius:8px;padding:12px 14px;text-decoration:none}
.list{display:grid;gap:14px;margin-top:20px}.list a{display:block;border:1px solid var(--line);border-radius:10px;padding:16px 18px;text-decoration:none;color:inherit}
.list a b{display:block;font-size:1.15rem;margin-bottom:4px;color:var(--navy,#0F1E38)}
.list a span{color:var(--muted)}'''

def head(title, desc, url, img, img_alt, ld):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
<meta name="theme-color" content="#0F1E38">
<meta property="og:type" content="article">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Bestands-Manager.com">
<meta property="og:image" content="{img}">
<meta property="og:image:alt" content="{H.escape(img_alt)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="../styles.css?v=20261101">
<style>{CSS}</style>
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '</script>' + chr(10) for x in ld)}</head>
<body>
<header class="top"><div class="wrap subnav">{LOGO}<a class="back" href="index.html">Alle Artikel</a></div></header>
'''

AUTHOR = {"@type": "Person", "@id": BASE + "#bernd", "name": "Bernd Schäfer", "url": BASE + "#ueber", "jobTitle": "Berater für Bestandsoptimierung im Handel"}
PUB = {"@type": "Organization", "@id": BASE + "#firma", "name": "Bestands-Manager.com", "logo": {"@type": "ImageObject", "url": BASE + "img/icon-512.png"}}

def strip(s): return H.unescape(re.sub(r'<[^>]+>', '', s)).strip()

for a in ARTICLES:
    url = BASE + 'wissen/' + a['slug'] + '.html'
    img = BASE + f"img/{a['img']}-1200-bestands-manager.com.webp"
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['desc'], "image": img,
         "author": AUTHOR, "publisher": PUB, "datePublished": a['date'], "dateModified": a['date'], "inLanguage": "de",
         "mainEntityOfPage": url, "about": a['about']},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(ans)}} for q, ans in a['faq']]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Start", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Wissen", "item": BASE + "wissen/"},
            {"@type": "ListItem", "position": 3, "name": a['h1'], "item": url}]}]
    faq = ''.join(f'<details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in a['faq'])
    more = ''.join(f'<a href="{b["slug"]}.html">{b["h1"]}</a>' for b in ARTICLES if b is not a)
    body = f'''<main class="wrap pg">
<p class="eyebrow">Wissen für Händler</p>
<h1>{a['h1']}</h1>
<p class="meta">Von Bernd Schäfer · Bestandsoptimierung für den Handel · Stand {a['date_de']}</p>
<div class="kurz"><b>Kurz gesagt</b><p>{a['kurz']}</p></div>
<figure class="fig"><img src="../img/{a['img']}-1200-bestands-manager.com.webp" srcset="../img/{a['img']}-720-bestands-manager.com.webp 720w, ../img/{a['img']}-1200-bestands-manager.com.webp 1200w" sizes="(max-width:820px) 100vw, 780px" width="1200" height="800" alt="{H.escape(a['img_alt'])}"><figcaption>{a['img_alt']} · KI-Bild · Bestands-Manager.com</figcaption></figure>
{a['body']}
<h2>Häufige Fragen</h2>
<div class="faq">{faq}</div>
<div class="cta"><h2>{a['cta_h']}</h2><p>{a['cta_p']}</p><a class="btn btn-primary" href="{a['cta_href']}">{a['cta_btn']}</a></div>
<h2>Weiterlesen</h2>
<div class="mehr">{more}<a href="../glossar.html">Glossar: alle Fachbegriffe kurz erklärt</a></div>
</main>
'''
    open(os.path.join(OUT, a['slug'] + '.html'), 'w').write(head(a['title'], a['desc'], url, img, a['img_alt'] + ' · Bestands-Manager.com', ld) + body + FOOT + '\n</body>\n</html>\n')

# Übersicht
items = ''.join(f'<a href="{a["slug"]}.html"><b>{a["h1"]}</b><span>{a["kurz_list"]}</span></a>' for a in ARTICLES)
url = BASE + 'wissen/'
ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Wissen für Händler: Bestände optimieren", "url": url, "inLanguage": "de", "publisher": PUB,
       "hasPart": [{"@type": "Article", "headline": a['h1'], "url": BASE + 'wissen/' + a['slug'] + '.html'} for a in ARTICLES]}]
idx = head('Wissen für Händler: Bestände optimieren · Bestands-Manager.com', 'Praxisartikel für Groß- und Einzelhändler: Ladenhüter abbauen, Überbestand reduzieren, Sicherheitsbestand und Meldebestand berechnen. Mit Rechenbeispielen aus dem Handel.', url, BASE + 'img/vorschaubild.png', 'Bestands-Manager.com', ld).replace('<a class="back" href="index.html">Alle Artikel</a>', '<a class="back" href="../index.html#angebot">Alle Angebote</a>')
idx += f'''<main class="wrap pg">
<p class="eyebrow">Wissen für Händler</p>
<h1>Bestände optimieren: Praxiswissen für den Handel</h1>
<p>Kurze Antworten auf die Fragen, die sich Groß- und Einzelhändler zu ihrem Lager stellen. Mit Rechenbeispielen, ohne Statistik-Studium und ohne neue Software.</p>
<div class="list">{items}</div>
<p style="margin-top:28px">Mehr Fachbegriffe im <a href="../glossar.html">Glossar</a>. Alles zusammenhängend erklärt im Praxisbuch <a href="../buch.html">„Geld im Regal“</a>.</p>
</main>
''' + FOOT + '\n</body>\n</html>\n'
open(os.path.join(OUT, 'index.html'), 'w').write(idx)
print('ok', [a['slug'] for a in ARTICLES])
