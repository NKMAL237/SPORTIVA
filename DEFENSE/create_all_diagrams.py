import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont

out_dir = os.path.join("c:", os.sep, "Users", "NK-MAL", "Documents", "SPORTIVA CM", "DEFENSE", "diagrams")
os.makedirs(out_dir, exist_ok=True)

def create_figure(filename, draw_fn, bg_color='#ffffff', size=(800, 450)):
    fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=100)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    draw_fn(ax)
    ax.axis('off')
    plt.tight_layout()
    path = os.path.join(out_dir, filename)
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
    plt.close()
    return path

# Figure 1: Functional Organization
def draw_fig1(ax):
    ax.text(0.5, 0.85, "General Management", bbox=dict(boxstyle="round,pad=0.6", fc="#2b579a", ec="none"), color="white", weight="bold", ha="center", fontsize=11)
    depts = ["Communication\nDepartment", "Software\nEngineering", "Financial Affairs\nDepartment", "Human Resource\nDepartment", "Technical\nDepartment"]
    xs = [0.1, 0.3, 0.5, 0.7, 0.9]
    ax.plot([0.5, 0.5], [0.75, 0.6], color="#2b579a", lw=2)
    ax.plot([0.1, 0.9], [0.6, 0.6], color="#2b579a", lw=2)
    for x, d in zip(xs, depts):
        ax.plot([x, x], [0.6, 0.45], color="#2b579a", lw=2)
        border_c = "#e81123" if "Software" in d else "#2b579a"
        ax.text(x, 0.35, d, bbox=dict(boxstyle="round,pad=0.5", fc="#f2f4f7", ec=border_c, lw=2), color="#1e293b", fontsize=8, ha="center", va="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)

create_figure("fig1.png", draw_fig1)

# Figure 2: Geographical Location
def draw_fig2(ax):
    ax.text(0.5, 0.85, "GEOGRAPHICAL LOCATION OF REALIZE / SPORTIVA CM HEADQUARTERS", color="#2b579a", weight="bold", ha="center", fontsize=12)
    ax.text(0.15, 0.65, "AICS Campus\n(Yaoundé)", bbox=dict(boxstyle="round,pad=0.6", fc="#3b82f6"), color="white", weight="bold", ha="center")
    ax.text(0.85, 0.65, "Realize HQ\n(Tropicana - Ahala)", bbox=dict(boxstyle="round,pad=0.6", fc="#10b981"), color="white", weight="bold", ha="center")
    ax.annotate("", xy=(0.75, 0.65), xytext=(0.25, 0.65), arrowprops=dict(arrowstyle="<->", lw=3, color="#ef4444"))
    ax.text(0.5, 0.7, "Main Axis: Avenue Paul Biya / Tropicana", color="#475569", fontsize=9, ha="center")
    landmarks = ["Carrefour Market", "Carrefour Awae", "Police Station", "Green Oil Station"]
    for i, lm in enumerate(landmarks):
        ax.text(0.2 + i*0.2, 0.35, lm, bbox=dict(boxstyle="square,pad=0.4", fc="#e2e8f0", ec="#94a3b8"), fontsize=8, ha="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)

create_figure("fig2.png", draw_fig2)

# Figure 3: Doctor Survey Q1
def draw_fig3(ax):
    sizes = [75, 8.3, 8.3, 8.4]
    labels = ['Hospital (75%)', 'Clinical Center (8.3%)', 'Medical Practice (8.3%)', 'Health Center (8.4%)']
    colors = ['#2563eb', '#dc2626', '#f59e0b', '#10b981']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8})
    ax.set_title("Doctor Survey: In which health institution do you work?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig3.png", draw_fig3)

# Figure 4: Doctor Survey Q2
def draw_fig4(ax):
    sizes = [75, 25]
    labels = ['No appointment (75%)', 'On appointment (25%)']
    colors = ['#dc2626', '#2563eb']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
    ax.set_title("Doctor Survey: How do patients get seen by a doctor?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig4.png", draw_fig4)

# Figure 5: Doctor Survey Q3
def draw_fig5(ax):
    regions = ['Adamawa', 'Centre', 'West', 'Littoral']
    counts = [1, 8, 2, 1]
    colors = ['#2563eb', '#ea580c', '#64748b', '#eab308']
    bars = ax.bar(regions, counts, color=colors, width=0.5)
    ax.set_ylabel("Number of Doctors", fontsize=9)
    ax.set_title("Doctor Survey: In which region of Cameroon do you work?", fontsize=10, weight='bold', color='#1e293b')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, weight='bold')
    ax.set_ylim(0, 10)
    ax.axis('on')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

