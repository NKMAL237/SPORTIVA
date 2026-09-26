from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, FancyArrowPatch
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_DIR = ROOT / 'DEFENSE' / 'prsd_diagrams'
OUTPUT = ROOT / 'SPORTIVA_PROJECT_REQUIREMENTS_SPECIFICATIONS.docx'
DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)

NAVY = '#12304A'
BLUE = '#1E6A8A'
TEAL = '#0D9488'
GOLD = '#D49A24'
RED = '#B84A4A'
INK = '#1F2937'
MUTED = '#64748B'
PALE = '#F4F8FA'
WHITE = '#FFFFFF'


def setup_ax(title, figsize=(12, 7)):
    fig, ax = plt.subplots(figsize=figsize, dpi=180)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=15, fontweight='bold', color=NAVY, pad=16)
    return fig, ax


def box(ax, x, y, w, h, text, fill=PALE, edge=BLUE, color=INK, size=9, radius=0.025):
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.008,rounding_size={radius}',
                           linewidth=1.5, edgecolor=edge, facecolor=fill)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', color=color,
            fontsize=size, wrap=True, linespacing=1.15)


def actor(ax, x, y, label):
    ax.plot([x, x], [y + 0.035, y - 0.035], color=INK, lw=1.5)
    ax.plot([x - 0.025, x + 0.025], [y, y], color=INK, lw=1.5)
    ax.plot([x, x - 0.025], [y - 0.035, y - 0.07], color=INK, lw=1.5)
    ax.plot([x, x + 0.025], [y - 0.035, y - 0.07], color=INK, lw=1.5)
    ax.add_patch(plt.Circle((x, y + 0.065), 0.022, fill=False, color=INK, lw=1.5))
    ax.text(x, y - 0.105, label, ha='center', va='top', fontsize=8.5, color=INK)


def arrow(ax, start, end, label=None, color=BLUE, dashed=False, mutation='->'):
    style = '-' if not dashed else '--'
    ax.annotate('', xy=end, xytext=start, arrowprops=dict(arrowstyle=mutation, lw=1.2, color=color, linestyle=style))
    if label:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + 0.018, label, fontsize=7.5, color=color, ha='center', va='center')


def save(fig, name):
    path = DIAGRAM_DIR / f'{name}.png'
    fig.savefig(path, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def diagram_use_case():
    fig, ax = setup_ax('UML Use-Case Diagram - SPORTIVA CM')
    ax.add_patch(Rectangle((0.25, 0.08), 0.52, 0.82, fill=False, linestyle='--', linewidth=1.5, edgecolor=NAVY))
    ax.text(0.51, 0.875, 'SPORTIVA CM PLATFORM', ha='center', fontsize=10, fontweight='bold', color=NAVY)
    roles = [(0.10, 0.78, 'Athlete / Fan'), (0.10, 0.47, 'Organization / Coach'), (0.10, 0.18, 'Sponsor'), (0.90, 0.78, 'Administrator')]
    for x, y, label in roles:
        actor(ax, x, y, label)
    cases = [(0.32, 0.70, 'Register / Login'), (0.54, 0.70, 'Manage Profile'), (0.32, 0.51, 'Discover & Follow'),
             (0.54, 0.51, 'Create / Join Event'), (0.32, 0.32, 'Publish & Engage'), (0.54, 0.32, 'Buy / Sell Gear'),
             (0.32, 0.14, 'Sponsor Campaign'), (0.54, 0.14, 'Private Chat')]
    for x, y, label in cases:
        ax.add_patch(Ellipse((x, y), 0.18, 0.09, facecolor='#E7F3F5', edgecolor=BLUE, linewidth=1.3))
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color=INK)
    for start, end in [((0.12, 0.75), (0.32, 0.70)), ((0.12, 0.75), (0.54, 0.70)), ((0.12, 0.75), (0.32, 0.51)), ((0.12, 0.75), (0.54, 0.51)), ((0.12, 0.75), (0.32, 0.32)), ((0.12, 0.75), (0.54, 0.32)), ((0.12, 0.75), (0.54, 0.14)), ((0.12, 0.75), (0.32, 0.14)), ((0.12, 0.44), (0.54, 0.51)), ((0.12, 0.44), (0.32, 0.32)), ((0.12, 0.44), (0.54, 0.14)), ((0.12, 0.15), (0.32, 0.14)), ((0.12, 0.15), (0.54, 0.14)), ((0.88, 0.75), (0.54, 0.70)), ((0.88, 0.75), (0.54, 0.51)), ((0.88, 0.75), (0.32, 0.51)), ((0.88, 0.75), (0.54, 0.14))]:
        arrow(ax, start, end, color=MUTED)
    return save(fig, '01_use_case')


