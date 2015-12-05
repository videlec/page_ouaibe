[comment]: # (Copyright 2015 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

Comment marche ce site
======================

Dans ce bref article, j'explique comment j'ai construit ce site ouaibe.
Il s'adresse plutôt à des gens connaissant (ou voulant
découvrir) les langages [HTML](https://fr.wikipedia.org/wiki/Hypertext_Markup_Language)
et [Python](https://fr.wikipedia.org/wiki/Python_%28langage%29).

Tout le code de ce site ouaibe (incluant le contenu des pages) est disponible sur
github: [https://github.com/videlec/page_ouaibe](https://github.com/videlec/page_ouaibe).

La première remarque importante est qu'il s'agit d'un site ouaibe
statique. Autrement dit, il ne s'agit que de pages HTML. Il utilise quand
même [MathJax](https://www.mathjax.org/) (c'est du javascript) pour mettre
en forme les formules mathématiques.

Il y a un script principal ([generate.py](https://github.com/videlec/page_ouaibe/blob/master/generate.py)) qui est un fichier Python et
qui s'occuppe de recoller les morceaux. Les morceaux (i.e. les pages)
sont divisées en deux catégories: les pages principales (i.e. ce qui est
disponible dans le menu en haut) et les articles (i.e. le contenu de la section
Misc).

Les page principales
--------------------

Chaque page est un template [jinja](http://jinja.pocoo.org/). Jinja c'est à la
fois un format de fichier et une librairie Python qui permet de les transformer.
Un template jinja est un fichier qui décrit la structure d'une page. On peut rajouter
dedans des substitutions comme

    Voici la liste de mes animaux: {{ mes_animaux }}

ou bien des boucles

    :::html
    <ul>
    {% for animal in animaux %}
    <li> {{ animal }} </li>
    {% endfor %}
    </ul>

Pour fabriquer la page à partir du template il faut lui expliquer quoi
mettre dans les trous (`mes_animaux` et `animaux` ci-dessus). C'est le
script principal qui s'occupe de ça. Pour avoir un exemple concret,
la liste de mes articles n'est pas codée en dur dans le template. Il
s'agit d'un fichier [json](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation)
([publications.json](https://github.com/videlec/page_ouaibe/blob/master/webpage/data/publications.json)). C'est encore une fois le
script principal qui s'occupe de le lire.

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
