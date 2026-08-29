# Public Release Checklist / 公开发布检查表

Repository: <https://github.com/wangzijian0x7C6/human-understanding-checkpoint>

The repository is public and its CI is passing. A formal versioned release still requires the owner-selected legal choice below. Run `python3 scripts/validate_skill.py --release` after completing it.

仓库已经公开，CI 已通过。创建正式版本 Release 前仍需完成下面由所有者决定的法律选择；完成后运行 `python3 scripts/validate_skill.py --release`。

- [x] Replace every `<owner>` placeholder in both READMEs with the GitHub user or organization.
- [x] 替换两份 README 中的全部 `<owner>` 占位符。
- [ ] Choose and add a `LICENSE` file. This is an owner decision; the project does not assume MIT, Apache-2.0, or another license.
- [ ] 选择并添加 `LICENSE` 文件。这是所有者的决定，项目不会擅自选择 MIT、Apache-2.0 或其他许可证。
- [x] Create the GitHub repository and enable the included Actions workflow.
- [x] 创建 GitHub 仓库并启用已有的 Actions workflow。
- [x] Set the description: `Verify human understanding before consequential LLM or agent output is acted on, forwarded, or used as a dependency.`
- [x] 设置仓库简介。
- [x] Add topics: `agent-skills`, `human-in-the-loop`, `llm`, `ai-safety`, `comprehension`, `benchmark`.
- [ ] Add the repository to skills.sh after the public URL is stable, if desired.
- [ ] 如有需要，在公开 URL 稳定后提交到 skills.sh。
- [ ] Create a `v0.1.0` release only after CI passes from a clean checkout.
- [ ] 仅在干净 checkout 的 CI 全部通过后创建 `v0.1.0` release。
