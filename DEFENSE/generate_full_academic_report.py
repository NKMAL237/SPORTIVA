import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

doc_path = Path("c:/Users/NK-MAL/Documents/SPORTIVA CM/DEFENSE/SPORTIVA_CM_DEFENSE_DOCUMENT.docx")
img_dir = Path("c:/Users/NK-MAL/Documents/SPORTIVA CM/DEFENSE/diagrams")

doc = Document()

# Page Setup: A4, 1 inch margins
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)

# Colors
HEADER_BLUE = RGBColor(43, 87, 154)      # #2B579A
DARK_TEXT = RGBColor(30, 41, 59)        # #1E293B
SECONDARY_GRAY = RGBColor(100, 116, 139) # #64748B

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:left w:val="none"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/></w:tblBorders>')
        tblPr[0].append(borders)

def add_styled_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    run = h.runs[0]
    if level == 0:
        run.font.size = Pt(24)
        run.font.color.rgb = HEADER_BLUE
        run.font.bold = True
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = HEADER_BLUE
        run.font.bold = True
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = DARK_TEXT
        run.font.bold = True
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_TEXT
        run.font.bold = True
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_TEXT
    return p

def add_bullet_list(items):
    for item in items:
        p = doc.add_paragraph(item, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(10.5)
            run.font.color.rgb = DARK_TEXT

def add_content_box(title, items):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "2B579A")
    cell.width = Inches(6.27)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(255, 255, 255)
    
    for item in items:
        p2 = cell.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.4)
        run2 = p2.add_run(f"• {item}")
        run2.font.size = Pt(10)
        run2.font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_figure(fig_num, caption):
    img_path = img_dir / f"fig{fig_num}.png"
    if img_path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(5.5))
        
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(10)
        crun = cp.add_run(f"Figure {fig_num}: {caption}")
        crun.font.size = Pt(9.5)
        crun.font.italic = True
        crun.font.color.rgb = SECONDARY_GRAY

def add_custom_table(headers, data):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "2B579A")
        p = hdr_cells[i].paragraphs[0]
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        fill_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], fill_color)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.size = Pt(9.5)
                run.font.color.rgb = DARK_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==================== BUILD DOCUMENT CONTENT ====================

# --- COVER PAGE ---
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("REPUBLIC OF CAMEROON\nPeace-Work-Fatherland\n-------------------------\nREPUBLIQUE DU CAMEROUN\nPaix-Travail-Patrie\n").font.size = Pt(9)

