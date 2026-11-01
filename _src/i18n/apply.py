#!/usr/bin/env python3
"""Swap the English translations into copies of the Portuguese fragments.

Reads  _src/i18n/units.json (offsets), pt_list.json (frozen order) and en/c*.json (index -> English),
writes  _src/lessons-en/*.html  and  _src/shell.en.html.   Run from the course root:  python _src/i18n/apply.py
Every unit is checked before it is written: same tags, same ${…} expressions, same placeholders, same non-text attributes.
Exit code 1 if a check fails (the list is printed), so a bad translation never reaches the build.
"""
import glob, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
I18N = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(I18N))
import extract  # noqa: E402  (re-run so that the offsets always match the files on disk)

TEXT_ATTRS = {'alt', 'aria-label', 'title', 'data-title', 'data-k', 'data-cta', 'data-front', 'data-back', 'aria-roledescription', 'placeholder', 'data-tip'}
SVG = re.compile(r'<svg\b.*?</svg>', re.S)
TAG = re.compile(r'</?([A-Za-z][\w-]*)')
EXPR = re.compile(r'\$\{(?:[^{}]|\{[^{}]*\})*\}')
ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
AMP = re.compile(r'&(?!(?:[A-Za-z]+|#\d+|#x[0-9a-fA-F]+);)')
# units whose structure is deliberately different in English (the STOP names, a split() index)
STRUCT_OK = {950, 951, 953, 954}
BS = chr(92)
QUOTES = chr(39) + chr(34)


def skel(s):
    """JS expression with the text of its string literals removed (what is left is the code, which must not change)"""
    out, n = [], len(s)

    def code(i, closing=False):
        depth = 0
        while i < n:
            c = s[i]
            if c in QUOTES:
                out.append(c); i += 1
                while i < n and s[i] != c: i += 2 if s[i] == BS else 1
                out.append(c); i += 1; continue
            if c == '`':
                out.append('`'); i += 1
                while i < n and s[i] != '`':
                    if s[i] == BS: i += 2; continue
                    if s.startswith('${', i):
                        out.append('${'); i = code(i + 2, True); out.append('}'); continue
                    i += 1
                out.append('`'); i += 1; continue
            if c == '/' and i + 1 < n and s[i + 1] not in '/*' and out and out[-1] in '(,=:[!&|?{;':  # regex literal
                j = i + 1
                while j < n and s[j] != '/': j += 2 if s[j] == BS else 1
                out.append('/re/'); i = j + 1; continue
            if c == '{': depth += 1
            elif c == '}':
                if closing and depth == 0: return i + 1
                depth -= 1
            out.append(c); i += 1
        return i
    code(0)
    return ''.join(out)


def exprs(s):
    """every top-level ${…} of a unit, balanced"""
    res, i = [], 0
    while True:
        i = s.find('${', i)
        if i < 0: return res
        out_len = len(s)
        depth, j = 0, i + 2
        while j < out_len:
            c = s[j]
            if c in QUOTES + '`':
                q = c; j += 1
                while j < out_len and s[j] != q:
                    if s[j] == BS: j += 2; continue
                    if q == '`' and s.startswith('${', j):
                        d2, j = 1, j + 2
                        while j < out_len and d2:
                            d2 += (s[j] == '{') - (s[j] == '}'); j += 1
                        continue
                    j += 1
                j += 1; continue
            if c == '{': depth += 1
            elif c == '}':
                if depth == 0: break
                depth -= 1
            j += 1
        res.append(s[i:j + 1]); i = j + 1


def load_en():
    en = {}
    for f in sorted(glob.glob(str(I18N / 'en' / 'c[0-9]*.json'))):
        en.update({int(k): v for k, v in json.loads(pathlib.Path(f).read_text(encoding='utf-8')).items()})
    return en


def restore(en, svgs, label):
    def r(m):
        k = int(m.group(1))
        if not 1 <= k <= len(svgs):
            raise ValueError('%s: svg placeholder #%d does not exist' % (label, k))
        return svgs[k - 1]
    out = re.sub(r'<svg#(\d+)/>', r, en)
    return out


def esc_q(s, q):
    """escape the quote character q (and raw newlines) the way a JS string literal needs it, leaving existing escapes alone"""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            out.append(s[i:i + 2]); i += 2; continue
        if q == '`' and s.startswith('${', i):
            # a ${…} expression is code: copy it as it is (its own quotes and backticks are not part of the literal)
            depth, j = 0, i + 2
            while j < len(s):
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    if depth == 0: break
                    depth -= 1
                j += 1
            out.append(s[i:j + 1]); i = j + 1; continue
        if c == q:
            out.append('\\' + c)
        elif c == '\n' and q in '\'"':
            out.append('\\n')
        else:
            out.append(c)
        i += 1
    return ''.join(out)


