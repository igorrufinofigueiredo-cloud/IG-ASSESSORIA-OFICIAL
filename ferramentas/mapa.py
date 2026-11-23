#!/usr/bin/env python3
"""Mapa de projeto da IG Assessoria.
Le um ou mais arquivos (.html, .js, .css) e gera MAPA.md com o endereco
(linha inicial e final) de cada secao, bloco de estilo, script e funcao,
para o Claude ler so o trecho necessario em vez do arquivo inteiro.
Uso: python3 mapa.py arquivo.html [outro.html ...] > MAPA.md
"""
import re, sys, os, hashlib

PESADA = 2000  # linha com mais caracteres que isso nao deve ser lida
VENDOR = re.compile(r'gsap|GreenSock|ScrollTrigger|Lenis|three\.js|jQuery|Chart\.js|supabase-js|@license|jspdf|html2canvas|qrcode', re.I)
SEC = re.compile(r'<(section|header|footer|nav|main|form|dialog|aside|article)\b([^>]*)>', re.I)
ATTR = lambda a, n: (re.search(n + r'\s*=\s*["\']([^"\']+)', a) or [None, None])[1]
HCOM = re.compile(r'<!--\s*(.{3,80}?)\s*-->')
TIT = re.compile(r'<(h1|h2)\b[^>]*>(.*?)</\1>', re.I | re.S)
CCOM = re.compile(r'/\*\s*[=\-#*\s]*([^*]{3,70}?)[=\-#*\s]*\*/')
JCOM = re.compile(r'^\s*//\s*[=\-#\s]{2,}\s*(.{3,70}?)\s*[=\-#]*\s*$')
FUN = [re.compile(r'^\s*(?:export\s+)?(?:async\s+)?function\s*\*?\s*([A-Za-z_$][\w$]*)\s*\('),
       re.compile(r'^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)'),
       re.compile(r'^\s*(?:async\s+)?([A-Za-z_$][\w$]{2,})\s*\([^)]*\)\s*\{\s*$'),
       re.compile(r'^\s*class\s+([A-Za-z_$][\w$]*)')]
EVT = re.compile(r'addEventListener\(\s*["\'](\w+)')
NAO = {'if', 'for', 'while', 'switch', 'catch', 'function', 'return', 'else', 'setTimeout', 'setInterval',
       'forEach', 'then', 'requestAnimationFrame', 'map', 'filter', 'addEventListener', 'Promise'}

def limpa(t): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip()[:70]

def tipo_pesada(l):
    m = re.search(r'data:(\w+/[\w+.-]+)', l)
    if m: return 'arquivo embutido (' + m.group(1) + ')'
    if VENDOR.search(l[:3000]): return 'biblioteca de terceiros minificada'
    return 'codigo minificado'

def mapear(path):
    linhas = open(path, encoding='utf-8', errors='replace').read().split('\n')
    tot = sum(len(l) for l in linhas)
    out, pesadas, blocos = [], [], []
    modo, ini, attrs = None, 0, ''
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.js', '.mjs'): modo, ini = 'script', 1
    if ext == '.css': modo, ini = 'style', 1
    itens = []  # (linha, zona, texto)
    for i, l in enumerate(linhas, 1):
        if len(l) > PESADA:
            pesadas.append((i, len(l), tipo_pesada(l)))
        low = l.lower()
        if modo is None:
            m = re.search(r'<(script|style)\b([^>]*)>', low)
            if m and 'src=' not in m.group(2):
                modo, ini, attrs = m.group(1), i, m.group(2)
                if f'</{modo}>' in low[m.end():]:
                    blocos.append((modo, i, i, attrs)); modo = None
                continue
            if len(l) > PESADA: continue
            for m in SEC.finditer(l):
                nome = ATTR(m.group(2), 'id') or ATTR(m.group(2), 'class') or ''
                itens.append((i, 'html', f'<{m.group(1).lower()}> {nome}'.strip()))
            for m in HCOM.finditer(l): itens.append((i, 'html', '-- ' + m.group(1)))
            for m in TIT.finditer(l): itens.append((i, 'html', f'{m.group(1).upper()}: {limpa(m.group(2))}'))
        else:
            if f'</{modo}>' in low and not (ext in ('.js', '.css')):
                blocos.append((modo, ini, i, attrs)); modo = None; continue
            if len(l) > PESADA: continue
            if modo == 'style':
                for m in CCOM.finditer(l): itens.append((i, 'css', m.group(1).strip()))
            else:
                m = JCOM.match(l)
                if m: itens.append((i, 'js', '-- ' + m.group(1))); continue
                for f in FUN:
                    m = f.match(l)
                    if m and m.group(1) not in NAO:
                        itens.append((i, 'js', m.group(1) + '()')); break
                for m in EVT.finditer(l): itens.append((i, 'js', 'evento ' + m.group(1)))
    if modo: blocos.append((modo, ini, len(linhas), attrs))
    peso_p = sum(p[1] for p in pesadas)
    h = hashlib.md5('\n'.join(linhas).encode()).hexdigest()[:10]
    out.append(f'## {path}\n')
    out.append(f'- {len(linhas)} linhas, {tot//1024} KB, cerca de {tot//4:,} tokens se lido inteiro'.replace(',', '.'))
    out.append(f'- {len(pesadas)} linhas pesadas somam {peso_p//1024} KB: NUNCA ler essas linhas')
    out.append(f'- assinatura do arquivo: {h} (se mudar, rodar o mapa de novo)\n')
    if pesadas:
        out.append('### Linhas proibidas (pular na leitura)')
        for n, t, k in pesadas: out.append(f'- L{n}: {k}, {t//1024} KB')
        out.append('')
    if blocos:
        out.append('### Blocos de estilo e script')
        for k, a, b, at in blocos:
            viz = [p for p in pesadas if a <= p[0] <= b]
            nota = ' (tem linha pesada, ver lista acima)' if viz else ''
            tag = (' ' + at.strip()) if at.strip() else ''
            out.append(f'- L{a}-{b}: <{k}{tag}>{nota}')
        out.append('')
    marcos = sorted({x[0] for x in itens} | {b[1] for b in blocos} | {b[2] + 1 for b in blocos} | {len(linhas) + 1})
    import bisect
    for zona, titulo in (('html', 'Secoes do HTML'), ('css', 'Partes do CSS'), ('js', 'Funcoes e eventos do JS')):
        z = [x for x in itens if x[1] == zona]
        if not z: continue
        out.append(f'### {titulo}')
        for k, (n, _, t) in enumerate(z):
            j = bisect.bisect_right(marcos, n)
            fim = marcos[j] - 1 if j < len(marcos) else None
            out.append(f'- L{n}' + (f'-{fim}' if fim and fim > n else '') + f': {t}')
        out.append('')
    return '\n'.join(out)

if __name__ == '__main__':
    print('# MAPA do projeto\n')
    print('Gerado por mapa.py. Ler este mapa antes de abrir qualquer arquivo e abrir so as linhas indicadas (Read com offset e limit).\n')
    for p in sys.argv[1:]: print(mapear(p))