def diagram_class():
    fig, ax = setup_ax('UML Class Diagram - Core Domain Model', (13, 8))
    classes = {
        'User': (0.03, 0.70, 0.18, 0.18, ['role', 'country, city', 'sportiva_score']),
        'OrganizationProfile': (0.29, 0.77, 0.19, 0.12, ['user', 'sport', 'location']),
        'Event': (0.56, 0.77, 0.19, 0.15, ['organizer', 'sport, category', 'venue, dates, capacity']),
        'EventRegistration': (0.82, 0.72, 0.16, 0.20, ['event, user', 'status', 'payment_status']),
        'Post': (0.29, 0.46, 0.19, 0.14, ['author', 'content_type', 'sport, media']),
        'Product': (0.56, 0.47, 0.19, 0.14, ['seller', 'category', 'price, condition']),
        'Campaign': (0.29, 0.18, 0.19, 0.14, ['creator', 'target_amount', 'is_active']),
        'Pledge': (0.56, 0.18, 0.19, 0.14, ['campaign, sponsor', 'amount', 'is_anonymous']),
        'Conversation': (0.82, 0.39, 0.16, 0.18, ['participants', 'subject', 'updated_at']),
        'ChatMessage': (0.82, 0.16, 0.16, 0.16, ['conversation, sender', 'content', 'is_read'])}
    for name, (x, y, w, h, attrs) in classes.items():
        box(ax, x, y, w, h, name + '\n' + '\n'.join(attrs), fill='#F8FBFC', edge=BLUE, size=7.5)
    rels = [('User', 'OrganizationProfile'), ('User', 'Event'), ('Event', 'EventRegistration'), ('User', 'EventRegistration'), ('User', 'Post'), ('User', 'Product'), ('User', 'Campaign'), ('Campaign', 'Pledge'), ('User', 'Pledge'), ('User', 'Conversation'), ('Conversation', 'ChatMessage'), ('User', 'ChatMessage')]
    centers = {n: (x + w / 2, y + h / 2) for n, (x, y, w, h, _) in classes.items()}
    for a, b in rels:
        arrow(ax, centers[a], centers[b], color=MUTED, mutation='-')
    return save(fig, '02_class_model')


def diagram_sequence():
    fig, ax = setup_ax('UML Sequence Diagram - Event Registration and Invoice', (13, 8))
    participants = [('User', 0.10), ('Browser', 0.28), ('EventView', 0.47), ('Database', 0.66), ('InvoiceService', 0.86)]
    for label, x in participants:
        box(ax, x - 0.055, 0.88, 0.11, 0.07, label, fill='#E7F3F5', edge=BLUE, size=8)
        ax.plot([x, x], [0.84, 0.12], color=MUTED, lw=1, linestyle='--')
    messages = [('Open event', 0.78, 0.10, 0.28), ('GET event detail', 0.70, 0.28, 0.47), ('Query event and capacity', 0.62, 0.47, 0.66), ('Available', 0.54, 0.66, 0.47), ('Submit registration', 0.46, 0.10, 0.28), ('Validate duplicate/capacity', 0.38, 0.28, 0.47), ('Create EventRegistration', 0.30, 0.47, 0.66), ('Generate invoice PDF', 0.22, 0.47, 0.86), ('Return confirmation', 0.14, 0.28, 0.10)]
    for label, y, x1, x2 in messages:
        arrow(ax, (x1, y), (x2, y), label, color=TEAL)
    return save(fig, '03_sequence_event_registration')


def diagram_activity():
    fig, ax = setup_ax('UML Activity Diagram - Sponsorship Proposal to Contract')
    nodes = [(0.5, 0.88, 'Start', 'circle'), (0.5, 0.76, 'Create proposal', 'box'), (0.5, 0.63, 'Validate recipient and details', 'box'), (0.5, 0.50, 'Recipient reviews proposal', 'box'), (0.5, 0.37, 'Accepted?', 'diamond'), (0.30, 0.20, 'Decline and notify sender', 'box'), (0.70, 0.20, 'Create active contract', 'box'), (0.70, 0.08, 'End', 'circle')]
    for x, y, text, typ in nodes:
        if typ == 'circle':
            ax.add_patch(plt.Circle((x, y), 0.027, facecolor=NAVY, edgecolor=NAVY))
        elif typ == 'diamond':
            ax.add_patch(plt.Polygon([(x, y + 0.045), (x + 0.07, y), (x, y - 0.045), (x - 0.07, y)], facecolor='#FFF4D6', edgecolor=GOLD, linewidth=1.5))
            ax.text(x, y, text, ha='center', va='center', fontsize=8)
        else:
            box(ax, x - 0.12, y - 0.035, 0.24, 0.07, text, fill='#E7F3F5', edge=BLUE, size=8)
    for start, end, label in [((0.5, .85), (.5, .795), None), ((.5,.725),(.5,.675),None), ((.5,.595),(.5,.545),None), ((.5,.465),(.5,.415),None), ((.45,.35),(.30,.235),'No'), ((.55,.35),(.70,.235),'Yes'), ((.70,.165),(.70,.11),None)]:
        arrow(ax, start, end, label, color=TEAL)
    return save(fig, '04_activity_sponsorship')


