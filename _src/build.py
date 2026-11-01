#!/usr/bin/env python3
"""Assemble course chapters: shared shell (header, footer, menu, dialogs) + chapter fragment.

Each fragment in _src/lessons/<file>.html starts with a JSON front-matter comment:
<!--{"chapter":"2.1","title":"…","crumb":"Parte 2 · <b>2.1 Contextualização</b>"}-->
followed by the <section class="slide"> elements, then optionally a <script> block
with chapter-specific code. The script must end with PSP.start(); if absent, it is added.

English: _src/i18n/apply.py swaps the English translations (_src/i18n/en/c*.json, keyed by the position of each Portuguese string in
pt_list.json) into copies of the fragments: _src/lessons-en/ + _src/shell.en.html. They are built into en/ (same file names; assets/ is
shared, so its links get a "../" in front). A Portuguese string with no translation stops the English build and is listed.
Run: python3 _src/build.py   (from the course root; add --no-en to skip the English pages)
"""
import html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def alternate(body):
    """Every other light slide gets class s-white (pure white); the rest stay light grey. Red slides (s-navy) are skipped."""
    n = 0
    def mark(m):
        nonlocal n
        if 's-navy' in m.group(1).split():
            return m.group(0)
        n += 1
        return m.group(0) if n % 2 else '<section class="%s s-white"' % m.group(1)
    return re.sub(r'<section class="(slide[^"]*)"', mark, body)



PAGE = re.compile(r'(?<=["\'`])(\d-\d)-[a-z0-9-]+\.html')   # a link to another page: "2-1-contextualizacao.html#…"


def short_links(out, up):
    """Every page lives in a short folder (2-1/index.html), so a link to "2-1-contextualizacao.html" becomes "2-1/", from wherever
    the page is ("../2-1/" from inside another page's folder). The home page is the folder itself."""
    out = PAGE.sub(lambda m: up + m.group(1) + '/', out)
    return re.sub(r'(?<=["\'`])index\.html(?=["\'`#])', up or './', out)


def build(shell_file, lessons, dest, shared_prefix=''):
    """shared_prefix: the way from this language's root (dest) to the course root, where assets/ is ('' for Portuguese, '../' for en/).
    Short addresses: index.html stays at the root of dest; every other fragment is written as <dest>/<2-1>/index.html."""
    shell = shell_file.read_text(encoding='utf-8')
    dest.mkdir(exist_ok=True)
    for old in dest.glob('[0-9]-[0-9]-*.html'):   # the long file names of earlier builds
        old.unlink()
    slides = []   # for slides.json (review tool): hash id = m<chapter>-<data-id>, global order
    for frag in sorted(lessons.glob('*.html'), key=lambda f: (f.name != 'index.html', f.name)):
        src = frag.read_text(encoding='utf-8')
        m = re.match(r'\s*<!--(\{.*?\})-->', src, re.S)
        meta = json.loads(m.group(1))
        body = alternate(src[m.end():])
        script = ''
        sm = re.search(r'<script>(.*?)</script>\s*$', body, re.S)
        if sm:
            script = sm.group(1).strip()
            body = body[:sm.start()]
        if 'PSP.start()' not in script:
            script += '\nPSP.start();'
        out = (shell.replace('{{TITLE}}', meta['title'])
                    .replace('{{CHAPTER}}', meta['chapter'])
                    .replace('{{CRUMB}}', meta['crumb'])
                    .replace('{{SLIDES}}', body.strip())
                    .replace('{{SCRIPT}}', script))
        home = frag.name == 'index.html'
        up = '' if home else '../'                      # from this page to its language root
        prefix = up + shared_prefix                     # from this page to the course root (assets/)
        out = short_links(out, up)
        if prefix:
            # assets/ and downloads/ stay in the course root: every reference that opens a quote, a backtick or a url( gets the prefix
            out = re.sub(r'''(?<=["'`(])((?:assets|downloads)/)''', prefix + r'\1', out)
        target = dest / 'index.html' if home else dest / frag.name[:3] / 'index.html'
        target.parent.mkdir(exist_ok=True)
        target.write_text(out, encoding='utf-8')
        for sec in re.finditer(r'<section class="slide[^"]*"([^>]*)>', body):
            a = sec.group(1)
            sid = re.search(r'data-id="([^"]+)"', a).group(1)
            ttl = re.search(r'data-title="([^"]*)"', a)
            slides.append({'id': 'm%s-%s' % (meta['chapter'].replace('.', '-'), sid), 'module': meta['title'], 'title': html.unescape(ttl.group(1)) if ttl else sid, 'order': len(slides) + 1})
        print('built', dest.relative_to(ROOT) if dest != ROOT else '.', frag.name, len(out))
    (dest / 'slides.json').write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding='utf-8')


build(ROOT / '_src' / 'shell.html', ROOT / '_src' / 'lessons', ROOT)
if '--no-en' not in sys.argv:
    r = subprocess.run([sys.executable, str(ROOT / '_src' / 'i18n' / 'apply.py')], cwd=ROOT)
    if r.returncode:
        sys.exit('English fragments not built (see the messages above); the Portuguese pages are done.')
    build(ROOT / '_src' / 'shell.en.html', ROOT / '_src' / 'lessons-en', ROOT / 'en', '../')
