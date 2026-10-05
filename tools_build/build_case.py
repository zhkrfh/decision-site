# -*- coding: utf-8 -*-
"""build_case.py: 从母版md生成案例网页正文并注入站点模板"""
import re
from pathlib import Path
ROOT = Path(r"E:\Documents\lingxi-claw\20261002-14-24-38-883")
SITE = ROOT / "站点"
# 1) 母版 -> html（md2html 已含品牌样式，取其 body 内容）
import subprocess, sys
subprocess.run([sys.executable, str(ROOT/"正典仓库/tools/md2html.py"),
                str(ROOT/"正典仓库/docs/案例01_工银泰国1.12.md"),
                str(ROOT/"正典仓库/docs/素材/公众号素材2_案例01.html")], check=True)
src = (ROOT/"正典仓库/docs/素材/公众号素材2_案例01.html").read_text(encoding="utf-8")
m = re.search(r"<body[^>]*>(.*)</body>", src, re.S)
body = m.group(1) if m else src
# 去掉素材自带样式/脚本块
body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
# 2) 注入模板
tpl = (SITE/"案例01.html").read_text(encoding="utf-8")
out = re.sub(r"<!--BODY-->.*?</article>", "<!--BODY-->\n" + body + "\n</article>", tpl, flags=re.S)
(SITE/"案例01.html").write_text(out, encoding="utf-8")
print("案例01.html rebuilt, body chars:", len(body))