def diagram_state():
    fig, ax = setup_ax('UML State-Machine Diagram - Event Registration')
    states = [(0.10, 0.46, 'Created'), (0.31, 0.46, 'Pending\nValidation'), (0.54, 0.68, 'Confirmed'), (0.54, 0.24, 'Cancelled'), (0.78, 0.68, 'Completed'), (0.91, 0.46, 'Refunded')]
    for x, y, label in states:
        box(ax, x - 0.07, y - 0.045, 0.14, 0.09, label, fill='#E7F3F5', edge=BLUE, size=8)
    for start, end, label in [((.17,.505),(.31,.505),'submit'), ((.45,.52),(.54,.68),'validate'), ((.45,.48),(.54,.24),'cancel'), ((.68,.68),(.78,.68),'event ends'), ((.68,.24),(.91,.46),'refund')]:
        arrow(ax, start, end, label, color=TEAL)
    return save(fig, '05_state_registration')


def diagram_component():
    fig, ax = setup_ax('UML Component Diagram - Django Application Modules', (13, 8))
    components = [('Browser / PWA', 0.04, 0.42, 0.15, 0.17, GOLD), ('Core / Home', 0.27, 0.72, 0.16, 0.13, BLUE), ('Accounts', 0.27, 0.50, 0.16, 0.13, TEAL), ('Events', 0.27, 0.28, 0.16, 0.13, BLUE), ('Organizations', 0.27, 0.06, 0.16, 0.13, TEAL), ('Media Feed', 0.53, 0.72, 0.16, 0.13, TEAL), ('Marketplace', 0.53, 0.50, 0.16, 0.13, BLUE), ('Sponsorships', 0.53, 0.28, 0.16, 0.13, TEAL), ('Chat', 0.53, 0.06, 0.16, 0.13, BLUE), ('Django ORM / SQLite', 0.79, 0.40, 0.17, 0.18, NAVY)]
    for name, x, y, w, h, color in components:
        box(ax, x, y, w, h, '[component]\n' + name, fill='#F8FBFC', edge=color, size=8)
    for start, end in [((.19,.505),(.27,.785)),((.19,.505),(.27,.565)),((.19,.505),(.27,.345)),((.19,.505),(.27,.125)),((.43,.785),(.79,.49)),((.43,.565),(.79,.49)),((.43,.345),(.79,.49)),((.43,.125),(.79,.49)),((.69,.785),(.79,.49)),((.69,.565),(.79,.49)),((.69,.345),(.79,.49)),((.69,.125),(.79,.49))]:
        arrow(ax, start, end, color=MUTED)
    return save(fig, '06_component_architecture')


def diagram_deployment():
    fig, ax = setup_ax('UML Deployment Diagram - Local and Production Topology')
    nodes = [('Client Device\nBrowser / PWA', .06, .38, .20, .22, GOLD), ('Web Server\nDjango WSGI/ASGI', .40, .60, .22, .20, BLUE), ('Static / Media\nStorage', .40, .20, .22, .20, TEAL), ('Database Server\nSQLite (MVP)', .74, .60, .20, .20, NAVY), ('External Contact\nWhatsApp Links', .74, .20, .20, .20, RED)]
    for name, x, y, w, h, color in nodes:
        box(ax, x, y, w, h, '<<node>>\n' + name, fill='#F8FBFC', edge=color, size=8)
    for start, end, label in [((.26,.49),(.40,.70),'HTTP/HTTPS'),((.51,.60),(.51,.40),'uploads'),((.62,.70),(.74,.70),'ORM queries'),((.62,.30),(.74,.30),'contact URL'),((.26,.49),(.40,.30),'cached assets')]:
        arrow(ax, start, end, label, color=MUTED)
    return save(fig, '07_deployment')


def diagram_package():
    fig, ax = setup_ax('UML Package Diagram - SPORTIVA CM Modular Structure')
    packages = [('sportiva_cm', .39, .78, .22, .12, NAVY), ('core', .08, .55, .17, .12, BLUE), ('accounts', .31, .55, .17, .12, TEAL), ('organizations', .54, .55, .17, .12, BLUE), ('events', .77, .55, .17, .12, TEAL), ('media_feed', .08, .27, .17, .12, TEAL), ('marketplace', .31, .27, .17, .12, BLUE), ('sponsorships', .54, .27, .17, .12, TEAL), ('chat', .77, .27, .17, .12, BLUE)]
    for name, x, y, w, h, color in packages:
        box(ax, x, y, w, h, '<<package>>\n' + name, fill='#F8FBFC', edge=color, size=8)
    for start, end in [((.50,.78),(.16,.67)),((.50,.78),(.395,.67)),((.50,.78),(.625,.67)),((.50,.78),(.855,.67)),((.395,.55),(.395,.39)),((.625,.55),(.395,.39)),((.625,.55),(.625,.39)),((.625,.55),(.855,.39)),((.395,.39),(.165,.39)),((.625,.39),(.395,.39))]:
        arrow(ax, start, end, color=MUTED, dashed=True)
    return save(fig, '08_package_structure')


