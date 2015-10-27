#!/usr/bin/env python

import re
import markdown
import os
import subprocess
import tempfile
import md5
from xdg import BaseDirectory


# Global vars
FENCED_BLOCK_RE = re.compile(
    r'^\{% dot\s+(?P<out>[^\s]+)\s*\n(?P<code>.*?)%}\s*$',
    re.MULTILINE | re.DOTALL
)


class DotBlockExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add DotBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)
        md.preprocessors.add('dot_block', DotBlockPreprocessor(md), "_begin")


class DotBlockPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        super(DotBlockPreprocessor, self).__init__(md)

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """
        print("text reading")
        text = "\n".join(lines)
        print("text read")
        while 1:
            m = FENCED_BLOCK_RE.search(text)
            if m:
                out_file = m.group('out')
                code = m.group('code')
                show = True
                if out_file[0] == '!':
                    show = False
                    out_file = out_file[1:]
                ext = os.path.splitext(out_file)[1][1:].strip()
                h_path = md5.new(out_file).hexdigest()
                h_code = md5.new(code).hexdigest()
                cache = BaseDirectory.save_cache_path('markdown-dot') + h_path
                if self.should_generate(out_file, cache, h_code):
                    self.ensure_dir_exists(out_file)
                    print("generate " + out_file)
                    dot = subprocess.Popen(['dot', '-T', ext, '-o', out_file], bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print("".join(dot.communicate(input=code.encode('utf8'))))
                else:
                    print("pass " + out_file)
                if show:
                    img = "![%s](%s)" % (os.path.basename(out_file), out_file)
                    text = '%s\n%s\n%s' % (text[:m.start()], img, text[m.end():])
                else:
                    text = '%s\n%s' % (text[:m.start()], text[m.end():])
            else:
                break
        return text.split("\n")

    def ensure_dir_exists(self, f):
        d = os.path.dirname(f)
        if d and not os.path.exists(d):
            os.makedirs(d)

    def should_generate(self, f, cache, h):
        return not os.path.exists(f) or not os.path.exists(cache) or open(cache).read() != h


def makeExtension(*args, **kwargs):
    return DotBlockExtension(*args, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
