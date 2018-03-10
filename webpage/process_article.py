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
import markdown
import os

# for static version
from markdown.extensions.codehilite import CodeHiliteExtension
from .sageparser import SageCellExtension
from .mdx_math import MathExtension

code_hilite = CodeHiliteExtension([])
code_hilite.setConfig('guess_lang', False)
code_hilite.setConfig('css_class', 'code-highlight')

celler = SageCellExtension()

math = MathExtension()

def process_article(text, sage=False):
    extensions = [code_hilite, math, 'markdown.extensions.tables']
    if sage:
        extensions.insert(0, celler)

    return markdown.markdown(
        text,
        encoding="utf-8",
        extensions=extensions,
        )

