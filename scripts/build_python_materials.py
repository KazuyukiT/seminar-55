"""Quarto原稿から演習・解答ノートブックを生成し、例を順に実行する。"""
import contextlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "lesson/python-basics.qmd").read_text()
body = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
body = re.sub(r"^:::.*$", "", body, flags=re.M)
body = re.sub(r" \{#sec-python-basics\}", "", body)
body = re.sub(r'\{download="[^"]+"\}', "", body)
lesson, answers = body.split("## 解答例と振り返り", 1)

def notebook(text, execute=False):
    cells = []
    scope = {}
    counter = 0
    for i, chunk in enumerate(re.split(r"^```python\n(.*?)^```\s*$", text, flags=re.M | re.S)):
        if not chunk.strip():
            continue
        if i % 2 == 0:
            cells.append({"cell_type": "markdown", "metadata": {}, "source": chunk.strip()})
        else:
            counter += 1
            outputs = []
            if execute:
                stream = io.StringIO()
                with contextlib.redirect_stdout(stream):
                    exec(compile(chunk, f"cell-{counter}", "exec"), scope)
                if stream.getvalue() and "sys.executable" not in chunk:
                    outputs.append({"output_type": "stream", "name": "stdout", "text": stream.getvalue()})
            cells.append({"cell_type": "code", "metadata": {}, "source": chunk.rstrip(),
                          "execution_count": counter if execute else None, "outputs": outputs})
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.9"}}, "nbformat": 4, "nbformat_minor": 4}, scope

# 演習版は解答節を含めず、学生が追記するセルを設ける。
student, _ = notebook(lesson)
for cell in student["cells"]:
    if cell["cell_type"] == "markdown":
        cell["source"] = re.sub(r"^配布ファイル：.*$", "配布ファイルは教材Webページから取得してください。", cell["source"], flags=re.M)
        cell["source"] = cell["source"].replace("[演習ノートブック](../materials/python-basics.ipynb)をダウンロードします。", "このノートブックを自分の環境に保存します。")
for number in range(1, 7):
    student["cells"].extend([
        {"cell_type": "markdown", "metadata": {}, "source": f"## 演習{number}の回答\n本文の演習に取り組み、コードと説明を追記してください。"},
        {"cell_type": "code", "metadata": {}, "source": "# ここに自分のコードを書く", "execution_count": None, "outputs": []},
    ])
student["cells"].extend([
    {"cell_type": "markdown", "metadata": {}, "source": "## 総合課題の回答\n人数・合計・平均・5時間以上の人数と割合・中央値を求めます。"},
    {"cell_type": "code", "metadata": {}, "source": "survey_hours = [2, 5, 0, 3, 10]\n# ここから集計する", "execution_count": None, "outputs": []},
    {"cell_type": "markdown", "metadata": {}, "source": "## 考察\nここに3〜5文で記入してください。\n\n## AIの利用と確認\n相談した内容、確認したことを記入してください。未使用なら未使用と記入します。"},
])
solution, scope = notebook(lesson + "\n## 解答例と振り返り" + answers, execute=True)
assert scope["n"] == 5 and scope["total"] == 20 and scope["count"] == 2
assert scope["percentage"](2, 5) == 40.0
assert scope["median"](scope["survey_hours"]) == 3
assert scope["to_minutes"](2.5) == 150.0
assert scope["selected"] == [5, 10]
target = ROOT / "materials"
target.mkdir(exist_ok=True)
for name, data in [("python-basics.ipynb", student), ("python-basics-solutions.ipynb", solution)]:
    (target / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print("全コード例を順に実行し、総合課題・関数・抽出結果を検証しました。")
print(f"演習版: {len(student['cells'])}セル / 解答版: {len(solution['cells'])}セル")