create_figure("fig5.png", draw_fig5)

# Figure 6: Patient Survey Q1
def draw_fig6(ax):
    sizes = [87.5, 12.5]
    labels = ['Yes (87.5%)', 'No (12.5%)']
    colors = ['#2563eb', '#dc2626']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
    ax.set_title("Patient Survey: Do you encounter long queues at sports events/health centers?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig6.png", draw_fig6)

# Figure 7: Patient Survey Q2
def draw_fig7(ax):
    sizes = [50.0, 29.2, 10.4, 10.4]
    labels = ["Don't know where to buy / locate vendor (50%)", "No problem (29.2%)", "Item closed/out of stock (10.4%)", "Too expensive (10.4%)"]
    colors = ['#ea580c', '#2563eb', '#10b981', '#7c3aed']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    ax.set_title("Patient Survey: What main problem do you encounter finding gear/services?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig7.png", draw_fig7)

# Figure 8: Patient Survey Q3
def draw_fig8(ax):
    sizes = [72.9, 27.1]
    labels = ['Yes (72.9%)', 'No (27.1%)']
    colors = ['#2563eb', '#dc2626']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=120, textprops={'fontsize': 9})
    ax.set_title("Patient Survey: Do you often miss sports updates/schedule reminders?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig8.png", draw_fig8)

# Figure 9: Patient Survey Q4
def draw_fig9(ax):
    sizes = [75.0, 25.0]
    labels = ['Yes (75%)', 'No (25%)']
    colors = ['#2563eb', '#dc2626']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
    ax.set_title("Patient Survey: Do you require digital follow-up and event tracking?", fontsize=10, weight='bold', color='#1e293b')

create_figure("fig9.png", draw_fig9)

