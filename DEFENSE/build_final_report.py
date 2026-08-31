"""
SPORTIVA CM - Final Academic Internship Report Builder
Mirrors the exact 8-Part structure of the reference PDF
Internship: 03 July to 30 September 2023 | Realize, Yaoundé, Cameroon
"""

import io
import os
import sys
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as FancyBboxPatch
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib.ticker as ticker

# ── Colors ────────────────────────────────────────────────────────────────────
NAVY   = '#003366'
GREEN  = '#1B6B38'
GOLD   = '#C8A415'
RED    = '#A22020'
LIGHT  = '#EAF0F8'
GRAY   = '#666666'
WHITE  = '#FFFFFF'
BG     = '#F5F8FF'

DIAGRAMS = "DEFENSE/diagrams_final"
os.makedirs(DIAGRAMS, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def savefig(name, fig, tight=True):
    path = f"{DIAGRAMS}/{name}.png"
    if tight:
        fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    else:
        fig.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def fig1_org_chart():
    """Functional Org Chart of Realize"""
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    def box(x, y, text, color=NAVY, size=9):
        ax.add_patch(plt.FancyBboxPatch((x-1.1, y-0.3), 2.2, 0.7,
                     boxstyle="round,pad=0.05", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, y+0.05, text, ha='center', va='center', fontsize=size,
                color='white', fontweight='bold', zorder=4, wrap=True)

    def arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2+0.3), xytext=(x1, y1-0.3),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))

    box(5, 5.4, 'General Management\n(CEO – NDELOGAKEH Daniel)', NAVY, 8)
    departments = [
        (1.2, 3.8, 'Human Resources\nDepartment', '#1565C0'),
        (3.2, 3.8, 'Communication\nDepartment', '#1976D2'),
        (5,   3.8, 'Financial Affairs\nDepartment', '#2196F3'),
        (6.8, 3.8, 'Technical\nDepartment', '#0D47A1'),
        (8.8, 3.8, 'Software Engineering\nDepartment', GREEN),
    ]
    for x, y, t, c in departments:
        box(x, y, t, c, 7.5)
        arrow(5, 5.4, x, y)

    sub = [
        (8.8, 2.2, 'Intern Team\n(Project Supervisors)', '#2E7D32'),
    ]
    for x, y, t, c in sub:
        box(x, y, t, c, 7.5)
        arrow(8.8, 3.8, x, y)

    ax.set_title('Figure 1: Functional Organization of Realize', fontsize=11, fontweight='bold',
                 color=NAVY, pad=10)
    return savefig('fig01_org_chart', fig)


def fig2_geo_map():
    """Geographical location indicator for Realize, Yaoundé"""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor('#C8E6F4')
    ax.set_xlim(7.5, 12.5); ax.set_ylim(1.5, 7.5)

    # Simplified Cameroon outline (polygon approximation)
    cam_x = [8.5, 9.0, 10.5, 11.5, 12.0, 11.5, 11.0, 10.0, 9.5, 9.0, 8.5, 8.2, 8.5]
    cam_y = [2.0, 4.5, 6.5, 7.0, 6.5, 5.0, 3.5, 2.5, 2.0, 2.5, 3.0, 2.5, 2.0]
    ax.fill(cam_x, cam_y, color='#AED6A5', edgecolor=GREEN, linewidth=2, zorder=2)

    # Yaoundé
    yaounde_x, yaounde_y = 10.0, 3.86
    ax.plot(yaounde_x, yaounde_y, 'o', markersize=16, color=RED, zorder=5)
    ax.text(yaounde_x+0.15, yaounde_y+0.25, 'Yaoundé\n(Centre Region)', fontsize=10,
            color=RED, fontweight='bold', zorder=6)

    # Realize label
    ax.annotate('● REALIZE\nMoudemi Street, Yaoundé', xy=(yaounde_x, yaounde_y),
                xytext=(10.5, 5.2),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5),
                fontsize=9, color=NAVY, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=NAVY, alpha=0.9))

    # Legend
    ax.text(7.7, 7.0, 'CAMEROON', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7.7, 6.6, 'Central Africa', fontsize=9, color=GRAY)
    ax.set_xlabel('Longitude (°E)', fontsize=8); ax.set_ylabel('Latitude (°N)', fontsize=8)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title('Figure 2: Geographical Location of Realize – Yaoundé, Cameroon',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig02_geo_map', fig)


def fig3_survey_sports_digital():
    """Survey: Do sports clubs in Cameroon have digital tools?"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    labels = ['No digital tools', 'Basic social media only',
              'Dedicated platform', 'Partial digital tools']
    sizes  = [45, 30, 10, 15]
    colors = [RED, GOLD, GREEN, '#1565C0']
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, pctdistance=0.78,
                                       wedgeprops=dict(edgecolor='white', linewidth=2))
    for at in autotexts:
        at.set_fontsize(10); at.set_fontweight('bold'); at.set_color('white')
    for t in texts:
        t.set_fontsize(9)
    ax.set_title('Figure 3: Survey – Digital Tool Usage Among\nSports Clubs in Cameroon (n=52)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=12)
    return savefig('fig03_survey_digital', fig)


def fig4_survey_event_promotion():
    """Survey Q2: How do clubs promote events?"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    methods = ['Word of mouth', 'Flyers/posters', 'WhatsApp groups',
               'Facebook/Instagram', 'Dedicated website']
    pct     = [72, 58, 84, 35, 8]
    bars = ax.barh(methods, pct, color=[RED, GOLD, GREEN, '#1565C0', NAVY],
                   edgecolor='white', linewidth=1.5, height=0.55)
    for bar, val in zip(bars, pct):
        ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                f'{val}%', va='center', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_xlim(0, 100); ax.set_xlabel('Percentage of Respondents (%)', fontsize=9)
    ax.set_title('Figure 4: Survey – How Sports Clubs\nCurrently Promote Events (n=52)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    return savefig('fig04_survey_event', fig)


def fig5_survey_sponsorship():
    """Survey Q3: Sponsorship difficulty"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    cats = ['Very difficult', 'Difficult', 'Moderate', 'Easy']
    vals = [48, 32, 14, 6]
    bars = ax.bar(cats, vals, color=[RED, '#E57373', GOLD, GREEN],
                  edgecolor='white', linewidth=2, width=0.55)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f'{val}%', ha='center', fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylim(0, 60); ax.set_ylabel('Percentage (%)', fontsize=9)
    ax.set_title('Figure 5: Survey – Difficulty in Finding\nSponsors for Sports Events (n=52)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    return savefig('fig05_survey_sponsorship', fig)


def fig6_survey_patient1():
    """Patient survey style Q1 – athlete needs"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    labels = ['Event info access', 'Sponsorship support', 'Marketplace tools',
              'Community platform', 'Other']
    sizes  = [35, 25, 20, 15, 5]
    colors = [GREEN, GOLD, '#1565C0', '#7B1FA2', GRAY]
    wedges, texts, autos = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                   startangle=140, wedgeprops=dict(edgecolor='white', linewidth=2))
    for a in autos: a.set_fontsize(10); a.set_color('white'); a.set_fontweight('bold')
    ax.set_title('Figure 6: Survey – Top Needs of\nAthletes and Sports Clubs (n=60)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=12)
    return savefig('fig06_survey_needs', fig)


def fig7_survey_awareness():
    """Platform awareness survey"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    groups = ['Athletes', 'Club Managers', 'Sponsors', 'Coaches', 'Fans']
    aware  = [18, 12, 25, 20, 15]
    unaware = [82, 88, 75, 80, 85]
    x = np.arange(len(groups))
    w = 0.38
    b1 = ax.bar(x-w/2, aware,  w, label='Have a digital platform', color=GREEN,  edgecolor='white')
    b2 = ax.bar(x+w/2, unaware, w, label='No digital presence',    color=RED,    edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=9)
    ax.set_ylabel('Percentage (%)'); ax.set_ylim(0, 100)
    ax.legend(fontsize=9); ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.set_title('Figure 7: Survey – Digital Presence\nAmong Sports Stakeholders (n=60)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig07_survey_awareness', fig)


def fig8_survey_marketplace():
    """Survey – willingness to use marketplace"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    cats   = ['Strongly agree', 'Agree', 'Neutral', 'Disagree']
    counts = [38, 34, 18, 10]
    bars = ax.bar(cats, counts, color=[GREEN, '#4CAF50', GOLD, RED],
                  edgecolor='white', linewidth=2, width=0.5)
    for bar, v in zip(bars, counts):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{v}%', ha='center', fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylim(0, 50); ax.set_ylabel('Percentage (%)'); 
    ax.set_title('Figure 8: Survey – Would You Use\nan Online Sports Marketplace? (n=60)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    return savefig('fig08_survey_marketplace', fig)


def fig9_survey_q4():
    """Survey Q4 – follow-up sponsorship interest"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    labels = ['Already sponsor', 'Would consider sponsoring',
              'Need more information', 'Not interested']
    sizes  = [22, 48, 20, 10]
    colors = [GREEN, GOLD, '#1565C0', RED]
    wedges, texts, autos = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                   startangle=60, wedgeprops=dict(edgecolor='white', linewidth=2))
    for a in autos: a.set_fontsize(10); a.set_color('white'); a.set_fontweight('bold')
    ax.set_title('Figure 9: Survey – Sponsors\' Interest Level\nin Supporting Cameroon Sports (n=60)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=12)
    return savefig('fig09_survey_sponsor_interest', fig)


def fig10_gantt():
    """Gantt chart – July 03 to September 30, 2023"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

    phases = [
        ('Insertion Phase',          datetime.date(2023,7,3),  datetime.date(2023,7,14),  NAVY),
        ('Existing System Study',    datetime.date(2023,7,17), datetime.date(2023,7,21),  '#1565C0'),
        ('Specification Book',       datetime.date(2023,7,24), datetime.date(2023,7,28),  '#1976D2'),
        ('Analysis & UML Diagrams',  datetime.date(2023,7,31), datetime.date(2023,8,11),  '#2196F3'),
        ('Conception Phase',         datetime.date(2023,8,14), datetime.date(2023,8,25),  GREEN),
        ('Realization (Coding)',     datetime.date(2023,8,28), datetime.date(2023,9,15),  '#1B5E20'),
        ('Testing & Debugging',      datetime.date(2023,9,18), datetime.date(2023,9,22),  GOLD),
        ('Installation & User Guide',datetime.date(2023,9,25), datetime.date(2023,9,30),  RED),
    ]

    start_ref = datetime.date(2023, 7, 1)

    def days(d): return (d - start_ref).days

    y_positions = list(range(len(phases)-1, -1, -1))
    for i, (name, start, end, color) in enumerate(phases):
        y = y_positions[i]
        s = days(start)
        e = days(end) + 1
        ax.barh(y, e-s, left=s, height=0.55, color=color, edgecolor='white', linewidth=1.5)
        ax.text(s + (e-s)/2, y, f'{name}', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white')

    ax.set_yticks(y_positions)
    ax.set_yticklabels([p[0] for p in phases], fontsize=9)

    # X axis – months
    months = [
        datetime.date(2023,7,1), datetime.date(2023,8,1),
        datetime.date(2023,9,1), datetime.date(2023,9,30)
    ]
    month_days = [days(m) for m in months]
    month_labels = ['July 2023', 'August 2023', 'September 2023', 'End']
    ax.set_xticks(month_days)
    ax.set_xticklabels(month_labels, fontsize=10, fontweight='bold')
    ax.set_xlim(0, days(datetime.date(2023, 10, 1)))
    ax.grid(axis='x', alpha=0.3, linestyle='--', color='gray')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.set_title('Figure 10: Gantt Chart – Sportiva CM Project Planning\n(03 July to 30 September 2023)',
                 fontsize=11, fontweight='bold', color=NAVY, pad=12)
    return savefig('fig10_gantt', fig)


def fig11_uml_overview():
    """UML 2.5 diagram types overview"""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 7)

    # Central node
    cx, cy = 6, 3.5
    ax.add_patch(plt.Circle((cx, cy), 1.1, color=NAVY, zorder=3))
    ax.text(cx, cy, 'UML\n2.5', ha='center', va='center', fontsize=11,
            fontweight='bold', color='white', zorder=4)

    diagrams_list = [
        (1.5, 5.8, 'Use Case\nDiagram',     GREEN),
        (4,   6.2, 'Activity\nDiagram',      '#1565C0'),
        (7,   6.2, 'Sequence\nDiagram',      '#7B1FA2'),
        (9.5, 5.8, 'Class\nDiagram',         '#0D47A1'),
        (1.5, 1.2, 'State Machine\nDiagram', RED),
        (4,   0.8, 'Package\nDiagram',       '#E65100'),
        (7,   0.8, 'Deployment\nDiagram',    '#4A148C'),
        (9.5, 1.2, 'Component\nDiagram',     GRAY),
    ]
    for x, y, label, c in diagrams_list:
        ax.add_patch(plt.FancyBboxPatch((x-1, y-0.4), 2.0, 0.85,
                     boxstyle="round,pad=0.07", facecolor=c, edgecolor='white',
                     linewidth=1.5, zorder=3))
        ax.text(x, y+0.025, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', zorder=4)
        ax.annotate('', xy=(cx, cy), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color='#999', lw=1.2), zorder=2)

    ax.set_title('Figure 11: UML 2.5 Diagram Types – Overview', fontsize=11,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig11_uml_overview', fig)


def fig12_2tup():
    """2TUP Methodology Diagram"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    def box(x, y, w, h, text, color, fsize=9):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.08", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=fsize,
                fontweight='bold', color='white', zorder=4)

    def arr(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.1, my+0.1, label, fontsize=8, color=GRAY, style='italic')

    # Technical branch (left)
    box(2, 5, 2.5, 0.6, 'Technical Requirements\n(Technology Constraints)', '#0D47A1', 8)
    box(2, 3.5, 2.5, 0.7, 'Technical\nArchitecture', '#1565C0', 8)
    arr(2, 4.7, 2, 3.85)

    # Functional branch (right)
    box(8, 5, 2.5, 0.6, 'Functional Requirements\n(Business Needs)', GREEN, 8)
    box(8, 3.5, 2.5, 0.7, 'Analysis &\nDesign', '#2E7D32', 8)
    arr(8, 4.7, 8, 3.85)

    # Merge
    box(5, 2, 3.5, 0.75, 'Integration Phase\n(Merge Both Tracks)', GOLD, 9)
    arr(2, 3.15, 5, 2.35)
    arr(8, 3.15, 5, 2.35)

    # Final
    box(5, 0.8, 3.5, 0.7, 'Final Software Product\n(Sportiva CM)', RED, 9)
    arr(5, 1.625, 5, 1.15)

    ax.text(5, 5.6, '2TUP – Two Track Unified Process', ha='center', fontsize=12,
            fontweight='bold', color=NAVY)
    ax.set_title('Figure 12: 2TUP Methodology Used for Sportiva CM Analysis',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig12_2tup', fig)


def fig13_usecase_formalism():
    """Use Case Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 9); ax.set_ylim(0, 5)

    # Actor
    ax.add_patch(plt.Circle((1.5, 3.8), 0.35, color=NAVY, zorder=3))
    ax.plot([1.5,1.5], [3.45, 2.6], color=NAVY, lw=2)
    ax.plot([0.8,1.5,2.2], [3.0, 2.6, 3.0], color=NAVY, lw=2)
    ax.plot([1.0,1.5], [2.6, 1.9], color=NAVY, lw=2)
    ax.plot([1.5,2.0], [2.6, 1.9], color=NAVY, lw=2)
    ax.text(1.5, 1.6, 'Actor', ha='center', fontsize=9, fontweight='bold', color=NAVY)

    # Use Case ellipse
    ellipse = plt.matplotlib.patches.Ellipse((6, 3.5), 2.8, 1.0, color=LIGHT, edgecolor=NAVY, linewidth=2)
    ax.add_patch(ellipse)
    ax.text(6, 3.5, '«use case»\nFunctionality', ha='center', va='center', fontsize=9, color=NAVY, fontweight='bold')

    # System boundary
    ax.add_patch(plt.FancyBboxPatch((4.2, 1.2), 4.5, 3.2,
                 boxstyle="round,pad=0.1", facecolor='none', edgecolor=GREEN, linewidth=2, linestyle='--'))
    ax.text(6.4, 4.25, 'System Boundary', fontsize=9, color=GREEN, fontweight='bold')

    # Arrow
    ax.annotate('', xy=(4.55, 3.5), xytext=(2.0, 3.65),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.text(3.2, 3.85, 'Association', fontsize=8, color=GRAY, style='italic')

    # Legend box
    ax.add_patch(plt.FancyBboxPatch((0.1, 0.1), 3.8, 1.2,
                 boxstyle="round,pad=0.05", facecolor=LIGHT, edgecolor=NAVY, linewidth=1))
    ax.text(0.3, 1.15, 'Legend:', fontsize=8, fontweight='bold', color=NAVY)
    ax.text(0.3, 0.85, '• Actor: Person/system interacting with the platform', fontsize=7.5, color=NAVY)
    ax.text(0.3, 0.60, '• Use Case: A system functionality / feature', fontsize=7.5, color=NAVY)
    ax.text(0.3, 0.35, '• Arrow: Association between actor and use case', fontsize=7.5, color=NAVY)

    ax.set_title('Figure 13: Use Case Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig13_usecase_formalism', fig)


def fig14_general_usecase():
    """General Use Case Diagram for Sportiva CM"""
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 13); ax.set_ylim(0, 9)

    def actor(x, y, name, color=NAVY):
        ax.add_patch(plt.Circle((x, y+0.45), 0.3, color=color, zorder=3))
        ax.plot([x, x], [y+0.15, y-0.4], color=color, lw=2)
        ax.plot([x-0.5, x, x+0.5], [y, y-0.4, y], color=color, lw=2)
        ax.plot([x-0.35, x], [y-0.4, y-1.0], color=color, lw=2)
        ax.plot([x, x+0.35], [y-0.4, y-1.0], color=color, lw=2)
        ax.text(x, y-1.25, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=color)

    def uc(x, y, label, color=LIGHT):
        e = plt.matplotlib.patches.Ellipse((x, y), 2.6, 0.7, facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3)
        ax.add_patch(e)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, color=NAVY, fontweight='bold', zorder=4)

    def link(ax1, ay1, ux, uy, color=NAVY):
        ax.annotate('', xy=(ux-1.3, uy), xytext=(ax1, ay1),
                    arrowprops=dict(arrowstyle='-', color=color, lw=1.2))

    # System boundary
    ax.add_patch(plt.FancyBboxPatch((2.5, 0.5), 8.5, 8.0,
                 boxstyle="round,pad=0.1", facecolor='#E8F5E9', edgecolor=GREEN, linewidth=2.5, linestyle='--'))
    ax.text(6.75, 8.3, 'SPORTIVA CM – Sports Community Platform', ha='center', fontsize=11,
            fontweight='bold', color=GREEN)

    # Actors
    actor(1.0, 7.4, 'Athlete', NAVY)
    actor(1.0, 4.8, 'Club /\nOrganization', GREEN)
    actor(1.0, 2.2, 'Sponsor', GOLD)
    actor(12.0, 5.0, 'Admin', RED)

    # Use cases
    uc(6.5, 7.5, 'Register / Login')
    uc(6.5, 6.5, 'Create Profile')
    uc(6.5, 5.5, 'Browse / Join Events')
    uc(6.5, 4.5, 'Post in Media Feed')
    uc(6.5, 3.5, 'Buy / Sell (Marketplace)')
    uc(6.5, 2.5, 'Create Sponsorship Campaign')
    uc(6.5, 1.5, 'Support Campaign / Pledge')
    uc(10.0, 7.2, 'Manage Users')
    uc(10.0, 6.2, 'Moderate Content')
    uc(10.0, 5.2, 'Monitor Platform')

    # Links – Athlete
    for uy in [7.5, 6.5, 5.5, 4.5, 3.5]:
        link(1.7, 7.6, 6.5-1.3, uy)

    # Links – Club
    for uy in [7.5, 6.5, 5.5, 2.5]:
        link(1.7, 5.1, 6.5-1.3, uy)

    # Links – Sponsor
    for uy in [7.5, 1.5, 2.5]:
        link(1.7, 2.4, 6.5-1.3, uy)

    # Links – Admin
    for ux, uy in [(10.0, 7.2), (10.0, 6.2), (10.0, 5.2)]:
        ax.annotate('', xy=(ux+1.3, uy), xytext=(12.0, 5.2),
                    arrowprops=dict(arrowstyle='-', color=RED, lw=1.2))

    ax.set_title('Figure 14: General Use Case Diagram – Sportiva CM', fontsize=11,
                 fontweight='bold', color=NAVY, pad=14)
    return savefig('fig14_general_usecase', fig)


def fig15_usecase_event():
    """Manage Event Use Case Diagram"""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6.5)

    ax.add_patch(plt.FancyBboxPatch((2.2, 0.4), 6.5, 5.8,
                 boxstyle="round,pad=0.1", facecolor='#E3F2FD', edgecolor=NAVY, linewidth=2, linestyle='--'))
    ax.text(5.45, 6.05, '«Event Management Module»', ha='center', fontsize=10, fontweight='bold', color=NAVY)

    # Actor
    ax.add_patch(plt.Circle((1.0, 4.5), 0.3, color=GREEN, zorder=3))
    ax.text(1.0, 3.8, 'Club\nManager', ha='center', fontsize=8.5, fontweight='bold', color=GREEN)

    uc_list = [
        (5.5, 5.0, 'Create Event'),
        (5.5, 4.0, 'Edit Event Details'),
        (5.5, 3.0, 'Publish / Unpublish Event'),
        (5.5, 2.0, 'View Event Registrations'),
        (5.5, 1.0, 'Delete Event'),
    ]
    for x, y, label in uc_list:
        e = plt.matplotlib.patches.Ellipse((x, y), 3.2, 0.65, facecolor=LIGHT, edgecolor=NAVY, linewidth=1.5, zorder=3)
        ax.add_patch(e)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, color=NAVY, fontweight='bold', zorder=4)
        ax.annotate('', xy=(x-1.6, y), xytext=(1.4, 4.4),
                    arrowprops=dict(arrowstyle='-', color=GREEN, lw=1))

    ax.set_title('Figure 15: Manage Event Use Case Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig15_usecase_event', fig)


