import json
import subprocess


def main():
    # Run ruff check with JSON output
    result = subprocess.run(
        ["ruff", "check", ".", "--output-format", "json"],
        capture_output=True,
        text=True,
    )

    report = result.stdout
    violations = json.loads(report) if report else []
    violation_count = len(violations)

    # Write ruff report
    problems_path = ".repo-reports/ruff-report.json"
    with open(problems_path, "w+", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(violations, indent=2))

    # Calculate quality score (0-10, inverse of violations)
    # 0 violations = 10, 1-5 = 8, 6-10 = 6, 11+ = 4
    if violation_count == 0:
        quality_score = 10
    elif violation_count <= 5:
        quality_score = 8
    elif violation_count <= 10:
        quality_score = 6
    else:
        quality_score = max(4 - (violation_count - 10) // 10, 1)

    # Determine color
    score_color = "red"
    if quality_score >= 8:
        score_color = "#34D058"
    elif quality_score >= 6:
        score_color = "yellow"

    # Create shield
    shield_path = ".repo-shields/quality_shield.json"
    with open(shield_path, "w+", encoding="utf-8", newline="\n") as f:
        f.write(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "label": "code quality",
                    "message": f"{quality_score}/10 ({violation_count} issues)",
                    "color": score_color,
                },
            )
        )

    return quality_score


if __name__ == "__main__":
    main()