def diagram_er():
    fig, ax = setup_ax('Entity Relationship Diagram - Persistence Model', (13, 8))
    entities = [('USER', .05, .68, .16, .16), ('EVENT', .30, .72, .16, .14), ('REGISTRATION', .55, .72, .19, .14), ('POST', .30, .42, .16, .14), ('PRODUCT', .55, .42, .16, .14), ('CAMPAIGN', .05, .18, .16, .14), ('PLEDGE', .30, .18, .16, .14), ('CONVERSATION', .55, .18, .19, .14), ('MESSAGE', .82, .18, .14, .14), ('ORGANIZATION', .05, .42, .16, .14)]
    for name, x, y, w, h in entities:
        box(ax, x, y, w, h, name, fill='#F8FBFC', edge=BLUE, size=8)
    links = [((.21,.76),(.30,.79),'organizes'),((.46,.79),(.55,.79),'has'),((.21,.76),(.55,.79),'registers'),((.21,.49),(.30,.49),'authors'),((.21,.49),(.55,.49),'sells'),((.13,.32),(.30,.25),'receives'),((.46,.25),(.55,.25),'contains'),((.74,.25),(.82,.25),'contains'),((.13,.42),(.13,.32),'owns')]
    for start, end, label in links:
        arrow(ax, start, end, label, color=MUTED)
    return save(fig, '09_er_model')


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False, color=INK, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(str(text))
    run.bold = bold
    run.font.name = 'Aptos'
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color.replace('#', ''))
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for i, header in enumerate(headers):
        set_cell_shading(table.rows[0].cells[i], NAVY.replace('#', ''))
        set_cell_text(table.rows[0].cells[i], header, bold=True, color=WHITE, size=8.5)
    for ridx, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            set_cell_shading(cells[i], 'F3F7F9' if ridx % 2 else 'FFFFFF')
            set_cell_text(cells[i], value, size=8.2)
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = 'Aptos Display'
    run.font.color.rgb = RGBColor.from_string(NAVY.replace('#', ''))
    if level == 1:
        run.font.size = Pt(16)
    elif level == 2:
        run.font.size = Pt(12.5)
    return p


