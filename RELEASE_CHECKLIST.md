# Public Release Checklist / 公开发布检查表

The repository is technically ready for publication after the owner completes the legal and identity choices below. Run `python3 scripts/validate_skill.py --release` after completing them.

完成以下法律与仓库身份选择后，项目即可公开发布。完成后运行 `python3 scripts/validate_skill.py --release`。

- [x] Replace every `<owner>` placeholder in both READMEs with the GitHub user or organization.
- [x] 替换两份 README 中的全部 `<owner>` 占位符。
- [ ] Choose and add a `LICENSE` file. This is an owner decision; the project does not assume MIT, Apache-2.0, or another license.
- [ ] 选择并添加 `LICENSE` 文件。这是所有者的决定，项目不会擅自选择 MIT、Apache-2.0 或其他许可证。
- [ ] Create the GitHub repository and enable the included Actions workflow.
- [ ] 创建 GitHub 仓库并启用已有的 Actions workflow。
- [ ] Suggested description: `Verify human understanding before consequential LLM or agent output is acted on, forwarded, or used as a dependency.`
- [ ] 建议简介：`在关键 LLM/Agent 输出被执行、转发或作为后续依赖前，取得人的理解证据。`
- [ ] Suggested topics: `agent-skills`, `human-in-the-loop`, `llm`, `ai-safety`, `comprehension`, `benchmark`.
- [ ] Add the repository to skills.sh after the public URL is stable, if desired.
- [ ] 如有需要，在公开 URL 稳定后提交到 skills.sh。
- [ ] Create a `v0.1.0` release only after CI passes from a clean checkout.
- [ ] 仅在干净 checkout 的 CI 全部通过后创建 `v0.1.0` release。
