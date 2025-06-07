from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import ast
import matplotlib.pyplot as plt
import tempfile
import os
import zipfile
from collections import defaultdict, Counter
from datetime import datetime
from fastapi.responses import JSONResponse


app = FastAPI()

def analyze_python_code(code, filename):
    tree = ast.parse(code)
    function_lengths = []
    issues = defaultdict(list)
    assigned_vars = {}
    used_vars = set()
    lines = code.splitlines()

    # Track file length
    if len(lines) > 200:
        issues["File Length"].append(f"{filename}: File is longer than 200 lines ({len(lines)})")

    # Collect function info
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = max(
                [child.lineno for child in ast.walk(node) if hasattr(child, "lineno")],
                default=start_line
            )
            length = end_line - start_line + 1
            function_lengths.append(length)
            if length > 20:
                issues["Function Length"].append(f"{filename}: Function '{node.name}' is too long ({length} lines)")
            if not ast.get_docstring(node):
                issues["Missing Docstrings"].append(f"{filename}: Function '{node.name}' missing docstring")
            # Track assigned vars in function
            for n in ast.walk(node):
                if isinstance(n, ast.Assign):
                    for target in n.targets:
                        if isinstance(target, ast.Name):
                            assigned_vars[target.id] = node.name
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    used_vars.add(n.id)

    # Check for unused variables
    for var, func in assigned_vars.items():
        if var not in used_vars:
            issues["Unused Variables"].append(f"{filename}: Variable '{var}' assigned in function '{func}' but never used")

    return function_lengths, issues

def plot_histogram(function_lengths, out_path):
    plt.figure(figsize=(8,6))
    plt.hist(function_lengths, bins=range(1, max(function_lengths)+2), edgecolor='black')
    plt.title("Histogram of Function Lengths")
    plt.xlabel("Function Length (lines)")
    plt.ylabel("Number of Functions")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_pie(issue_counts, out_path):
    plt.figure(figsize=(6,6))
    labels = list(issue_counts.keys())
    sizes = list(issue_counts.values())
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Issue Types Distribution")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_bar(issues_per_file, out_path):
    plt.figure(figsize=(10,6))
    files = list(issues_per_file.keys())
    counts = list(issues_per_file.values())
    plt.bar(files, counts, color='skyblue')
    plt.title("Number of Issues per File")
    plt.xlabel("File Name")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_line(issue_history, out_path):
    # issue_history: list of (date, count)
    if not issue_history:
        return
    issue_history = sorted(issue_history)
    dates, counts = zip(*issue_history)
    plt.figure(figsize=(8,5))
    plt.plot(dates, counts, marker='o')
    plt.title("Number of Issues Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Issues")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = file.filename
    if not filename.endswith(".py"):
        return {"error": "Only Python (.py) files are supported."}
    code = (await file.read()).decode("utf-8")

    # Analyze code
    function_lengths, issues = analyze_python_code(code, filename)

    # Prepare data for graphs
    issue_counts = {k: len(v) for k, v in issues.items()}
    total_issues = sum(issue_counts.values())
    issues_per_file = Counter()
    for k, v in issues.items():
        for item in v:
            # Extract file name from issue description
            fname = item.split(":")[0]
            issues_per_file[fname] += 1

    tempdir = tempfile.mkdtemp()
    # Histogram
    hist_path = os.path.join(tempdir, "histogram.png")
    plot_histogram(function_lengths, hist_path)
    # Pie
    pie_path = os.path.join(tempdir, "pie.png")
    plot_pie(issue_counts, pie_path)
    # Bar
    bar_path = os.path.join(tempdir, "bar.png")
    plot_bar(issues_per_file, bar_path)
    # Bonus: line chart (simulate history, usually you'd load from DB)
    line_path = os.path.join(tempdir, "line.png")
    # Example - current time and total issues
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    issue_history = [(now, total_issues)]
    plot_line(issue_history, line_path)

    # Create zip with all graphs
    zip_path = os.path.join(tempdir, "graphs.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(hist_path, "histogram.png")
        zipf.write(pie_path, "pie.png")
        zipf.write(bar_path, "bar.png")
        zipf.write(line_path, "line.png")

    # Optionally: create a text file with all issues
    issues_txt = os.path.join(tempdir, "issues.txt")
    with open(issues_txt, "w", encoding="utf-8") as f:
        for k, v in issues.items():
            f.write(f"--- {k} ---\n")
            for msg in v:
                f.write(msg + "\n")
            f.write("\n")
    with zipfile.ZipFile(zip_path, "a") as zipf:
        zipf.write(issues_txt, "issues.txt")

    return FileResponse(zip_path, filename="analysis_graphs.zip", media_type="application/zip")


@app.post("/alerts")
async def alerts(file: UploadFile = File(...)):
    filename = file.filename
    if not filename.endswith(".py"):
        return JSONResponse({"error": "Only Python (.py) files are supported."}, status_code=400)
    code = (await file.read()).decode("utf-8")

    # Analyze code
    _, issues = analyze_python_code(code, filename)

    # Write issues to a temporary text file
    import tempfile, os
    tempdir = tempfile.mkdtemp()
    issues_txt = os.path.join(tempdir, "issues.txt")
    with open(issues_txt, "w", encoding="utf-8") as f:
        for k, v in issues.items():
            f.write(f"--- {k} ---\n")
            for msg in v:
                f.write(msg + "\n")
            f.write("\n")

    return FileResponse(issues_txt, filename="issues.txt", media_type="text/plain")
