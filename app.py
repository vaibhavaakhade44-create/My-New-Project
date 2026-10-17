from flask import Flask, request, jsonify, render_template
from contextlib import closing
from html import escape
import sqlite3
import json
import os
from datetime import datetime

import database

app = Flask(__name__)
INDEX_TEMPLATE = 'index.html'

# Initialize database
database.init_db()

QUESTIONS = [
    {
        "id": "q1",
        "question": "Python madhe list banvnyasathi konta bracket vapartat?",
        "type": "mcq",
        "options": ["Square brackets [ ]", "Curly brackets { }", "Round brackets ( )", "Angle brackets < >"],
        "correct": "Square brackets [ ]",
        "points": 5,
        "explanation": "Python lists he square brackets [ ] madhe define hotat. Udhaharana: my_list = [1, 2, 3]"
    },
    {
        "id": "q2",
        "question": "HTML cha full form kay ahe?",
        "type": "mcq",
        "options": [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Hyperlinks and Text Management Language",
            "Home Tool Markup Language"
        ],
        "correct": "Hyper Text Markup Language",
        "points": 5,
        "explanation": "HTML mhanje Hyper Text Markup Language — web pages cha structure banvnyasathi vapartat."
    },
    {
        "id": "q3",
        "question": "Frontend ani Database madhe communication kon karto?",
        "type": "mcq",
        "options": ["API / Backend Server", "Fakat CSS", "Browser Console", "Photoshop"],
        "correct": "API / Backend Server",
        "points": 5,
        "explanation": "Backend API server Frontend chi request gheun process karto ani Database madhe save karto."
    },
    {
        "id": "q4",
        "question": "CSS madhe element la center karaycha asel tar konti property vaparatat?",
        "type": "mcq",
        "options": ["margin: auto", "padding: center", "align: middle", "position: center"],
        "correct": "margin: auto",
        "points": 5,
        "explanation": "margin: auto he block elements la horizontally center karayla vapartat (width set aslyavar)."
    },
    {
        "id": "q5",
        "question": "Database madhun data kadhnyasathi konti SQL command vapartat? (One word, uppercase madhe lihा)",
        "type": "text",
        "correct": "SELECT",
        "points": 10,
        "explanation": "SELECT command vaparun apan database madhun data fetch karto. Udhaharana: SELECT * FROM students;"
    }
]

@app.route('/', methods=['GET'])
def home():
  if os.path.exists(os.path.join('templates', INDEX_TEMPLATE)):
    return render_template(INDEX_TEMPLATE)
  with open(INDEX_TEMPLATE, encoding='utf-8') as f:
        return f.read()

@app.route('/meetup', methods=['GET'])
def meetup_registration():
    return render_template('meetup_form.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    q_list = []
    for q in QUESTIONS:
        item = {"id": q["id"], "question": q["question"], "type": q["type"], "points": q["points"]}
        if q["type"] == "mcq":
            item["options"] = q["options"]
        q_list.append(item)
    return jsonify({"success": True, "questions": q_list, "total": len(q_list)})

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'success': False, 'message': 'Request body must be a JSON object.'}), 400

    name = data.get('name', '')
    email = data.get('email', '')
    answers = data.get('answers', {})

    if not isinstance(name, str) or not isinstance(email, str) or not isinstance(answers, dict):
        return jsonify({'success': False, 'message': 'Name, email, and answers have invalid formats.'}), 400

    name = name.strip()
    email = email.strip()
    if not name or not email:
        return jsonify({'success': False, 'message': 'Name ani Email required ahe!'}), 400

    total = 0
    obtained = 0
    analysis = []

    for q in QUESTIONS:
        total += q["points"]
        user_ans = str(answers.get(q["id"], '')).strip()
        if q["type"] == "text":
            correct = user_ans.lower() == q["correct"].lower()
        else:
            correct = user_ans == q["correct"]
        earned = q["points"] if correct else 0
        obtained += earned
        analysis.append({
            "id": q["id"],
            "question": q["question"],
            "user_answer": user_ans or "Uttar dile nahi",
            "correct_answer": q["correct"],
            "is_correct": correct,
            "earned": earned,
            "max": q["points"],
            "explanation": q["explanation"]
        })

    pct = round((obtained / total) * 100, 1)
    status = "Passed 🎉" if pct >= 50 else "Needs Improvement"

    database.save_submission(name, email, total, obtained, pct, status, analysis)

    return jsonify({
        "success": True,
        "name": name,
        "obtained": obtained,
        "total": total,
        "percentage": pct,
        "status": status,
        "analysis": analysis
    })

