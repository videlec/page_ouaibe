"""
CodeHilite Extension for Python-Markdown
========================================

Adds code/syntax highlighting to standard Python-Markdown code blocks.

See <https://Python-Markdown.github.io/extensions/code_hilite>
for documentation.

Original code Copyright 2006-2008 [Waylan Limberg](http://achinghead.com/).

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class SageCell(object):
    """
    Determine language of source code, and make it a Sage cell.

    Basic Usage:
        >>> code = SageCell(src = 'sage: 1+1')
        >>> html = code.sage_cell()

    * src: Source string or any object with a .readline attribute.

    * linenums: (Boolean) Set line numbering to 'on' (True),
      'off' (False) or 'auto'(None). Set to 'auto' by default.

    * guess_lang: (Boolean) Turn language auto-detection
      'on' or 'off' (on by default).

    * css_class: Set class name of wrapper div ('codehilite' by default).

    * hl_lines: (List of integers) Lines to emphasize, 1-indexed.

    Low Level Usage:
        >>> code = CodeHilite()
        >>> code.src = 'some text' # String or anything with a .readline attr.
        >>> code.linenos = True  # Turns line numbering on or of.
        >>> html = code.hilite()

    """
    template = """<div class="computecell"><script type="text/x-sage">\n{}\n</script></div>"""

    def __init__(self, src=None, linenums=None, guess_lang=True,
                 css_class="codehilite", lang=None, style='default',
                 noclasses=False, tab_length=4, hl_lines=None, use_pygments=True):
        self.src = src

    def sage_cell(self):
        """
        Pass code to the [Pygments](http://pygments.pocoo.org/) highliter with
        optional line numbers. The output should then be styled with css to
        your liking. No styles are applied by default - only styling hooks
        (i.e.: <span class="k">).

        returns : A string of html.

        """
        # remove "sage:" and "....:"
        output = ""
        lines = []
        for line in self.src.split('\n'):
            if line.startswith(':::'):
                continue
            if line.startswith('>>> ') or line.startswith('... '):
                lines.append(line[4:])
            elif line and lines:  # assume it is output
                output += self.template.format('\n'.join(lines))
                del lines[:]
        if lines:
            output += self.template.format('\n'.join(lines))
        return output


# ------------------ The Markdown Extension -------------------------------


class SageCellTreeprocessor(Treeprocessor):
    """ Hilight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        for block in root.iter('pre'):
            if len(block) == 1 and block[0].tag == 'code' and block[0].text.startswith(':::pycon'):
                code = SageCell(block[0].text)
                placeholder = self.markdown.htmlStash.store(code.sage_cell())
                # Clear codeblock in etree instance
                block.clear()
                # Change to p element which will later
                # be removed when inserting raw html
                block.tag = 'p'
                block.text = placeholder

class SageCellExtension(Extension):
    """ Add Sage cell to markdown codeblocks. """

    def __init__(self, **kwargs):
        # define default configs
        self.config = {}
        Extension.__init__(self, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add HilitePostprocessor to Markdown instance. """
        celler = SageCellTreeprocessor(md)
        celler.config = self.getConfigs()
        md.treeprocessors.add("sagecell", celler, "<inline")

        md.registerExtension(self)

def makeExtension(**kwargs):  # pragma: no cover
    return SageCellExtension(**kwargs)