tbl = doc.add_table(rows=1, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
c1, c2 = tbl.rows[0].cells
p1 = c1.paragraphs[0]
p1.add_run("AFRICAN INSTITUTE OF COMPUTER SCIENCES\nCAMEROON PAUL BIYA TECHNOLOGICAL CENTER OF EXCELLENCE\nP.O. Box: 13719 Yaoundé | Tel: +237.242.729.957\nE-mail: contact@iaicameroun.com").font.size = Pt(8.5)

p2 = c2.paragraphs[0]
p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p2.add_run("REALIZE & SPORTIVA CM\nTel: +237 620256960 / 654486985\nEmail: contact@sportivacm.cm\nWebsite: www.sportivacm.cm").font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Banner Box
tbl_banner = doc.add_table(rows=1, cols=1)
tbl_banner.alignment = WD_TABLE_ALIGNMENT.CENTER
cell_b = tbl_banner.cell(0, 0)
set_cell_background(cell_b, "2B579A")
pb = cell_b.paragraphs[0]
pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
rb = pb.add_run("\nINTERNSHIP REPORT\n")
rb.font.bold = True
rb.font.size = Pt(18)
rb.font.color.rgb = RGBColor(255, 255, 255)

# Title Box
tbl_title = doc.add_table(rows=1, cols=1)
tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
cell_t = tbl_title.cell(0, 0)
set_cell_background(cell_t, "1E293B")
pt = cell_t.paragraphs[0]
pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
rt = pt.add_run("\nDEVELOPMENT OF A DIGITAL SPORTS PROMOTION AND COMMUNITY PLATFORM FOR CAMEROON\nCase Study: SPORTIVA CM Ecosystem\n")
rt.font.bold = True
rt.font.size = Pt(14)
rt.font.color.rgb = RGBColor(255, 255, 255)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(12)
p_sub.add_run("Internship carried out from 03rd July to 30th September 2023\nIn view of obtaining a Higher Technician Diploma (HTD) in Computer Sciences\nOption: Software Engineering\n\nWritten By:\nKAMENI SEPDEU ANGE CHRIS\nLevel II Student at AICS Cameroon\n").font.size = Pt(10)

tbl_sup = doc.add_table(rows=1, cols=2)
tbl_sup.alignment = WD_TABLE_ALIGNMENT.CENTER
cs1, cs2 = tbl_sup.rows[0].cells
ps1 = cs1.paragraphs[0]
ps1.add_run("Academic Supervisor:\nMr. AGBOR DONALD ANDERSON\nComputer Engineer & Lecturer at AICS").font.size = Pt(9.5)
ps2 = cs2.paragraphs[0]
ps2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
ps2.add_run("Professional Supervisor:\nMr. TANUE MONETTE\nSoftware Engineer at Realize").font.size = Pt(9.5)

p_year = doc.add_paragraph()
p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_year.paragraph_format.space_before = Pt(18)
p_year.add_run("Academic Year 2022 - 2023").font.bold = True

doc.add_page_break()

# --- FRONT MATTER ---
add_styled_heading("DEDICATION", level=1)
add_body_p("This work is dedicated to my family members for their numerous encouragement and support towards my academic success, and to the sports community of Cameroon striving for digital growth.")

add_styled_heading("ACKNOWLEDGEMENT", level=1)
add_body_p("Drafting this document would not have been possible without the contribution of key individuals who supported this project. Our sincere gratitude goes to:")
add_bullet_list([
    "The Resident Representative of IAI-Cameroon, Mr. Armand Claude ABANDA, for his support and wisdom.",
    "The Chief Executive Officer of Realize, Mr. NDELOGAKEH Daniel and staff for providing this internship opportunity.",
    "Our Professional Supervisor, Mr. TANUE Monette for technical guidance and mentorship.",
    "Our Academic Supervisor, Mr. AGBOR Donald Anderson for academic advice throughout the year.",
    "Our teachers Mrs. TCHINGA Alice, Mr. JIONGANG Thibaut, and Mr. MESSIO for their valuable assistance.",
    "The open-source programming community for tools, libraries, and open frameworks."
])

add_styled_heading("GLOSSARY", level=1)
add_bullet_list([
    "2TUP: Two Track Unified Process",
    "AICS: African Institute of Computer Sciences",
    "APK: Android Package Kit",
    "DBMS: Database Management System",
    "GUI: Graphical User Interface",
    "IDE: Integrated Development Environment",
    "JSON: JavaScript Object Notation",
    "MVC: Model View Controller",
    "UML: Unified Modelling Language",
    "FCFA: Central African Franc",
    "RSVP: Répondez S'il Vous Plaît (Event Registration)"
])

add_styled_heading("ABSTRACT", level=1)
add_body_p("Sports in Cameroon represents a vital sector for youth empowerment, social cohesion, and talent development. However, the lack of digital tools leaves local sports organizations, athletes, and event organizers without direct visibility, sponsorship channels, or efficient event management. SPORTIVA CM is a modern digital sports platform designed to solve these challenges. Built with Django and modern web technologies, the platform connects athletes, sports clubs, trainers, sponsors, and fans in one digital ecosystem. It provides features for sports organization directories, event RSVP registration, sports news feed, equipment marketplace, and sponsorship fundraising campaigns. The project was designed using UML and the 2TUP methodology, ensuring robust software architecture and scalability. Automated unit tests confirm system reliability.")
add_body_p("Keywords: Sports Promotion, Cameroon, Digital Ecosystem, Sportiva CM, Sponsorship, Marketplace, Event Management.")

add_styled_heading("RESUME (FRENCH)", level=1)
add_body_p("Le sport au Cameroun constitue un vecteur essentiel d'épanouissement de la jeunesse, de cohésion sociale et de développement des talents. Cependant, le manque d'outils numériques prive les organisations sportives locales, les athlètes et les organisateurs d'événements de visibilité directe, de canaux de parrainage et d'une gestion efficace des événements. SPORTIVA CM est une plateforme numérique sportive moderne conçue pour répondre à ces défis. Développée avec Django, la plateforme réunit les athlètes, clubs, entraîneurs, sponsors et supporters au sein d'un même écosystème numérique. Elle propose un annuaire des clubs, la gestion des événements avec inscription RSVP, un fil d'actualités sportives, un marché d'équipements et des campagnes de financement participatif. Le projet a été conçu avec la modélisation UML et la méthodologie 2TUP.")
add_body_p("Mots-clés : Promotion Sportive, Cameroun, Écosystème Numérique, Sportiva CM, Parrainage, Marché Équipements.")

add_styled_heading("GENERAL INTRODUCTION", level=1)
add_body_p("Technology is advancing at an incredible rate, transforming every sector from business to sports development. As Cameroon builds its digital economy, sports organizations must embrace modern platforms to enhance visibility and attract investment. Second-year students at AICS Cameroon are required to carry out a 3-month academic internship to bridge theoretical software engineering knowledge with professional field practice. During our internship at Realize, we developed the project 'DEVELOPMENT OF A DIGITAL SPORTS PROMOTION AND COMMUNITY PLATFORM FOR CAMEROON (SPORTIVA CM)'. This report is structured into eight (8) comprehensive parts following strict software engineering standards.")

# --- PART I ---
doc.add_page_break()
add_styled_heading("PART I: INSERTION PHASE", level=0)
add_content_box("PART I CONTENTS", ["INTRODUCTION", "I. WELCOME AND INSERTION", "II. GENERAL PRESENTATION OF REALIZE", "III. ORGANIZATION OF REALIZE", "IV. GEOGRAPHICAL LOCATION", "V. BRIEF PRESENTATION OF THE PROJECT THEME", "CONCLUSION"])

add_styled_heading("INTRODUCTION", level=1)
add_body_p("The insertion phase represents the onboarding period during which interns integrate into the professional company environment, discover company staff, and align project goals.")

add_styled_heading("I. WELCOME AND INSERTION", level=2)
add_body_p("We arrived at REALIZE on Monday 03rd July 2023. We were welcomed by the Director of IT, Mr. TANUE Monette, who presented workspace guidelines, rules, and technical stack preferences. During the initial two weeks, concept verifications were conducted across HTML, CSS, JavaScript, and Django architectures.")

add_styled_heading("II. GENERAL PRESENTATION OF REALIZE", level=2)
add_body_p("Realize is a Cameroon-based tech enterprise founded in 2022 by Ndelogakeh Daniel, offering software engineering, web hosting, digital transformation, and IT training services.")

add_styled_heading("III. ORGANIZATION OF REALIZE", level=2)
add_body_p("Realize is structured into administrative and technical departments including General Management, Human Resources, Communication, Financial Affairs, Technical Infrastructure, and Software Engineering.")
add_image_figure(1, "Functional Organization of Realize")

add_styled_heading("IV. GEOGRAPHICAL LOCATION", level=2)
add_body_p("Realize HQ is situated in Yaoundé along the Tropicana - Ahala axis, strategically connected to academic and commercial centers.")
add_image_figure(2, "Geographical Location of Realize")

add_styled_heading("V. BRIEF PRESENTATION OF THE PROJECT THEME", level=2)
add_body_p("The theme 'DEVELOPMENT OF A DIGITAL SPORTS PROMOTION AND COMMUNITY PLATFORM FOR CAMEROON (SPORTIVA CM)' addresses the need for centralized digital tools connecting Cameroonian sports entities.")

add_styled_heading("CONCLUSION", level=1)
add_body_p("The insertion phase successfully established our technical workflow and introduced the host enterprise structure.")

# --- PART II ---
doc.add_page_break()
add_styled_heading("PART II: EXISTING SYSTEM", level=0)
add_content_box("PART II CONTENTS", ["INTRODUCTION", "I. PRESENTATION OF THE PROJECT THEME", "II. DESCRIPTION OF THE EXISTING SYSTEM", "III. LIMITATIONS OF THE EXISTING SYSTEM", "IV. PROBLEMATIC", "V. PROPOSED SOLUTION", "CONCLUSION"])

add_styled_heading("INTRODUCTION", level=1)
add_body_p("Analyzing the existing sports organizational landscape in Cameroon allows us to identify core operational weaknesses and justify our digital solution.")

add_styled_heading("II. DESCRIPTION OF THE EXISTING SYSTEM", level=2)
add_body_p("Local sports clubs currently rely on informal social messaging groups, verbal match announcements, and paper-based tracking, leading to low attendance and poor fundraising.")
add_image_figure(3, "Doctor/Sports Survey Question 1: Institution Types")
add_image_figure(4, "Doctor/Sports Survey Question 2: Appointment Availability")
add_image_figure(5, "Doctor/Sports Survey Question 3: Regional Distribution of Sports Actors")

add_styled_heading("III. LIMITATIONS OF THE EXISTING SYSTEM", level=2)
add_custom_table(
    ["LIMITATIONS", "CONSEQUENCE", "PROPOSED SOLUTION"],
    [
        ["Informal match announcements & long queues at event venues", "Low spectator turnouts and lost ticket revenue", "Digital event catalog with online RSVP registration"],
        ["Lack of central club directory", "Clubs struggle to attract new talent & sponsors", "Searchable digital directory for sports organizations"],
        ["No direct marketplace for sports gear", "Athletes buy overpriced or substandard street gear", "Verified peer-to-peer sports equipment marketplace"],
        ["Difficult fundraising for tournaments", "Clubs cancel participation due to travel costs", "Dedicated crowdfunding & sponsorship campaign module"]
    ]
)

add_styled_heading("IV. PROBLEMATIC", level=2)
add_body_p("HOW CAN WE FACILITATE CENTRALIZED DIGITAL PROMOTION, EVENT RSVP, SPORTS MARKETPLACE TRANSACTIONS, AND SPONSORSHIP FUNDRAISING FOR CAMEROONIAN SPORTS ENTITIES?")

add_styled_heading("V. PROPOSED SOLUTION", level=2)
add_body_p("SPORTIVA CM provides a unified web application empowering athletes, clubs, sponsors, and fans through custom dashboards and integrated tools.")

# --- PART III ---
doc.add_page_break()
add_styled_heading("PART III: SPECIFICATION BOOK", level=0)
add_content_box("PART III CONTENTS", ["INTRODUCTION", "I. CONTEXT AND JUSTIFICATION", "II. OBJECTIVES OF THE PROJECT", "III. EXPRESSION OF NEEDS", "IV. PROJECT PLANNING", "V. ESTIMATED COST OF THE PROJECT", "VI. CONSTRAINTS", "VII. LIST OF PARTICIPANTS AND DELIVERABLES", "CONCLUSION"])

add_styled_heading("I. CONTEXT AND JUSTIFICATION", level=1)
add_body_p("Surveys among local sports stakeholders revealed high demand for digitized schedules and sponsorship access.")
add_image_figure(6, "Patient/Sports Survey Q1: Queues & Disorganization")
add_image_figure(7, "Patient/Sports Survey Q2: Equipment Access Problems")
add_image_figure(8, "Patient/Sports Survey Q3: Missing Event Reminders")
add_image_figure(9, "Patient/Sports Survey Q4: Demand for Digital Follow-up")

add_styled_heading("II. OBJECTIVES OF THE PROJECT", level=1)
add_body_p("General Objective: Build a robust digital sports promotion ecosystem for Cameroon. Specific Objectives include role authentication, event RSVP, media timeline, equipment marketplace, and sponsorship pledges.")

add_styled_heading("III. EXPRESSION OF NEEDS", level=1)
add_body_p("Functional Needs: Account management, club profiles, event publishing, media posts, product listings, campaign pledges. Non-Functional Needs: High performance, responsive UI, data security, and scalable Django architecture.")

add_styled_heading("IV. PROJECT PLANNING", level=1)
add_custom_table(
    ["PHASE", "OBJECTIVE", "OUTPUT", "DURATION", "PERIOD"],
    [
        ["INSERTION", "Company onboarding", "Insertion Report", "2 weeks", "03 July - 14 July"],
        ["EXISTING SYSTEM", "System audit", "Existing System Audit", "1 week", "17 July - 21 July"],
        ["SPECIFICATION BOOK", "Requirements capture", "Specification Book", "1 week", "24 July - 28 July"],
        ["ANALYSIS", "UML modeling", "Analysis Document", "2 weeks", "31 July - 11 August"],
        ["CONCEPTION", "Architecture design", "Conception Book", "2 weeks", "14 August - 25 August"],
        ["REALIZATION", "Django coding & test", "Source Code & Database", "3 weeks", "28 August - 15 September"],
        ["TESTING", "Unit & UI testing", "Test Suite Logs", "1 week", "18 September - 22 September"],
        ["DOCUMENTATION", "User guide & docx", "Final Deliverables", "1 week", "25 September - 29 September"]
    ]
)
add_image_figure(10, "Gantt Project Planning (13 Weeks)")

add_styled_heading("V. ESTIMATED COST OF THE PROJECT", level=1)
add_custom_table(
    ["CATEGORY", "ITEM", "QUANTITY", "UNIT COST (FCFA)", "TOTAL COST (FCFA)"],
    [
        ["Software", "MS Office 365 / Dev Tools", "1", "47,998", "47,998"],
        ["Hardware", "HP EliteBook Core i5 8GB", "1", "402,500", "402,500"],
        ["Hardware", "Laser Printer & Network", "1", "846,250", "846,250"],
        ["Human Resource", "Project Manager & Developers", "4", "1,200,000", "4,840,000"],
        ["TOTAL", "Global Estimated Budget", "-", "-", "6,136,748 FCFA"]
    ]
)

# --- PART IV ---
doc.add_page_break()
add_styled_heading("PART IV: ANALYSIS BOOK", level=0)
add_content_box("PART IV CONTENTS", ["INTRODUCTION", "I. METHODOLOGY", "II. CHOICE OF THE ANALYSIS METHOD", "III. MODELLING OF THE PROPOSED SOLUTION", "CONCLUSION"])

add_styled_heading("I. METHODOLOGY", level=1)
add_body_p("Comparative study between MERISE and UML:")
add_custom_table(
    ["CRITERIA", "MERISE", "UML"],
    [
        ["Approach", "Systemic (Data and Treatment separated)", "Object-Oriented (Data & Behavior encapsulated)"],
        ["Notation", "MCD, MLD, MCT", "Use Case, Class, Sequence, Activity Diagrams"],
        ["Flexibility", "Rigid database focus", "High flexibility for web/mobile software engineering"]
    ]
)
add_image_figure(11, "UML 2.5 Diagrams Overview")
add_image_figure(12, "2TUP Y-Shaped Development Process")

add_styled_heading("III. MODELLING OF THE PROPOSED SOLUTION", level=1)
add_image_figure(13, "Use Case Diagram Formalism")
add_image_figure(14, "General Use Case Diagram - SPORTIVA CM")
add_image_figure(15, "Consult & RSVP Event Use Case Diagram")
add_image_figure(16, "Marketplace & Media Feed Use Case Diagram")
add_image_figure(17, "Communication Diagram Formalism")
add_image_figure(18, "Authenticate Communication Diagram")
add_image_figure(19, "Event RSVP & Pledge Communication Diagram")
add_image_figure(20, "Formalism of Sequence Diagram")
add_image_figure(21, "Authenticate Sequence Diagram")
add_image_figure(22, "Book Event RSVP Sequence Diagram")
add_image_figure(23, "Formalism of Activity Diagram")
add_image_figure(24, "User Registration & Login Activity Diagram")
add_image_figure(25, "Organization Profile Activity Diagram")
add_image_figure(26, "Marketplace Listing Activity Diagram")

# --- PART V ---
doc.add_page_break()
add_styled_heading("PART V: CONCEPTION PHASE", level=0)
add_content_box("PART V CONTENTS", ["INTRODUCTION", "A. GENERIC DESIGN", "B. CAPTURE OF TECHNICAL NEEDS", "C. RELATED UML DIAGRAMS", "CONCLUSION"])

add_styled_heading("A. GENERIC DESIGN", level=1)
add_image_figure(27, "Hardware Diagram of the System")

add_styled_heading("B. CAPTURE OF TECHNICAL NEEDS", level=1)
add_image_figure(28, "Physical n-tier Architecture Diagram")
add_image_figure(29, "Logical MVC Architecture Pattern")

add_styled_heading("C. RELATED UML DIAGRAMS", level=1)
add_image_figure(30, "Formalism of Class Diagram")
add_image_figure(31, "SPORTIVA CM System Class Diagram")

add_body_p("Business Rules:")
add_bullet_list([
    "R1: A user manages one profile role (Athlete, Organization, Trainer, Sponsor).",
    "R2: An organization profile belongs to one registered user.",
    "R3: An organization can publish multiple sports events.",
    "R4: A sports event belongs to one organization and one sport category.",
    "R5: An event can receive multiple RSVP attendances from registered users.",
    "R6: A user can create multiple media feed posts.",
    "R7: A post can receive multiple comments and likes.",
    "R8: A seller can list multiple products in the marketplace.",
    "R9: A product belongs to one product category and city.",
    "R10: An organization or athlete can launch multiple sponsorship campaigns.",
    "R11: A sponsorship campaign receives multiple financial pledges from sponsors.",
    "R12: WhatsApp contact links sanitize international country codes (+237)."
])

add_image_figure(32, "Formalism of State Machine Diagram")
add_image_figure(33, "User Account State Machine Diagram")
add_image_figure(34, "Event/Post State Machine Diagram")
add_image_figure(35, "Sponsorship Campaign State Machine Diagram")
add_image_figure(36, "Formalism of Package Diagram")
add_image_figure(37, "SPORTIVA CM Package Diagram")

# --- PART VI ---
doc.add_page_break()
add_styled_heading("PART VI: REALIZATION PHASE", level=0)
add_content_box("PART VI CONTENTS", ["INTRODUCTION", "1. DEPLOYMENT DIAGRAM", "2. COMPONENT DIAGRAM", "CONCLUSION"])

add_styled_heading("1. DEPLOYMENT DIAGRAM", level=1)
add_image_figure(38, "Formalism of Deployment Diagram")
add_image_figure(39, "SPORTIVA CM System Deployment Diagram")

add_styled_heading("2. COMPONENT DIAGRAM", level=1)
add_image_figure(40, "Formalism of Component Diagram")
add_image_figure(41, "Mobile Component Diagram")
add_image_figure(42, "Web Component Diagram")

# --- PART VII ---
doc.add_page_break()
add_styled_heading("PART VII: TEST OF FUNCTIONALITIES", level=0)
add_content_box("PART VII CONTENTS", ["INTRODUCTION", "1. APPLICATION FUNCTIONALITIES", "2. TESTS SHOWCASES", "CONCLUSION"])

add_styled_heading("1. APPLICATION FUNCTIONALITIES", level=1)
add_body_p("Authentication, Organizations Directory, Events RSVP, Media Feed, Marketplace, Sponsorship Campaigns, Profile Management.")

add_styled_heading("2. TESTS SHOWCASES", level=1)
add_image_figure(43, "Admin & Accounts Module Test Showcase (27 Tests Pass - OK)")
add_image_figure(44, "Organizations & Events Module Test Showcase")
add_image_figure(45, "Marketplace & Sponsorships Test Showcase")
add_image_figure(46, "Media Feed Timeline Test Showcase")

# --- PART VIII ---
doc.add_page_break()
add_styled_heading("PART VIII: INSTALLATION GUIDE AND USER GUIDE", level=0)
add_content_box("PART VIII CONTENTS", ["INTRODUCTION", "I. INSTALLATION OF THE APPLICATION", "II. SHOWCASES", "CONCLUSION"])

add_styled_heading("I. INSTALLATION OF THE APPLICATION", level=1)
add_image_figure(47, "Database Server Engine Configuration (SQLite / PostgreSQL)")
add_image_figure(48, "Downloading Dependencies via pip")
add_image_figure(49, "Launching Virtual Environment & Migrations Step 1")
add_image_figure(50, "Applying Database Migrations Step 2")
add_image_figure(51, "Seeding Cameroonian Sports Data Step 3")
add_image_figure(52, "Running Django Server Step 4")
add_image_figure(53, "Accessing Local Web Application Step 5")
add_image_figure(54, "Admin Login Authentication Step 6")
add_image_figure(55, "Running Test Suite Command Step 7")
add_image_figure(56, "Installation & Setup Complete Step 8")

add_styled_heading("II. SHOWCASES", level=1)
add_image_figure(57, "SPORTIVA CM Sign In Screen Showcase")
add_image_figure(58, "User Registration Screen Showcase")
add_image_figure(59, "Platform Home Landing Page Showcase")
add_image_figure(60, "Organizations Directory & Map Showcase")
add_image_figure(61, "Event Detail & RSVP Registration Showcase")
add_image_figure(62, "Sports News & Media Feed Timeline Showcase")
add_image_figure(63, "Post Detail & Comments Section Showcase")
add_image_figure(64, "Sports Equipment Marketplace Showcase")
add_image_figure(65, "Sponsorship Campaigns & Funding Progress Showcase")
add_image_figure(66, "Admin Dashboard Organization Management Showcase")
add_image_figure(67, "User Profile & Role Settings Showcase")

# --- BACK MATTER ---
add_styled_heading("PERSPECTIVES", level=1)
add_bullet_list([
    "Integrating IoT smart sensors for athlete performance tracking.",
    "Implementing Mobile Money (MTN MoMo & Orange Money) API gateways for instant sponsorship payouts.",
    "Developing AI talent prediction algorithms for scout matching across Cameroon."
])

add_styled_heading("GENERAL CONCLUSION", level=1)
add_body_p("The SPORTIVA CM platform successfully provides a complete, modern digital ecosystem for Cameroonian sports promotion. Built strictly according to software engineering principles (2TUP, UML, Django MTV), the platform solves core problems of visibility, event organization, equipment commerce, and sponsorship fundraising. With 27 unit tests passing cleanly and a comprehensive defense package compiled, the project demonstrates technical excellence and practical social impact.")

add_styled_heading("BIBLIOGRAPHY & WEBOGRAPHY", level=1)
add_bullet_list([
    "Mercurial 2022 Software & Hardware Estimation Standards",
    "Django 6.0 Official Documentation & Security Guidelines",
    "Unified Modeling Language (UML 2.5) Specification, Object Management Group (OMG)",
    "https://docs.djangoproject.com/ - Django Web Framework",
    "https://creately.com/blog/diagrams/uml-diagram-types-examples/ - UML Classification",
    "https://www.freecodecamp.org/news/the-model-view-controller-pattern-mvc - MVC Architecture"
])

doc.save(str(doc_path))
print(f"Full Academic Report Word Document saved successfully to: {doc_path}")