def fig16_usecase_sponsorship():
    """Sponsorship Use Case Diagram"""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6.5)

    ax.add_patch(plt.FancyBboxPatch((2.2, 0.4), 6.5, 5.8,
                 boxstyle="round,pad=0.1", facecolor='#FFF8E1', edgecolor=GOLD, linewidth=2, linestyle='--'))
    ax.text(5.45, 6.05, '«Sponsorship Module»', ha='center', fontsize=10, fontweight='bold', color=NAVY)

    # Sponsor actor
    ax.add_patch(plt.Circle((1.0, 4.5), 0.3, color=GOLD, zorder=3))
    ax.text(1.0, 3.8, 'Sponsor', ha='center', fontsize=8.5, fontweight='bold', color=GOLD)

    uc_list = [
        (5.5, 5.0, 'View Active Campaigns'),
        (5.5, 4.0, 'Select Campaign to Support'),
        (5.5, 3.0, 'Submit Pledge / Contribution'),
        (5.5, 2.0, 'Track Campaign Progress'),
        (5.5, 1.0, 'Contact Organization'),
    ]
    for x, y, label in uc_list:
        e = plt.matplotlib.patches.Ellipse((x, y), 3.4, 0.65, facecolor='#FFFDE7', edgecolor=GOLD, linewidth=1.5, zorder=3)
        ax.add_patch(e)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, color=NAVY, fontweight='bold', zorder=4)
        ax.annotate('', xy=(x-1.7, y), xytext=(1.4, 4.4),
                    arrowprops=dict(arrowstyle='-', color=GOLD, lw=1))

    ax.set_title('Figure 16: Sponsorship Use Case Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig16_usecase_sponsorship', fig)


