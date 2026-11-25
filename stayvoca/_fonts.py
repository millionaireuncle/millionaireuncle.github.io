"""앱 글꼴에서 랜딩 페이지에 나오는 글자만 뽑아 fonts/에 woff2로 만든다. 페이지 문구를 고친 뒤 다시 돌린다.

    pip install fonttools brotli
    python3 stayvoca/_fonts.py

앱 저장소가 이 저장소 옆(../stay-voca)에 있어야 한다. 글자는 lang 속성으로 나눈다:
한국어·영어 글은 KR, 일본어 글은 JP, 번체 중국어 글은 TC 글꼴에서 뽑는다(landing.css의 글꼴 규칙과 같다).
"""
import shutil
from html.parser import HTMLParser
from pathlib import Path

from fontTools import subset

here = Path(__file__).parent
src = here.parent.parent / "stay-voca" / "assets" / "fonts"
out = here / "fonts"
FONT = {"ko": "kr", "en": "kr", "ja": "jp", "zh-Hant": "tc"}
FILES = {
    "kr-400": "IBMPlexSansKR-Regular", "kr-700": "IBMPlexSansKR-Bold",
    "jp-400": "IBMPlexSansJP-Regular", "jp-700": "IBMPlexSansJP-Bold",
    "tc-400": "IBMPlexSansTC", "tc-700": "IBMPlexSansTC-Bold",
    "display-800": "Overpass-ExtraBold",
}
VOID = {"meta", "link", "img", "br", "source", "input", "hr"}
chars = {"kr": set(), "jp": set(), "tc": set()}


class Text(HTMLParser):
    """보이는 글자를 가장 가까운 lang의 글꼴 몫으로 모은다"""

    def __init__(self):
        super().__init__()
        self.stack = []  # (태그, lang)

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            lang = dict(attrs).get("lang") or (self.stack[-1][1] if self.stack else "ko")
            self.stack.append((tag, lang))

    def handle_endtag(self, tag):
        if tag not in VOID:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] not in ("title", "script", "style"):
            chars[FONT[self.stack[-1][1]]].update(data)


for page in sorted(here.glob("*/index.html")):
    Text().feed(page.read_text(encoding="utf-8"))

out.mkdir(exist_ok=True)
for name, file in FILES.items():
    family = name.split("-")[0]
    # 숫자·영어 글꼴(.num, .lv, 영어 말풍선)은 어디에 쓰일지 모르니 기본 라틴 글자를 다 넣는다
    text = "".join(map(chr, range(0x20, 0x7F))) if family == "display" else "".join(sorted(chars[family]))
    subset.main([str(src / f"{file}.ttf"), f"--text={text}", "--flavor=woff2", "--layout-features=*", f"--output-file={out / name}.woff2"])
    print(f"{name}.woff2  {(out / f'{name}.woff2').stat().st_size / 1024:.0f}KB  글자 {len(text)}")
for license in src.glob("OFL-*.txt"):
    shutil.copy(license, out)
