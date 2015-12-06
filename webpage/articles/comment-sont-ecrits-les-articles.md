[comment]: # (Copyright 2015 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

Comment marche ce site
======================

Dans ce bref article, j'explique comment j'ai construit ce site ouaibe.
Il s'adresse plutôt à des gens connaissant (ou voulant
découvrir) les langages [HTML](https://fr.wikipedia.org/wiki/Hypertext_Markup_Language)
et [Python](https://fr.wikipedia.org/wiki/Python_%28langage%29).

Tout le code qui a servi à construire ce site ouaibe est disponible sur
github: [https://github.com/videlec/page_ouaibe](https://github.com/videlec/page_ouaibe).

La première remarque importante est qu'il s'agit d'un site ouaibe
statique. Le ouaibe c'est principalement du HTML et il y a trois façon de faire

 1. on écrit directement des pages HTML (statique),

 2. on écrit un programme qui écrit des pages HTML (statique++),

 3. on écrit un programme qui génère du code HTML à la demande (dynamique).

Ce site est dans la deuxième catégorie. La partie visible du site n'est cependant
pas que du HTML. Il y aussi du CSS (pour les règles de mise en page) ainsi que
du javascript ([MathJax](https://www.mathjax.org/)) pour mettre
en forme les formules mathématiques.

Le programme principal qui construit les pages HTML s'appelle
[generate.py](https://github.com/videlec/page_ouaibe/blob/master/generate.py).
C'est un programme Python qui s'occuppe de recoller des morceaux: d'un côté
des squelettes (ou template) et de l'autre des données.

Les page principales
--------------------

Par page principale j'entends les pages accessibles par le menu en haut ("Présentation",
"Recherche", etc). Chacune de ces pages est un template [jinja](http://jinja.pocoo.org/).
Jinja c'est à la fois un format de fichier et une librairie Python qui permet de les transformer.
Un template jinja est un fichier dans lequel on a le droit de faire des substitutions

    Voici la liste de mes animaux: {{ mes_animaux }}

ou bien des boucles

    :::html
    <ul>
    {% for animal in animaux %}
    <li> {{ animal }} </li>
    {% endfor %}
    </ul>

Pour fabriquer la page à partir du template il faut lui expliquer quoi
mettre dans les trous (`mes_animaux` et `animaux` dans les exemples ci-dessus). C'est le
programme principal `generate.py` qui s'occupe de ça.

Un exemple concret de remplissage, est donnée par la liste de mes articles. La
template correspondant
([research.html](https://github.com/videlec/page_ouaibe/blob/master/webpage/templates/research.html)
ne contient pas cette liste. Il contient seulement des règles pour leur
mise en page qui ressemblent à

    :::html
    <ol reversed="true">
    {% for for pub in publications %}
    <li> {{ pub.title }}, {{ pub.journal }} {{ pub.volume }} n°{{ pub.issue }} ({{ pub.year }}) </li>
    {% endfor %}
    </ol>

C'est le programme principal qui construit la liste des publications à partir
d'un fichier [json](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation)
([publications.json](https://github.com/videlec/page_ouaibe/blob/master/webpage/data/publications.json)). Et c'est encore lui qui s'occuppe de réunir le template et les données
pour en faire une page HTML.

Les articles de la section Misc
-------------------------------

La section Misc est à part car je voulais que chaque article soit un fichier
simple à écrire et à réutiliser. J'ai choisi d'utiliser le langage
[Markdown](https://fr.wikipedia.org/wiki/Markdown). Le fichier
qui correspond à cet article est
[comment-sont-ecrits-les-articles.md](https://raw.githubusercontent.com/videlec/page_ouaibe/master/webpage/articles/comment-sont-ecrits-les-articles.md).

J'ai utilisé deux extensions de markdown. La première est [Pygments](http://pygments.org/)
qui permet de faire de la coloration syntaxique de code. Par exemple

	def hello():
        print 'hello world!'

devient

    :::python
    def hello():
       print 'hello world!'

La seconde est [python-markdown-math](https://pypi.python.org/pypi/python-markdown-math)
qui permet d'écrire des formules mathématiques en [Latex](https://fr.wikipedia.org/wiki/LaTeX).
Par exemple \frac{1}{2} devient \( \frac{1}{2} \) et on peut faire des choses
sophistiquées comme \[ \int_\mathbb{R} e^{\frac{-x^2}{2} } dx \].
