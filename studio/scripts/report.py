#!/usr/bin/env python3
"""Readable PDF of the implementation report, with embedded Cyrillic fonts."""
import argparse
from html import escape,unescape
from pathlib import Path
import re
import posixpath
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,LongTable,TableStyle,Preformatted,PageBreak

def main():
    p=argparse.ArgumentParser();p.add_argument('markdown');p.add_argument('--out',required=True);p.add_argument('--status',default='WARN',choices=['PASS','WARN','FAIL','NOT TESTED']);p.add_argument('--break-before',action='append',default=[]);a=p.parse_args()
    fontroot=Path('/usr/share/fonts/truetype/dejavu')
    for name,file in [('Studio','DejaVuSans.ttf'),('Studio-Bold','DejaVuSans-Bold.ttf'),('Studio-Italic','DejaVuSans-Oblique.ttf'),('StudioMono','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(fontroot/file)))
    pdfmetrics.registerFontFamily('Studio',normal='Studio',bold='Studio-Bold',italic='Studio-Italic',boldItalic='Studio-Bold')
    ink=colors.HexColor('#183D45');muted=colors.HexColor('#52666D')
    styles={
      'body':ParagraphStyle('body',fontName='Studio',fontSize=9.3,leading=14,textColor=ink,spaceAfter=7,splitLongWords=True),
      'h1':ParagraphStyle('h1',fontName='Studio-Bold',fontSize=23,leading=29,textColor=ink,spaceAfter=17,keepWithNext=True),
      'h2':ParagraphStyle('h2',fontName='Studio-Bold',fontSize=13,leading=18,textColor=ink,spaceBefore=13,spaceAfter=8,keepWithNext=True),
      'cell':ParagraphStyle('cell',fontName='Studio',fontSize=8.3,leading=12,textColor=ink,splitLongWords=True),
      'code':ParagraphStyle('code',fontName='StudioMono',fontSize=7.7,leading=11,textColor=muted,spaceAfter=8)}
    def inline(s):
        s=escape(s)
        def link(m):
            target=unescape(m.group(2))
            if not target.startswith(('http://','https://')):
                base=Path(a.markdown).resolve().parent.relative_to(Path(__file__).resolve().parents[2]).as_posix()
                target='https://github.com/denygrigo/IntTrade/blob/codex/research-design-studio-20261022/'+posixpath.normpath(base+'/'+target)
            return '<link href="'+escape(target,quote=True)+'" color="#00796D">'+m.group(1)+'</link>'
        s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
        s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
        s=re.sub(r'`([^`]+)`',r'<font name="StudioMono" size="8">\1</font>',s)
        return s
    lines=Path(a.markdown).read_text().splitlines();flow=[];i=0;paragraph=[]
    def flush():
        if paragraph:
            flow.append(Paragraph(inline(' '.join(paragraph)),styles['body']));paragraph.clear()
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            flush();code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            flow.append(Preformatted('\n'.join(code),styles['code'],maxLineLength=88));i+=1;continue
        if line.startswith('|'):
            flush();rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[v.strip() for v in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',c) for c in cells):rows.append([Paragraph(inline(c),styles['cell']) for c in cells])
                i+=1
            table=LongTable(rows,colWidths=[(A4[0]-80)/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E4EDE6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#9CB6AE')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D9E1DC')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            flow+=[table,Spacer(1,8)];continue
        if line.startswith('# '):flush();flow.append(Paragraph(inline(line[2:]),styles['h1']))
        elif line.startswith('## '):
            flush()
            if line[3:] in a.break_before:flow.append(PageBreak())
            flow.append(Paragraph(inline(line[3:]),styles['h2']))
        elif not line.strip():flush()
        elif re.match(r'^(\d+\. |\- )',line):flush();paragraph.append(line)
        else:paragraph.append(line)
        i+=1
    flush()
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=49,bottomMargin=43,title='Research & Design Studio — реализация и проверка',author='Research & Design Studio')
    def frame(canvas,doc):
        canvas.saveState();canvas.setFont('Studio',8);canvas.setFillColor(muted)
        canvas.drawString(40,A4[1]-30,'RESEARCH & DESIGN STUDIO  /  22.10.2026')
        canvas.setStrokeColor(colors.HexColor('#B9CAC1'));canvas.line(40,33,A4[0]-40,33)
        canvas.drawString(40,20,'Статус: '+a.status+' · выполненные проверки и ограничения указаны в отчёте')
        canvas.drawRightString(A4[0]-40,20,str(doc.page));canvas.restoreState()
    doc.build(flow,onFirstPage=frame,onLaterPages=frame)
    print(target)

if __name__=='__main__':main()