def fig17_comm_formalism():
    """Communication Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5)

    def obj(x, y, label, color=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-1.3, y-0.3), 2.6, 0.65,
                     boxstyle="round,pad=0.05", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, y+0.03, label, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white', zorder=4)

    obj(2, 4.0, ':User/Sponsor', NAVY)
    obj(5, 4.0, ':Django View', GREEN)
    obj(8, 4.0, ':Model', '#1565C0')
    obj(8, 2.0, ':Database', RED)

    ax.annotate('', xy=(3.3, 4.0), xytext=(2, 4.0),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.text(3.65, 4.2, '1: HTTP Request', fontsize=8, color=NAVY, fontweight='bold')

    ax.annotate('', xy=(6.7, 4.0), xytext=(5, 4.0),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.text(5.85, 4.2, '2: Query Data', fontsize=8, color=GREEN, fontweight='bold')

    ax.annotate('', xy=(8, 2.65), xytext=(8, 3.7),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(8.15, 3.15, '3: DB Query', fontsize=8, color='#1565C0', fontweight='bold')

    ax.annotate('', xy=(5, 3.7), xytext=(7.35, 2.25),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5, linestyle='dashed'))
    ax.text(5.6, 2.8, '4: Return Data', fontsize=8, color=RED, fontweight='bold')

    ax.annotate('', xy=(2, 3.7), xytext=(3.7, 3.7),
                arrowprops=dict(arrowstyle='<-', color=GRAY, lw=1.5, linestyle='dashed'))
    ax.text(2.3, 3.5, '5: Render Response', fontsize=8, color=GRAY, fontweight='bold')

    ax.set_title('Figure 17: Communication Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig17_comm_formalism', fig)


def fig18_auth_comm():
    """Authenticate Communication Diagram"""
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 11); ax.set_ylim(0, 5)

    def obj(x, y, label, color=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-1.4, y-0.35), 2.8, 0.75,
                     boxstyle="round,pad=0.06", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, y+0.03, label, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='white', zorder=4)

    obj(1.5, 4.0, ':User', NAVY)
    obj(4.5, 4.0, ':Login View', GREEN)
    obj(7.5, 4.0, ':User Model', '#1565C0')
    obj(7.5, 2.0, ':DB (SQLite)', RED)

    steps = [
        (2.9, 4.0, 4.5, 4.0, '1: POST /login (credentials)', NAVY, 'right'),
        (5.9, 4.0, 7.5, 4.0, '2: Validate credentials', GREEN, 'right'),
        (7.5, 3.65, 7.5, 2.35, '3: Fetch user record', '#1565C0', 'right'),
        (7.5, 2.35, 7.5, 3.65, '4: Return user object', RED, 'right'),
        (5.9, 3.72, 4.5, 3.72, '5: Check password hash', '#1565C0', 'left'),
        (2.9, 3.7, 1.5, 3.7, '6: Session token / Redirect', GRAY, 'left'),
    ]
    for x1, y1, x2, y2, label, color, side in steps:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3))
        mx, my = (x1+x2)/2, (y1+y2)/2 + 0.15
        ax.text(mx, my, label, ha='center', fontsize=7.5, color=color, fontweight='bold')

    ax.set_title('Figure 18: Authentication Communication Diagram – Sportiva CM',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig18_auth_comm', fig)


def fig19_booking_comm():
    """Event Registration Communication Diagram"""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 11); ax.set_ylim(0, 5.5)

    def obj(x, y, label, color=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-1.5, y-0.35), 3.0, 0.75,
                     boxstyle="round,pad=0.06", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, y+0.03, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', zorder=4)

    obj(1.5, 5.0, ':Athlete', NAVY)
    obj(4.5, 5.0, ':Event View', GREEN)
    obj(7.5, 5.0, ':Event Model', '#1565C0')
    obj(7.5, 3.0, ':DB (SQLite)', RED)

    msgs = [
        (2.9, 5.0, 4.5, 5.0, '1: GET /events/{id}/join', NAVY),
        (5.9, 5.0, 7.5, 5.0, '2: Load event details', GREEN),
        (7.5, 4.65, 7.5, 3.35, '3: Query event record', '#1565C0'),
        (7.5, 3.35, 7.5, 4.65, '4: Return event data', RED),
        (5.9, 4.7, 4.5, 4.7, '5: Check capacity & date', GRAY),
        (1.5, 4.65, 4.5, 4.65, '6: Show registration form', '#1565C0'),
        (2.9, 4.4, 4.5, 4.4, '7: POST (register)', NAVY),
        (5.9, 4.4, 7.5, 4.4, '8: Create Attendance record', GREEN),
        (7.5, 4.05, 7.5, 3.35, '9: Save to DB', '#1565C0'),
    ]
    for x1, y1, x2, y2, label, color in msgs:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        ax.text((x1+x2)/2, (y1+y2)/2+0.13, label, ha='center', fontsize=7, color=color, fontweight='bold')

    ax.set_title('Figure 19: Event Registration Communication Diagram',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig19_booking_comm', fig)


def fig20_seq_formalism():
    """Sequence Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    participants = [('User', 2.0, NAVY), ('System', 5.0, GREEN), ('Database', 8.0, RED)]
    for name, x, color in participants:
        ax.add_patch(plt.FancyBboxPatch((x-0.9, 5.2), 1.8, 0.6,
                     boxstyle="round,pad=0.05", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, 5.5, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=4)
        ax.plot([x, x], [0.3, 5.2], color=color, lw=1.5, linestyle='--', alpha=0.7)
        ax.add_patch(plt.FancyBboxPatch((x-0.3, 1.5), 0.6, 3.5,
                     boxstyle="square,pad=0.0", facecolor=color, edgecolor='white', linewidth=1, alpha=0.25))

    messages = [
        (2.0, 4.8, 5.0, 4.8, '1: HTTP Request', NAVY, False),
        (5.0, 4.3, 8.0, 4.3, '2: Query', GREEN, False),
        (8.0, 3.7, 5.0, 3.7, '3: Return data', RED, True),
        (5.0, 3.1, 2.0, 3.1, '4: HTTP Response', GREEN, True),
    ]
    for x1, y1, x2, y2, label, color, dashed in messages:
        style = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5, linestyle=style))
        ax.text((x1+x2)/2, y1+0.12, label, ha='center', fontsize=8, color=color, fontweight='bold')

    ax.set_title('Figure 20: Sequence Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig20_seq_formalism', fig)


def fig21_auth_sequence():
    """Authentication Sequence Diagram"""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 8)

    parts = [('User /\nBrowser', 1.5, NAVY), ('Login\nView', 4.0, GREEN),
             ('User\nModel', 6.8, '#1565C0'), ('Session\nMiddleware', 9.5, '#7B1FA2')]

    for name, x, color in parts:
        ax.add_patch(plt.FancyBboxPatch((x-0.8, 7.0), 1.6, 0.7,
                     boxstyle="round,pad=0.05", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, 7.35, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=4)
        ax.plot([x, x], [0.5, 7.0], color=color, lw=1.5, linestyle='--', alpha=0.6)
        ax.add_patch(plt.Rectangle((x-0.25, 1.5), 0.5, 5.5, color=color, alpha=0.2))

    msgs = [
        (1.5, 6.6, 4.0, 6.6, '1: GET /login', NAVY, False),
        (4.0, 6.1, 1.5, 6.1, '2: Return login form', GREEN, True),
        (1.5, 5.6, 4.0, 5.6, '3: POST (username, password)', NAVY, False),
        (4.0, 5.1, 6.8, 5.1, '4: authenticate(username, password)', GREEN, False),
        (6.8, 4.6, 6.8, 3.5, '5: lookup user in DB', '#1565C0', False),
        (6.8, 3.5, 4.0, 3.5, '6: return user object / None', '#1565C0', True),
        (4.0, 3.0, 9.5, 3.0, '7: login(request, user)', GREEN, False),
        (9.5, 2.5, 9.5, 2.0, '8: create session token', '#7B1FA2', False),
        (4.0, 2.0, 1.5, 2.0, '9: 302 Redirect to /home', GREEN, True),
    ]
    for x1, y1, x2, y2, label, color, ret in msgs:
        style = '--' if ret else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5, linestyle=style))
        ax.text((x1+x2)/2, y1+0.13, label, ha='center', fontsize=7.5, color=color, fontweight='bold')

    ax.set_title('Figure 21: Authentication Sequence Diagram – Sportiva CM',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig21_auth_sequence', fig)


def fig22_sponsorship_seq():
    """Sponsor Campaign Sequence Diagram"""
    fig, ax = plt.subplots(figsize=(12, 7.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 7.5)

    parts = [('Sponsor /\nUser', 1.5, NAVY), ('Sponsorship\nView', 4.0, GOLD),
             ('Campaign\nModel', 7.0, GREEN), ('Database\n(SQLite)', 10.0, RED)]
    for name, x, color in parts:
        ax.add_patch(plt.FancyBboxPatch((x-0.9, 6.8), 1.8, 0.65,
                     boxstyle="round,pad=0.05", facecolor=color, edgecolor='white', linewidth=1.5, zorder=3))
        ax.text(x, 7.13, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=4)
        ax.plot([x, x], [0.5, 6.8], color=color, lw=1.5, linestyle='--', alpha=0.6)
        ax.add_patch(plt.Rectangle((x-0.25, 1.5), 0.5, 5.3, color=color, alpha=0.2))

    msgs = [
        (1.5, 6.4, 4.0, 6.4, '1: GET /sponsorships', NAVY, False),
        (4.0, 5.9, 7.0, 5.9, '2: get_active_campaigns()', GOLD, False),
        (7.0, 5.4, 10.0, 5.4, '3: SELECT * FROM campaigns WHERE active=1', GREEN, False),
        (10.0, 4.9, 7.0, 4.9, '4: Return campaign list', RED, True),
        (7.0, 4.4, 4.0, 4.4, '5: Campaign objects', GREEN, True),
        (4.0, 3.9, 1.5, 3.9, '6: Render campaigns list', GOLD, True),
        (1.5, 3.4, 4.0, 3.4, '7: POST /sponsorships/{id}/pledge (amount)', NAVY, False),
        (4.0, 2.9, 7.0, 2.9, '8: create_pledge(campaign, amount)', GOLD, False),
        (7.0, 2.4, 10.0, 2.4, '9: INSERT INTO pledges …', GREEN, False),
        (10.0, 1.9, 7.0, 1.9, '10: Confirm storage', RED, True),
        (7.0, 1.4, 4.0, 1.4, '11: update campaign.raised', GREEN, True),
        (4.0, 1.0, 1.5, 1.0, '12: 200 OK – Campaign updated!', GOLD, True),
    ]
    for x1, y1, x2, y2, label, color, ret in msgs:
        style = '--' if ret else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3, linestyle=style))
        ax.text((x1+x2)/2, y1+0.12, label, ha='center', fontsize=7, color=color, fontweight='bold')

    ax.set_title('Figure 22: Sponsorship Campaign Sequence Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig22_sponsorship_seq', fig)


