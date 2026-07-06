import json
import re
from collections import Counter
from pathlib import Path

REPORT = Path("/app/report.json")
LOG = Path("/app/access.log")


def expected():
    """Independently compute the expected summary from the access log."""
    paths, ips, total = Counter(), set(), 0
    for line in LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def load_report():
    assert REPORT.exists(), "no /app/report.json found"
    try:
        return json.loads(REPORT.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"/app/report.json is not valid JSON: {e}")


def test_report_exists_and_valid_json():
    """Criterion 1: /app/report.json exists and contains valid JSON (a JSON object)."""
    report = load_report()
    assert isinstance(report, dict), "report.json must contain a JSON object"


def test_report_has_exact_keys():
    """Criterion 2: the JSON object has exactly the keys total_requests, unique_ips, and top_path."""
    report = load_report()
    assert set(report.keys()) == {"total_requests", "unique_ips", "top_path"}, (
        f"unexpected keys: {sorted(report.keys())}"
    )


def test_total_requests_correct():
    """Criterion 3: total_requests equals the number of non-empty lines in /app/access.log."""
    report = load_report()
    assert report["total_requests"] == expected()["total_requests"]


def test_unique_ips_correct():
    """Criterion 4: unique_ips equals the number of distinct client IPs in /app/access.log."""
    report = load_report()
    assert report["unique_ips"] == expected()["unique_ips"]


def test_top_path_correct():
    """Criterion 5: top_path equals the most frequently requested path in /app/access.log."""
    report = load_report()
    assert report["top_path"] == expected()["top_path"]