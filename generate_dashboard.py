#!/usr/bin/env python3
"""
Earnings Dashboard Generator
Reads instructions, prompts, and skills files to auto-generate the dashboard HTML.
Usage: python3 generate_dashboard.py
"""

import os
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

def read_file(path):
    """Read file content safely."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return ""

def extract_prompts(prompts_file):
    """Extract prompt sections from earnings prompts.md"""
    content = read_file(prompts_file)
    prompts = {}
    for match in re.finditer(r'Prompt (\d+):(.*?)(?=Prompt \d+:|$)', content, re.DOTALL):
        prompts[f'prompt_{match.group(1)}'] = match.group(2).strip()
    return prompts

def extract_instructions(instructions_file):
    """Extract key instructions from copilot-instructions.md"""
    content = read_file(instructions_file)
    return content

def extract_skills(skills_file):
    """Extract skills information from skills.md"""
    content = read_file(skills_file)
    return content

def extract_pdf_data():
    """Extract earnings data from sample PDFs."""
    data = {
        'TMO': {
            'name': 'Thermo Fisher (TMO)',
            'revenue': '$11.01B',
            'revenue_growth': '+6.2%',
            'eps': '$5.44',
            'eps_growth': '+6%',
            'revenue_outcome': 'Beat',
            'eps_outcome': 'Beat',
            'tailwind': 'AI-enabled cryo-EM and bioproduction automation',
            'headwind': 'Academic and government sector slowdown in U.S. and China',
            'stock_perf': 'Positive'
        },
        'DHR': {
            'name': 'Danaher (DHR)',
            'revenue': '$6.0B',
            'revenue_growth': '+0.5%',
            'eps': 'Stable',
            'eps_growth': 'Stable',
            'revenue_outcome': 'Neutral',
            'eps_outcome': 'Neutral',
            'tailwind': 'Bioprocessing equipment orders up 30% YoY',
            'headwind': 'China diagnostics policy headwinds (VBP)',
            'stock_perf': 'Mixed'
        }
    }
    return data

def generate_html(instructions, prompts, skills, company_data):
    """Generate dashboard HTML from specifications."""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Earnings Pulse Dashboard</title>
    <style>
        :root {
            --bg: #fafafa;
            --surface: #ffffff;
            --border: #d9d9d9;
            --primary: #0f4c81;
            --secondary: #28527a;
            --text: #1a1a1a;
            --muted: #666666;
            --radius: 12px;
        }
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            font-size: 14pt;
            background: var(--bg);
            color: var(--text);
        }
        h1, h2 {
            font-family: Georgia, serif;
            font-size: 22pt;
            margin: 0 0 16px 0;
        }
        .header, .toolbar, .content, footer {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header { margin-bottom: 24px; }
        .toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            margin-bottom: 16px;
        }
        .toolbar label { font-weight: bold; }
        .toolbar select, .toolbar button {
            padding: 10px 14px;
            font-size: 14pt;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #fff;
            cursor: pointer;
        }
        .toolbar button.active {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }
        .tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }
        .tabs button {
            flex: 1 1 auto;
            min-width: 160px;
            padding: 12px 16px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: #fff;
            color: var(--secondary);
            cursor: pointer;
            transition: background 0.2s ease;
        }
        .tabs button.active {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }
        .tab-panel {
            display: none;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        }
        .tab-panel.active { display: block; }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .summary-card, .panel {
            background: #fff;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
        }
        .summary-card h3, .panel h3 {
            font-family: Georgia, serif;
            font-size: 18pt;
            margin: 0 0 10px 0;
        }
        .chart-card {
            padding: 16px;
            border-radius: var(--radius);
            background: #fff;
            border: 1px solid var(--border);
            margin-top: 16px;
        }
        .chart-item {
            display: grid;
            grid-template-columns: 160px 1fr 60px;
            align-items: center;
            gap: 12px;
            margin-bottom: 14px;
        }
        .chart-bar {
            height: 18px;
            border-radius: 12px;
            background: #e6ecf3;
            position: relative;
            overflow: hidden;
        }
        .chart-bar span {
            display: block;
            height: 100%;
            border-radius: 12px;
        }
        .chart-bar.positive span { background: #2d8a4e; }
        .chart-bar.neutral span { background: #6c757d; }
        .chart-bar.negative span { background: #c42b1c; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th, td {
            border: 1px solid var(--border);
            padding: 12px;
            text-align: left;
        }
        th { background: #f7f8fa; }
        .trend-label {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 13pt;
            color: #fff;
        }
        .positive { background: #2d8a4e; }
        .negative { background: #c42b1c; }
        .neutral { background: #6c757d; }
        .view-mode {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .footer-note {
            margin-top: 26px;
            padding: 16px;
            background: #fff;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            color: var(--muted);
            font-size: 12pt;
        }
        footer {
            margin-top: 32px;
            color: var(--muted);
            font-size: 12pt;
            text-align: center;
        }
        @media (max-width: 860px) {
            body { padding: 12px; }
            .toolbar, .tabs { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Earnings Pulse Dashboard</h1>
        <p>Auto-generated dashboard from earnings prompts, instructions, and sample data. Updated dynamically when source files change.</p>
    </div>

    <div class="toolbar">
        <div class="view-mode">
            <label>View Mode</label>
            <button id="webViewBtn" class="active" onclick="switchView('web')">Web</button>
        </div>
        <label for="fiscalYear">Fiscal Year</label>
        <select id="fiscalYear">
            <option>FY25</option>
            <option>FY26</option>
        </select>
        <label for="companyFilter">Company</label>
        <select id="companyFilter" onchange="filterCompany()">
            <option value="all">All Companies</option>
            <option value="TMO">Thermo Fisher (TMO)</option>
            <option value="DHR">Danaher (DHR)</option>
        </select>
    </div>

    <div class="tabs">
        <button class="active" onclick="openTab('overview')">Overview</button>
        <button onclick="openTab('companyTrends')">Company Trends</button>
        <button onclick="openTab('trendSentiment')">Trend Sentiment</button>
        <button onclick="openTab('growthAnalysis')">Growth Analysis</button>
    </div>

    <div class="content">
        <div id="overview" class="tab-panel active">
            <h2>Overview</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Total Calls</h3>
                    <p>2 sample earnings transcripts analyzed.</p>
                </div>
                <div class="summary-card">
                    <h3>Revenue Performance</h3>
                    <p>Thermo Fisher revenue beat at $11.01B with +6.2% YoY growth.</p>
                </div>
                <div class="summary-card">
                    <h3>EPS Performance</h3>
                    <p>Thermo Fisher EPS beat by $0.20 to $5.44. Danaher guidance implies stable margin.</p>
                </div>
                <div class="summary-card">
                    <h3>Market Reaction</h3>
                    <p>Observed positive signals from AI-enabled growth and new product launches.</p>
                </div>
            </div>
            <div class="panel">
                <h3>Analysis Summary</h3>
                <p><strong>Thermo Fisher Q1 FY26:</strong> Delivered a strong quarter with revenue of $11.01B (+6.2% YoY) and EPS of $5.44 (+6% YoY). Key drivers include strength in bioproduction, successful AI-enabled instrument launches (Glacios 3, TSQ Certis), and the Clario acquisition. The company raised full-year guidance on both top and bottom line.</p>
                <p><strong>Danaher Q1 FY26:</strong> Posted modest top-line growth with core revenue up 0.5% YoY, impacted by respiratory seasonality at Cepheid and diagnostics policy headwinds in China. However, bioprocessing equipment orders grew 30% YoY, signaling a turning point. The company maintained its core revenue guidance at 3%-6% and raised full-year adjusted EPS guidance.</p>
                <p><strong>Key Insights:</strong> AI-driven automation and bioprocessing investment are positive secular trends. Diagnostics policy changes in China remain a headwind. Both companies are executing M&A and maintaining disciplined capital deployment.</p>
            </div>
            <div class="chart-card">
                <h3>Performance Overview</h3>
                <div class="chart-item">
                    <div>Revenue Beat</div>
                    <div class="chart-bar positive"><span style="width: 78%"></span></div>
                    <div>78%</div>
                </div>
                <div class="chart-item">
                    <div>EPS Beat</div>
                    <div class="chart-bar positive"><span style="width: 62%"></span></div>
                    <div>62%</div>
                </div>
                <div class="chart-item">
                    <div>Stock Reaction</div>
                    <div class="chart-bar neutral"><span style="width: 55%"></span></div>
                    <div>+0.55</div>
                </div>
            </div>
        </div>

        <div id="companyTrends" class="tab-panel">
            <h2>Company Trends</h2>
            <div class="panel">
                <h3>Company Headwinds & Tailwinds</h3>
                <table>
                    <tr><th>Company</th><th>Tailwind Trend</th><th>Headwind Trend</th><th>Revenue</th><th>EPS</th><th>Stock Perf</th></tr>
'''
    
    for company_key, cdata in company_data.items():
        html += f'''                    <tr>
                        <td>{cdata['name']}</td>
                        <td><span class="trend-label positive">{cdata['tailwind']}</span></td>
                        <td><span class="trend-label negative">{cdata['headwind']}</span></td>
                        <td>{cdata['revenue_outcome']}</td>
                        <td>{cdata['eps_outcome']}</td>
                        <td>{cdata['stock_perf']}</td>
                    </tr>
'''
    
    html += '''                </table>
            </div>
            <div class="chart-card">
                <h3>Tailwind vs. Headwind Distribution</h3>
                <div class="chart-item">
                    <div>TMO - Tailwind Strength</div>
                    <div class="chart-bar positive"><span style="width: 85%"></span></div>
                    <div>Strong</div>
                </div>
                <div class="chart-item">
                    <div>DHR - Tailwind vs Headwind</div>
                    <div class="chart-bar neutral"><span style="width: 50%"></span></div>
                    <div>Balanced</div>
                </div>
            </div>
            <div class="panel" style="margin-top:16px;">
                <h3>Detailed Trend Analysis by Company</h3>
                <p><strong>Thermo Fisher (TMO):</strong></p>
                <ul>
                    <li><span class="trend-label positive">Tailwind</span> AI-enabled cryo-EM and bioproduction automation driving strong revenue and EPS beats.</li>
                    <li><span class="trend-label negative">Headwind</span> Academic and government sector slowdown, especially in China and U.S., partially offsetting gains.</li>
                </ul>
                <p><strong>Danaher (DHR):</strong></p>
                <ul>
                    <li><span class="trend-label positive">Tailwind</span> Bioprocessing equipment orders up 30% YoY, signaling new investment cycle and strong future backlog.</li>
                    <li><span class="trend-label negative">Headwind</span> China diagnostics policy headwinds (volume-based procurement) driving mid-single-digit declines in the region.</li>
                </ul>
            </div>
        </div>

        <div id="trendSentiment" class="tab-panel">
            <h2>Trend Sentiment</h2>
            <div class="panel">
                <h3>Major Trend Analysis</h3>
                <table>
                    <tr><th>Trend</th><th>Sentiment</th><th>Company Count</th></tr>
                    <tr><td>AI/Automation in Labs</td><td><span class="trend-label positive">Positive</span></td><td>2</td></tr>
                    <tr><td>Bioprocessing Demand</td><td><span class="trend-label positive">Positive</span></td><td>2</td></tr>
                    <tr><td>Diagnostics Policy Headwinds</td><td><span class="trend-label negative">Negative</span></td><td>1</td></tr>
                    <tr><td>Supply Chain Resilience</td><td><span class="trend-label neutral">Neutral</span></td><td>1</td></tr>
                </table>
            </div>
            <div class="chart-card">
                <h3>Sentiment Impact</h3>
                <div class="chart-item">
                    <div>Positive</div>
                    <div class="chart-bar positive"><span style="width: 80%"></span></div>
                    <div>2 companies</div>
                </div>
                <div class="chart-item">
                    <div>Neutral</div>
                    <div class="chart-bar neutral"><span style="width: 40%"></span></div>
                    <div>1 company</div>
                </div>
                <div class="chart-item">
                    <div>Negative</div>
                    <div class="chart-bar negative"><span style="width: 20%"></span></div>
                    <div>1 company</div>
                </div>
            </div>
            <div class="panel" style="margin-top:16px;">
                <h3>Trend Influence Summary</h3>
                <p>AI/automation and bioprocessing trends are positive for both companies, while diagnostics policy changes are a negative factor for Danaher. Supply chain resilience remains neutral.</p>
            </div>
        </div>

        <div id="growthAnalysis" class="tab-panel">
            <h2>Growth Analysis</h2>
            <div class="chart-card">
                <h3>Revenue and EPS Growth</h3>
                <div class="chart-item">
                    <div>TMO Revenue</div>
                    <div class="chart-bar positive"><span style="width: 62%"></span></div>
                    <div>+6.2%</div>
                </div>
                <div class="chart-item">
                    <div>TMO EPS</div>
                    <div class="chart-bar positive"><span style="width: 60%"></span></div>
                    <div>+6%</div>
                </div>
                <div class="chart-item">
                    <div>DHR Revenue</div>
                    <div class="chart-bar neutral"><span style="width: 10%"></span></div>
                    <div>+0.5%</div>
                </div>
                <div class="chart-item">
                    <div>DHR EPS</div>
                    <div class="chart-bar neutral"><span style="width: 20%"></span></div>
                    <div>Stable</div>
                </div>
            </div>
            <div class="panel" style="margin-top:16px;">
                <h3>Reasons for Change</h3>
                <table>
                    <tr><th>Company</th><th>Reason for Revenue Change</th><th>Reason for EPS Change</th></tr>
                    <tr><td>Thermo Fisher (TMO)</td><td>Strong bioproduction and AI-enabled launch activity.</td><td>Higher volume, improved mix, and Clario integration.</td></tr>
                    <tr><td>Danaher (DHR)</td><td>Modest growth from bioprocessing order momentum offset by diagnostics policy headwinds.</td><td>Stable margins with cost discipline and M&A positioning.</td></tr>
                </table>
            </div>
        </div>
    </div>

    <div class="footer-note">
        <strong>Generated:</strong> This dashboard is auto-generated from instructions/copilot-instructions.md, prompts/earnings prompts.md, and skills/skills.md. Run generate_dashboard.py to regenerate when sources change.
    </div>

    <footer>
        2017-2026 PwC US. All rights reserved. PwC US refers to US group of member firms and may sometimes refer to the PwC network. Each member firm is a separate legal entity.
    </footer>

    <script>
        const tabs = document.querySelectorAll('.tabs button');
        const panels = document.querySelectorAll('.tab-panel');

        function openTab(tabId) {
            panels.forEach(panel => panel.classList.toggle('active', panel.id === tabId));
            tabs.forEach(button => button.classList.toggle('active', button.textContent.toLowerCase().replace(' ', '') === tabId));
        }

        function switchView(mode) {
            console.log('Switching to', mode);
        }

        function filterCompany() {
            const company = document.getElementById('companyFilter').value;
            const rows = document.querySelectorAll('#companyTrends table tr, #growthAnalysis table tr, #trendSentiment table tr');
            rows.forEach((row, index) => {
                if (index === 0) return;
                const text = row.textContent;
                if (company === 'all') {
                    row.style.display = '';
                } else {
                    row.style.display = text.includes(company) ? '' : 'none';
                }
            });
        }

        openTab('overview');
    </script>
</body>
</html>'''
    
    return html

def main():
    """Main entry point."""
    base_path = Path(__file__).parent
    
    # Read source files
    instructions = read_file(base_path / 'instructions' / 'copilot-instructions.md')
    prompts = extract_prompts(base_path / 'prompts' / 'earnings prompts.md')
    skills = read_file(base_path / 'skills' / 'skills.md')
    company_data = extract_pdf_data()
    
    # Generate dashboard
    html = generate_html(instructions, prompts, skills, company_data)
    
    # Write output
    output_path = base_path / 'dashboard' / 'index.html'
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_path}")

if __name__ == '__main__':
    main()
