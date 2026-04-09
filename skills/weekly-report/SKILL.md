---
name: weekly-report
description: Capture git activity between a user-specified timeframe, export a template-backed summary, and feed the artifact into AI to craft a leadership-style weekly report. Trigger from `/weekly-report` or any agent hookup that has this skill installed.
metadata: '{"openclaw": {"requires": {"binaries": ["git","python3"]}}}'
---

# Weekly-Report Skill

## Workflow overview
- **确认仓库与时间窗口**： `/weekly-report since=YYYY-MM-DD until=YYYY-MM-DD` 或运行 `scripts/generate_weekly_report.py`，让脚本自动识别当前 Git 仓库和所需周期（默认最近 7 天）。
- **可选模板**： 默认模板 `default`，也可指定 `executive` 等，通过 `--template <name>` 选择。请先使用 `--list-templates` 查看可用模板。
- **提取日志并生成 TXT**： 脚本会加载所选模板，插入 `{{commit_list}}`、`{{status_summary}}`、`{{repo}}`、`{{branch}}` 等占位符，输出到 `reports/weekly-report-<since>-<until>.txt`。
- **交给 AI 分析**： 生成完文本后，把 TXT 作为 prompt 或附件传给 AI，让模型 “扮演领导周报助理” 形式，整理完成的成果、状态、计划、风险/阻塞并写成可发给领导的周报内容。
- **遵循领导格式**： 明确列出成果、状态、计划、阻塞和需要领导决策的事项；保持摘要层次清晰，文字简洁，以便复制到邮件或汇报文档。

## 实现建议
1. 如果脚本提示 “找不到 Git 仓库”，请确认 workspace 目录与 `/weekly-report` 命令运行时的当前目录一致。
2. 使用 `--since`/`--until` 时，格式必须是 `YYYY-MM-DD`。参数缺省值分别为上周 7 天前和当前日期。
3. 可通过 `--output` 强制输出到特定路径，比如 `reports/weekly-report-final.txt`；路径会相对于仓库根目录。
4. 模板文件位于 `templates/`，可以复制并创建自定义模板，只要在脚本调用时使用对应的名称即可。

## 与 AI 的衔接
后续用 `/weekly-report` 描述 “这是最新的日志导出，请帮我按照模板写一个给领导的周报”，要在 prompt 里附上 TXT 内容，或引用该文件的关键段落。可以额外提供需要突出或避免的事项，比如 “重点提到风险 A” 或 “避免技术细节堆砌”。