@app.route('/api/responses', methods=['GET'])
def responses():
    return jsonify(database.get_all_submissions())

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    submissions = database.get_all_submissions()
    stats = database.get_stats()
    total_candidates = stats['total_submissions']
    passed_count = stats['passed_count']
    avg_score = stats['average_score']

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Admin Dashboard | Database Submissions</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Outfit', sans-serif; }}
    body {{ background: #070913; color: #f8fafc; padding: 32px 20px; min-height: 100vh; }}
    .container {{ max-width: 1000px; margin: 0 auto; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; flex-wrap: wrap; gap: 16px; }}
    .title h1 {{ font-size: 28px; font-weight: 800; }}
    .title p {{ color: #94a3b8; font-size: 14px; margin-top: 4px; }}
    .btn {{ padding: 10px 18px; border-radius: 10px; font-weight: 600; font-size: 14px; text-decoration: none; cursor: pointer; border: none; }}
    .btn-primary {{ background: linear-gradient(135deg, #6366f1, #06b6d4); color: #fff; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }}
    .stat-card {{ background: rgba(18, 22, 38, 0.75); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; }}
    .stat-card .num {{ font-size: 32px; font-weight: 800; color: #fff; margin-bottom: 4px; }}
    .stat-card .lbl {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }}
    .table-card {{ background: rgba(18, 22, 38, 0.75); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
    th {{ background: rgba(255,255,255,0.04); padding: 16px 20px; color: #94a3b8; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.08); }}
    td {{ padding: 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #e2e8f0; }}
    tr:hover td {{ background: rgba(255,255,255,0.02); }}
    .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; }}
    .badge-pass {{ background: rgba(16, 185, 129, 0.15); color: #34d399; }}
    .badge-fail {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; }}
    .time-txt {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #64748b; }}
    .empty-msg {{ padding: 48px 20px; text-align: center; color: #64748b; font-size: 15px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title">
        <h1>📊 SQLite Database Records</h1>
        <p>Live submissions saved in <code>quiz.db</code> table <code>submissions</code></p>
      </div>
      <div style="display: flex; gap: 10px;">
        <a href="/" class="btn btn-primary">← Go to Assessment</a>
        <button onclick="location.reload()" class="btn" style="background: rgba(255,255,255,0.08); color: #fff;">🔄 Refresh</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="num">{total_candidates}</div>
        <div class="lbl">Total Submissions</div>
      </div>
      <div class="stat-card">
        <div class="num" style="color: #34d399;">{passed_count}</div>
        <div class="lbl">Passed Candidates</div>
      </div>
      <div class="stat-card">
        <div class="num" style="color: #38bdf8;">{avg_score} pts</div>
        <div class="lbl">Average Score</div>
      </div>
    </div>

    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Candidate Name</th>
            <th>Email</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Status</th>
            <th>Submission Date & Time</th>
          </tr>
        </thead>
        <tbody>'''

    if not submissions:
        html += '''
          <tr>
            <td colspan="7" class="empty-msg">No submissions recorded yet. Take the test on the home page!</td>
          </tr>'''
    else:
        for s in submissions:
            is_pass = 'Pass' in s.get('status', '')
            badge_class = 'badge-pass' if is_pass else 'badge-fail'
            html += f'''
          <tr>
            <td style="color:#64748b; font-weight:700;">#{s['id']}</td>
            <td style="font-weight:600; color:#fff;">{escape(s['student_name'])}</td>
            <td style="color:#94a3b8;">{escape(s['student_email'])}</td>
            <td><strong style="color:#38bdf8;">{s['obtained_marks']}</strong> / {s['total_marks']}</td>
            <td><strong>{s['percentage']}%</strong></td>
            <td><span class="badge {badge_class}">{escape(s['status'])}</span></td>
            <td class="time-txt">{s['submitted_at']}</td>
          </tr>'''

    html += '''
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>'''
    return html

if __name__ == '__main__':
    print("\n" + "="*55)
    print("  DevQuest Assessment Server READY!")
    print("  Assessment: http://127.0.0.1:5000")
    print("  Admin DB:   http://127.0.0.1:5000/admin")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, debug=True)

