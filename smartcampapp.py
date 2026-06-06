import os
import io
import base64
from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash

# Data Analysis Imports
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Headless web-safe server mode
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "smart_campus_synchronized_key"

# ==========================================
# CENTRALIZED DYNAMIC MEMORY (SYNCHRONIZED ACROSS LABS)
# ==========================================
GLOBAL_STUDENT_DB = {}

# Lab 7: Custom Directory Exception Scanner Node
class InvalidDirectoryError(Exception):
    pass

# ==========================================
# JINJA2 WORKSPACE HTML BLOCKS
# ==========================================
HTML_INDEX = '''{% extends "base.html" %} {% block content %}
<div class="p-5 mb-4 bg-white rounded-3 border text-center">
    <h1 class="display-4 fw-bold">Smart Campus Dashboard</h1>
    <p class="fs-5 text-muted">Mini Project Integration Framework (Labs 1 to 8 Cross-Linked Ecosystem)</p>
    <hr class="my-4">
    <p>Register student details in <strong>Lab 1</strong> to automatically seed records throughout the rest of the workspace application tabs.</p>
    <a href="/grades" class="btn btn-primary btn-lg">Step 1: Register a Student</a>
</div>
{% endblock %}'''

HTML_GRADES = '''{% extends "base.html" %} {% block content %}
<h2>Lab 1: Student ID Registration & Grade Evaluation</h2>
<div class="row">
    <div class="col-md-5">
        <div class="card p-4">
            <h5>New Student Intake Form</h5>
            <form method="POST">
                <div class="mb-3"><input type="number" name="student_id" class="form-control" placeholder="Student ID (e.g., 101)" required></div>
                <div class="mb-3"><input type="text" name="name" class="form-control" placeholder="Student Full Name" required></div>
                <div class="mb-3"><input type="number" name="score" class="form-control" step="0.1" placeholder="Exam Score (0-100)" required></div>
                <button type="submit" class="btn btn-primary w-100">Evaluate & Register Profile</button>
            </form>
        </div>
    </div>
    <div class="col-md-7">
        <div class="card p-4">
            <h5>Currently Registered Base Memory Rosters</h5>
            <div class="table-responsive">
                <table class="table table-striped border">
                    <thead>
                        <tr><th>ID</th><th>Name</th><th>Score</th><th>Grade</th><th>Remark</th></tr>
                    </thead>
                    <tbody>
                        {% for sid, info in db.items() %}
                        <tr>
                            <td><strong>{{ sid }}</strong></td>
                            <td>{{ info.name }}</td>
                            <td>{{ info.score }}</td>
                            <td><span class="badge bg-secondary">{{ info.grade }}</span></td>
                            <td><small>{{ info.remark }}</small></td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" class="text-muted text-center">No students registered in core memory yet.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

HTML_ENROLLMENT = '''{% extends "base.html" %} {% block content %}
<h2>Lab 2: Course Enrollment Management System</h2>
<div class="row">
    <div class="col-md-5">
        <div class="card p-3">
            <h5>Assign Courses to Student ID</h5>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">Select Target Profile:</label>
                    <select name="student_id" class="form-select" required>
                        <option value="">-- Choose Registered Student ID --</option>
                        {% for sid, info in db.items() %}
                        <option value="{{ sid }}">{{ sid }} - {{ info.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="mb-2"><input type="text" name="course_name" class="form-control" placeholder="Course Name (e.g. Data Structures)"></div>
                <div class="mb-2"><input type="number" name="credits" class="form-control" placeholder="Credit Value"></div>
                <button type="submit" class="btn btn-success w-100">Commit Loop Registry Entry</button>
            </form>
        </div>
    </div>
    <div class="col-md-7">
        <div class="card p-3">
            <h5>Final Student Course Allocations Output</h5>
            {% for sid, info in db.items() %}
                <div class="p-2 border rounded bg-white mb-2">
                    <h6><strong>ID {{ sid }}:</strong> {{ info.name }}</h6>
                    <ul class="mb-0">
                        {% for cname, cred in info.courses.items() %}
                            <li><small>{{ cname }} — <span class="text-primary fw-bold">{{ cred }} Credits</span></small></li>
                        {% else %}
                            <li class="text-muted"><small>No courses registered yet for this student.</small></li>
                        {% endfor %}
                    </ul>
                </div>
            {% else %}
                <p class="text-muted text-center my-3">Register profiles in Lab 1 to initialize course mapping matrices.</p>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}'''

HTML_RECORDS = '''{% extends "base.html" %} {% block content %}
<h2>Lab 3: Structural Record Layout & Event Participation Matrix</h2>
<div class="row">
    <div class="col-md-6">
        <div class="card p-3">
            <h5>Consolidated Data Structures System View</h5>
            <p class="text-muted"><small>Generated via deep runtime collection tracking lists and inner dictionaries attributes maps.</small></p>
            <pre class="bg-dark text-light p-3 rounded" style="max-height: 350px;">{{ structured_dump }}</pre>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card p-3">
            <h5>Set Event Analyzer Matrix</h5>
            <form method="POST" class="p-3 border rounded bg-white mb-3">
                <div class="mb-2">
                    <label class="form-label small fw-bold">Hackathon Participants (IDs separated by commas):</label>
                    <input type="text" name="hackathon" class="form-control form-control-sm" placeholder="101, 102, 105" value="{{ request.form.hackathon }}">
                </div>
                <div class="mb-2">
                    <label class="form-label small fw-bold">Cultural Fest Participants (IDs separated by commas):</label>
                    <input type="text" name="cultural" class="form-control form-control-sm" placeholder="102, 103, 105" value="{{ request.form.cultural }}">
                </div>
                <button type="submit" class="btn btn-info text-white btn-sm w-100">Evaluate Event Participation</button>
            </form>
            {% if sets %}
            <div class="p-3 border rounded bg-light">
                <h6 class="text-secondary fw-bold">Analysis Output Breakdown:</h6>
                <p class="mb-1"><small><strong>Specific Event - Hackathon Only Participants:</strong> {{ sets.hackathon_only }}</small></p>
                <p class="mb-1"><small><strong>Specific Event - Cultural Only Participants:</strong> {{ sets.cultural_only }}</small></p>
                <hr class="my-2">
                <p class="mb-1 text-dark"><small><strong>All Event Participants (Union):</strong> {{ sets.all_participants }}</small></p>
                <div class="alert alert-success py-1 px-2 mb-0 mt-2 small">
                    <strong>Common Event Overlapping Participants:</strong> {{ sets.common }}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}'''

HTML_SEARCH_SORT = '''{% extends "base.html" %} {% block content %}
<h2>Lab 4: Sorting and Searching of Student IDs</h2>
<div class="row">
    <div class="col-md-6">
        <div class="card p-3">
            <h5>Sorting Pipelines Summary Matrix</h5>
            <table class="table table-bordered table-sm mt-2">
                <tr><th>Original ID List Order</th><td class="font-monospace text-danger">{{ original }}</td></tr>
                <tr><th>Bubble Sorted Output Sequence</th><td class="font-monospace text-success">{{ bubble_sorted }}</td></tr>
                <tr><th>Selection Sorted Output Sequence</th><td class="font-monospace text-primary">{{ selection_sorted }}</td></tr>
            </table>
            <p class="text-muted small"><em>*Pipeline maps automatically from dynamic ID entries captured inside Lab 1 engine buffers.</em></p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card p-3">
            <h5>Search Verification Engine</h5>
            <form method="POST" class="row g-2 mb-3">
                <div class="col-8"><input type="number" name="target" class="form-control" placeholder="Target Search Student ID" required></div>
                <div class="col-4"><button type="submit" class="btn btn-dark w-100">Query ID</button></div>
            </form>
            {% if searched %}
            <div class="border rounded p-2 bg-white mb-2">
                <small class="text-muted d-block fw-bold">Linear Search Execution (Evaluated on Sorted Array Order):</small>
                <span class="text-info font-monospace small">{{ l_res }}</span>
            </div>
            <div class="border rounded p-2 bg-white">
                <small class="text-muted d-block fw-bold">Binary Search Execution (Evaluated on Sorted Array Order):</small>
                <span class="text-success font-monospace small">{{ b_res }}</span>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}'''

HTML_FEE = '''{% extends "base.html" %} {% block content %}
<h2>Lab 5: Student Fee Calculation Component</h2>
<div class="row">
    <div class="col-md-5">
        <div class="card p-3">
            <h5>Compute Profile Outflow</h5>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">Select Target Profile:</label>
                    <select name="student_id" class="form-select" required>
                        <option value="">-- Choose Registered Student ID --</option>
                        {% for sid, info in db.items() %}
                        <option value="{{ sid }}">{{ sid }} - {{ info.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="mb-2"><input type="number" name="tuition" class="form-control" placeholder="Tuition Fee (Base Required Amount)" required></div>
                <div class="mb-2"><input type="number" name="hostel" class="form-control" placeholder="Hostel Fee (Optional fallback parameter)"></div>
                <div class="mb-2"><input type="number" name="transport" class="form-control" placeholder="Transportation Fee (Optional fallback parameter)"></div>
                <button type="submit" class="btn btn-info text-white w-100">Calculate & Save Stack</button>
            </form>
        </div>
    </div>
    <div class="col-md-7">
        <div class="card p-3">
            <h5>Calculated Ledger Sheets</h5>
            <div class="table-responsive">
                <table class="table table-bordered table-striped table-sm">
                    <thead><tr><th>ID</th><th>Name</th><th>Total Payable Fee Amount</th></tr></thead>
                    <tbody>
                        {% for sid, info in db.items() %}
                        <tr>
                            <td>{{ sid }}</td>
                            <td>{{ info.name }}</td>
                            <td class="text-success fw-bold">
                                {% if info.fee > 0 %}Rs. {{ "{:,.2f}".format(info.fee) }}{% else %}Uncalculated{% endif %}
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="3" class="text-center text-muted">No student nodes initialized yet.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

HTML_FILE_HANDLING = '''{% extends "base.html" %} {% block content %}
<h2>Lab 6: Local Disk Storage & Report Processor</h2>
<div class="row mb-3">
    <div class="col-12">
        <div class="card p-3 bg-white border">
            <h5>Commit Records Payload to Secondary Storage</h5>
            <p class="text-muted small">Clicking this completely builds, serializes, and pushes active memory data tables directly into <code>academic_records.txt</code> file system strings.</p>
            <form method="POST">
                <button type="submit" class="btn btn-danger">Commit File System Build Operations</button>
            </form>
        </div>
    </div>
</div>
{% if report_generated %}
<div class="row">
    <div class="col-md-6">
        <div class="card p-3">
            <h5>Raw File Contents Display Stream (<code>academic_records.txt</code>)</h5>
            <pre class="bg-light p-3 border rounded text-monospace" style="font-size: 0.85rem;">{% for line in file_raw %}{{ line }}{% endfor %}</pre>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card p-3 bg-dark text-white border-0">
            <h5 class="text-warning">Processed Analytics Matrix Report</h5>
            <hr class="bg-warning">
            <ul>
                <li class="mb-2">Total Managed Core Student Population: <strong class="text-info fs-5">{{ report.total_students }}</strong></li>
                <li class="mb-2">Average Registry Performance Mark: <strong class="text-info fs-5">{{ report.avg_marks }}</strong></li>
                <li class="mb-2">Top Valedictorian Performance Track: 
                    <div class="p-2 border border-secondary rounded bg-secondary text-white mt-1">
                        <strong>Name:</strong> {{ report.top_student }}<br>
                        <strong>Score Metric:</strong> {{ report.top_score }}
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}'''

HTML_DIRECTORY = '''{% extends "base.html" %} {% block content %}
<h2>Lab 7: Custom Exception Architecture Scanner Directory</h2>
<div class="card p-3">
    <form method="POST">
        <div class="mb-3"><input type="text" name="path" class="form-control" placeholder="Provide absolute system target directory path..." required></div>
        <button type="submit" class="btn btn-warning fw-bold text-dark">Scan Nodes Structure</button>
    </form>
    {% if error %}
    <div class="alert alert-danger mt-3"><strong>Triggered Custom Error Catch:</strong> {{ error }}</div>
    {% endif %}
    {% if structure %}
    <h5 class="mt-3">Discovered System Architecture Node Tree Map:</h5>
    <div class="bg-white p-3 border rounded font-monospace small">
        {% for node in structure %}
        <strong>Root Folder context:</strong> {{ node.root }}<br>
        <span class="text-muted">Sub-Directories:</span> {{ node.dirs }} | <span class="text-muted">Files Context:</span> {{ node.files }}
        <hr>
        {% endfor %}
    </div>
    {% endif %}
</div>
{% endblock %}'''

# LAB 8 FIXED JINJA WORKSPACE BLOCK
HTML_ANALYTICS = '''{% extends "base.html" %} {% block content %}
<h2>Lab 8: Pandas, NumPy & Matplotlib Analytical Core Dashboard</h2>
<div class="row">
    <div class="col-12 mb-3">
        <div class="card p-3 shadow-sm">
            <h5>Performance Registration Engine</h5>
            {% if not db %}
                <p class="text-danger my-2">No students registered in Lab 1 yet. Please register profiles first.</p>
            {% else %}
                <form method="POST" action="/analytics_setup" class="row g-3 align-items-center mb-3 bg-light p-2 rounded border">
                    <div class="col-auto">
                        <label class="col-form-label fw-bold">Step 1: Set/Change 3rd Subject Name</label>
                    </div>
                    <div class="col-md-3">
                        <input type="text" name="new_subject_title" class="form-control form-control-sm" placeholder="e.g. Coding, History, Arts" value="{{ custom_sub_name }}">
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary btn-sm">Add/Update Subject Slot</button>
                    </div>
                </form>
                
                <form method="POST" action="/analytics">
                    <input type="hidden" name="active_custom_subject" value="{{ custom_sub_name }}">
                    <div class="table-responsive">
                        <table class="table table-bordered align-middle bg-white mb-2">
                            <thead class="table-light text-center">
                                <tr>
                                    <th>Student Context (ID - Name)</th>
                                    <th>Math Marks (0-100)</th>
                                    <th>Science Marks (0-100)</th>
                                    {% if custom_sub_name %}
                                        <th class="table-info">{{ custom_sub_name }} Marks (0-100)</th>
                                    {% endif %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for sid, info in db.items() %}
                                <tr>
                                    <td><strong>{{ sid }}</strong> - {{ info.name }}</td>
                                    <td>
                                        <input type="number" name="math_{{ sid }}" class="form-control form-control-sm text-center" min="0" max="100" required>
                                    </td>
                                    <td>
                                        <input type="number" name="science_{{ sid }}" class="form-control form-control-sm text-center" min="0" max="100" required>
                                    </td>
                                    {% if custom_sub_name %}
                                    <td class="table-info">
                                        <input type="number" name="custom_{{ sid }}" class="form-control form-control-sm text-center" min="0" max="100" required>
                                    </td>
                                    {% endif %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    <button type="submit" class="btn btn-success px-4">Step 2: Submit Marks & Generate Analytics Charts</button>
                </form>
            {% endif %}
        </div>
    </div>
    
    {% if computed %}
    <div class="col-md-5">
        <div class="card p-3 mb-3">
            <h5>Parsed Performance Table Overview</h5>
            <div class="table-responsive">{{ table_html | safe }}</div>
            
            <h5 class="mt-3 text-primary">Subject Top Performers</h5>
            <ul class="list-group list-group-flush small border rounded">
                {% for subject, topper in summary.items() %}
                    <li class="list-group-item"><strong>{{ subject }}</strong> Topper: <span>{{ topper.name }}</span> (Score: <strong>{{ topper.score }}</strong>)</li>
                {% endfor %}
            </ul>
        </div>
    </div>
    <div class="col-md-7">
        <div class="card p-3 mb-3 text-center">
            <h5>Graph 1: Subjects vs Average Score</h5>
            <img src="data:image/png;base64,{{ chart_avg }}" class="img-fluid border rounded mb-4" alt="Subject Averages">
            
            <h5>Graph 2: Student-Wise Performance Comparison</h5>
            <img src="data:image/png;base64,{{ chart_student }}" class="img-fluid border rounded" alt="Student Individual Breakdown">
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}'''

# ==========================================
# BACKEND ACTION ROUTING CONTROLLERS
# ==========================================

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

# LAB 1: Student ID Registration and Grade Evaluation
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == 'POST':
        try:
            student_id = int(request.form['student_id'])
            name = request.form['name'].strip()
            score = float(request.form['score'])
            
            if score >= 90: grade, remark = "A", "Excellent"
            elif score >= 80: grade, remark = "B", "Very Good"
            elif score >= 70: grade, remark = "C", "Good"
            elif score >= 50: grade, remark = "D", "Average"
            else: grade, remark = "F", "Needs Improvement"
            
            GLOBAL_STUDENT_DB[student_id] = {
                'name': name, 'score': score, 'grade': grade, 'remark': remark,
                'courses': {}, 'fee': 0.0
            }
            flash(f"Profile committed successfully for Student ID {student_id}!")
        except ValueError:
            flash("Error parsing numeric format configurations input fields values.")
            
    return render_template_string(HTML_GRADES, db=GLOBAL_STUDENT_DB)

# LAB 2: Course Enrollment System linked with Student IDs
@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():
    MAX_COURSES_LIMIT = 5
    if request.method == 'POST':
        try:
            sid = int(request.form.get('student_id', 0))
            course_name = request.form.get('course_name', '').strip()
            credits_str = request.form.get('credits', '').strip()
            
            if sid not in GLOBAL_STUDENT_DB:
                flash("Target identity assignment failed lookup reference parameter anomalies.")
                return redirect(url_for('enrollment'))
                
            if not course_name or not credits_str:
                flash("Skip Event Triggered: Invalid blank inputs parsed.")
                return redirect(url_for('enrollment'))
                
            credits = int(credits_str)
            if credits <= 0:
                flash("Skip Event Triggered: Credits count boundary violates constraints.")
                return redirect(url_for('enrollment'))
                
            if len(GLOBAL_STUDENT_DB[sid]['courses']) >= MAX_COURSES_LIMIT:
                flash(f"Break Event Triggered: Course limit cap ({MAX_COURSES_LIMIT}) reached for this student.")
                return redirect(url_for('enrollment'))
                
            GLOBAL_STUDENT_DB[sid]['courses'][course_name] = credits
            flash(f"Course '{course_name}' map synchronized to Student ID {sid}.")
        except ValueError:
            flash("Format error parsing credit configuration digits parameters.")
            
    return render_template_string(HTML_ENROLLMENT, db=GLOBAL_STUDENT_DB)

# LAB 3: Student Record Storage and Event Sets Analyzer
@app.route('/records', methods=['GET', 'POST'])
def records():
    sets_render_payload = None
    if request.method == 'POST':
        h_raw = request.form.get('hackathon', '')
        c_raw = request.form.get('cultural', '')
        
        h_set = {int(x.strip()) for x in h_raw.split(',') if x.strip().isdigit()}
        c_set = {int(x.strip()) for x in c_raw.split(',') if x.strip().isdigit()}
        
        common_set = h_set.intersection(c_set)
        all_participants = h_set.union(c_set)
        hackathon_only = h_set.difference(c_set)
        cultural_only = c_set.difference(h_set)
        
        sets_render_payload = {
            'h_set': h_set if h_set else "{Empty}",
            'c_set': c_set if c_set else "{Empty}",
            'common': common_set if common_set else "{No overlapping Student IDs detected}",
            'all_participants': all_participants if all_participants else "{No participants entered}",
            'hackathon_only': hackathon_only if hackathon_only else "{None}",
            'cultural_only': cultural_only if cultural_only else "{None}"
        }
        
    dump_list_structure = []
    for sid, info in GLOBAL_STUDENT_DB.items():
        dump_list_structure.append({
            "StudentID": sid, "Name": info['name'], "PerformanceScore": info['score'],
            "GradesArray": [info['grade']], "AssignedCoursesMap": info['courses']
        })
        
    import json
    readable_string_dump = json.dumps(dump_list_structure, indent=4)
    return render_template_string(HTML_RECORDS, structured_dump=readable_string_dump, sets=sets_render_payload)

# LAB 4: Sorting and Searching of Student IDs
@app.route('/search_sort', methods=['GET', 'POST'])
def search_sort():
    base_ids = list(GLOBAL_STUDENT_DB.keys())
    
    bubble_sorted = base_ids.copy()
    n_b = len(bubble_sorted)
    for i in range(n_b):
        for j in range(0, n_b-i-1):
            if bubble_sorted[j] > bubble_sorted[j+1]:
                bubble_sorted[j], bubble_sorted[j+1] = bubble_sorted[j+1], bubble_sorted[j]
                
    selection_sorted = base_ids.copy()
    n_s = len(selection_sorted)
    for i in range(n_s):
        min_idx = i
        for j in range(i+1, n_s):
            if selection_sorted[j] < selection_sorted[min_idx]:
                min_idx = j
        selection_sorted[i], selection_sorted[min_idx] = selection_sorted[min_idx], selection_sorted[i]
        
    searched, l_res, b_res = False, "", ""
    
    if request.method == 'POST':
        try:
            target = int(request.form['target'])
            searched = True
            
            linear_index = -1
            for i in range(len(selection_sorted)):
                if selection_sorted[i] == target:
                    linear_index = i
                    break
            if linear_index != -1:
                l_res = f"Target ID found at index pointer position {linear_index} via Linear Search."
            else:
                l_res = "Target entity not found inside array via Linear Search."
                
            low, high, binary_index = 0, len(selection_sorted) - 1, -1
            while low <= high:
                mid = (low + high) // 2
                if selection_sorted[mid] == target:
                    binary_index = mid
                    break
                elif selection_sorted[mid] < target:
                    low = mid + 1
                else:
                    high = mid - 1
            if binary_index != -1:
                b_res = f"Target ID found at layout checkpoint {binary_index} via Binary Search."
            else:
                b_res = "Target entity completely missing from binary tree calculations search space."
        except ValueError:
            flash("Invalid digits search parameters parsed.")
            
    return render_template_string(
        HTML_SEARCH_SORT, 
        original=base_ids, 
        bubble_sorted=bubble_sorted, 
        selection_sorted=selection_sorted, 
        searched=searched, l_res=l_res, b_res=b_res
    )

# LAB 5: Default Arguments Student Fee Calculation Engine
def execute_fee_calculation(tuition, hostel=0.0, transport=0.0):
    return tuition + hostel + transport

@app.route('/fee', methods=['GET', 'POST'])
def fee():
    if request.method == 'POST':
        try:
            sid = int(request.form.get('student_id', 0))
            tuition = float(request.form['tuition'])
            hostel = float(request.form['hostel']) if request.form['hostel'] else 0.0
            transport = float(request.form['transport']) if request.form['transport'] else 0.0
            
            if sid in GLOBAL_STUDENT_DB:
                total_computed = execute_fee_calculation(tuition, hostel, transport)
                GLOBAL_STUDENT_DB[sid]['fee'] = total_computed
                flash(f"Outflow payload locked for ID {sid} at amount: Rs. {total_computed}")
            else:
                flash("Target database node structural index mapping lookup failure.")
        except ValueError:
            flash("Numerical parsing mismatch exception encountered.")
            
    return render_template_string(HTML_FEE, db=GLOBAL_STUDENT_DB)

# LAB 6: File Handling Interface & Metric Report Compiler
@app.route('/file_handling', methods=['GET', 'POST'])
def file_handling():
    target_disk_path = "academic_records.txt"
    report_generated = False
    analytics_report = {}
    file_lines = []
    
    if request.method == 'POST':
        if not GLOBAL_STUDENT_DB:
            flash("Memory matrix tables blank. Feed record parameters from Lab 1 before exporting.")
            return redirect(url_for('file_handling'))
            
        with open(target_disk_path, "w") as out_stream:
            out_stream.write("ID,Name,ExamScore,AssignedGrade\n")
            for sid, payload in GLOBAL_STUDENT_DB.items():
                out_stream.write(f"{sid},{payload['name']},{payload['score']},{payload['grade']}\n")
                
        flash("Successfully generated report text arrays onto active storage disk.")
        report_generated = True
        
    if os.path.exists(target_disk_path):
        with open(target_disk_path, "r") as in_stream:
            file_lines = in_stream.readlines()
            
        scores_array = []
        top_student_name = "N/A"
        max_score_val = -1.0
        
        for line in file_lines[1:]:
            parts = line.strip().split(',')
            if len(parts) == 4:
                p_name = parts[1]
                p_score = float(parts[2])
                scores_array.append(p_score)
                if p_score > max_score_val:
                    max_score_val = p_score
                    top_student_name = p_name
                    
        if scores_array:
            analytics_report = {
                'total_students': len(scores_array),
                'avg_marks': round(sum(scores_array) / len(scores_array), 2),
                'top_student': top_student_name,
                'top_score': max_score_val
            }
            report_generated = True
            
    return render_template_string(HTML_FILE_HANDLING, report_generated=report_generated, file_raw=file_lines, report=analytics_report)

# LAB 7: Directory Scanner Tree Handling Exceptions
@app.route('/directory', methods=['GET', 'POST'])
def directory():
    structure, error_output = None, None
    if request.method == 'POST':
        target_path = request.form['path']
        try:
            if not os.path.exists(target_path) or not os.path.isdir(target_path):
                raise InvalidDirectoryError(f"User-Defined Exception: Path '{target_path}' failed directory verification attributes mapping rules.")
            
            structure = []
            for root, dirs, files in os.walk(target_path):
                structure.append({'root': root, 'dirs': dirs, 'files': files})
        except InvalidDirectoryError as custom_err:
            error_output = str(custom_err)
        except Exception as system_err:
            error_output = f"Standard OS layer intercept: {str(system_err)}"
            
    return render_template_string(HTML_DIRECTORY, structure=structure, error=error_output)


# ==========================================
# IMPROVISED LAB 8 ROUTING CORE CONTROLLERS
# ==========================================

# Endpoint helper to register the slot layout name, then display it immediately
@app.route('/analytics_setup', methods=['POST'])
def analytics_setup():
    custom_title = request.form.get('new_subject_title', '').strip()
    return render_template_string(HTML_ANALYTICS, db=GLOBAL_STUDENT_DB, computed=False, custom_sub_name=custom_title)

# Primary analytical processor engine endpoint
@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    custom_sub = request.form.get('active_custom_subject', '').strip()
    
    if request.method == 'POST':
        try:
            data_records = []
            for sid, info in GLOBAL_STUDENT_DB.items():
                record = {
                    'StudentID': sid,
                    'Student': info['name'],
                    'Math': float(request.form.get(f'math_{sid}', 0)),
                    'Science': float(request.form.get(f'science_{sid}', 0))
                }
                if custom_sub:
                    record[custom_sub] = float(request.form.get(f'custom_{sid}', 0))
                    
                data_records.append(record)
            
            if not data_records:
                flash("No records detected inside parameters matrix.")
                return render_template_string(HTML_ANALYTICS, db=GLOBAL_STUDENT_DB, computed=False, custom_sub_name=custom_sub)
            
            df = pd.DataFrame(data_records)
            
            active_subjects = ['Math', 'Science']
            if custom_sub:
                active_subjects.append(custom_sub)
                
            subject_averages = [round(np.mean(df[sub]), 2) for sub in active_subjects]
            
            summary_metrics = {}
            for sub in active_subjects:
                top_idx = df[sub].idxmax()
                summary_metrics[sub] = {
                    'name': df.loc[top_idx]['Student'],
                    'score': df.loc[top_idx][sub]
                }
            
            # --- GRAPH 1: SUBJECTS VS AVERAGE SCORE ---
            plt.figure(figsize=(5, 4))
            bar_colors = ['teal', 'crimson', 'purple'][:len(active_subjects)]
            plt.bar(active_subjects, subject_averages, color=bar_colors, alpha=0.85, width=0.4)
            plt.title('Graph 1: Subject vs Average Score')
            plt.ylabel('Average Performance Mark')
            for i, val in enumerate(subject_averages):
                plt.text(i, val + 1, str(val), ha='center', fontweight='bold')
            plt.tight_layout()
            
            buf_avg = io.BytesIO()
            plt.savefig(buf_avg, format='png')
            buf_avg.seek(0)
            base64_avg = base64.b64encode(buf_avg.getvalue()).decode('utf-8')
            plt.close()
            
            # --- GRAPH 2: STUDENT PERFORMANCE IN ALL SUBJECTS ---
            plt.figure(figsize=(7, 4))
            x_positions = np.arange(len(df['Student']))
            bar_width = 0.25 if custom_sub else 0.35
            
            if len(active_subjects) == 3:
                plt.bar(x_positions - bar_width, df['Math'], bar_width, label='Math Marks', color='teal', alpha=0.9)
                plt.bar(x_positions, df['Science'], bar_width, label='Science Marks', color='crimson', alpha=0.9)
                plt.bar(x_positions + bar_width, df[custom_sub], bar_width, label=f'{custom_sub} Marks', color='purple', alpha=0.9)
            else:
                plt.bar(x_positions - bar_width/2, df['Math'], bar_width, label='Math Marks', color='teal', alpha=0.9)
                plt.bar(x_positions + bar_width/2, df['Science'], bar_width, label='Science Marks', color='crimson', alpha=0.9)
                
            plt.title('Graph 2: Individual Performance Comparison')
            plt.xlabel('Registered Roster Student Profiles')
            plt.ylabel('Marks Scored (0-100)')
            plt.xticks(x_positions, df['Student'])
            plt.legend()
            plt.tight_layout()
            
            buf_student = io.BytesIO()
            plt.savefig(buf_student, format='png')
            buf_student.seek(0)
            base64_student = base64.b64encode(buf_student.getvalue()).decode('utf-8')
            plt.close()
            
            dataframe_html_matrix = df.to_html(classes="table table-striped table-hover table-bordered table-sm text-center", index=False)
            return render_template_string(HTML_ANALYTICS, db=GLOBAL_STUDENT_DB, computed=True, summary=summary_metrics, table_html=dataframe_html_matrix, chart_avg=base64_avg, chart_student=base64_student, custom_sub_name=custom_sub)
            
        except Exception as err:
            flash(f"Analytical operational logic mismatch exception: {str(err)}")
            return render_template_string(HTML_ANALYTICS, db=GLOBAL_STUDENT_DB, computed=False, custom_sub_name=custom_sub)
            
    return render_template_string(HTML_ANALYTICS, db=GLOBAL_STUDENT_DB, computed=False, custom_sub_name=custom_sub)

if __name__ == '__main__':
    app.run(debug=True, port=5000)