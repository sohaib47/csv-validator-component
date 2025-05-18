# src/csv_validator/reporter.py

import json
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CSV Validation Report</title>
  <style>
    body { font-family: sans-serif; padding: 2rem; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    thead th {
      position: sticky;
      top: 0;
      background: #f0f0f0;
      z-index: 1;
    }
    tbody tr:nth-child(odd) { background: #fafafa; }
    tbody tr:hover { background: #f1f7ff; }
  </style>
</head>
<body>
  <h1>CSV Validation Report</h1>
  {% if errors %}
    <table>
      <thead>
        <tr>
          <th style="width: 80px">Row</th>
          <th>Errors</th>
        </tr>
      </thead>
      <tbody>
      {% for row, errs in errors.items()|sort %}
        <tr>
          <td>{{ row }}</td>
          <td>
            <ul>
              {% for e in errs %}
                <li>{{ e }}</li>
              {% endfor %}
            </ul>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p><strong>No validation errors found.</strong></p>
  {% endif %}
</body>
</html>
"""

class Reporter:
    @staticmethod
    def write_reports(errors: dict, prefix: str):
        # JSON report
        with open(f"{prefix}.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2)
        # HTML report
        tmpl = Template(HTML_TEMPLATE)
        html = tmpl.render(errors=errors)
        with open(f"{prefix}.html", "w", encoding="utf-8") as f:
            f.write(html)