def add_para(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.08
    if bold_prefix and text.startswith(bold_prefix):
        p.add_run(bold_prefix).bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        p.add_run(text)
    for run in p.runs:
        run.font.name = 'Aptos'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor.from_string(INK.replace('#', ''))
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(item)
        r.font.name = 'Aptos'
        r.font.size = Pt(10.2)
        r.font.color.rgb = RGBColor.from_string(INK.replace('#', ''))


def add_figure(doc, path, number, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(7)
    p.add_run().add_picture(str(path), width=Inches(6.65))
    cap = doc.add_paragraph(f'Figure {number}. {title}')
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    for run in cap.runs:
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(MUTED.replace('#', ''))


def add_page_number(section):
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run('SPORTIVA CM | Project Requirements & Specifications | ')
    run.font.size = Pt(8)
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)


def build_document(images):
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.6)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(1.8)
    add_page_number(section)
    styles = doc.styles
    styles['Normal'].font.name = 'Aptos'
    styles['Normal'].font.size = Pt(10.5)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(70)
    r = p.add_run('SPORTIVA CM')
    r.bold = True; r.font.size = Pt(28); r.font.color.rgb = RGBColor.from_string(NAVY.replace('#', ''))
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run('PROJECT REQUIREMENTS & SPECIFICATIONS DOCUMENT')
    r.bold = True; r.font.size = Pt(19); r.font.color.rgb = RGBColor.from_string(BLUE.replace('#', ''))
    p3 = doc.add_paragraph(); p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p3.add_run('Implementation-grounded analysis and UML specification')
    r.italic = True; r.font.size = Pt(12); r.font.color.rgb = RGBColor.from_string(MUTED.replace('#', ''))
    doc.add_paragraph('\n\n')
    add_table(doc, ['Document field', 'Value'], [
        ('Version', '1.0'), ('Date', '7 September 2026'), ('Status', 'MVP / academic demonstration release'),
        ('Technology', 'Python, Django, SQLite, HTML, CSS, JavaScript'),
        ('Scope', 'Sports promotion, community, events, media, marketplace, sponsorships, and messaging')], [2.0, 4.1])
    doc.add_paragraph('\n')
    p = doc.add_paragraph('Prepared from the current SPORTIVA CM source code, migrations, templates, and project documentation.')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs: run.font.size = Pt(9); run.font.color.rgb = RGBColor.from_string(MUTED.replace('#', ''))
    doc.add_page_break()

    add_heading(doc, 'Document Control and Executive Summary', 1)
    add_para(doc, 'SPORTIVA CM is a Django-based digital sports ecosystem designed to connect athletes, clubs, coaches, sponsors, organizers, sellers, and fans. It combines identity and profile management with event registration, achievement verification, a social media feed, a sports marketplace, sponsorship campaigns, and private chat.')
    add_para(doc, 'The current release is an MVP suitable for demonstration, academic defense, and continued development. It provides a working modular foundation, but production deployment still requires hardened configuration, real payment services, stronger testing, and operational infrastructure.')
    add_table(doc, ['Revision', 'Date', 'Description'], [('1.0', '2026-09-07', 'Generated project requirements, analysis, specifications, and UML diagrams from the current implementation.')])

    add_heading(doc, 'Table of Contents', 1)
    add_para(doc, 'In Microsoft Word, right-click the table of contents field below and choose “Update Field” to refresh page numbers after editing.')
    p = doc.add_paragraph()
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'TOC \\o "1-3" \\h \\z \\u'); p._p.append(fld)
    doc.add_page_break()

    add_heading(doc, '1. Project Context and Problem Analysis', 1)
    add_heading(doc, '1.1 Background', 2)
    add_para(doc, 'Sports stakeholders often operate across disconnected channels: social networks for announcements, messaging applications for coordination, spreadsheets for attendance, and informal contacts for sponsorship. This fragmentation reduces visibility, makes participation difficult to measure, and limits access to opportunities for athletes and organizations.')
    add_heading(doc, '1.2 Problem statement', 2)
    add_bullets(doc, ['Local athletes and clubs have limited professional digital visibility.', 'Event discovery, registration, capacity management, and attendance records are fragmented.', 'Sponsors have difficulty finding credible athletes, events, and funding opportunities.', 'Sports media, marketplace activity, and community discussion are separated across different channels.', 'Many sports communities need a Cameroon-focused platform that can also support international sports categories.'])
    add_heading(doc, '1.3 Proposed solution', 2)
    add_para(doc, 'SPORTIVA CM provides one role-aware web platform where users can create profiles, discover sports organizations and events, publish media, list equipment, communicate privately, and create or support sponsorship activity. The system uses Django modular applications and a responsive PWA-oriented interface.')
    add_heading(doc, '1.4 Objectives', 2)
    add_bullets(doc, ['Increase visibility of athletes, clubs, academies, and tournaments.', 'Improve discovery and participation in sports events.', 'Create a structured merit and achievement profile for athletes.', 'Connect sponsors with athletes, organizations, events, and campaigns.', 'Support community interaction through posts, likes, comments, follows, and chat.', 'Create a foundation for future mobile, API, payment, and analytics capabilities.'])

    add_heading(doc, '2. Stakeholder and User Analysis', 1)
    add_table(doc, ['Role', 'Goals', 'Main capabilities'], [
        ('Athlete', 'Build credibility and find opportunities', 'Profile, exploits, endorsements, events, posts, sponsorships, chat'),
        ('Organization / club / academy', 'Promote activities and manage events', 'Organization profile, event publishing, sponsorship proposals, discovery'),
        ('Coach / trainer', 'Validate and support athlete development', 'Profiles, exploit verification, events, communication'),
        ('Sponsor / business', 'Find and support sports opportunities', 'Sponsor profile, campaigns, pledges, proposals, contracts, chat'),
        ('Fan / visitor', 'Discover and follow sports activity', 'Browse profiles, events, feed, marketplace, and campaigns'),
        ('Seller', 'Promote sports products', 'Product listings, filtering, WhatsApp contact'),
        ('Administrator / staff', 'Operate and govern the platform', 'Django admin, user management, verification, access control')], [1.45, 2.2, 2.45])
    add_para(doc, 'Implementation note: the current User model combines club, academy, organization, and manager behavior under the ORGANIZATION role. If these stakeholders require separate permissions, the role model should be expanded in a future release.')

    add_heading(doc, '3. System Scope and Boundaries', 1)
    add_heading(doc, '3.1 Included in the MVP', 2)
    add_bullets(doc, ['Authentication and role-aware profiles.', 'Organizations and sports directory.', 'Events, RSVP/registration, capacity checks, payment status, and invoice PDF generation.', 'Posts, shorts, likes, comments, and feed filtering.', 'Sports products and seller contact.', 'Sponsors, campaigns, pledges, proposals, and contracts.', 'One-to-one messaging with attachments and unread tracking.', 'PWA manifest, service worker, cached navigation, and offline fallback.', 'Internationalization configuration for English, French, Spanish, German, Arabic, and Portuguese.'])
    add_heading(doc, '3.2 Excluded or simulated', 2)
    add_bullets(doc, ['No real payment gateway or financial settlement is integrated.', 'Marketplace checkout, orders, delivery, and inventory are not implemented.', 'Offline writes and conflict-safe synchronization are not guaranteed.', 'External live sports-news ingestion is not implemented as a production integration.', 'Formal legal electronic signatures and contract audit trails are not implemented.', 'Native mobile applications and a dedicated public mobile API are future work.'])

    add_heading(doc, '4. Functional Requirements Specification', 1)
    requirements = [
        ('FR-01', 'The system shall allow a visitor to register with username, email, password, role, location, and sports information.', 'Must'),
        ('FR-02', 'The system shall authenticate users and provide protected session-based access.', 'Must'),
        ('FR-03', 'Users shall view and edit profile, avatar, biography, location, sports, and social links.', 'Must'),
        ('FR-04', 'Users shall browse, search, filter, sort, follow, and view community profiles.', 'Must'),
        ('FR-05', 'Athletes shall submit exploits with evidence; authorized roles shall verify or reject them.', 'Must'),
        ('FR-06', 'The system shall calculate a Sportiva Score and tier from verified exploits and activity.', 'Should'),
        ('FR-07', 'Organizations shall publish profiles and users shall filter organizations by sport and location.', 'Must'),
        ('FR-08', 'Authorized organizers shall create and publish events with venue, schedule, capacity, fee, and contact data.', 'Must'),
        ('FR-09', 'Users shall register for events; duplicate registrations and capacity overflow shall be rejected.', 'Must'),
        ('FR-10', 'The system shall track registration status/payment status and generate an invoice or entry-pass PDF.', 'Should'),
        ('FR-11', 'Users shall publish posts and interact through likes, comments, shorts, and feed filters.', 'Must'),
        ('FR-12', 'Sellers shall publish sports product listings with price, condition, media, location, and contact data.', 'Must'),
        ('FR-13', 'Users shall create sponsorship campaigns, pledges, proposals, and contracts.', 'Must'),
        ('FR-14', 'Users shall communicate through participant-restricted one-to-one conversations.', 'Must'),
        ('FR-15', 'The system shall provide a responsive interface, manifest, service worker, and offline fallback.', 'Should'),
        ('FR-16', 'Administrators shall manage data, verification, users, and custom tab access.', 'Must')]
    add_table(doc, ['ID', 'Requirement', 'Priority'], requirements, [0.7, 5.3, 0.9])
    add_heading(doc, '4.1 Business rules', 2)
    add_bullets(doc, ['A user cannot register for the same event more than once.', 'An event cannot accept confirmed participants beyond max_participants.', 'A user cannot create duplicate follow or like relationships.', 'Only authorized verifiers can approve athlete exploits.', 'Only conversation participants can access conversation messages.', 'Accepted sponsorship proposals create active contract records in the current workflow.', 'Pledge and sponsorship amounts are records only until payment integration is added.', 'Protected mutations require authentication and server-side authorization.'])

    add_heading(doc, '5. Non-Functional Requirements', 1)
    add_table(doc, ['Category', 'Specification'], [
        ('Security', 'Use Django authentication, CSRF protection, password validation, clickjacking protection, and server-side authorization. Production must disable DEBUG, restrict hosts, use secure cookies/HTTPS, and protect uploads.'),
        ('Performance', 'Use efficient filtered queries, pagination where needed, compressed/resized media, and safe static asset caching.'),
        ('Availability', 'Provide cached navigation and offline fallback; define backups and recovery before production deployment.'),
        ('Usability', 'Responsive layouts, clear validation feedback, accessible labels, role-aware navigation, and usable small-screen layouts.'),
        ('Maintainability', 'Keep domain concerns in modular Django apps; manage schema changes through migrations; record dependencies and test critical workflows.'),
        ('Internationalization', 'Use LocaleMiddleware and configured language choices; verify translation completeness and right-to-left behavior before release.'),
        ('Privacy', 'Limit public exposure of personal data, protect private chat, validate uploads, and define retention rules for media and messages.')], [1.45, 5.45])

    add_heading(doc, '6. Technical Architecture and Analysis', 1)
    add_heading(doc, '6.1 Technology stack', 2)
    add_table(doc, ['Layer', 'Technology / implementation'], [
        ('Presentation', 'Django templates, HTML, CSS, JavaScript, Tailwind-oriented styling, local fonts, responsive layouts'),
        ('Application', 'Python, Django views, forms, decorators, services, URL routing, Django messages'),
        ('Persistence', 'Django ORM with SQLite development database and migrations'),
        ('Media', 'Pillow-compatible image uploads and local media storage'),
        ('API / filtering', 'Django REST Framework and django-filter dependencies'),
        ('PWA', 'Web manifest, service worker, cached static assets and offline fallback'),
        ('Integration', 'WhatsApp contact URLs; no payment provider or live-news provider in the MVP')], [1.45, 5.45])
    add_heading(doc, '6.2 Application modules', 2)
    add_table(doc, ['Module', 'Responsibility'], [
        ('core', 'Home dashboard, shared logic, sports news endpoint, offline page'),
        ('accounts', 'Custom User, authentication, profiles, follows, exploits, endorsements, permissions'),
        ('organizations', 'Sports categories, organization profiles, directory'),
        ('events', 'Event categories, events, registrations, invoices, organizer workflows'),
        ('media_feed', 'Posts, comments, likes, shorts, feed browsing'),
        ('marketplace', 'Product categories, products, seller contact'),
        ('sponsorships', 'Sponsor profiles, campaigns, pledges, proposals, contracts'),
        ('chat', 'Conversations, messages, attachments, read state')], [1.45, 5.45])
    add_figure(doc, images[0], 1, 'Use-case view of the SPORTIVA CM platform.')
    add_figure(doc, images[5], 2, 'Component view of the modular Django architecture.')
    add_figure(doc, images[6], 3, 'Deployment view for the current local MVP topology.')

    add_heading(doc, '7. Data and Domain Analysis', 1)
    add_para(doc, 'The custom User entity is the central identity object. It participates in social relationships, event registration, content authorship, marketplace selling, sponsorship activity, and private messaging. Domain objects are separated into Django apps and connected through foreign keys, one-to-one relations, many-to-many relations, and unique constraints.')
    add_table(doc, ['Entity', 'Key relationships and purpose'], [
        ('User', 'Central identity; owns profiles, posts, products, campaigns, proposals, and messages.'),
        ('OrganizationProfile', 'Optional organization identity linked to a user; associated with events.'),
        ('Event / EventRegistration', 'Event belongs to organizer, sport, category, and optionally organization; registrations link users to events uniquely.'),
        ('Post / Comment / Like', 'Social content owned by users; comments and likes are dependent interactions.'),
        ('Campaign / Pledge', 'Campaign belongs to creator and collects pledge records from sponsors.'),
        ('SponsorshipRequest / Contract', 'Proposal workflow that can produce an active contract.'),
        ('Conversation / ChatMessage', 'Private participant group and ordered messages with attachment/read state.'),
        ('AthleteExploit / AthleteEndorsement', 'Achievement verification and community reputation signals.')], [1.8, 5.1])
    add_figure(doc, images[1], 4, 'Core UML classes and principal associations.')
    add_figure(doc, images[8], 5, 'Entity relationship view of persistent platform records.')

    add_heading(doc, '8. UML Behavioral Specifications', 1)
    add_heading(doc, '8.1 Event registration sequence', 2)
    add_para(doc, 'The browser requests event details, the view checks event availability and existing registrations, a valid registration is stored, and the invoice service generates a downloadable document. The current payment workflow records a status and does not connect to a payment gateway.')
    add_figure(doc, images[2], 6, 'Sequence diagram for event registration and invoice generation.')
    add_heading(doc, '8.2 Sponsorship proposal activity', 2)
    add_para(doc, 'A proposal is created, validated, reviewed by its recipient, and either declined with notification or accepted with contract creation. This represents the current application workflow and should be extended with audit history for production use.')
    add_figure(doc, images[3], 7, 'Activity diagram for sponsorship proposal handling.')
    add_heading(doc, '8.3 Registration state machine', 2)
    add_para(doc, 'A registration moves from creation through validation to confirmation, cancellation, completion, or refund-related handling. The exact financial semantics depend on future payment integration.')
    add_figure(doc, images[4], 8, 'State-machine diagram for event registrations.')
    add_figure(doc, images[7], 9, 'Package diagram showing Django application organization.')

    add_heading(doc, '9. Interface and Route Specification', 1)
    add_table(doc, ['Area', 'Representative routes', 'Access'], [
        ('Home and PWA', '/, /offline/, /sw.js, /manifest.json', 'Public'),
        ('Accounts', '/accounts/register/, /accounts/login/, /accounts/profile/', 'Mixed / authenticated'),
        ('Profiles', '/profiles/, /accounts/profile/<username>/', 'Public with protected mutations'),
        ('Organizations', '/organizations/', 'Public with protected creation/editing'),
        ('Events', '/events/, /events/create/, /events/<id>/', 'Public discovery; authenticated actions'),
        ('Media', '/media-feed/, /media-feed/create/, /media-feed/<id>/', 'Public browsing; authenticated publishing'),
        ('Marketplace', '/marketplace/, /marketplace/sell/, /marketplace/<id>/', 'Public browsing; authenticated selling'),
        ('Sponsorships', '/sponsorships/ and campaign/proposal routes', 'Authenticated workflows'),
        ('Chat', '/chat/, /chat/<conversation_id>/', 'Authenticated participants only'),
        ('API and admin', '/api/sports-news/, /admin/', 'Mixed / staff')], [1.25, 3.7, 1.95])

    add_heading(doc, '10. Security, Privacy, and Operational Analysis', 1)
    add_heading(doc, '10.1 Implemented protections', 2)
    add_bullets(doc, ['Django session authentication and custom user model.', 'CSRF middleware and clickjacking protection.', 'Django password validators for similarity, length, common passwords, and numeric-only passwords.', 'Role-based tab access with staff and superuser override.', 'Object-level checks for event registration, invoices, exploits, and chat participation.', 'Unique constraints for event registrations, follows, and likes.', 'Phone normalization before WhatsApp URL construction.'])
    add_heading(doc, '10.2 Production security gaps', 2)
    add_bullets(doc, ['DEBUG currently defaults to True and ALLOWED_HOSTS defaults to wildcard behavior.', 'A fallback development secret key exists and must be replaced through environment configuration.', 'HTTPS, HSTS, secure cookies, CSP, rate limiting, upload scanning, and audit logging require production configuration.', 'Local media storage and SQLite require replacement or hardening for scalable deployment.', 'Email verification, password reset, moderation, abuse reports, and notification controls are not complete.'])

    add_heading(doc, '11. Installation, Deployment, and Maintenance', 1)
    add_heading(doc, '11.1 Local installation', 2)
    add_para(doc, 'The documented local workflow is: create a virtual environment, install Django/Pillow/form/API/filter dependencies, apply migrations, seed sample data, and run the development server.')
    p = doc.add_paragraph(); p.style = 'No Spacing'
    r = p.add_run('python -m venv .venv\n.venv\\Scripts\\activate\npip install django pillow django-crispy-forms crispy-tailwind djangorestframework django-filter\npython manage.py migrate\npython manage.py seed_data\npython manage.py runserver')
    r.font.name = 'Consolas'; r.font.size = Pt(9)
    add_heading(doc, '11.2 Production readiness requirements', 2)
    add_bullets(doc, ['Use environment variables for SECRET_KEY, DEBUG, ALLOWED_HOSTS, database, email, and external services.', 'Use PostgreSQL or another supported production database.', 'Serve static files through a controlled web server/CDN and media through secure object storage.', 'Configure HTTPS, secure cookies, HSTS, CSP, monitoring, backups, and log retention.', 'Add dependency locking and continuous integration for migrations, checks, and tests.'])

    add_heading(doc, '12. Verification and Acceptance Criteria', 1)
    criteria = [
        ('AC-01', 'A visitor can register, log in, view a profile, and update profile information.'),
        ('AC-02', 'An athlete can submit an exploit and an authorized verifier can approve or reject it.'),
        ('AC-03', 'An organizer can create an event and a user can register only once.'),
        ('AC-04', 'Capacity limits prevent additional confirmed registrations.'),
        ('AC-05', 'A registration can produce an invoice or entry-pass PDF.'),
        ('AC-06', 'A user can publish, like, comment on, and filter feed content.'),
        ('AC-07', 'A seller can publish a product and a visitor can contact the seller.'),
        ('AC-08', 'A campaign can receive a pledge record and display funding progress.'),
        ('AC-09', 'An accepted sponsorship proposal produces a contract record.'),
        ('AC-10', 'Only conversation participants can view private messages.'),
        ('AC-11', 'Previously visited pages can load through the offline cache and unavailable pages show the fallback.'),
        ('AC-12', 'Django checks and the automated test suite pass after dependencies are installed.')]
    add_table(doc, ['ID', 'Acceptance criterion'], criteria, [0.8, 6.1])

    add_heading(doc, '13. Testing Strategy', 1)
    add_bullets(doc, ['Model tests: constraints, score calculations, relations, and status transitions.', 'Form tests: required fields, invalid values, file handling, and validation feedback.', 'View tests: authentication, authorization, redirects, filtering, and protected object access.', 'Workflow tests: event registration, invoice generation, sponsorship proposal conversion, chat privacy, and feed interactions.', 'Security tests: CSRF, upload restrictions, unauthorized access, and sensitive data exposure.', 'PWA/browser tests: manifest, service-worker registration, cache behavior, and offline fallback.', 'Usability tests: responsive layouts, language switching, keyboard navigation, and long translated strings.'])
    add_para(doc, 'Recommended commands: python manage.py check and python manage.py test. The current document describes the required test strategy; test execution should be recorded separately for each release.')

    add_heading(doc, '14. Risks, Limitations, and Roadmap', 1)
    add_table(doc, ['Risk / limitation', 'Impact', 'Recommended response'], [
        ('Development security defaults', 'Potential exposure in public deployment', 'Harden settings and enforce environment configuration.'),
        ('SQLite/local media', 'Limited concurrency, scaling, and resilience', 'Move to production database and managed media storage.'),
        ('Simulated payments', 'No financial settlement or reconciliation', 'Integrate and audit a payment provider.'),
        ('Cached-read offline mode', 'Users cannot reliably create data offline', 'Add a queued write/sync design with conflict handling.'),
        ('Basic search and moderation', 'Lower discovery quality and governance', 'Add indexing, pagination, reporting, moderation, and audit tools.'),
        ('Role overlap', 'Ambiguous permissions for managers and organizations', 'Define a permission matrix and separate roles where required.')], [1.6, 2.2, 3.1])
    add_heading(doc, '15. Conclusion', 1)
    add_para(doc, 'SPORTIVA CM provides a coherent modular foundation for a sports promotion and community platform. Its strongest implemented capabilities are the domain separation across Django apps, role-aware user experience, event and sponsorship workflows, community interaction, and PWA-oriented access. The next engineering priority is production hardening: secure configuration, dependable payment and notification integrations, stronger automated verification, and scalable infrastructure.')
    add_heading(doc, 'Appendix A - Source and Evidence Basis', 1)
    add_bullets(doc, ['README.md and SPORTIVA_USER_GUIDE.md for product goals and user workflows.', 'sportiva_cm/settings.py and sportiva_cm/urls.py for configuration and route boundaries.', 'accounts, organizations, events, media_feed, marketplace, sponsorships, chat, and core apps for implemented domain behavior.', 'Django migrations for persisted schema history.', 'Static manifest, service worker, templates, and JavaScript for PWA and interface behavior.', 'The generated diagrams in DEFENSE/prsd_diagrams are aligned to the current implementation rather than legacy generic figures.'])

    doc.core_properties.title = 'SPORTIVA CM Project Requirements and Specifications'
    doc.core_properties.subject = 'Requirements, analysis, architecture, and UML diagrams'
    doc.core_properties.author = 'SPORTIVA CM Project'
    doc.core_properties.comments = 'Generated from the current project implementation.'
    doc.save(OUTPUT)


def main():
    images = [diagram_use_case(), diagram_class(), diagram_sequence(), diagram_activity(), diagram_state(), diagram_component(), diagram_deployment(), diagram_package(), diagram_er()]
    build_document(images)
    print(OUTPUT)
    print(f'Generated {len(images)} UML/architecture diagrams in {DIAGRAM_DIR}')


if __name__ == '__main__':
    main()
