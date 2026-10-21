# Elfie Zoungrana — Projets & Expériences Numériques

Portfolio personnel : projets de licence, expériences professionnelles et engagements associatifs dans le numérique, le design et la communication.

## Le contenu

Le site comprend quatre pages principales — accueil, projets, à propos et parcours — et une page pour chacun des douze projets. Les images, les documents présentés et la vidéo sont inclus. Les maquettes Figma et les créations Canva restent accessibles par leurs liens.

## Modifier le site

- `dist/projects.mjs` : textes et ressources des projets.
- `src/page-template.html` : contenu et structure des pages principales.
- `scripts/build_pages.py` : préparation des pages HTML.
- `dist/app.mjs` : navigation, filtres et interactions.
- `dist/styles.css`, `dist/pages.css` et `dist/portfolio.css` : présentation du site.
- `dist/assets/` : images, documents, polices et vidéo.

Après une modification des textes ou de la structure, lancer avec Python 3 et Node.js installés :

```sh
python3 scripts/build_pages.py
```

Les fichiers à publier se trouvent dans `dist/`. Ils sont déjà générés dans ce dépôt ; aucun abonnement à un outil de création n’est nécessaire pour servir ces fichiers.

## Héberger le portfolio

Pour Netlify, importer ce dépôt et utiliser `dist` comme dossier de publication. Le fichier `netlify.toml` contient ce réglage. Les pages déjà générées peuvent être publiées sans commande de construction.

Pour GitHub Pages dans un sous-dossier, adapter les chemins des liens et des ressources au nom du dépôt avant de publier.

## Crédits

Les fiches précisent les contributions personnelles, les réalisations de groupe et les éléments appartenant à d’autres autrices, auteurs ou structures. Les crédits présents dans les documents et les visuels sont conservés.

© Elfie Zoungrana.