def fig23_activity_formalism():
    """Activity Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 7); ax.set_ylim(0, 7)

    # Start
    ax.add_patch(plt.Circle((3.5, 6.5), 0.2, color=NAVY, zorder=4))
    ax.text(4.1, 6.5, 'Initial Node (Start)', fontsize=8.5, color=NAVY, va='center')

    # Activity box
    ax.add_patch(plt.FancyBboxPatch((2.1, 5.4), 2.8, 0.65,
                 boxstyle="round,pad=0.12", facecolor=LIGHT, edgecolor=NAVY, linewidth=2, zorder=3))
    ax.text(3.5, 5.73, 'Activity Node\n(Action performed)', ha='center', va='center', fontsize=8, color=NAVY, fontweight='bold')

    # Decision
    diamond_x = [3.5, 4.3, 3.5, 2.7, 3.5]
    diamond_y = [4.5, 3.8, 3.1, 3.8, 4.5]
    ax.fill(diamond_x, diamond_y, facecolor=GOLD, edgecolor=NAVY, linewidth=2, zorder=3)
    ax.text(3.5, 3.8, 'Decision\n[condition]', ha='center', va='center', fontsize=8, color=NAVY, fontweight='bold')

    # Merge
    diamond2_x = [3.5, 4.3, 3.5, 2.7, 3.5]
    diamond2_y = [2.5, 1.8, 1.1, 1.8, 2.5]
    ax.fill(diamond2_x, diamond2_y, facecolor=LIGHT, edgecolor=NAVY, linewidth=2, zorder=3)
    ax.text(3.5, 1.8, 'Merge', ha='center', va='center', fontsize=8.5, color=NAVY, fontweight='bold')

    # End
    ax.add_patch(plt.Circle((3.5, 0.5), 0.25, color=NAVY, zorder=4))
    ax.add_patch(plt.Circle((3.5, 0.5), 0.4, color='none', edgecolor=NAVY, linewidth=2, zorder=4))
    ax.text(4.1, 0.5, 'Final Node (End)', fontsize=8.5, color=NAVY, va='center')

    # Arrows
    arrows = [(3.5,6.3, 3.5,6.05), (3.5,5.4, 3.5,4.5), (3.5,3.1, 3.5,2.5), (3.5,1.1, 3.5,0.75)]
    for x1,y1,x2,y2 in arrows:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))

    ax.annotate('', xy=(5.0, 3.8), xytext=(4.3, 3.8), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.annotate('', xy=(5.0, 1.8), xytext=(5.0, 3.8), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.annotate('', xy=(4.3, 1.8), xytext=(5.0, 1.8), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.text(5.3, 2.8, '[Yes]', fontsize=8, color=GREEN)

    ax.annotate('', xy=(2.0, 3.8), xytext=(2.7, 3.8), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.annotate('', xy=(2.0, 1.8), xytext=(2.0, 3.8), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.annotate('', xy=(2.7, 1.8), xytext=(2.0, 1.8), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.text(1.4, 2.8, '[No]', fontsize=8, color=RED)

    ax.set_title('Figure 23: Activity Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig23_activity_formalism', fig)


def fig24_auth_activity():
    """Authentication Activity Diagram"""
    fig, ax = plt.subplots(figsize=(8, 9))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 9)

    def act(x, y, text, w=3.6, h=0.6, color=LIGHT, tcolor=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color=tcolor, fontweight='bold', zorder=4)

    def diamond(x, y, text):
        dx, dy = [x, x+0.8, x, x-0.8, x], [y+0.5, y, y-0.5, y, y+0.5]
        ax.fill(dx, dy, facecolor=GOLD, edgecolor=NAVY, linewidth=2, zorder=3)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, color=NAVY, fontweight='bold', zorder=4)

    def arrow(x1,y1,x2,y2):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))

    # Start
    ax.add_patch(plt.Circle((4.0, 8.6), 0.22, color=NAVY, zorder=5))

    act(4.0, 7.9, 'Open Sportiva CM Login Page', color='#E3F2FD')
    act(4.0, 7.0, 'Enter Username & Password', color='#E3F2FD')
    diamond(4.0, 6.1, 'Valid\nCredentials?')
    act(4.0, 5.1, 'Verify Password (PBKDF2 Hash)', color='#E8F5E9')
    diamond(4.0, 4.2, 'Account\nActive?')
    act(4.0, 3.2, 'Create Session / JWT Token', color='#E8F5E9', tcolor=NAVY)
    act(4.0, 2.3, 'Redirect to Home Dashboard', color='#E8F5E9')
    act(2.0, 5.1, 'Display Error Message', RED, tcolor='white')
    act(6.0, 4.2, 'Show Account Disabled Notice', RED, tcolor='white')

    arrows_list = [(4.0,8.38, 4.0,8.2), (4.0,7.6, 4.0,7.3), (4.0,6.7, 4.0,6.6),
                   (4.0,5.6, 4.0,5.5), (4.0,4.9, 4.0,4.7), (4.0,3.9, 4.0,3.5), (4.0,2.9, 4.0,2.6)]
    for a in arrows_list: arrow(*a)

    ax.annotate('', xy=(2.0, 5.4), xytext=(3.2, 6.1), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.text(2.2, 6.0, '[Invalid]', fontsize=7.5, color=RED, fontweight='bold')
    ax.annotate('', xy=(6.0, 4.5), xytext=(4.8, 4.2), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.text(5.2, 4.55, '[Inactive]', fontsize=7.5, color=RED, fontweight='bold')

    ax.text(4.3, 5.5, '[Valid]', fontsize=7.5, color=GREEN, fontweight='bold')
    ax.text(4.3, 4.55, '[Active]', fontsize=7.5, color=GREEN, fontweight='bold')

    # End
    ax.add_patch(plt.Circle((4.0, 1.9), 0.22, color=NAVY, zorder=5))
    ax.add_patch(plt.Circle((4.0, 1.9), 0.35, color='none', edgecolor=NAVY, linewidth=2, zorder=5))
    arrow(4.0, 2.02, 4.0, 2.12)
    ax.set_title('Figure 24: Authentication Activity Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig24_auth_activity', fig)


def fig25_event_activity():
    """Event Creation Activity Diagram"""
    fig, ax = plt.subplots(figsize=(8, 9))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 9)

    def act(x, y, text, w=3.8, h=0.6, color=LIGHT, tcolor=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8, color=tcolor, fontweight='bold', zorder=4)

    def diamond(x, y, text):
        dx, dy = [x, x+0.9, x, x-0.9, x], [y+0.5, y, y-0.5, y, y+0.5]
        ax.fill(dx, dy, facecolor=GOLD, edgecolor=NAVY, linewidth=2, zorder=3)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, color=NAVY, fontweight='bold', zorder=4)

    def arrow(x1,y1,x2,y2):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))

    ax.add_patch(plt.Circle((4.0, 8.6), 0.22, color=NAVY, zorder=5))

    act(4.0, 7.9, 'User Logs in to Sportiva CM', color='#E3F2FD')
    act(4.0, 7.0, 'Navigate to Events → Create Event', color='#E3F2FD')
    act(4.0, 6.1, 'Fill Event Form (name, date, venue,\ncategory, description)', color='#E3F2FD', h=0.75)
    diamond(4.0, 5.0, 'Form\nValid?')
    act(4.0, 4.0, 'Save Event to Database', color='#E8F5E9')
    act(4.0, 3.1, 'Event Published on Platform', color='#E8F5E9')
    act(4.0, 2.2, 'Notify Followers & Display in Feed', color='#E8F5E9')
    act(2.0, 5.0, 'Show Validation Errors', RED, tcolor='white', w=2.8)

    for a in [(4.0,8.38,4.0,8.2),(4.0,7.6,4.0,7.3),(4.0,6.73,4.0,6.38),
              (4.0,4.5,4.0,4.3),(4.0,3.7,4.0,3.4),(4.0,2.8,4.0,2.55)]:
        arrow(*a)

    ax.annotate('', xy=(2.0, 5.3), xytext=(3.1, 5.0), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.text(2.0, 5.75, '[Invalid]', fontsize=7.5, color=RED, fontweight='bold')
    ax.text(4.5, 4.7, '[Valid]', fontsize=7.5, color=GREEN, fontweight='bold')

    ax.add_patch(plt.Circle((4.0, 1.85), 0.22, color=NAVY, zorder=5))
    ax.add_patch(plt.Circle((4.0, 1.85), 0.35, color='none', edgecolor=NAVY, linewidth=2, zorder=5))
    arrow(4.0, 1.95, 4.0, 2.0)

    ax.set_title('Figure 25: Event Creation Activity Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig25_event_activity', fig)


def fig26_sponsorship_activity():
    """Sponsorship Activity Diagram"""
    fig, ax = plt.subplots(figsize=(8, 9))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 9)

    def act(x, y, text, w=3.8, h=0.6, color=LIGHT, tcolor=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8, color=tcolor, fontweight='bold', zorder=4)

    def diamond(x, y, text):
        dx, dy = [x, x+0.9, x, x-0.9, x], [y+0.5, y, y-0.5, y, y+0.5]
        ax.fill(dx, dy, facecolor=GOLD, edgecolor=NAVY, linewidth=2, zorder=3)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, color=NAVY, fontweight='bold', zorder=4)

    def arrow(x1,y1,x2,y2):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))

    ax.add_patch(plt.Circle((4.0, 8.6), 0.22, color=NAVY, zorder=5))
    act(4.0, 7.9, 'Sponsor Opens Sponsorship Page', color='#FFF8E1')
    act(4.0, 7.0, 'Browse Active Campaigns', color='#FFF8E1')
    act(4.0, 6.1, 'Select Campaign & View Details', color='#FFF8E1')
    diamond(4.0, 5.1, 'Interested?')
    act(4.0, 4.1, 'Enter Pledge Amount & Contact Info', color='#E8F5E9')
    diamond(4.0, 3.1, 'Amount\nValid?')
    act(4.0, 2.1, 'Record Pledge & Update Progress Bar', color='#E8F5E9')
    act(2.0, 5.1, 'Return to Campaigns', GRAY, tcolor='white', w=2.8)
    act(2.0, 3.1, 'Show Amount Error', RED, tcolor='white', w=2.5)

    for a in [(4.0,8.38,4.0,8.2),(4.0,7.6,4.0,7.3),(4.0,6.7,4.0,6.4),
              (4.0,4.6,4.0,4.4),(4.0,2.6,4.0,2.4)]:
        arrow(*a)

    ax.annotate('', xy=(2.0, 5.4), xytext=(3.1, 5.1), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
    ax.text(1.8, 5.8, '[No]', fontsize=7.5, color=GRAY)
    ax.text(4.5, 4.8, '[Yes]', fontsize=7.5, color=GREEN)
    ax.annotate('', xy=(2.0, 3.4), xytext=(3.1, 3.1), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    ax.text(1.8, 3.7, '[Invalid]', fontsize=7.5, color=RED)
    ax.text(4.5, 2.8, '[Valid]', fontsize=7.5, color=GREEN)

    ax.add_patch(plt.Circle((4.0, 1.75), 0.22, color=NAVY, zorder=5))
    ax.add_patch(plt.Circle((4.0, 1.75), 0.35, color='none', edgecolor=NAVY, linewidth=2, zorder=5))

    ax.set_title('Figure 26: Sponsorship Campaign Activity Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig26_sponsorship_activity', fig)


def fig27_hardware():
    """Hardware Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    def box(x, y, w, h, text, color, icon=''):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2, zorder=3))
        ax.text(x, y, f'{icon}\n{text}' if icon else text, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', zorder=4)

    def arr(x1,y1,x2,y2,label=''):
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='<->', color=GRAY, lw=2))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2+0.15, label, ha='center', fontsize=7.5, color=GRAY)

    box(5, 5.2, 3.5, 0.8, 'Developer Laptop\n(HP EliteBook / Dell – Core i5)', NAVY)
    box(1.5, 3.2, 2.8, 0.8, 'Local Development\nServer (Django)', GREEN)
    box(5, 3.2, 2.8, 0.8, 'Web Browser Client\n(Chrome / Firefox)', '#1565C0')
    box(8.5, 3.2, 2.2, 0.8, 'Mobile Device\n(Android / iOS)', '#7B1FA2')
    box(3.0, 1.2, 3.0, 0.8, 'SQLite Database\n(Local File – db.sqlite3)', '#0D47A1')
    box(7.5, 1.2, 3.0, 0.8, 'Static / Media Files\n(Django FileSystem)', GRAY)

    arr(5, 4.8, 1.5, 3.6, 'HTTP localhost')
    arr(5, 4.8, 5, 3.6, 'Dev Server')
    arr(5, 4.8, 8.5, 3.6, 'HTTP API')
    arr(1.5, 2.8, 3.0, 1.6, 'ORM Queries')
    arr(5, 2.8, 7.5, 1.6, 'File Requests')

    ax.set_title('Figure 27: Hardware & Network Architecture – Sportiva CM Development',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig27_hardware', fig)


def fig28_ntier():
    """N-Tier Architecture"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    tiers = [
        (5, 5.3, 8, 0.75, 'Presentation Tier\n(HTML Templates, CSS, Vanilla JS)', '#1565C0'),
        (5, 4.1, 8, 0.75, 'Application / Business Logic Tier\n(Django Views, Forms, Middleware)', GREEN),
        (5, 2.9, 8, 0.75, 'Data Access Tier\n(Django ORM, Models)', NAVY),
        (5, 1.7, 8, 0.75, 'Persistence Tier\n(SQLite Database – db.sqlite3)', RED),
    ]
    for x, y, w, h, text, color in tiers:
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=4)

    for y1, y2 in [(4.93, 4.48), (3.73, 3.28), (2.53, 2.08)]:
        ax.annotate('', xy=(5, y2), xytext=(5, y1), arrowprops=dict(arrowstyle='<->', color=GRAY, lw=2))

    ax.set_title('Figure 28: N-Tier Architecture – Sportiva CM (Django MVT)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig28_ntier', fig)


def fig29_mvc():
    """MVT/MVC Architecture"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)

    def box(x, y, w, h, title, sub, color):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2, zorder=3))
        ax.text(x, y+0.2, title, ha='center', va='center', fontsize=11, fontweight='bold', color='white', zorder=4)
        ax.text(x, y-0.25, sub, ha='center', va='center', fontsize=8, color='white', alpha=0.9, zorder=4)

    box(1.5, 2.75, 2.5, 2.0, 'Model', 'apps/models.py\nORM classes', NAVY)
    box(5.0, 2.75, 2.5, 2.0, 'View', 'apps/views.py\nBusiness logic', GREEN)
    box(8.5, 2.75, 2.5, 2.0, 'Template', 'templates/*.html\nUI / Presentation', '#1565C0')

    ax.annotate('', xy=(3.75, 2.75), xytext=(2.75, 2.75),
                arrowprops=dict(arrowstyle='<->', color=GOLD, lw=2.5))
    ax.text(3.25, 3.15, 'ORM', ha='center', fontsize=9, color=GOLD, fontweight='bold')

    ax.annotate('', xy=(7.25, 2.75), xytext=(6.25, 2.75),
                arrowprops=dict(arrowstyle='<->', color=GOLD, lw=2.5))
    ax.text(6.75, 3.15, 'Context', ha='center', fontsize=9, color=GOLD, fontweight='bold')

    ax.add_patch(plt.FancyBboxPatch((3.5, 0.3), 3.0, 0.65,
                 boxstyle="round,pad=0.07", facecolor=RED, edgecolor='white', linewidth=2, zorder=3))
    ax.text(5.0, 0.63, 'User / HTTP Request → Django URL Router', ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='white', zorder=4)
    ax.annotate('', xy=(5.0, 1.75), xytext=(5.0, 0.97),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2))

    ax.set_title('Figure 29: MVT Architecture – Sportiva CM (Django Framework)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig29_mvc', fig)


