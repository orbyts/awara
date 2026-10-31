"""Build the current manual reference. Run: uv run --with reportlab python scripts/build_reference.py."""
from pathlib import Path
from html import escape
import json
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
ROOT = Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
styles["Heading2"].keepWithNext = True
styles["Title"].keepWithNext = True
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 14
styles["BodyText"].spaceAfter = 8
story = []
import re
manual = (ROOT / "docs/getting-started/manual-setup.md").read_text()
manual = re.sub(r"(?m)^(#{1,2} .+)\n(?!\n)", r"\1\n\n", manual)
for block in manual.split("\n\n"):
    block = block.strip()
    if not block: continue
    style = "Title" if block.startswith("# ") else "Heading2" if block.startswith("## ") else "BodyText"
    story.append(Paragraph(escape(block.lstrip("# ")).replace("\n", " "), styles[style]))
story.append(Spacer(1, 18))
story.append(Paragraph("Configuration reference", styles["Title"]))
story.append(Paragraph("Generated from the same versioned JSON catalog used by the recipe. These are descriptive settings, not executable Resolve API calls.", styles["BodyText"]))
recipe=json.loads((ROOT/"recipes/resolve-multicamera-hdr/recipe.json").read_text())
def flatten(obj, prefix=""):
    for key, value in obj.items():
        label = f"{prefix} / {key}" if prefix else key
        if isinstance(value,dict): yield from flatten(value,label)
        else: yield label, json.dumps(value,ensure_ascii=True)
for filename in recipe["application"]["settings"]["config_files"]:
    story.append(Paragraph(escape(filename),styles["Heading2"]))
    for key,value in flatten(json.loads((ROOT/filename).read_text())):
        story.append(Paragraph(f"<b>{escape(key)}</b>: {escape(value)}",styles["BodyText"]))
story.append(Paragraph("Obtain third-party dependencies",styles["Heading2"]))
for p in sorted((ROOT/"resources/dependencies").glob("*.json")):
    d=json.loads(p.read_text());story.append(Paragraph(f'<b>{escape(d["name"])}</b> (tested {escape(d["tested_version"])}): <link href="{escape(d["url"])}">{escape(d["url"])}</link>',styles["BodyText"]))
def footer(canvas,doc):
    canvas.setFont("Helvetica",8);canvas.setFillColor(colors.HexColor("#556677"))
    canvas.drawString(42,26,"AWARA | Resolve manual setup | recipe 0.1.0 | 2026-10-31")
    canvas.drawRightString(553,26,str(doc.page))
out=ROOT/"output/pdf/awara-resolve-manual-reference.pdf";out.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(out),rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=44,title="Awara - Resolve manual setup",author="Awara").build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
