import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Initialize a crisp, report-ready canvas
fig, ax = plt.subplots(figsize=(10, 12), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Helper function to draw neat process blocks
def draw_box(ax, text, x, y, w, h, fillcolor="#E0F2FE", shape="rect"):
    if shape == "ellipse":
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", 
                                     linewidth=1.5, edgecolor="#111827", facecolor=fillcolor)
    else:
        box = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor="#111827", facecolor=fillcolor)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, 
            fontname='sans-serif', color='#111827', wrap=True)

# Helper function to draw directional pipeline arrows
def draw_arrow(ax, x1, y1, x2, y2, text=""):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#4B5563", lw=1.5, mutation_scale=15))
    if text:
        ax.text((x1 + x2)/2 + 0.1, (y1 + y2)/2, text, fontsize=8, color="#4B5563", fontname='sans-serif')

# --- DRAWING ARCHITECTURAL FLOW BLOCKS ---

# Start Node
draw_box(ax, "START:\nLaunch app.py", 3.75, 11.0, 2.5, 0.6, fillcolor="#10B981", shape="ellipse")

# System Setup Node
draw_box(ax, "Initialize Flask Web Server\n& Shared Global Database\n(GLOBAL_STUDENT_DB)", 2.5, 9.7, 5.0, 0.8, fillcolor="#F3F4F6")

# Central Workspace Dashboard Router
draw_box(ax, "Render Central Dashboard\n(Synchronized UI Workspace Layout)", 2.5, 8.4, 5.0, 0.7, fillcolor="#F3F4F6")

# Sequential Module Processing Blocks
draw_box(ax, "LAB 1 & 2: Student Intake & Enrollment\n- Evaluates Conditional Grades (A to F)\n- Maps Course Enrollment Loops (Cap Limit 5)\n- Seeds GLOBAL_STUDENT_DB Shared Memory Matrix", 1.5, 6.7, 7.0, 1.1, fillcolor="#E0F2FE")

draw_box(ax, "LAB 3 & 5: Structural Processing & Fees\n- Formats Nested Collections JSON Structural Dump\n- Evaluates Event Sets Matrix (Union, Overlap, Unique)\n- Computes Multi-Tier Accounting via Default Arguments", 1.5, 5.0, 7.0, 1.1, fillcolor="#FEF3C7")

draw_box(ax, "LAB 4: Searching & Sorting Pipelines\n- Copies Memory State Arrays to Isolate Sequences\n- Performs Algorithmic Bubble Sort & Selection Sort\n- Traces Linear & Binary Search Index Match Pointers", 1.5, 3.3, 7.0, 1.1, fillcolor="#FCE7F3")

draw_box(ax, "LAB 6 & 7: Storage Systems & Security\n- Serializes Local Disk Strings to 'academic_records.txt'\n- Parses File Streams to Extract Metric Valedictorian Reports\n- Runs os.walk() Trees inside Custom Try/Except Nodes", 1.5, 1.6, 7.0, 1.1, fillcolor="#E0F2FE")

draw_box(ax, "LAB 8: Scientific Data Visualization Engine\n- Dynamically Binds Custom 3rd Subject Column\n- Builds Pandas DataFrame Arrays & NumPy Statistical Averages\n- Headless Matplotlib Generates Subplots (Avg & Performance)", 1.5, -0.1, 7.0, 1.1, fillcolor="#D1FAE5")

# Render Cycle Block
draw_box(ax, "Convert Plots to Base64\n& Render Dynamic Layout View", 2.5, -1.3, 5.0, 0.7, fillcolor="#10B981")

# --- CONNECTING THE SYSTEM PIPELINES (ARROWS) ---
draw_arrow(ax, 5.0, 11.0, 5.0, 10.5)
draw_arrow(ax, 5.0, 9.7, 5.0, 9.1)
draw_arrow(ax, 5.0, 8.4, 5.0, 7.8, text="Step 1: Ingest Profiles")
draw_arrow(ax, 5.0, 6.7, 5.0, 6.1, text="Step 2: Enrich Entities")
draw_arrow(ax, 5.0, 5.0, 5.0, 4.4, text="Step 3: Sort & Search")
draw_arrow(ax, 5.0, 3.3, 5.0, 2.7, text="Step 4: Backup & Validate")
draw_arrow(ax, 5.0, 2.6, 5.0, 1.0, text="Step 5: Process Analytics")
draw_arrow(ax, 5.0, -0.1, 5.0, -0.6)

# Return Loop to Central System
ax.annotate('', xy=(2.5, 8.75), xytext=(2.5, -0.95),
            arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.5, connectionstyle="bar,angle=180,fraction=-0.28"))
ax.text(0.3, 3.8, "Event-Driven UI Update Loop", rotation=90, fontsize=9, fontweight='bold', color="#10B981")

# Adjust canvas framing and output to disk file
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
plt.savefig("flowchart.png", bbox_inches='tight', dpi=300)
print("Flowchart compiled successfully! Check your local folder for 'flowchart.png'.")