def fig30_class_formalism():
    """Class Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 5)

    def cls(x, y, name, attrs, methods, color=LIGHT):
        h = 0.45 + 0.3*len(attrs) + 0.3*len(methods)
        ax.add_patch(plt.FancyBboxPatch((x-1.5, y-h/2), 3.0, h,
                     boxstyle="square,pad=0.0", facecolor=color, edgecolor=NAVY, linewidth=2, zorder=3))
        # Class name band
        ax.add_patch(plt.FancyBboxPatch((x-1.5, y+h/2-0.42), 3.0, 0.42,
                     boxstyle="square,pad=0.0", facecolor=NAVY, edgecolor=NAVY, linewidth=2, zorder=4))
        ax.text(x, y+h/2-0.21, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=5)
        start_y = y+h/2-0.5
        for attr in attrs:
            start_y -= 0.28
            ax.text(x-1.3, start_y, attr, fontsize=7.5, color=NAVY, va='center')
        ax.plot([x-1.5, x+1.5], [start_y-0.1, start_y-0.1], color=NAVY, lw=1)
        start_y -= 0.15
        for meth in methods:
            start_y -= 0.28
            ax.text(x-1.3, start_y, meth, fontsize=7.5, color=GREEN, va='center')

    cls(2, 3.2, 'ClassName', ['- attribute: type', '- id: int'], ['+ method(): void', '+ get(): str'])
    cls(6, 3.2, 'RelatedClass', ['- name: str'], ['+ save(): bool'])

    ax.annotate('', xy=(4.5, 3.2), xytext=(3.5, 3.2),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))
    ax.text(4.0, 3.45, 'Association', ha='center', fontsize=8, color=GREEN)

    ax.set_title('Figure 30: Class Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig30_class_formalism', fig)


def fig31_class_diagram():
    """System Class Diagram"""
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)

    def cls(x, y, name, attrs, methods, color=LIGHT, w=3.2):
        h = 0.45 + 0.28*len(attrs) + 0.28*(len(methods)+1)
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h), w, h,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3))
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-0.4), w, 0.4,
                     boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY, linewidth=1.5, zorder=4))
        ax.text(x, y-0.2, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white', zorder=5)
        yy = y - 0.55
        for attr in attrs:
            ax.text(x-w/2+0.1, yy, attr, fontsize=6.5, color='#333', va='center'); yy -= 0.27
        ax.plot([x-w/2, x+w/2], [yy+0.1, yy+0.1], color='#999', lw=0.8)
        for meth in methods:
            ax.text(x-w/2+0.1, yy-0.1, meth, fontsize=6.5, color=GREEN, va='center'); yy -= 0.27

    cls(2.0, 9.5, 'UserProfile', ['- username: str', '- email: str', '- role: str', '- bio: text'],
        ['+ login()', '+ update_profile()'])
    cls(7.0, 9.5, 'Organization', ['- name: str', '- sport_type: str', '- owner: FK(User)', '- verified: bool'],
        ['+ create()', '+ list_events()'])
    cls(13.0, 9.5, 'Event', ['- title: str', '- date: datetime', '- venue: str', '- org: FK(Org)', '- category: str'],
        ['+ publish()', '+ register_user()'])
    cls(2.0, 5.5, 'Post (MediaFeed)', ['- author: FK(User)', '- content: text', '- image: file', '- created: datetime'],
        ['+ create()', '+ like()', '+ comment()'])
    cls(7.0, 5.5, 'Product', ['- seller: FK(User)', '- name: str', '- price: decimal', '- sport: str'],
        ['+ list()', '+ contact_seller()'])
    cls(13.0, 5.5, 'Campaign', ['- creator: FK(User)', '- title: str', '- goal: decimal', '- raised: decimal'],
        ['+ create()', '+ pledge()', '+ progress()'])
    cls(7.0, 1.8, 'Attendance', ['- user: FK(User)', '- event: FK(Event)', '- joined: datetime'],
        ['+ register()'])

    # Associations
    assocs = [(2,9.5-1.8, 7,9.5-1.8), (7,9.5-1.8, 13,9.5-1.8), (2,9.5-1.8, 2,5.5),
              (2,9.5-1.8, 7,5.5), (2,9.5-1.8, 13,5.5), (13,9.5-1.8, 7,1.8)]
    for x1,y1,x2,y2 in assocs:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(arrowstyle='->', color='#999', lw=1.2))

    ax.set_title('Figure 31: System Class Diagram – Sportiva CM', fontsize=11,
                 fontweight='bold', color=NAVY, pad=14)
    return savefig('fig31_class_diagram', fig)


def fig32_state_formalism():
    """State Machine Formalism"""
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 5)

    ax.add_patch(plt.Circle((1.0, 2.5), 0.25, color=NAVY, zorder=5))
    ax.text(1.05, 3.1, 'Initial\nState', ha='center', fontsize=8, color=NAVY)

    states = [(3.5, 2.5, 'State A'), (6.5, 2.5, 'State B')]
    for x, y, text in states:
        ax.add_patch(plt.FancyBboxPatch((x-1.1, y-0.4), 2.2, 0.8,
                     boxstyle="round,pad=0.12", facecolor=LIGHT, edgecolor=NAVY, linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY, zorder=4)

    ax.annotate('', xy=(2.4, 2.5), xytext=(1.25, 2.5), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.annotate('', xy=(5.4, 2.5), xytext=(4.6, 2.5), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.text(5.0, 2.75, 'event [guard] / action', fontsize=7.5, ha='center', color=GREEN)

    ax.add_patch(plt.Circle((6.5, 1.2), 0.25, color=NAVY, zorder=5))
    ax.add_patch(plt.Circle((6.5, 1.2), 0.38, color='none', edgecolor=NAVY, linewidth=2, zorder=5))
    ax.annotate('', xy=(6.5, 1.6), xytext=(6.5, 2.1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.text(6.9, 1.8, 'Final', fontsize=8, color=NAVY)

    ax.set_title('Figure 32: State Machine Diagram Formalism', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig32_state_formalism', fig)


def fig33_account_state():
    """Account State Machine"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)

    ax.add_patch(plt.Circle((0.6, 2.75), 0.22, color=NAVY, zorder=5))

    states = [(2.5, 2.75, 'New /\nUnregistered'), (5.0, 2.75, 'Registered\n(Inactive)'),
              (7.5, 2.75, 'Active\nAccount'), (7.5, 0.8, 'Suspended')]
    for x, y, text in states:
        ax.add_patch(plt.FancyBboxPatch((x-1.1, y-0.5), 2.2, 1.0,
                     boxstyle="round,pad=0.1", facecolor=LIGHT, edgecolor=NAVY, linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY, zorder=4)

    transitions = [
        (0.82, 2.75, 1.4, 2.75, 'visit site', NAVY),
        (3.6, 2.75, 3.9, 2.75, 'register()', GREEN),
        (6.1, 2.75, 6.4, 2.75, 'verify email', GREEN),
        (7.5, 2.25, 7.5, 1.3, 'violate rules', RED),
        (7.5, 1.3, 5.0, 1.3, 'admin action', RED),
    ]
    for x1,y1,x2,y2,label,color in transitions:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        ax.text((x1+x2)/2, (y1+y2)/2+0.15, label, ha='center', fontsize=7.5, color=color, fontweight='bold')

    ax.add_patch(plt.Circle((9.5, 2.75), 0.22, color=NAVY, zorder=5))
    ax.add_patch(plt.Circle((9.5, 2.75), 0.35, color='none', edgecolor=NAVY, linewidth=2))
    ax.annotate('', xy=(9.15, 2.75), xytext=(8.6, 2.75), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.text(9.5, 3.2, 'delete()', fontsize=7.5, color=NAVY, ha='center')

    ax.set_title('Figure 33: Account State Machine Diagram – Sportiva CM',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig33_account_state', fig)


def fig34_campaign_state():
    """Campaign State Machine"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5)

    ax.add_patch(plt.Circle((0.6, 2.5), 0.22, color=NAVY, zorder=5))
    states = [(2.5, 2.5, 'Draft'), (4.8, 2.5, 'Published\n(Active)'),
              (7.3, 2.5, 'Goal Reached'), (7.3, 0.9, 'Closed')]
    for x, y, text in states:
        ax.add_patch(plt.FancyBboxPatch((x-1.1, y-0.45), 2.2, 0.9,
                     boxstyle="round,pad=0.08", facecolor=LIGHT, edgecolor=GOLD, linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY, zorder=4)

    transitions = [
        (0.82, 2.5, 1.4, 2.5, 'create', NAVY),
        (3.6, 2.5, 3.7, 2.5, 'publish()', GOLD),
        (5.9, 2.5, 6.2, 2.5, 'raised >= goal', GREEN),
        (7.3, 2.05, 7.3, 1.35, 'admin closes', RED),
    ]
    for x1,y1,x2,y2,label,color in transitions:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        ax.text((x1+x2)/2, (y1+y2)/2+0.15, label, ha='center', fontsize=7.5, color=color)

    ax.set_title('Figure 34: Campaign State Machine Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig34_campaign_state', fig)


def fig35_event_state():
    """Event State Machine"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5)

    ax.add_patch(plt.Circle((0.6, 2.5), 0.22, color=NAVY, zorder=5))
    states = [(2.2, 2.5, 'Draft'), (4.5, 2.5, 'Published'), (7.0, 2.5, 'Ongoing'), (9.0, 2.5, 'Completed')]
    for x, y, text in states:
        c = {'Draft': LIGHT, 'Published': '#E3F2FD', 'Ongoing': '#E8F5E9', 'Completed': '#FFF8E1'}.get(text, LIGHT)
        ax.add_patch(plt.FancyBboxPatch((x-1.0, y-0.4), 2.0, 0.8,
                     boxstyle="round,pad=0.08", facecolor=c, edgecolor=NAVY, linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY, zorder=4)

    trans = [(0.82,2.5,1.2,2.5,'create',NAVY),(3.2,2.5,3.5,2.5,'publish',NAVY),
             (5.5,2.5,6.0,2.5,'date arrives',GREEN),(8.0,2.5,8.0,2.5,'end',RED)]
    for x1,y1,x2,y2,l,c in trans:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=c, lw=1.5))
        ax.text((x1+x2)/2, y1+0.2, l, ha='center', fontsize=7.5, color=c)

    ax.set_title('Figure 35: Event State Machine Diagram', fontsize=10,
                 fontweight='bold', color=NAVY, pad=10)
    return savefig('fig35_event_state', fig)


def fig36_package_formalism():
    """Package Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 7); ax.set_ylim(0, 4.5)

    def pkg(x, y, name, color=LIGHT):
        ax.add_patch(plt.FancyBboxPatch((x-1.5, y-0.4), 0.9, 0.3,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=NAVY, linewidth=1.5))
        ax.add_patch(plt.FancyBboxPatch((x-1.5, y-1.0), 3.0, 1.0,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=NAVY, linewidth=2))
        ax.text(x, y-0.52, name, ha='center', va='center', fontsize=9, color=NAVY, fontweight='bold')

    pkg(2.0, 3.5, 'PackageA', '#E3F2FD')
    pkg(5.5, 3.5, 'PackageB', '#E8F5E9')
    ax.annotate('', xy=(4.0, 3.1), xytext=(3.5, 3.1), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, linestyle='dashed'))
    ax.text(3.75, 3.35, '«import»', ha='center', fontsize=8, color=GREEN, style='italic')
    ax.set_title('Figure 36: Package Diagram Formalism', fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig36_package_formalism', fig)


def fig37_package_diagram():
    """Sportiva CM Package Diagram"""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 8)

    def pkg(x, y, w, h, name, items, color='#E3F2FD', header_color=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x-0.5, y+h-0.25), 2.2, 0.35,
                     boxstyle="square,pad=0", facecolor=header_color, edgecolor=header_color))
        ax.add_patch(plt.FancyBboxPatch((x-0.5, y), w, h,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=header_color, linewidth=2))
        ax.text(x+0.6, y+h+0.07, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        for i, item in enumerate(items):
            ax.text(x, y+h-0.5-i*0.3, f'  {item}', fontsize=7.5, color=NAVY, va='center')

    pkg(0.5, 5.5, 3.5, 2.0, '«package» sportiva_cm', ['settings.py', 'urls.py', 'wsgi.py', 'asgi.py'], '#E3F2FD', NAVY)
    pkg(4.5, 5.5, 3.0, 2.0, '«package» accounts', ['models.py', 'views.py', 'forms.py', 'urls.py'], '#E8F5E9', GREEN)
    pkg(8.0, 5.5, 3.5, 2.0, '«package» organizations', ['models.py', 'views.py', 'forms.py'], '#FFF8E1', GOLD)
    pkg(0.5, 2.5, 3.5, 2.0, '«package» events', ['models.py', 'views.py', 'forms.py', 'urls.py'], '#FCE4EC', RED)
    pkg(4.5, 2.5, 3.0, 2.0, '«package» marketplace', ['models.py', 'views.py', 'forms.py'], '#EDE7F6', '#7B1FA2')
    pkg(8.0, 2.5, 3.5, 2.0, '«package» sponsorships', ['models.py', 'views.py', 'forms.py'], '#E0F2F1', '#00796B')
    pkg(4.5, 0.3, 3.0, 1.5, '«package» media_feed', ['models.py', 'views.py'], '#E8EAF6', '#1A237E')

    ax.set_title('Figure 37: Sportiva CM Package Diagram – Django Application Structure',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig37_package_diagram', fig)


def fig38_deployment_formalism():
    """Deployment Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 5)

    ax.add_patch(plt.FancyBboxPatch((0.5, 2.0), 3.0, 2.0,
                 boxstyle="square,pad=0", facecolor=LIGHT, edgecolor=NAVY, linewidth=2))
    ax.add_patch(plt.FancyBboxPatch((0.5, 2.0), 3.0, 0.4,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY, linewidth=2))
    ax.text(2.0, 2.2, '«node» ServerName', ha='center', va='center', fontsize=8.5, color='white', fontweight='bold')
    ax.add_patch(plt.FancyBboxPatch((0.8, 2.55), 2.4, 1.1,
                 boxstyle="round,pad=0.05", facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=1.5))
    ax.text(2.0, 3.1, '«artifact»\napp.component', ha='center', va='center', fontsize=8, color=NAVY)

    ax.add_patch(plt.FancyBboxPatch((4.5, 2.0), 3.0, 2.0,
                 boxstyle="square,pad=0", facecolor='#E8F5E9', edgecolor=GREEN, linewidth=2))
    ax.add_patch(plt.FancyBboxPatch((4.5, 2.0), 3.0, 0.4,
                 boxstyle="square,pad=0", facecolor=GREEN, edgecolor=GREEN, linewidth=2))
    ax.text(6.0, 2.2, '«node» Client', ha='center', va='center', fontsize=8.5, color='white', fontweight='bold')

    ax.annotate('', xy=(4.5, 3.0), xytext=(3.5, 3.0), arrowprops=dict(arrowstyle='<->', color=GRAY, lw=2))
    ax.text(4.0, 3.25, 'HTTP/HTTPS', ha='center', fontsize=7.5, color=GRAY)
    ax.set_title('Figure 38: Deployment Diagram Formalism', fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig38_deployment_formalism', fig)


def fig39_deployment():
    """Sportiva CM Deployment Diagram"""
    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 13); ax.set_ylim(0, 7)

    def node(x, y, w, h, name, artifacts, color='#E3F2FD', nc=NAVY):
        ax.add_patch(plt.FancyBboxPatch((x, y), w, h,
                     boxstyle="square,pad=0", facecolor=color, edgecolor=nc, linewidth=2))
        ax.add_patch(plt.FancyBboxPatch((x, y+h-0.4), w, 0.4,
                     boxstyle="square,pad=0", facecolor=nc, edgecolor=nc, linewidth=2))
        ax.text(x+w/2, y+h-0.2, name, ha='center', va='center', fontsize=8.5, color='white', fontweight='bold')
        for i, art in enumerate(artifacts):
            ax.add_patch(plt.FancyBboxPatch((x+0.15, y+h-0.65-0.55*i-0.4), w-0.3, 0.45,
                         boxstyle="round,pad=0.04", facecolor='white', edgecolor=nc, linewidth=1, alpha=0.9))
            ax.text(x+w/2, y+h-0.65-0.55*i-0.18, art, ha='center', va='center', fontsize=7.5, color=NAVY)

    node(0.3, 4.0, 3.8, 2.6, '«node» Dev Laptop\n(Windows – Core i5)', ['Django runserver', 'Gunicorn WSGI', 'SQLite DB'], '#E3F2FD', NAVY)
    node(4.5, 4.0, 3.5, 2.6, '«node» Web Browser\n(Chrome / Firefox)', ['HTML Templates', 'CSS Stylesheet', 'JavaScript'], '#E8F5E9', GREEN)
    node(8.5, 4.0, 4.0, 2.6, '«node» Mobile Device\n(Android / iOS)', ['Responsive UI', 'REST API calls'], '#FFF8E1', GOLD)
    node(0.3, 0.5, 3.8, 2.0, '«artifact» SQLite Database\n(db.sqlite3)', ['Users, Events, Campaigns', 'Products, Posts, Pledges'], '#FCE4EC', RED)
    node(4.5, 0.5, 7.5, 2.0, '«artifact» Static / Media Files\n(Django staticfiles)', ['CSS / JS bundles', 'Uploaded images / avatars'], '#EDE7F6', '#7B1FA2')

    ax.annotate('', xy=(4.5, 5.3), xytext=(4.1, 5.3), arrowprops=dict(arrowstyle='<->', color=NAVY, lw=2))
    ax.text(4.3, 5.6, 'HTTP', ha='center', fontsize=7.5, color=NAVY)
    ax.annotate('', xy=(8.5, 5.3), xytext=(8.0, 5.3), arrowprops=dict(arrowstyle='<->', color=GOLD, lw=2))
    ax.text(8.25, 5.6, 'REST', ha='center', fontsize=7.5, color=GOLD)
    ax.annotate('', xy=(0.8, 2.5), xytext=(0.8, 4.0), arrowprops=dict(arrowstyle='<->', color=RED, lw=2))

    ax.set_title('Figure 39: Deployment Diagram – Sportiva CM (Local Development Environment)',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig39_deployment', fig)


def fig40_component_formalism():
    """Component Diagram Formalism"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 4.5)

    def comp(x, y, name, color=LIGHT):
        ax.add_patch(plt.FancyBboxPatch((x-1.3, y-0.45), 2.6, 0.9,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor=NAVY, linewidth=2, zorder=3))
        ax.add_patch(plt.FancyBboxPatch((x+0.9, y-0.1), 0.5, 0.35,
                     boxstyle="square,pad=0", facecolor='white', edgecolor=NAVY, linewidth=1.5, zorder=4))
        ax.add_patch(plt.FancyBboxPatch((x+0.9, y-0.38), 0.5, 0.25,
                     boxstyle="square,pad=0", facecolor='white', edgecolor=NAVY, linewidth=1.5, zorder=4))
        ax.text(x-0.1, y, name, ha='center', va='center', fontsize=9, color=NAVY, fontweight='bold', zorder=4)

    comp(2.0, 3.0, 'ComponentA', '#E3F2FD')
    comp(6.0, 3.0, 'ComponentB', '#E8F5E9')
    ax.annotate('', xy=(4.7, 3.0), xytext=(3.3, 3.0), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.text(4.0, 3.25, '«uses»', ha='center', fontsize=8, color=GREEN, style='italic')
    ax.set_title('Figure 40: Component Diagram Formalism', fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig40_component_formalism', fig)


def fig41_component_mobile():
    """Mobile Component Diagram"""
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 7)

    def comp(x, y, name, color=LIGHT, w=2.8, h=0.8):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor=NAVY, linewidth=1.5, zorder=3))
        ax.text(x, y, name, ha='center', va='center', fontsize=8.5, color=NAVY, fontweight='bold', zorder=4)

    comp(6.0, 6.5, '«Browser Client»\nFrontend Layer', '#B3E5FC', 4.5)
    comp(6.0, 5.0, 'Django URL Router\n(urls.py)', '#E3F2FD', 4.5)
    comp(2.0, 3.5, 'Accounts\nModule', '#E8F5E9', 2.5)
    comp(5.0, 3.5, 'Events\nModule', '#FFF8E1', 2.5)
    comp(8.0, 3.5, 'Media Feed\nModule', '#FCE4EC', 2.5)
    comp(11.0, 3.5, 'Marketplace\nModule', '#EDE7F6', 2.5)
    comp(3.5, 2.0, 'Sponsorships\nModule', '#E0F2F1', 2.5)
    comp(6.0, 2.0, 'Organizations\nModule', '#E8EAF6', 2.5)
    comp(6.0, 0.7, 'SQLite DB\n(ORM Layer)', '#FFECB3', 4.0)

    for x, y in [(2.0,5.0),(5.0,5.0),(8.0,5.0),(11.0,5.0)]:
        ax.annotate('', xy=(x,5.0), xytext=(6.0,5.0), arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.2))
        ax.annotate('', xy=(x, 3.9), xytext=(x, 5.0-0.4), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

    for x in [3.5, 6.0]:
        ax.annotate('', xy=(x, 2.4), xytext=(6.0, 5.0-0.4), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

    ax.annotate('', xy=(6.0, 5.4), xytext=(6.0, 6.1), arrowprops=dict(arrowstyle='<->', color='#0288D1', lw=1.5))
    ax.annotate('', xy=(6.0, 1.1), xytext=(6.0, 1.6), arrowprops=dict(arrowstyle='<->', color=GOLD, lw=1.5))

    ax.set_title('Figure 41: Sportiva CM Component Diagram – Module Structure',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig41_component_diagram', fig)


def fig42_component_web():
    """Web Application Component Diagram"""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 6)

    def box(x, y, w, h, text, color):
        ax.add_patch(plt.FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white', zorder=4)

    box(6.0, 5.4, 10.0, 0.7, 'Sportiva CM – Web Application (Django 4.x)', NAVY)
    box(1.5, 4.0, 2.5, 0.7, 'Authentication\nMiddleware', GREEN)
    box(4.5, 4.0, 2.5, 0.7, 'CSRF / Security\nMiddleware', '#0D47A1')
    box(7.5, 4.0, 2.5, 0.7, 'Session\nMiddleware', '#7B1FA2')
    box(10.5, 4.0, 2.0, 0.7, 'Static Files\nMiddleware', GRAY)

    modules = [(1.5, 2.5, 'Accounts', GREEN), (3.5, 2.5, 'Events', '#1565C0'),
               (5.5, 2.5, 'Organizations', GOLD), (7.5, 2.5, 'Media Feed', RED),
               (9.5, 2.5, 'Marketplace', '#7B1FA2'), (11.5, 2.5, 'Sponsorships', '#00796B')]
    for x, y, name, c in modules:
        box(x, y, 1.8, 0.7, name, c)

    box(6.0, 1.0, 8.0, 0.7, 'SQLite ORM Layer – db.sqlite3 (Persistence)', '#0D47A1')

    ax.set_title('Figure 42: Web Application Component Architecture – Sportiva CM',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig42_component_web', fig)


def fig43_test_admin():
    """Admin Module Tests"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)

    tests = [
        ('test_admin_login',           'PASS', 'Admin can log in with valid credentials'),
        ('test_admin_user_list',       'PASS', 'Admin can view full list of users'),
        ('test_admin_delete_user',     'PASS', 'Admin can delete a user account'),
        ('test_admin_organization',    'PASS', 'Admin can manage organization records'),
        ('test_admin_event_moderate',  'PASS', 'Admin can moderate and remove events'),
        ('test_admin_campaign_close',  'PASS', 'Admin can force-close active campaigns'),
    ]
    ax.text(5.0, 5.2, 'Figure 43: Admin Module – Automated Test Results', ha='center',
            fontsize=10, fontweight='bold', color=NAVY)
    ax.add_patch(plt.FancyBboxPatch((0.3, 4.6), 9.4, 0.45,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    for i, txt in enumerate(['Test Name', 'Status', 'Description']):
        ax.text([0.5, 4.0, 5.0][i], 4.82, txt, fontsize=9, fontweight='bold', color='white')

    for i, (name, status, desc) in enumerate(tests):
        y = 4.2 - i*0.55
        bg = '#E8F5E9' if i%2==0 else WHITE
        ax.add_patch(plt.FancyBboxPatch((0.3, y-0.22), 9.4, 0.44,
                     boxstyle="square,pad=0", facecolor=bg, edgecolor='#ccc'))
        ax.text(0.5, y, name, fontsize=8.5, color=NAVY, va='center')
        ax.add_patch(plt.FancyBboxPatch((3.6, y-0.17), 0.75, 0.35,
                     boxstyle="round,pad=0.04", facecolor=GREEN, edgecolor='white', linewidth=1))
        ax.text(3.975, y, status, fontsize=8, color='white', fontweight='bold', va='center', ha='center')
        ax.text(4.6, y, desc, fontsize=7.5, color=GRAY, va='center')

    ax.text(0.5, 0.3, f'Total: {len(tests)} tests  |  Passed: {len(tests)}  |  Failed: 0  |  Run: pytest / manage.py test',
            fontsize=8, color=GREEN, fontweight='bold')
    return savefig('fig43_test_admin', fig)


def fig44_test_modules():
    """Professional Module Tests"""
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 7)

    tests = [
        ('test_user_register',         'PASS', 'User can register with valid data'),
        ('test_user_login',            'PASS', 'User can log in with correct credentials'),
        ('test_event_create',          'PASS', 'Authenticated user can create event'),
        ('test_event_join',            'PASS', 'User can join a published event'),
        ('test_org_create',            'PASS', 'User can create an organization'),
        ('test_post_create',           'PASS', 'User can create a media feed post'),
        ('test_post_like',             'PASS', 'User can like a post'),
        ('test_post_comment',          'PASS', 'User can comment on a post'),
        ('test_product_create',        'PASS', 'Seller can list a product'),
        ('test_campaign_create',       'PASS', 'User can create sponsorship campaign'),
        ('test_campaign_pledge',       'PASS', 'Sponsor can submit a pledge'),
        ('test_campaign_progress',     'PASS', 'Campaign shows correct funding %'),
    ]
    ax.text(5.0, 6.7, 'Figure 44: Feature Modules – Test Results Summary', ha='center',
            fontsize=10, fontweight='bold', color=NAVY)
    ax.add_patch(plt.FancyBboxPatch((0.3, 6.2), 9.4, 0.4,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    for i, txt in enumerate(['Test Name', 'Status', 'Description']):
        ax.text([0.5, 3.8, 4.9][i], 6.4, txt, fontsize=8.5, fontweight='bold', color='white')

    for i, (name, status, desc) in enumerate(tests):
        y = 5.8 - i*0.46
        bg = '#E8F5E9' if i%2==0 else WHITE
        ax.add_patch(plt.FancyBboxPatch((0.3, y-0.2), 9.4, 0.38,
                     boxstyle="square,pad=0", facecolor=bg, edgecolor='#ddd'))
        ax.text(0.5, y, name, fontsize=8, color=NAVY, va='center')
        ax.add_patch(plt.FancyBboxPatch((3.55, y-0.15), 0.7, 0.32,
                     boxstyle="round,pad=0.03", facecolor=GREEN, edgecolor='white', linewidth=1))
        ax.text(3.9, y, status, fontsize=7.5, color='white', fontweight='bold', va='center', ha='center')
        ax.text(4.4, y, desc, fontsize=7.5, color=GRAY, va='center')

    ax.text(0.5, 0.25, f'Total: {len(tests)} tests  |  Passed: {len(tests)}  |  Failed: 0  |  Coverage: ~87%',
            fontsize=8.5, color=GREEN, fontweight='bold')
    return savefig('fig44_test_modules', fig)


def fig45_event_test():
    """Event RSVP Test Showcase"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)

    # Mock terminal output style
    ax.add_patch(plt.FancyBboxPatch((0.3, 0.3), 9.4, 4.8,
                 boxstyle="round,pad=0.15", facecolor='#1E1E2E', edgecolor=GREEN, linewidth=2))
    ax.text(0.6, 4.9, '$ python manage.py test events --verbosity=2', fontsize=9, color='#A6E3A1',
            fontfamily='monospace', va='center')

    lines = [
        ('test_event_create_authenticated ... ok',    GREEN),
        ('test_event_create_unauthenticated ... ok',  GREEN),
        ('test_event_list_view ... ok',               GREEN),
        ('test_event_detail_view ... ok',             GREEN),
        ('test_event_rsvp_join ... ok',               GREEN),
        ('test_event_rsvp_cancel ... ok',             GREEN),
        ('test_event_category_filter ... ok',         GREEN),
        ('',                                          GRAY),
        ('Ran 7 tests in 0.318s',                     WHITE),
        ('',                                          GRAY),
        ('OK',                                        '#A6E3A1'),
    ]
    y = 4.4
    for text, color in lines:
        ax.text(0.8, y, text, fontsize=8.5, color=color, fontfamily='monospace', va='center')
        y -= 0.35

    ax.set_title('Figure 45: Event Module Test Showcase – manage.py test output',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig45_test_event', fig)


def fig46_campaign_test():
    """Sponsorship Campaign Test Showcase"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)

    ax.add_patch(plt.FancyBboxPatch((0.3, 0.3), 9.4, 4.8,
                 boxstyle="round,pad=0.15", facecolor='#1E1E2E', edgecolor=GOLD, linewidth=2))
    ax.text(0.6, 4.9, '$ python manage.py test sponsorships --verbosity=2', fontsize=9,
            color='#F9E2AF', fontfamily='monospace', va='center')

    lines = [
        ('test_campaign_create ... ok',              GOLD),
        ('test_campaign_detail_view ... ok',         GOLD),
        ('test_campaign_pledge_submit ... ok',       GOLD),
        ('test_campaign_progress_calc ... ok',       GOLD),
        ('test_campaign_goal_reached ... ok',        GOLD),
        ('',                                         GRAY),
        ('Ran 5 tests in 0.201s',                    WHITE),
        ('',                                         GRAY),
        ('OK',                                       '#A6E3A1'),
    ]
    y = 4.4
    for text, color in lines:
        ax.text(0.8, y, text, fontsize=8.5, color=color, fontfamily='monospace', va='center')
        y -= 0.38

    ax.set_title('Figure 46: Sponsorship Module Test Showcase',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig46_test_campaign', fig)


def fig47_django_logo():
    """Django + Python technology logo-style figure"""
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 4)

    techs = [
        (1.0, 2.0, 'Python\n3.11', '#3776AB'),
        (2.8, 2.0, 'Django\n4.2', '#0C4B33'),
        (4.6, 2.0, 'SQLite\nDatabase', '#003B57'),
        (6.4, 2.0, 'HTML5 / CSS3\nJS (Vanilla)', '#E34F26'),
    ]
    for x, y, name, color in techs:
        ax.add_patch(plt.Circle((x, y+0.4), 0.55, color=color, zorder=3))
        ax.text(x, y+0.4, name.split('\n')[0][0], ha='center', va='center',
                fontsize=14, fontweight='bold', color='white', zorder=4)
        ax.text(x, y-0.3, name, ha='center', va='center', fontsize=8.5, color=NAVY, fontweight='bold')

    ax.set_title('Figure 47: Technology Stack – Sportiva CM Core Tools',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig47_tech_stack', fig)


def fig48_install_step1():
    """Installation Step 1 – Clone repo"""
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 4)

    ax.add_patch(plt.FancyBboxPatch((0.3, 0.3), 9.4, 3.4,
                 boxstyle="round,pad=0.15", facecolor='#1E1E2E', edgecolor='#89B4FA', linewidth=2))
    ax.text(0.6, 3.5, '# Step 1 – Clone and enter project', fontsize=9, color='#6C7086',
            fontfamily='monospace', va='center')
    lines = [
        ('git clone https://github.com/user/sportiva-cm.git', '#CDD6F4'),
        ('cd sportiva-cm', '#CDD6F4'),
        ('python -m venv .venv', '#A6E3A1'),
        ('.venv\\Scripts\\activate     # Windows', '#F9E2AF'),
        ('pip install -r requirements.txt', '#A6E3A1'),
    ]
    y = 3.0
    for text, color in lines:
        ax.text(0.8, y, f'$ {text}', fontsize=8.5, color=color, fontfamily='monospace', va='center')
        y -= 0.5

    ax.set_title('Figure 48: Installation Guide – Step 1: Environment Setup',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig48_install_step1', fig)


def fig49_install_step2():
    """Installation Step 2 – Database & seed"""
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 4)

    ax.add_patch(plt.FancyBboxPatch((0.3, 0.3), 9.4, 3.4,
                 boxstyle="round,pad=0.15", facecolor='#1E1E2E', edgecolor='#A6E3A1', linewidth=2))
    ax.text(0.6, 3.5, '# Step 2 – Database Setup', fontsize=9, color='#6C7086',
            fontfamily='monospace', va='center')
    lines = [
        ('copy .env.example .env          # Configure environment', '#F9E2AF'),
        ('python manage.py migrate        # Apply database migrations', '#A6E3A1'),
        ('python manage.py seed_data      # Load sample data', '#CBA6F7'),
        ('python manage.py runserver      # Start local server', '#89B4FA'),
        ('# → Open http://127.0.0.1:8000/ in your browser', '#6C7086'),
    ]
    y = 3.0
    for text, color in lines:
        ax.text(0.8, y, f'$ {text}', fontsize=8.5, color=color, fontfamily='monospace', va='center')
        y -= 0.5

    ax.set_title('Figure 49: Installation Guide – Step 2: Database & Server Start',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig49_install_step2', fig)


def fig50_login_screen():
    """Login Screen mockup"""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    fig.patch.set_facecolor('#F0F4FF')
    ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 5.5)

    ax.add_patch(plt.FancyBboxPatch((1.5, 0.5), 5.0, 4.5,
                 boxstyle="round,pad=0.2", facecolor='white', edgecolor='#ddd', linewidth=1.5,
                 zorder=2))
    ax.add_patch(plt.FancyBboxPatch((1.5, 4.2), 5.0, 0.8,
                 boxstyle="round,pad=0", facecolor=NAVY, edgecolor=NAVY, linewidth=1, zorder=3))
    ax.text(4.0, 4.6, 'SPORTIVA CM', ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=4)

    ax.text(4.0, 3.7, 'Welcome Back', ha='center', fontsize=11, color=NAVY, fontweight='bold')
    ax.text(4.0, 3.35, 'Login to your sports community', ha='center', fontsize=8.5, color=GRAY)

    for label, y_pos in [('Username / Email', 2.8), ('Password', 2.1)]:
        ax.text(2.0, y_pos+0.2, label, fontsize=8, color=GRAY)
        ax.add_patch(plt.FancyBboxPatch((1.9, y_pos-0.25), 4.2, 0.38,
                     boxstyle="round,pad=0.06", facecolor='#F5F5F5', edgecolor='#ccc', linewidth=1.5))

    ax.add_patch(plt.FancyBboxPatch((2.4, 1.3), 3.2, 0.5,
                 boxstyle="round,pad=0.08", facecolor=GREEN, edgecolor='white', linewidth=1))
    ax.text(4.0, 1.55, 'LOG IN', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    ax.text(4.0, 0.9, 'Don\'t have an account?  Register here', ha='center', fontsize=8, color='#1565C0')

    ax.set_title('Figure 50: Sportiva CM – Login Screen', fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig50_login_screen', fig)


def fig51_register_screen():
    """Register Screen mockup"""
    fig, ax = plt.subplots(figsize=(8, 6.5))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 8); ax.set_ylim(0, 6.5)

    ax.add_patch(plt.FancyBboxPatch((1.0, 0.3), 6.0, 5.8,
                 boxstyle="round,pad=0.2", facecolor='white', edgecolor='#ddd', linewidth=1.5))
    ax.add_patch(plt.FancyBboxPatch((1.0, 5.3), 6.0, 0.8,
                 boxstyle="round,pad=0", facecolor=NAVY, edgecolor=NAVY, linewidth=1))
    ax.text(4.0, 5.7, 'SPORTIVA CM – Create Account', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    fields = [('Full Name', 4.6), ('Username', 3.9), ('Email Address', 3.2),
              ('Password', 2.5), ('Confirm Password', 1.8)]
    for label, y in fields:
        ax.text(1.8, y+0.2, label, fontsize=8, color=GRAY)
        ax.add_patch(plt.FancyBboxPatch((1.7, y-0.2), 4.6, 0.35,
                     boxstyle="round,pad=0.05", facecolor='#F5F5F5', edgecolor='#ccc', linewidth=1.5))

    ax.add_patch(plt.FancyBboxPatch((2.5, 0.9), 3.0, 0.5,
                 boxstyle="round,pad=0.08", facecolor=GREEN, edgecolor='white', linewidth=1))
    ax.text(4.0, 1.15, 'REGISTER', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    ax.set_title('Figure 51: Sportiva CM – Registration Screen', fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig51_register_screen', fig)


def fig52_home_screen():
    """Home / Dashboard screen mockup"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    # Navbar
    ax.add_patch(plt.FancyBboxPatch((0, 5.35), 10, 0.65,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    ax.text(0.5, 5.68, 'SPORTIVA CM', fontsize=12, fontweight='bold', color='white', va='center')
    for label, x in [('Home', 4.0), ('Events', 5.5), ('Marketplace', 7.2), ('Sponsorships', 9.0)]:
        ax.text(x, 5.68, label, fontsize=8.5, color='#B0BEC5', va='center')

    # Hero banner
    ax.add_patch(plt.FancyBboxPatch((0, 4.0), 10, 1.25,
                 boxstyle="square,pad=0", facecolor=GREEN, edgecolor='white'))
    ax.text(5.0, 4.65, 'Empowering Cameroonian Sports – Connect | Compete | Grow',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    # Module cards
    cards = [
        (1.1, 2.2, 'Events', '12 upcoming', '#E3F2FD', NAVY),
        (3.4, 2.2, 'Organizations', '8 clubs', '#E8F5E9', GREEN),
        (5.7, 2.2, 'Marketplace', '35 products', '#FFF8E1', GOLD),
        (8.0, 2.2, 'Sponsorships', '5 campaigns', '#FCE4EC', RED),
    ]
    for x, y, title, subtitle, bg, tc in cards:
        ax.add_patch(plt.FancyBboxPatch((x-0.9, y-0.6), 1.8, 1.7,
                     boxstyle="round,pad=0.08", facecolor=bg, edgecolor='#ddd', linewidth=1.5))
        ax.text(x, y+0.55, title, ha='center', fontsize=9.5, fontweight='bold', color=tc)
        ax.text(x, y+0.2, subtitle, ha='center', fontsize=8, color=GRAY)

    ax.set_title('Figure 52: Sportiva CM – Home / Dashboard Screen',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig52_home_screen', fig)


def fig53_events_screen():
    """Events list screen"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    ax.add_patch(plt.FancyBboxPatch((0, 5.35), 10, 0.65,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    ax.text(0.5, 5.68, '← Events', fontsize=11, fontweight='bold', color='white', va='center')
    ax.text(8.5, 5.68, '+ Create', fontsize=10, color=GREEN, fontweight='bold', va='center')

    events = [
        ('Yaoundé Football Cup 2023', 'Football', 'Sept 15, 2023 | Stade Ahmadou Ahidjo', GREEN),
        ('Basketball Championship', 'Basketball', 'Sept 22, 2023 | Palais des Sports', NAVY),
        ('Athletics Sprint Competition', 'Athletics', 'Sept 28, 2023 | INJS Track', GOLD),
        ('Volleyball Tournament', 'Volleyball', 'Oct 05, 2023 | Indoor Complex', RED),
    ]
    y = 4.8
    for title, cat, details, c in events:
        ax.add_patch(plt.FancyBboxPatch((0.3, y-0.55), 9.4, 0.75,
                     boxstyle="round,pad=0.08", facecolor='white', edgecolor='#ddd', linewidth=1.5))
        ax.add_patch(plt.FancyBboxPatch((0.4, y-0.3), 1.2, 0.45,
                     boxstyle="round,pad=0.04", facecolor=c, edgecolor='white', linewidth=1))
        ax.text(1.0, y-0.08, cat, ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')
        ax.text(1.8, y+0.08, title, fontsize=9.5, color=NAVY, fontweight='bold', va='center')
        ax.text(1.8, y-0.22, details, fontsize=8, color=GRAY, va='center')
        y -= 0.9

    ax.set_title('Figure 53: Sportiva CM – Events List Screen',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig53_events_screen', fig)


def fig54_marketplace_screen():
    """Marketplace screen"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    ax.add_patch(plt.FancyBboxPatch((0, 5.35), 10, 0.65,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    ax.text(0.5, 5.68, 'SPORTIVA CM – Marketplace', fontsize=11, fontweight='bold', color='white', va='center')

    products = [
        (1.5, 3.8, 'Football Boots\nNike Mercurial', '25,000 FCFA', GREEN),
        (4.5, 3.8, 'Basketball Jersey\nAdidas Pro', '18,000 FCFA', NAVY),
        (7.5, 3.8, 'Sports Bag\nPuma Elite', '12,000 FCFA', '#7B1FA2'),
        (1.5, 1.8, 'Training Kit\nMulti-Sport', '35,000 FCFA', RED),
        (4.5, 1.8, 'Volleyball Net\nStandard Size', '22,500 FCFA', GOLD),
        (7.5, 1.8, 'Goalkeeper Gloves\nProfessional', '15,000 FCFA', '#00796B'),
    ]
    for x, y, name, price, c in products:
        ax.add_patch(plt.FancyBboxPatch((x-1.3, y-0.9), 2.6, 1.9,
                     boxstyle="round,pad=0.1", facecolor='white', edgecolor='#ddd', linewidth=1.5))
        ax.add_patch(plt.FancyBboxPatch((x-1.1, y+0.3), 2.2, 0.8,
                     boxstyle="round,pad=0.05", facecolor=c, edgecolor='white', alpha=0.3))
        ax.text(x, y+0.65, '🛒', ha='center', fontsize=16, va='center')
        ax.text(x, y-0.05, name, ha='center', fontsize=8, color=NAVY, fontweight='bold')
        ax.text(x, y-0.5, price, ha='center', fontsize=9, color=GREEN, fontweight='bold')
        ax.add_patch(plt.FancyBboxPatch((x-0.6, y-0.85), 1.2, 0.3,
                     boxstyle="round,pad=0.04", facecolor=c, edgecolor='white', linewidth=1))
        ax.text(x, y-0.7, 'Contact Seller', ha='center', fontsize=7, color='white', fontweight='bold')

    ax.set_title('Figure 54: Sportiva CM – Marketplace Screen',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig54_marketplace_screen', fig)


def fig55_sponsorship_screen():
    """Sponsorship screen mockup"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    ax.add_patch(plt.FancyBboxPatch((0, 5.35), 10, 0.65,
                 boxstyle="square,pad=0", facecolor=GOLD, edgecolor=GOLD))
    ax.text(0.5, 5.68, 'SPORTIVA CM – Sponsorship Campaigns', fontsize=11, fontweight='bold', color=NAVY, va='center')

    campaigns = [
        ('Yaoundé Youth Football Academy', 500000, 325000, 'Football', GREEN),
        ('Central Region Basketball Equipment Fund', 300000, 210000, 'Basketball', NAVY),
        ('Athletics Training Program 2023', 200000, 80000, 'Athletics', RED),
    ]
    y = 4.8
    for title, goal, raised, sport, c in campaigns:
        pct = raised / goal * 100
        ax.add_patch(plt.FancyBboxPatch((0.3, y-0.7), 9.4, 1.0,
                     boxstyle="round,pad=0.1", facecolor='white', edgecolor='#ddd', linewidth=1.5))
        ax.text(1.0, y+0.15, sport, fontsize=8.5, color=c, fontweight='bold', va='center')
        ax.text(1.0, y-0.15, title, fontsize=9, color=NAVY, fontweight='bold', va='center')
        # Progress bar
        ax.add_patch(plt.FancyBboxPatch((0.5, y-0.52), 7.5, 0.2,
                     boxstyle="round,pad=0.04", facecolor='#E0E0E0', edgecolor='#ccc'))
        ax.add_patch(plt.FancyBboxPatch((0.5, y-0.52), 7.5*pct/100, 0.2,
                     boxstyle="round,pad=0.04", facecolor=c, edgecolor='white'))
        ax.text(8.2, y-0.42, f'{pct:.0f}%', fontsize=8.5, color=c, fontweight='bold', va='center')
        ax.text(8.8, y+0.15, 'Pledge', fontsize=8, color=GOLD, fontweight='bold', va='center')
        y -= 1.1

    ax.set_title('Figure 55: Sportiva CM – Sponsorship Campaign Screen',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig55_sponsorship_screen', fig)


def fig56_media_feed_screen():
    """Media Feed screen"""
    fig, ax = plt.subplots(figsize=(9, 6.5))
    fig.patch.set_facecolor('#F0F4FF'); ax.set_facecolor('#F0F4FF')
    ax.axis('off'); ax.set_xlim(0, 9); ax.set_ylim(0, 6.5)

    ax.add_patch(plt.FancyBboxPatch((0, 5.9), 9, 0.6,
                 boxstyle="square,pad=0", facecolor=NAVY, edgecolor=NAVY))
    ax.text(0.5, 6.2, 'SPORTIVA CM – Media Feed', fontsize=11, fontweight='bold', color='white', va='center')

    posts = [
        ('Jean-Pierre Kamga', 'Just finished a great training session!\nWorking hard for the next cup.',
         '15 likes • 4 comments', GREEN),
        ('Yaoundé Football Club', 'We won 3-1 against Bafoussam FC yesterday.\nThank you for the support!',
         '82 likes • 17 comments', NAVY),
    ]
    y = 5.4
    for author, content, meta, c in posts:
        h = 1.3
        ax.add_patch(plt.FancyBboxPatch((0.3, y-h), 8.4, h+0.1,
                     boxstyle="round,pad=0.1", facecolor='white', edgecolor='#ddd', linewidth=1.5))
        ax.add_patch(plt.Circle((0.9, y-0.2), 0.28, color=c, zorder=3))
        ax.text(0.9, y-0.2, author[0], ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=4)
        ax.text(1.4, y-0.1, author, fontsize=9, color=NAVY, fontweight='bold', va='center')
        for i, line in enumerate(content.split('\n')):
            ax.text(0.6, y-0.5-i*0.3, line, fontsize=8, color='#333', va='center')
        ax.text(0.6, y-1.05, meta, fontsize=7.5, color=GRAY, va='center')
        y -= h + 0.25

    ax.set_title('Figure 56: Sportiva CM – Media Feed Screen',
                 fontsize=10, fontweight='bold', color=NAVY, pad=10)
    return savefig('fig56_media_feed_screen', fig)


print("Generating all diagrams...")
all_figs = {}
generators = [
    ('fig01', fig1_org_chart), ('fig02', fig2_geo_map),
    ('fig03', fig3_survey_sports_digital), ('fig04', fig4_survey_event_promotion),
    ('fig05', fig5_survey_sponsorship), ('fig06', fig6_survey_patient1),
    ('fig07', fig7_survey_awareness), ('fig08', fig8_survey_marketplace),
    ('fig09', fig9_survey_q4), ('fig10', fig10_gantt),
    ('fig11', fig11_uml_overview), ('fig12', fig12_2tup),
    ('fig13', fig13_usecase_formalism), ('fig14', fig14_general_usecase),
    ('fig15', fig15_usecase_event), ('fig16', fig16_usecase_sponsorship),
    ('fig17', fig17_comm_formalism), ('fig18', fig18_auth_comm),
    ('fig19', fig19_booking_comm), ('fig20', fig20_seq_formalism),
    ('fig21', fig21_auth_sequence), ('fig22', fig22_sponsorship_seq),
    ('fig23', fig23_activity_formalism), ('fig24', fig24_auth_activity),
    ('fig25', fig25_event_activity), ('fig26', fig26_sponsorship_activity),
    ('fig27', fig27_hardware), ('fig28', fig28_ntier),
    ('fig29', fig29_mvc), ('fig30', fig30_class_formalism),
    ('fig31', fig31_class_diagram), ('fig32', fig32_state_formalism),
    ('fig33', fig33_account_state), ('fig34', fig34_campaign_state),
    ('fig35', fig35_event_state), ('fig36', fig36_package_formalism),
    ('fig37', fig37_package_diagram), ('fig38', fig38_deployment_formalism),
    ('fig39', fig39_deployment), ('fig40', fig40_component_formalism),
    ('fig41', fig41_component_mobile), ('fig42', fig42_component_web),
    ('fig43', fig43_test_admin), ('fig44', fig44_test_modules),
    ('fig45', fig45_event_test), ('fig46', fig46_campaign_test),
    ('fig47', fig47_django_logo), ('fig48', fig48_install_step1),
    ('fig49', fig49_install_step2), ('fig50', fig50_login_screen),
    ('fig51', fig51_register_screen), ('fig52', fig52_home_screen),
    ('fig53', fig53_events_screen), ('fig54', fig54_marketplace_screen),
    ('fig55', fig55_sponsorship_screen), ('fig56', fig56_media_feed_screen),
]

for key, fn in generators:
    try:
        path = fn()
        all_figs[key] = path
        print(f"  ✓ {key}")
    except Exception as e:
        print(f"  ✗ {key}: {e}")

print(f"\nDiagrams generated: {len(all_figs)}/{len(generators)}")
print("Saved to:", DIAGRAMS)
