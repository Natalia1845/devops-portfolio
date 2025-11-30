import re
import argparse
from collections import Counter
from datetime import datetime
import html

def parse_log_line(line):
    # Простий регулярний вираз для парсингу Apache логів
    pattern = r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" (?P<status>\d{3}) \S+ "[^"]*" "(?P<agent>[^"]+)"'
    match = re.match(pattern, line)
    return match.groupdict() if match else None

def analyze_log(file_path, top_n=5):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    ip_list = []
    agent_list = []
    status_list = []

    for line in lines:
        data = parse_log_line(line)
        if data:
            ip_list.append(data['ip'])
            agent_list.append(data['agent'])
            status_list.append(data['status'])

    top_ips = Counter(ip_list).most_common(top_n)
    top_agents = Counter(agent_list).most_common(top_n)
    status_counts = Counter(status_list)

    return top_ips, top_agents, status_counts

def generate_html_report(top_ips, top_agents, status_counts, output_file):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Apache Log Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 80%; margin: 20px auto; }}
            th, td {{ border: 1px solid #999; padding: 8px; text-align: center; }}
            th {{ background-color: #eee; }}
        </style>
    </head>
    <body>
        <h1>📊 Apache Log Analysis Report</h1>
        <p><b>Generated:</b> {now}</p>

        <h2>Top IP Addresses</h2>
        <table>
            <tr><th>IP</th><th>Requests</th></tr>
            {''.join(f"<tr><td>{html.escape(ip)}</td><td>{count}</td></tr>" for ip, count in top_ips)}
        </table>

        <h2>Top User Agents</h2>
        <table>
            <tr><th>User Agent</th><th>Requests</th></tr>
            {''.join(f"<tr><td>{html.escape(agent)}</td><td>{count}</td></tr>" for agent, count in top_agents)}
        </table>

        <h2>HTTP Status Codes</h2>
        <table>
            <tr><th>Status</th><th>Count</th></tr>
            {''.join(f"<tr><td>{code}</td><td>{count}</td></tr>" for code, count in status_counts.items())}
        </table>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Report saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Parse Apache/Nginx log and generate HTML report")
    parser.add_argument("--file", type=str, required=True, help="Path to log file")
    parser.add_argument("--top", type=int, default=5, help="Number of top results to display")
    parser.add_argument("--output", type=str, default="report.html", help="Output HTML file name")

    args = parser.parse_args()

    top_ips, top_agents, status_counts = analyze_log(args.file, args.top)
    generate_html_report(top_ips, top_agents, status_counts, args.output)

if __name__ == "__main__":
    main()
