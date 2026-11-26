"""Draw the project cards in assets/card-*.svg. Edit the text at the bottom, then run: python3 scripts/cards.py"""
import pathlib
from xml.sax.saxutils import escape as e
out = pathlib.Path(__file__).resolve().parent.parent / 'assets'

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-label="{label}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0d1117"/><stop offset=".6" stop-color="#1a1033"/><stop offset="1" stop-color="#2a1458"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#a78bfa" stop-opacity=".35"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#a78bfa" stroke-opacity=".06"/>
  </pattern>
</defs>
<style>
  text {{ font-family: 'Segoe UI', 'Noto Sans', 'Noto Sans Thai', Ubuntu, sans-serif; }}
  .num {{ font-size: 64px; font-weight: 800; fill: #a78bfa; fill-opacity: .18; }}
  .name {{ font-size: 44px; font-weight: 700; fill: #f5f3ff; }}
  .th {{ font-size: 22px; fill: #c4b5fd; }}
  .li {{ font-size: 19px; fill: #c9d1d9; }}
  .dot {{ fill: #a78bfa; }}
  .url {{ font-size: 16px; font-weight: 600; fill: #ede9fe; letter-spacing: .5px; }}
  .pulse {{ animation: pulse 3s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  .dash {{ stroke-dasharray: 8 6; animation: march 1.2s linear infinite; }}
  .scan {{ animation: scan 3.5s ease-in-out infinite; }}
  .blink {{ animation: blink 2.4s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .25; transform: scale(.8); }} 50% {{ opacity: .9; transform: scale(1.15); }} }}
  @keyframes march {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes scan {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(170px); }} }}
  @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
</style>
<rect x="1" y="1" width="1198" height="328" rx="22" fill="url(#bg)" stroke="#3b2a6b" stroke-width="2"/>
<rect x="1" y="1" width="1198" height="328" rx="22" fill="url(#grid)"/>
<circle cx="985" cy="165" r="190" fill="url(#glow)"/>
'''

def card(n, name, th, items, url, art):
    y = 205
    lis = ''.join(f'<circle class="dot" cx="66" cy="{y + i*36 - 6}" r="4"/><text x="84" y="{y + i*36}" class="li">{e(t)}</text>\n'
                  for i, t in enumerate(items))
    w = 16 + len(url) * 9.6 + 34
    return (HEAD.format(label=e(f'{name}: {th}')) +
        f'<text x="52" y="96" class="num">0{n}</text>\n'
        f'<text x="150" y="94" class="name">{e(name)}</text>\n'
        f'<text x="56" y="146" class="th">{e(th)}</text>\n'
        f'<line x1="56" y1="166" x2="740" y2="166" stroke="#a78bfa" stroke-opacity=".2"/>\n' + lis +
        f'<rect x="{1150-w}" y="268" width="{w}" height="36" rx="18" fill="#8b5cf6" fill-opacity=".9"/>\n'
        f'<text x="{1150-w+18}" y="292" class="url">{e(url)}  ↗</text>\n' + art + '</svg>\n')

# 01: a camera frame with a car under a live detection box
bkk = '''<g transform="translate(860 50)">
  <rect x="0" y="0" width="250" height="170" rx="14" fill="#0d1117" stroke="#3b2a6b" stroke-width="2"/>
  <path d="M20 160 L105 40 M230 160 L145 40" stroke="#3b2a6b" stroke-width="3"/>
  <path d="M125 150 v-14 M125 120 v-14 M125 90 v-12 M125 64 v-10" stroke="#8b949e" stroke-width="3" stroke-opacity=".5"/>
  <g transform="translate(70 92)">
    <rect x="0" y="12" width="70" height="26" rx="8" fill="#c4b5fd"/>
    <path d="M10 12 L20 0 H50 L60 12 Z" fill="#a78bfa"/>
    <circle cx="16" cy="40" r="7" fill="#1a1033"/><circle cx="54" cy="40" r="7" fill="#1a1033"/>
    <rect class="dash" x="-10" y="-10" width="90" height="64" fill="none" stroke="#4ade80" stroke-width="2.5"/>
    <rect x="-10" y="-30" width="76" height="20" fill="#4ade80"/>
    <text x="-4" y="-15" style="font-size:13px;font-weight:700;fill:#0d1117">car 0.94</text>
  </g>
  <circle class="blink" cx="226" cy="22" r="6" fill="#f87171"/>
  <text x="168" y="27" style="font-size:13px;font-weight:700;fill:#f87171">LIVE</text>
</g>
'''
# 02: a map with pins and a price bubble on the selected spot
plot = '''<g transform="translate(860 50)">
  <rect x="0" y="0" width="250" height="170" rx="14" fill="#0d1117" stroke="#3b2a6b" stroke-width="2"/>
  <path d="M0 120 C60 100 90 140 150 110 S230 70 250 80" stroke="#3b82f6" stroke-opacity=".5" stroke-width="10" fill="none"/>
  <path d="M40 0 V170 M0 50 H250 M170 0 V170" stroke="#3b2a6b" stroke-width="3"/>
  <g fill="#6d5bd0"><circle cx="70" cy="80" r="7"/><circle cx="200" cy="130" r="7"/><circle cx="210" cy="30" r="7"/><circle cx="100" cy="145" r="7"/></g>
  <circle class="pulse" cx="130" cy="78" r="22" fill="#a78bfa" fill-opacity=".35"/>
  <path d="M130 92 C118 76 114 68 114 60 a16 16 0 0 1 32 0 c0 8 -4 16 -16 32 Z" fill="#c4b5fd"/>
  <circle cx="130" cy="60" r="6" fill="#1a1033"/>
  <rect x="146" y="14" width="88" height="34" rx="10" fill="#8b5cf6"/>
  <text x="158" y="37" style="font-size:16px;font-weight:700;fill:#fff">฿4.2M</text>
</g>
'''
# 03: a page with confidence boxes and a moving scan line
ocr = '''<g transform="translate(900 40)">
  <rect x="0" y="0" width="170" height="210" rx="10" fill="#ede9fe"/>
  <path d="M130 0 H170 V40 Z" fill="#c4b5fd"/>
  <g fill="#6b7280"><rect x="20" y="30" width="100" height="10" rx="3"/><rect x="20" y="62" width="130" height="8" rx="3"/>
    <rect x="20" y="86" width="115" height="8" rx="3"/><rect x="20" y="110" width="125" height="8" rx="3"/>
    <rect x="20" y="134" width="90" height="8" rx="3"/><rect x="20" y="166" width="60" height="8" rx="3"/></g>
  <g fill="none" stroke-width="2"><rect x="14" y="24" width="112" height="22" rx="3" stroke="#22c55e"/>
    <rect x="14" y="56" width="142" height="20" rx="3" stroke="#22c55e"/><rect x="14" y="80" width="127" height="20" rx="3" stroke="#22c55e"/>
    <rect x="14" y="104" width="137" height="20" rx="3" stroke="#eab308"/><rect x="14" y="128" width="102" height="20" rx="3" stroke="#22c55e"/>
    <rect class="blink" x="14" y="160" width="140" height="20" rx="3" stroke="#ef4444" stroke-dasharray="5 4"/></g>
  <g class="scan"><rect x="-8" y="16" width="186" height="3" fill="#8b5cf6"/><rect x="-8" y="2" width="186" height="14" fill="#8b5cf6" fill-opacity=".18"/></g>
  <text x="44" y="200" style="font-size:14px;font-weight:700;fill:#6d28d9">ก ข ค · A B C</text>
</g>
'''

cards = {
 'card-streetsmart.svg': card(1, 'BKK StreetSmart', 'รถติด น้ำท่วม ฝุ่น และกล้อง AI ของกรุงเทพฯ แบบสด ๆ',
   ['Traffic, floods, rain and PM2.5 on one live map',
    'YOLO counts cars, spots no-helmet and wrong-way riders',
    'AI writes plain-Thai summaries from the live numbers'], 'bkksmartstreet.com', bkk),
 'card-openplot.svg': card(2, 'OpenPlot', 'แผนที่บ้านและโครงการ คลิกตรงไหนก็ได้ราคาประเมิน',
   ['Resale homes and new projects around Bangkok',
    'Click any spot for an asking-price estimate',
    'CatBoost + LightGBM + XGBoost · test R² 0.858'], 'openplot.bkksmartstreet.com', plot),
 'card-ocr.svg': card(3, 'Thai OCR', 'อ่านไทย-อังกฤษจากรูปและ PDF บน CPU ไม่ต้องใช้ GPU',
   ['Small files are read in your browser and stay there',
    'Books up to 1,000 pages go to a server queue',
    'Confidence boxes, form-field finder, AI summary'], 'ocr.bkksmartstreet.com', ocr),
}
for f, s in cards.items():
    open(f'{out}/{f}', 'w').write(s)
