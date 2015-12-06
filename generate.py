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
STATIC_DIR = 'webpage/static/'
OUTPUT_DIR = 'output/'

#TODO: implement timestamps for everything using a dependency mechanism

def article_list():
    articles = []
    for article in os.listdir(ARTICLES_DIR):
        if not article.endswith('.md'):
            print "WARNING: {} does not end in .md (ignored)".format(article)
            continue
        filename = os.path.join(ARTICLES_DIR, article)
        mtime = os.path.getmtime(filename)
        articles.append((mtime, article))
    articles.sort()
    return articles

# copy files from the static dir that are not already in the output one
for name in os.listdir(STATIC_DIR):
    static_filename = os.path.join(STATIC_DIR, name)
    output_filename = os.path.join(OUTPUT_DIR, name)

    static_mtime = os.path.getmtime(static_filename)
    try:
        output_mtime = os.path.getmtime(output_filename)
    except OSError:
        output_mtime = 0.0

    if static_mtime > output_mtime:
        print "Copy static file {}".format(name)
        shutil.copy(static_filename, output_filename)


mtime_data = 0.0
data = {}
for kind in ["journals",
             "publications",
             "prepublications",
             "conference_papers"]:
    print "Loading json data: {}".format(kind)
    filename = os.path.join(DATA_DIR, kind + '.json')
    data[kind] = json.load(open(filename))
    mtime_data = min(mtime_data, os.path.getmtime(filename))

for content in ["general_presentation",
                "research_description"]:
    filename = os.path.join(DATA_DIR, content + '.md')
    print "Loading {}".format(filename)
    with codecs.open(filename, encoding='utf-8') as f:
        data[content] = markdown.markdown(f.read())
    mtime_data = max(mtime_data, os.path.getmtime(filename))

blog_posts = []
mtime_posts = 0.0
for mtime, article in article_list():
    name = os.path.splitext(article)[-2]
    print "Loading blog post {}".format(name)
    filename = os.path.join(ARTICLES_DIR, article)
    with codecs.open(filename, encoding='utf-8') as f:
        title = None
        while not title or title.isspace() or title.startswith('[comment]'):
            title = f.readline()
    mtime_posts = max(mtime_posts, mtime)
    mtime_date = datetime.datetime.fromtimestamp(mtime)
    blog_posts.append({'name': name,
                       'path': os.path.join(ARTICLES_DIR, article),
                       'url': name+'.html',
                       'mtime': mtime,
                       'lastmodif': mtime_date.strftime("%y/%m/%d"),
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
    filename = os.path.join(OUTPUT_DIR, page['link'])
    template = os.path.join('webpage', 'templates', page['link'])
    page['mtime_template'] = os.path.getmtime(template)
    try:
        page['mtime_output'] = os.path.getmtime(filename)
    except OSError:
        page['mtime_output'] = 0.0

for page in pages:
    if page['mtime_output'] < max(page['mtime_template'], mtime_data):
        print u"Generate {}".format(page['name'])

        template = env.get_template(page['template'])
        filename = os.path.join('output', page['template'])
        page['status'] = 'selected'
        with codecs.open(filename, "w", encoding='utf-8') as output:
            output.write(template.render(pages=pages, **data))
        page['status'] = 'unselected'
    else:
        print u"Skip {} because already up to date".format(page['name'])

page['status'] = 'selected'  # reselect the blog !!
template = env.get_template('base_blog.html')

for blog in blog_posts:
    input_filename = blog['path']
    name = blog['name']
    output_filename = os.path.join('output', name + '.html')

    mtime_output = os.path.getmtime(output_filename)

    if mtime_output < blog['mtime']:
        print "Process blog '{}' last modified on {}".format(name, blog['lastmodif'])

        with codecs.open(input_filename, encoding="utf-8") as f:
            content = process_article(f.read())

        with codecs.open(output_filename, "w", encoding="utf-8") as f:
            f.write(template.render(blog_content=content, pages=pages))
    else:
        print "Skip blog '{}' because already up to date".format(name)