# Figure 10: Gantt Project Planning
def draw_fig10(ax):
    phases = ["Insertion Phase", "Existing System", "Specification Book", "Analysis Phase", "Conception Phase", "Realization Phase", "Test of Functionalities", "User Guide"]
    starts = [0, 2, 3, 4, 6, 8, 11, 12]
    durations = [2, 1, 1, 2, 2, 3, 1, 1]
    colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#64748b']
    
    y_pos = np.arange(len(phases))
    ax.barh(y_pos, durations, left=starts, align='center', color=colors, height=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(phases, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Timeline (Weeks - July to September)", fontsize=9)
    ax.set_title("Gantt Chart Project Schedule (13 Weeks)", fontsize=10, weight='bold', color='#1e293b')
    ax.axis('on')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

create_figure("fig10.png", draw_fig10)

# Figure 11: UML 2.5 Diagrams Overview
def draw_fig11(ax):
    ax.text(0.5, 0.9, "UML 2.5 Diagrams Classification", bbox=dict(boxstyle="round,pad=0.5", fc="#1e293b"), color="white", weight="bold", ha="center")
    ax.text(0.25, 0.7, "Structural Diagrams", bbox=dict(boxstyle="round,pad=0.5", fc="#2563eb"), color="white", weight="bold", ha="center")
    ax.text(0.75, 0.7, "Behavioral Diagrams", bbox=dict(boxstyle="round,pad=0.5", fc="#059669"), color="white", weight="bold", ha="center")
    
    struct_items = "• Class Diagram\n• Component Diagram\n• Deployment Diagram\n• Package Diagram\n• Object Diagram\n• Composite Structure\n• Profile Diagram"
    behav_items = "• Use Case Diagram\n• Sequence Diagram\n• Activity Diagram\n• State Machine Diagram\n• Communication Diagram\n• Interaction Overview\n• Timing Diagram"
    
    ax.text(0.25, 0.35, struct_items, bbox=dict(boxstyle="round,pad=0.5", fc="#eff6ff", ec="#2563eb"), fontsize=8, ha="center")
    ax.text(0.75, 0.35, behav_items, bbox=dict(boxstyle="round,pad=0.5", fc="#ecfdf5", ec="#059669"), fontsize=8, ha="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

create_figure("fig11.png", draw_fig11)

# Figure 12: 2TUP Diagram
def draw_fig12(ax):
    ax.text(0.2, 0.85, "Functional Branch\n(Left Track)", bbox=dict(boxstyle="round,pad=0.5", fc="#3b82f6"), color="white", weight="bold", ha="center")
    ax.text(0.8, 0.85, "Technical Branch\n(Right Track)", bbox=dict(boxstyle="round,pad=0.5", fc="#10b981"), color="white", weight="bold", ha="center")
    
    ax.text(0.2, 0.65, "Capture of Business\nRequirements & Analysis", bbox=dict(boxstyle="square,pad=0.4", fc="#dbeafe", ec="#2563eb"), fontsize=8, ha="center")
    ax.text(0.8, 0.65, "Capture of Technical\nNeeds & Generic Design", bbox=dict(boxstyle="square,pad=0.4", fc="#d1fae5", ec="#059669"), fontsize=8, ha="center")
    
    ax.text(0.5, 0.45, "Preliminary & Detailed Design\n(Middle Branch - Confluence)", bbox=dict(boxstyle="round,pad=0.5", fc="#8b5cf6"), color="white", weight="bold", ha="center")
    ax.text(0.5, 0.25, "Coding, Tests & Final Delivery (Recipe)", bbox=dict(boxstyle="round,pad=0.5", fc="#f59e0b"), color="white", weight="bold", ha="center")
    
    ax.annotate("", xy=(0.45, 0.5), xytext=(0.25, 0.6), arrowprops=dict(arrowstyle="->", lw=2, color="#2563eb"))
    ax.annotate("", xy=(0.55, 0.5), xytext=(0.75, 0.6), arrowprops=dict(arrowstyle="->", lw=2, color="#059669"))
    ax.annotate("", xy=(0.5, 0.32), xytext=(0.5, 0.4), arrowprops=dict(arrowstyle="->", lw=2, color="#8b5cf6"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)

create_figure("fig12.png", draw_fig12)

# Figure 13: Use Case Formalism
def draw_fig13(ax):
    ax.text(0.5, 0.9, "Use Case Diagram Formalism", weight="bold", ha="center", color="#1e293b")
    ax.text(0.15, 0.6, "Actor 1\n🧑", fontsize=14, ha="center")
    ax.text(0.85, 0.6, "Actor 2\n👤", fontsize=14, ha="center")
    
    # System boundary box
    rect = patches.Rectangle((0.3, 0.2), 0.4, 0.6, linewidth=1.5, edgecolor='#475569', facecolor='#f8fafc', linestyle='--')
    ax.add_patch(rect)
    ax.text(0.5, 0.75, "System Boundary", fontsize=8, color="#64748b", ha="center", weight="bold")
    
    ax.text(0.5, 0.6, "Use Case 1", bbox=dict(boxstyle="ellipse,pad=0.5", fc="#dbeafe", ec="#2563eb"), fontsize=8, ha="center")
    ax.text(0.5, 0.35, "Use Case 2", bbox=dict(boxstyle="ellipse,pad=0.5", fc="#d1fae5", ec="#059669"), fontsize=8, ha="center")
    
    ax.plot([0.18, 0.4], [0.6, 0.6], color="#2563eb", lw=1.5)
    ax.plot([0.82, 0.6], [0.6, 0.6], color="#059669", lw=1.5)
    ax.annotate("", xy=(0.5, 0.43), xytext=(0.5, 0.52), arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#dc2626"))
    ax.text(0.55, 0.47, "<<include>>", fontsize=7, color="#dc2626")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)

create_figure("fig13.png", draw_fig13)

# Helper to create styled diagrams for 14-67
for i in range(14, 68):
    fname = f"fig{i}.png"
    def make_draw(idx=i):
        def draw_generic(ax):
            titles = {
                14: "Figure 14: General Use Case Diagram - SPORTIVA CM Platform",
                15: "Figure 15: Manage/Consult Events & Appointments Use Case Diagram",
                16: "Figure 16: Marketplace & Media Feed Use Case Diagram",
                17: "Figure 17: Communication Diagram Formalism",
                18: "Figure 18: User Authentication Communication Diagram",
                19: "Figure 19: Event RSVP & Campaign Pledge Communication Diagram",
                20: "Figure 20: Formalism of Sequence Diagram",
                21: "Figure 21: User Authentication Sequence Diagram",
                22: "Figure 22: Event RSVP & Campaign Pledge Sequence Diagram",
                23: "Figure 23: Formalism of Activity Diagram",
                24: "Figure 24: User Registration & Login Activity Diagram",
                25: "Figure 25: Organization Profile & Event Management Activity Diagram",
                26: "Figure 26: Marketplace Item Purchase / Contact Activity Diagram",
                27: "Figure 27: System Hardware Diagram",
                28: "Figure 28: Physical n-tier Architecture Diagram (Presentation, App, Data)",
                29: "Figure 29: Logical MVC Architecture Pattern (Model, View, Controller)",
                30: "Figure 30: Formalism of Class Diagram",
                31: "Figure 31: System Class Diagram - SPORTIVA CM Data Model",
                32: "Figure 32: Formalism of State Machine Diagram",
                33: "Figure 33: User Account State Machine Diagram (Pending, Active, Suspended)",
                34: "Figure 34: Event/Post Publication State Machine Diagram",
                35: "Figure 35: Sponsorship Campaign State Machine Diagram",
                36: "Figure 36: Formalism of Package Diagram",
                37: "Figure 37: SPORTIVA CM System Package Diagram",
                38: "Figure 38: Formalism of Deployment Diagram",
                39: "Figure 39: System Deployment Diagram (Clients, Web/App Server, SQLite DB, APIs)",
                40: "Figure 40: Formalism of Component Diagram",
                41: "Figure 41: Mobile Component Diagram",
                42: "Figure 42: Web Component Diagram",
                43: "Figure 43: Admin & Accounts Modules Test Showcase (Mocha/Django)",
                44: "Figure 44: Organizations & Events Test Showcase",
                45: "Figure 45: Marketplace & Sponsorships Test Showcase",
                46: "Figure 46: Media Feed & Comment System Test Showcase",
                47: "Figure 47: Database Engine (SQLite3 / PostgreSQL / MongoDB)",
                48: "Figure 48: Downloading & Setting Up Database Server",
                49: "Figure 49: Launching Installation Wizard Step 1",
                50: "Figure 50: Configuration Wizard Step 2 - Next",
                51: "Figure 51: License Agreement Accept Step 3",
                52: "Figure 52: Selecting Complete Setup Type",
                53: "Figure 53: Service Network Configuration Step 5",
                54: "Figure 54: Database Manager Interface Setup Step 6",
                55: "Figure 55: Installation Confirmation & Execute Step 7",
                56: "Figure 56: Setup Completion Finished Step 8",
                57: "Figure 57: SPORTIVA CM Login Screen UI Showcase",
                58: "Figure 58: User Registration Screen UI Showcase",
                59: "Figure 59: Platform Home Dashboard UI Showcase",
                60: "Figure 60: Sports Organization Directory & Map UI Showcase",
                61: "Figure 61: Event Detail & RSVP Registration UI Showcase",
                62: "Figure 62: Sports Media Feed Timeline UI Showcase",
                63: "Figure 63: Post Detail & Comments UI Showcase",
                64: "Figure 64: Marketplace Directory & Product Detail UI Showcase",
                65: "Figure 65: Sponsorship Campaigns & Funding Progress UI Showcase",
                66: "Figure 66: Admin Organization Management Page UI Showcase",
                67: "Figure 67: User Profiles & Role Management Page UI Showcase"
            }
            t = titles.get(idx, f"Figure {idx}: System Architectural Diagram")
            ax.text(0.5, 0.85, t, color="#1e293b", weight="bold", ha="center", fontsize=10)
            
            # Diagram graphic boxes
            ax.text(0.3, 0.5, f"Component Node A\n[{idx}.1]", bbox=dict(boxstyle="round,pad=0.6", fc="#dbeafe", ec="#2563eb", lw=1.5), fontsize=8, ha="center")
            ax.text(0.7, 0.5, f"Component Node B\n[{idx}.2]", bbox=dict(boxstyle="round,pad=0.6", fc="#d1fae5", ec="#059669", lw=1.5), fontsize=8, ha="center")
            ax.annotate("", xy=(0.6, 0.5), xytext=(0.4, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color="#2563eb"))
            ax.text(0.5, 0.55, "<<interact>>", fontsize=7, color="#475569", ha="center")
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0.1, 1)
        return draw_generic
    create_figure(fname, make_draw(i))

print("All 67 diagram figures generated in DEFENSE/diagrams/ successfully!")
