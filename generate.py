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

import datetime
import markdown
import json
import os
import shutil
import subprocess
import re

from webpage.process_article import process_article
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('webpage', 'templates'))

DATA_DIR = 'webpage/data/'
ARTICLES_DIR = 'webpage/articles/'
STATIC_DIR = 'webpage/static/'
OUTPUT_DIR = 'output/'

re_sage_code = re.compile('    :::pycon')

def article_mtime(path):
    """Last commit time touching `path`, or fs mtime if untracked/dirty.

    Git time is used so the displayed date survives a fresh clone, where
    filesystem mtimes all reset to checkout time.
    """
    try:
        dirty = subprocess.check_output(
            ['git', 'status', '--porcelain', '--', path]).strip()
        if not dirty:
            ts = subprocess.check_output(
                ['git', 'log', '-1', '--format=%ct', '--', path]).strip()
            if ts:
                return int(ts)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return os.path.getmtime(path)

def article_list():
    articles = []
    for article in os.listdir(ARTICLES_DIR):
        if not article.endswith('.md'):
            print("WARNING: {} does not end in .md (ignored)".format(article))
            continue

        # check whether it contains Sage code
        with open(os.path.join(ARTICLES_DIR, article)) as f:
            try:
                next(re_sage_code.finditer(f.read()))
                has_sage_code = True
            except StopIteration:
                has_sage_code = False

        filename = os.path.join(ARTICLES_DIR, article)
        articles.append((article_mtime(filename), article, has_sage_code))
    articles.sort()
    return articles

for name in os.listdir(STATIC_DIR):
    print("Copy static file {}".format(name))
    shutil.copy(os.path.join(STATIC_DIR, name), os.path.join(OUTPUT_DIR, name))

data = {}
for kind in ["journals",
             "publications",
             "conference_papers",
             "news"]:
    print("Loading json data: {}".format(kind))
    filename = os.path.join(DATA_DIR, kind + '.json')
    data[kind] = json.load(open(filename))

# Split the merged publications list: an entry is a prepublication iff it has
# no associated venue (no `journal` for an article, no `book-title` for a book
# chapter).
all_pubs = data['publications']
data['publications'] = [p for p in all_pubs if 'journal' in p or 'book-title' in p]
data['prepublications'] = [p for p in all_pubs if 'journal' not in p and 'book-title' not in p]

# Process news items:
#  - render markdown `content` to HTML (drop the wrapping <p>...</p>)
#  - format `date` for display: an ISO single date "YYYY-MM-DD" becomes
#    "5 avril 2027", a range "YYYY-MM-DD to YYYY-MM-DD" becomes "du 5 au 28
#    avril 2027" (or wider variants for cross-month / cross-year ranges)
#  - sort the list newest-first using the start of the interval; future
#    events naturally float to the top by date and need no extra label.
MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
             'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

def _fmt_fr(iso_date):
    y, m, d = iso_date.split('-')
    return "{} {} {}".format(int(d), MONTHS_FR[int(m) - 1], y)

def format_news_date(date_field):
    if ' to ' in date_field:
        start, end = date_field.split(' to ', 1)
        sy, sm, sd = start.split('-')
        ey, em, ed = end.split('-')
        if sy == ey and sm == em:
            return "du {} au {} {} {}".format(
                int(sd), int(ed), MONTHS_FR[int(sm) - 1], sy)
        if sy == ey:
            return "du {} {} au {} {} {}".format(
                int(sd), MONTHS_FR[int(sm) - 1],
                int(ed), MONTHS_FR[int(em) - 1], sy)
        return "du {} au {}".format(_fmt_fr(start), _fmt_fr(end))
    return _fmt_fr(date_field)

for item in data['news']:
    html = markdown.markdown(item['content'])
    if html.startswith('<p>') and html.endswith('</p>'):
        html = html[3:-4]
    item['content'] = html
    item['date_display'] = format_news_date(item['date'])
    item['sort_date'] = item['date'].split(' to ', 1)[0]
data['news'].sort(key=lambda it: it['sort_date'], reverse=True)

for content in ["general_presentation",
                "research_description"]:
    filename = os.path.join(DATA_DIR, content + '.md')
    print("Loading {}".format(filename))
    with open(filename) as f:
        data[content] = markdown.markdown(f.read(),
                extensions=['markdown.extensions.tables'])

blog_posts = []
for mtime, article, has_sage_code in article_list():
    name = os.path.splitext(article)[-2]
    print("Loading blog post {}".format(name))
    filename = os.path.join(ARTICLES_DIR, article)
    with open(filename) as f:
        title = None
        while not title or title.isspace() or title.startswith('[comment]'):
            title = f.readline()
    mtime_date = datetime.datetime.fromtimestamp(mtime)
    blog_posts.append({'name': name,
                       'path': os.path.join(ARTICLES_DIR, article),
                       'url': name+'.html',
                       'lastmodif': mtime_date.strftime("%y/%m/%d"),
                       'title': title,
                       'sage': has_sage_code,
                       'url_sage': name + '_sage.html'
                       })

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
    print(u"Generate {}".format(page['name']))
    template = env.get_template(page['template'])
    filename = os.path.join('output', page['template'])
    page['status'] = 'selected'
    with open(filename, "w") as output:
        output.write(template.render(pages=pages, **data))
    page['status'] = 'unselected'

# Off-menu pages: rendered with the parent section highlighted in the nav so
# the visitor still feels anchored, but no extra entry in the top menu.
off_menu = [
    {'template': 'news.html', 'parent': 'index.html'},
]
for off in off_menu:
    print(u"Generate (off-menu) {}".format(off['template']))
    for page in pages:
        page['status'] = 'selected' if page['link'] == off['parent'] else 'unselected'
    template = env.get_template(off['template'])
    with open(os.path.join('output', off['template']), 'w') as output:
        output.write(template.render(pages=pages, **data))
for page in pages:
    page['status'] = 'unselected'

page['status'] = 'selected'  # reselect the blog !!
template = env.get_template('base_blog.html')
template_sage = env.get_template('base_blog_sagecell.html')

for blog in blog_posts:
    input_filename = blog['path']
    name = blog['name']
    output_filename = os.path.join('output', name + '.html')

    print("Process blog '{}' last modified on {}".format(name, blog['lastmodif']))

    with open(input_filename) as f:
        content = process_article(f.read())

    with open(output_filename, "w") as f:
        f.write(template.render(blog_content=content, pages=pages))

    if blog['sage']:
        output_filename_sage = os.path.join('output', name + '_sage.html')
        with open(input_filename) as f:
            content = process_article(f.read(), sage=True)
        with open(output_filename_sage, "w") as f:
            f.write(template_sage.render(blog_content=content, pages=pages))
