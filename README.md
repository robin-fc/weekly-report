# weekly-report

这是一个 **weekly-report** Skill 项目，提供 `/weekly-report` 命令和 `scripts/generate_weekly_report.py` 脚本，可在 Codex、Claude Code、OpenClaw 等 Agent 平台中安装使用。

## 插件/市场兼容
- `.codex-plugin/plugin.json` 让 Codex/Claude Code/Claw 探测这个仓库并注册入口（manifest 指向 `./skills` 目录）。
- `.agents/plugins/marketplace.json` 是本地市场 catalog，`source.path` 指向 repo 根，可供市场部署者一键安装。

## 安装
1. 将 `skills/weekly-report` 整个目录放到目标合约的 Skill 根目录（比如 `~/.codex/skills` 或插件的 `skills/`）下。
2. 确保环境中有 `git` 与 `python3`，并且当前目录可以访问仓库的 `.git`。
3. 使用市场/插件机制发布或更新时，技能目录应与平台的 manifest 同步（例如 `.codex-plugin/plugin.json` + marketplace entry）。

## 使用
- 运行 `/weekly-report since=2026-04-01 until=2026-04-07 template=executive`：由 Agent 调用脚本并接管后续 AI 总结；
- 也可在仓库内执行 `python skills/weekly-report/scripts/generate_weekly_report.py --since 2026-04-01 --until 2026-04-07 --template executive`；
- 使用 `--list-templates` 查看所有模板名称，`--output` 定义自定义输出文件；
- 脚本会在 `reports/` 中产出带有 `commit_list`、`status_summary` 等占位符的 TXT 文件，把它交给 AI 生成给领导的周报摘要。

## 模板
- `default`：适合常规周报，列出提交与状态、计划、关注项；
- `executive`：更偏领导视角，强调关键成果与风险。

## 扩展
- 可在 `skills/weekly-report/templates/` 添加新的 `.md` 模板后，同步 `--template` 参数；
- `scripts/generate_weekly_report.py` 的输出可作为 prompt 直接送给 AI，让它“提炼成领导周报”。