def esc_json(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            out.append(s[i:i + 2]); i += 2; continue
        out.append('\\"' if c == '"' else c)
        i += 1
    return ''.join(out)


def escape(u, s):
    k = u['kind']
    if k in ('html', 'text'):
        return AMP.sub('&amp;', s)
    if k == 'attr':
        return AMP.sub('&amp;', s).replace('"', '&quot;')
    if k == 'js':
        return esc_q(s, u['q'])
    if k == 'meta':
        return esc_json(s)
    raise ValueError(k)


def attrs_of(s):
    return sorted((n, v) for n, v in ATTR.findall(s) if n not in TEXT_ATTRS and n != 'lang')


def check(pt, en):
    """pt/en are the 'view' strings (svg placeholders kept). Returns a list of problems."""
    bad = []
    if TAG.findall(pt) != TAG.findall(en):
        bad.append('tags differ: %s vs %s' % (TAG.findall(pt), TAG.findall(en)))
    if [skel(x) for x in exprs(pt)] != [skel(x) for x in exprs(en)]:
        bad.append('${} code differs: %s vs %s' % ([skel(x) for x in exprs(pt)], [skel(x) for x in exprs(en)]))
    if sorted(re.findall(r'<svg#\d+/>', pt)) != sorted(re.findall(r'<svg#\d+/>', en)):
        bad.append('svg placeholders differ')
    if attrs_of(pt) != attrs_of(en):
        bad.append('attributes differ: %s vs %s' % (attrs_of(pt), attrs_of(en)))
    if re.findall(r'\{\{\w+\}\}', pt) != re.findall(r'\{\{\w+\}\}', en):
        bad.append('{{placeholders}} differ')
    return bad


DL = re.compile(r'href="downloads/([^"/]+)\.pdf"')
DLBTN = re.compile(r'(href="downloads/en/[^"]+"(?:(?!</a>).)*?)<small>PDF[^<]*</small>', re.S)


def english_downloads(text, info):
    """the English pages open the English extracts (downloads/en/, built by build_docs.py) and show their real size"""
    def href(m):
        e = info.get(m.group(1))
        return 'href="downloads/en/%s"' % e['file'] if e else m.group(0)
    text = DL.sub(href, text)

    def label(m):
        name = re.search(r'downloads/en/([^"]+)"', m.group(1)).group(1)
        e = next((v for v in info.values() if v['file'] == name), None)
        if not e:
            return m.group(0)
        n = e['pages']
        return m.group(1) + '<small>PDF · %d %s%s</small>' % (n, 'page' if n == 1 else 'pages', ' · %g MB' % e['mb'] if e['mb'] >= 3 else '')
    return DLBTN.sub(label, text)


VIDEO = re.compile(r'"assets/video/(video-\w+)\.mp4"')
TRACK = re.compile(r'srclang="pt-PT" label="Português" src="assets/video/(video-\w+)\.vtt"')


def english_videos(text):
    """the English pages play the dubbed videos (assets/video/en/, same picture, English audio) with English captions"""
    text = VIDEO.sub(lambda m: '"assets/video/en/%s.mp4"' % m.group(1), text)
    return TRACK.sub(lambda m: 'srclang="en-GB" label="English" src="assets/video/en/%s.vtt"' % m.group(1), text)


def main():
    extract.main()  # refresh units.json / pt_list.json (append-only), so the offsets are current
    pt_list = json.loads((I18N / 'pt_list.json').read_text(encoding='utf-8'))
    en = load_en()
    index = {s: i for i, s in enumerate(pt_list)}
    units = json.loads((I18N / 'units.json').read_text(encoding='utf-8'))
    used = {index[u['view']] for us in units.values() for u in us}
    missing = sorted(i for i in used if i not in en)  # strings that no fragment uses any more (kept in pt_list to freeze the numbering) need no translation
    if missing:
        print('NOT TRANSLATED yet:', len(missing), [pt_list[i][:60] for i in missing[:10]])
        return 1
    ovf = I18N / 'en' / 'overrides.json'
    overrides = json.loads(ovf.read_text(encoding='utf-8')) if ovf.exists() else {}
    dlf = I18N / 'en' / 'downloads.json'
    dl_info = json.loads(dlf.read_text(encoding='utf-8')) if dlf.exists() else {}
    problems, outdir = [], ROOT / '_src' / 'lessons-en'
    outdir.mkdir(exist_ok=True)
    srcs = [(f, outdir / f.name) for f in sorted((ROOT / '_src' / 'lessons').glob('*.html'))] + [(ROOT / '_src' / 'shell.html', ROOT / '_src' / 'shell.en.html')]
    for f, dest in srcs:
        text = f.read_text(encoding='utf-8')
        us = sorted(units[f.name], key=lambda u: (u['start'], -u['end']))
        out, pos = [], 0
        for u in us:
            assert text[u['start']:u['end']] == u['text'], (f.name, u['start'])
            if u['end'] <= pos:
                continue  # nested inside the previous (outer) unit, whose translation already contains it
            if u['start'] < pos:
                problems.append((f.name, u['view'][:60], 'overlaps the previous unit')); continue
            i = index[u['view']]; e = overrides.get(f.name, {}).get(u['view'], en[i])  # a file can override one string (same Portuguese word, different English in that context)
            svgs = SVG.findall(u['text'])
            view_pt = u['view']
            errs = check(view_pt, e)
            if errs and i not in STRUCT_OK and "l[0].split(' ')[1]" not in view_pt:
                problems.append((f.name, view_pt[:70], '; '.join(errs)[:300]))
            try:
                e2 = restore(e, svgs, f.name)
            except ValueError as ex:
                problems.append((f.name, view_pt[:70], str(ex))); e2 = e
            out.append(text[pos:u['start']]); out.append(escape(u, e2)); pos = u['end']
        out.append(text[pos:])
        res = ''.join(out)
        if dl_info and f.name != 'shell.html':
            res = english_downloads(res, dl_info)
        res = english_videos(res)
        if f.name == 'shell.html':
            res = res.replace('<html lang="pt-PT">', '<html lang="en-GB">')
            res = res.replace('class="lngflag" src="assets/img/flag-pt-sq.svg"', 'class="lngflag" src="assets/img/flag-en-sq.svg"')  # the header switch shows the flag of the current language
        dest.write_text(res, encoding='utf-8')
    if problems:
        print('PROBLEMS:', len(problems))
        for p in problems:
            print(' -', p[0], '|', p[1], '|', p[2])
        return 1
    print('ok: %d fragments written' % len(srcs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
