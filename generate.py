#!/usr/bin/env python
# -*- coding: utf8 -*-

#*****************************************************************************
#       Copyright (C) 2015 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import codecs
import datetime
import markdown
import json
import os
import shutil

from webpage.process_article import process_article
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('webpage', 'templates'))

DATA_DIR = 'webpage/data/'
ARTICLES_DIR = 'webpage/articles/'

def article_list():
    articles = []
    for article in os.listdir(ARTICLES_DIR):
        if not article.endswith('.md'):
            print "WARNING: {} does not end in .md (ignored)".format(article)
            continue
        filename = os.path.join(ARTICLES_DIR, article)
        articles.append((os.path.getmtime(filename), filename))
    articles.sort()
    return articles

data = {}
for kind in ["journals",
             "publications",
             "prepublications",
             "conference_papers"]:
    print "Loading json data: {}".format(kind)
    data[kind] = json.load(open(os.path.join(DATA_DIR, kind + '.json')))

for content in ["general_presentation",
                "research_description"]:
    filename = os.path.join(DATA_DIR, content + '.md')
    print "Loading {}".format(filename)
    with codecs.open(filename, encoding='utf-8') as f:
        data[content] = markdown.markdown(f.read())

blog_posts = []
for mtime, article in article_list():
    name = os.path.splitext(os.path.split(article)[-1])[-2]
    print "Loading blog post {}".format(name)
    with codecs.open(article, encoding='utf-8') as f:
        title = f.readline()
    mtime = datetime.datetime.fromtimestamp(mtime)
    blog_posts.append({'name': name,
                       'path': article,
                       'source': name+'.md',
                       'url': name+'.html',
                       'mtime': mtime,
                       'lastmodif': mtime.strftime("%y/%m/%d"),
                       'title': title})
data['blog_posts'] = blog_posts

pages = [
   {'link': 'index.html', 'name': u'Présentation', 'template': 'index.html'},
   {'link': 'research.html', 'name': u'Recherche', 'template': 'research.html'},
   {'link': 'teaching.html', 'name': u'Enseignement, diffusion', 'template': 'teaching.html'},
   {'link': 'programming.html', 'name': u'Programmation', 'template': 'programming.html'},
   {'link': 'contact.html', 'name': u'Contact', 'template': 'contact.html'},
   {'link': 'blog.html', 'name': u'Misc', 'template': 'blog.html'}
   ]

for page in pages:
    page['status'] = 'unselected'

for page in pages:
    print u"Generate {}".format(page['name'])
    template = env.get_template(page['template'])
    filename = os.path.join('output', page['template'])
    page['status'] = 'selected'
    with codecs.open(filename, "w", encoding='utf-8') as output:
        output.write(template.render(pages=pages, **data))
    page['status'] = 'unselected'

page['status'] = 'selected'  # reselect the blog !!
template = env.get_template('base_blog.html')

for blog in blog_posts:
    input_filename = blog['path']
    name = blog['name']
    output_filename = os.path.join('output', name + '.html')

    shutil.copy(input_filename, 'output/')

    print "process blog '{}' last modified on {}".format(name, blog['lastmodif'])

    with codecs.open(input_filename, encoding="utf-8") as f:
        content = process_article(f.read())

    with codecs.open(output_filename, "w", encoding="utf-8") as f:
        f.write(template.render(blog_content=content, pages=pages))
