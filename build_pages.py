from pathlib import Path
import re
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / 'src/page-template.html').read_text()
prefix, body = template.split('  <main id="contenu">', 1)
_, suffix = body.split('  </main>', 1)

def section(section_id):
    found = re.search(r'<section\b[^>]*\bid="' + re.escape(section_id) + r'".*?</section>', body, re.S)
    if not found:
        raise ValueError(f'Missing section: {section_id}')
    return found.group(0)

def page_heading(content, heading_id):
    pattern = r'<h2 id="' + re.escape(heading_id) + r'">(.*?)</h2>'
    return re.sub(pattern, lambda match: f'<h1 id="{heading_id}">{match.group(1)}</h1>', content, count=1, flags=re.S)

hero = section('accueil')
pillars = section('piliers')
projects = section('projets')
about = section('a-propos')
journey = section('parcours')
strip = re.search(r'<div class="interest-strip".*?</div></div>', body, re.S).group(0)
closing = re.search(r'<section class="closing-section".*?</section>', body, re.S).group(0)

home_projects = re.sub(r'<div class="project-toolbar">.*?</label>\s*</div>', '', projects, flags=re.S)
home_projects = home_projects.replace('01 / Mes projets', '01 / Une sélection de projets')
home_projects = home_projects.replace('<div class="collection-note mono">', '<div class="all-projects-link"><a class="button button-secondary" href="/projets.html">Tous mes projets <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a></div><div class="collection-note mono">')

about_teaser = '''<section class="about-home"><div class="section-wrap about-home-inner"><div class="about-home-mark" aria-hidden="true">E<span>.Z</span><svg><use href="#i-star"/></svg></div><div><p class="eyebrow">LA PERSONNE DERRIÈRE LES PROJETS</p><h2>Créative, curieuse.<br>Et tournée vers <span class="serif">les autres.</span></h2><p>Des projets de cours aux engagements associatifs, le numérique offre beaucoup de choses à découvrir. Au fil des expériences, une même envie : apprendre, créer et échanger avec les autres.</p><a class="text-link" href="/a-propos.html">En savoir plus sur moi <span aria-hidden="true">↗</span></a></div></div></section>'''

motivations = '''<section class="motivation-section section-wrap" aria-labelledby="motivations-title"><p class="eyebrow">CE QUI ME MOTIVE</p><div class="motivation-layout"><h2 id="motivations-title">La tech m’intéresse.<br>Ce qu’elle rend<br><span class="serif">possible, encore plus.</span></h2><div class="motivation-list"><article><span class="mono">01</span><div><h3>Comprendre avant de créer</h3><p>Un projet commence par des questions simples : à qui s’adresse-t-il, et de quoi cette personne a-t-elle besoin ? Les réponses aident à choisir les informations, le format et les étapes.</p></div></article><article><span class="mono">02</span><div><h3>Une tech plus ouverte</h3><p>Les sciences et la tech m’intéressent, avec l’envie que davantage de filles s’y sentent à leur place. Les engagements avec BECOMTECH et Elles bougent permettent de rencontrer des professionnelles, de partager des expériences et de faire découvrir ces métiers.</p><div class="association-links"><a class="small-link" href="#projet-becomtech">BECOMTECH <span aria-hidden="true">↗</span></a><a class="small-link" href="#projet-elles-bougent">Elles bougent <span aria-hidden="true">↗</span></a></div></div></article><article><span class="mono">03</span><div><h3>Travailler en équipe</h3><p>Écouter les idées, se répartir les tâches et avancer ensemble : le travail en équipe fait partie de mes expériences de cours et d’association. Chacun apporte son regard, et les projets évoluent grâce aux échanges.</p></div></article></div></div></section>'''

interests = '''<section class="interests-section section-wrap" aria-labelledby="interests-title"><p class="eyebrow">EN DEHORS DES PROJETS</p><h2 id="interests-title">D’autres<br><span class="serif">découvertes.</span></h2><div class="interests-grid"><article><span class="mono">01 /</span><h3>Lecture & récits</h3><p>Lire des romans de différents horizons pour découvrir des histoires et d’autres façons de voir le monde.</p></article><article><span class="mono">02 /</span><h3>Culture & découvertes</h3><p>Voyager, visiter des musées contemporains et découvrir d’autres cultures à travers la cuisine.</p></article><article><span class="mono">03 /</span><h3>Sciences & technologies</h3><p>Découvrir de nouveaux outils et comprendre ce qu’ils changent dans notre quotidien.</p></article></div></section>'''

connections = '''<section class="connections-section section-wrap" aria-labelledby="connections-title"><p class="eyebrow">CE QUE CES EXPÉRIENCES M’APPRENNENT</p><h2 id="connections-title">Apprendre,<br>puis <span class="serif">mettre en pratique.</span></h2><div class="connection-list"><a href="#projet-nextstep"><span class="mono">ANALYSER & CONCEVOIR</span><p>Comprendre les besoins, organiser les informations et imaginer les étapes d’une application.</p><span class="small-link">Avec NextStep <span aria-hidden="true">↗</span></span></a><a href="#projet-paris8-communication"><span class="mono">RÉDIGER & INTÉGRER</span><p>Écrire selon le support, mettre les contenus en ligne et vérifier leur affichage.</p><span class="small-link">Au service communication de Paris 8 <span aria-hidden="true">↗</span></span></a><a href="#projet-becomtech"><span class="mono">COORDONNER & PRÉSENTER</span><p>Organiser le travail d’une équipe, préparer une rencontre et prendre la parole.</p><span class="small-link">Avec BECOMTECH <span aria-hidden="true">↗</span></span></a></div></section>'''

pages = {
  'index.html': ('home', 'Elfie Zoungrana — Projets & Expériences Numériques', hero + strip + pillars + home_projects + about_teaser + closing),
  'projets.html': ('projects', 'Mes projets — Elfie Zoungrana', page_heading(projects, 'projects-title') + closing),
  'a-propos.html': ('about', 'À propos — Elfie Zoungrana · Portfolio', page_heading(about, 'about-title') + motivations + interests + closing),
  'parcours.html': ('journey', 'Mon parcours — Elfie Zoungrana', page_heading(journey, 'journey-title') + connections + closing)
}

for filename, (name, title, content) in pages.items():
    header = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', prefix)
    header = header.replace('<body>', f'<body data-page="{name}" class="page-{name}">')
    html = header + '  <main id="contenu">\n' + content + '\n  </main>' + suffix
    for anchor, destination in [('accueil', '/#accueil'), ('projets', '/projets.html'), ('parcours', '/parcours.html'), ('a-propos', '/a-propos.html')]:
        html = html.replace(f'href="#{anchor}"', f'href="{destination}"')
    if name == 'home':
        html = html.replace('href="/projets.html">Voir mes projets', 'href="/projets.html">Voir mes projets')
    (ROOT / 'dist' / filename).write_text(html)
    print(filename)

subprocess.run(['node',str(ROOT/'scripts/build_project_pages.mjs')],check=True,cwd=ROOT)
