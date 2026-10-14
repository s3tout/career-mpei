#!/usr/bin/env python3
"""Собирает dist/index.html - одностраничник со всеми ассетами внутри.
Нужен только для предпросмотра одним файлом. На сервер кладется index.html + assets/."""
import base64, io, os, re, mimetypes
src = io.open('index.html', encoding='utf-8').read()

def inline_font(m):
    p = m.group(1)
    data = base64.b64encode(open(p, 'rb').read()).decode()
    return 'url(data:font/woff2;base64,%s)' % data

def inline_img(m):
    tag, p = m.group(0), m.group(1)
    mime = mimetypes.guess_type(p)[0] or 'image/jpeg'
    data = base64.b64encode(open(p, 'rb').read()).decode()
    return tag.replace('src="%s"' % p, 'src="data:%s;base64,%s"' % (mime, data))

out = re.sub(r'url\((assets/fonts/[^)]+)\)', inline_font, src)
out = re.sub(r'<img[^>]*src="(assets/img/[^"]+)"[^>]*>', inline_img, out)
os.makedirs('dist', exist_ok=True)
io.open('dist/index.html', 'w', encoding='utf-8').write(out)
print('dist/index.html:', len(out.encode('utf-8')), 'байт')
