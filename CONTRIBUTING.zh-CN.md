# 参与贡献

[English](CONTRIBUTING.md) | 中文

感谢你帮助改进 Human Understanding Checkpoint。

## 值得贡献的内容

- 揭示可复用失败模式的公开回归案例，或由独立方维护的密封评估。
- 更好地平衡“检查不足”和“不必要摩擦”。
- 无障碍、多语言以及成年人之间协作语气的改进。
- 独立 benchmark 复现、人工评分和模型适配器。
- 对局限或相关工作的更清晰说明。

## 修改运行时 skill 之前

面向人的说明应放在 `README*` 或 `docs/` 中。只有会改变模型行为的内容，才加入 `SKILL.md` 或 `references/`。优先写一条可泛化规则，不要堆积场景脚本。

提交到本仓库的所有案例都应视为公开回归案例。如果其措辞或结果已经影响 skill 修改，就不能再用它支持新的泛化结论。密封保留集必须由独立方维护，并在分析前保持不可见。

## 验证修改

```sh
python3 scripts/validate_skill.py
python3 benchmark/benchmark.py validate
python3 -m unittest discover -s benchmark/tests -p 'test_*.py'
```

行为变更应按 [benchmark/BENCHMARK.md](benchmark/BENCHMARK.md) 进行成对盲测。除了平均分，也应报告退化与硬失败。

## Pull request 检查表

- 说明要解决的行为或文档问题。
- 保持中英文用户文档一致。
- 修改 harness 时添加或更新测试。
- 说明 benchmark 案例或成功门槛是否改变。
- 不要提交盲化密钥、私有 prompt、凭据或参与者数据。
- 保持“对话证据”与“证明人的内在理解”之间的边界。
