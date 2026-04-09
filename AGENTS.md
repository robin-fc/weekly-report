# AGENTS instructions for this repository

1. Always reply in Simplified Chinese when operating in or about this repository.
2. The primary skill is `skills/weekly-report`. `/weekly-report` and `scripts/generate_weekly_report.py` should confirm the git root, timeframe (since/until), optional template, and produce a TXT that feeds the AI summary.
3. Templates live under `skills/weekly-report/templates`. Add `.md` files with `{{commit_list}}`/`{{status_summary}}` placeholders to expose more shapes.
4. After editing scripts or templates, rerun `python skills/weekly-report/scripts/generate_weekly_report.py --list-templates` to ensure the CLI still executes (no fancy tests required).
5. The plugin manifest sits at `.codex-plugin/plugin.json` and the marketplace entry is `.agents/plugins/marketplace.json`; update them only when metadata, default prompts, or policy need adjusting.
