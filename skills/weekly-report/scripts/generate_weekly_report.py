#!/usr/bin/env python3
import argparse
import datetime
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gather git activity between two dates, render a template, and export a weekly-report-ready TXT file."
    )
    parser.add_argument(
        "--since",
        metavar="YYYY-MM-DD",
        help="Start of the window (inclusive). Defaults to 7 days ago.",
    )
    parser.add_argument(
        "--until",
        metavar="YYYY-MM-DD",
        help="End of the window (inclusive). Defaults to today.",
    )
    parser.add_argument(
        "--template",
        default="default",
        help="Template name from templates/ (omit extension). Use --list-templates to see choices.",
    )
    parser.add_argument(
        "--output",
        help="Custom output path relative to git root. If omitted, writes to reports/weekly-report-<since>-<until>.txt.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Maximum number of commits to include (default 40).",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available template names and exit.",
    )
    return parser.parse_args()


def list_templates():
    return sorted([p.stem for p in TEMPLATE_DIR.glob("*.md")])


def format_date(value, default):
    if value:
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("日期必须为 YYYY-MM-DD 格式。")
    return default


def run_git(args, git_root):
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=git_root,
            text=True,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"git 命令失败：{exc.stderr.strip() or exc.stdout.strip()}")
    return result.stdout.strip()


def gather_commits(git_root, since, until, limit):
    git_args = [
        "log",
        f"--since={since.isoformat()}",
        f"--until={until.isoformat()}",
        f"-n{limit}",
        "--date=short",
        "--pretty=format:%h | %cd | %s",
        "--abbrev-commit",
    ]
    output = run_git(git_args, git_root)
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        return ["（此时间段无提交）"]
    return lines


def current_branch(git_root):
    branch = run_git(["branch", "--show-current"], git_root).strip()
    return branch or "（detached 或未知分支）"


def status_summary(git_root):
    status = run_git(["status", "-sb"], git_root)
    return status or "工作区干净"


def render_template(template_text, context):
    rendered = template_text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def main():
    args = parse_args()

    if args.list_templates:
        print("可用模板：")
        for name in list_templates():
            print(f"- {name}")
        sys.exit(0)

    today = datetime.date.today()
    default_since = today - datetime.timedelta(days=7)
    since = format_date(args.since, default_since)
    until = format_date(args.until, today)
    if since > until:
        raise SystemExit("开始日期必须早于或等于结束日期。")

    try:
        git_root = Path(run_git(["rev-parse", "--show-toplevel"], Path.cwd()))
    except SystemExit as err:
        raise SystemExit(f"无法确定 Git 根目录：{err}")

    try:
        template_path = TEMPLATE_DIR / f"{args.template}.md"
        template_text = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        available = ", ".join(list_templates())
        raise SystemExit(f"未找到模板 '{args.template}'。可用模板：{available}")

    commits = gather_commits(git_root, since, until, args.limit)
    commit_list = "\n".join(f"- {line}" for line in commits)
    branch = current_branch(git_root)
    status = status_summary(git_root)
    context = {
        "repo": git_root.name,
        "since": since.isoformat(),
        "until": until.isoformat(),
        "branch": branch,
        "commit_list": commit_list,
        "status_summary": status,
        "template_note": "提示：请补充下周计划与阻塞，并标注需要领导决策的部分。",
    }

    report_body = render_template(template_text, context)

    if args.output:
        report_path = git_root / args.output
    else:
        since_token = since.strftime("%Y%m%d")
        until_token = until.strftime("%Y%m%d")
        report_path = git_root / "reports" / f"weekly-report-{since_token}-{until_token}.txt"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_body, encoding="utf-8")

    print(f"日志已写入：{report_path}")
    print("下一步：将这个 TXT 作为 prompt/参考提供给 AI，说明要生成给领导的周报，重点突出成果、计划、状态与风险。")


if __name__ == "__main__":
    main()
