import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {projects,pillars,featuredProjectIds,projectUrl} from '../dist/projects.mjs';
import {renderCard,renderDetail} from '../dist/app.mjs';

const root=new URL('../dist/',import.meta.url);
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pillarCards=pillars.map(p=>`<a class="pillar-card pillar-${p.id}" href="/projets.html?categorie=${p.id}" aria-labelledby="pillar-${p.id}"><div class="pillar-card-top"><span class="mono">${p.number} /</span><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></div><h3 id="pillar-${p.id}">${escape(p.title)}</h3><p>${escape(p.description)}</p><span class="pillar-card-count mono">${String(projects.filter(project=>project.category===p.id).length).padStart(2,'0')} PROJET${projects.filter(project=>project.category===p.id).length>1?'S':''}</span></a>`).join('');

function rewriteProjectLinks(html){return html.replace(/href="#projet-([a-z0-9-]+)"/g,(_,id)=>`href="/projets/${id}.html"`);}
for(const file of ['index.html','projets.html','a-propos.html','parcours.html']){
  const path=new URL(file,root);
  let html=await readFile(path,'utf8');
  html=html.replace(/class="nav-count">\d+<\/span>/g,`class="nav-count">${String(projects.length).padStart(2,'0')}</span>`);
  html=html.replace(/(data-filter="([^"]+)"[^>]*>[\s\S]*?<span>)\d+(<\/span>)/g,(_,start,id,end)=>`${start}${String(projects.filter(project=>id==='all'||project.category===id).length).padStart(2,'0')}${end}`);
  html=html.replace('<!-- PILLAR-CARDS -->',pillarCards);
  const collection=file==='index.html'?featuredProjectIds.map(id=>projects.find(p=>p.id===id)):projects;
  html=html.replace('<div class="project-grid" id="project-grid"></div>',`<div class="project-grid" id="project-grid">${collection.map((p,index)=>renderCard(p,file!=='index.html'&&collection.length%2===1&&index===collection.length-1,file==='index.html'?3:2)).join('')}</div>`);
  html=html.replace('<p class="sr-only" role="status" id="project-count"></p>',`<p class="sr-only" role="status" id="project-count">${collection.length} projets affichés.</p>`);
  html=rewriteProjectLinks(html);
  await writeFile(path,html);
}

const homepage=await readFile(new URL('index.html',root),'utf8');
const prefix=homepage.slice(0,homepage.indexOf('  <main id="contenu">'));
const suffix=homepage.slice(homepage.indexOf('  </main>')+'  </main>'.length);
await mkdir(new URL('projets/',root),{recursive:true});
for(const project of projects){
  const title=`${project.title} — Elfie Zoungrana · Portfolio`;
  let head=prefix.replace(/<title>.*?<\/title>/,`<title>${escape(title)}</title>`)
    .replace(/<meta name="description" content="[^"]*">/,`<meta name="description" content="${escape(project.short)}">`)
    .replace(/<meta property="og:title" content="[^"]*">/,`<meta property="og:title" content="${escape(title)}">`)
    .replace(/<meta property="og:description" content="[^"]*">/,`<meta property="og:description" content="${escape(project.short)}">`)
    .replace('data-page="home" class="page-home"',`data-page="project" data-project="${project.id}" class="page-project"`);
  const html=`${head}  <main id="contenu"><article class="project-page section-wrap">${renderDetail(project)}</article></main>${suffix}`;
  await writeFile(new URL(`projets/${project.id}.html`,root),html);
}
console.log(`${projects.length} project pages generated across ${pillars.length} pillars.`);
