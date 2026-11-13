---
name: using-redberry
description: Use when starting or continuing requirements, research, design, implementation, debugging, verification, or code review in a Red Berry project.
---

# 红莓开发入口

按风险选择最短可验证路径，复用已有授权、方案和有效证据：

- 维护源码前读取适用的 `AGENTS.md`，核对实现与当前任务摘要。
- 使用项目能力前读取其使用说明；使用模块前读取该模块的 `README.LLMS.md`。
- 使用 Skill 前读取其 README 与 SKILL.md；同一上下文已读且未变化的内容直接复用，参考资料按本次决策选读。

## 默认路径

需求清楚、影响可定位时，由当前 agent 完成“实现 → 针对性验证 → 差异复查 → 交付”。用一句话明确改动和通过条件，读取 `redberry-coding`；验证与复查按下表按需读取。普通任务按需展开阶段；跨阶段记录写在当前任务摘要里。

| 尚需解决的问题 | 读取的 Skill |
| --- | --- |
| 范围或验收不清 | `redberry-requirements` |
| 事实未知 | `redberry-research` |
| 编写或修订模块 `README.LLMS.md` | `redberry-writing-readme-llms` |
| 职责、接口或选型变化 | `redberry-design` |
| 可行性待实测 | `redberry-proof-of-concept` |
| 任务有依赖 | `redberry-planning` |
| 变更已明确 | `redberry-coding` |
| 验收范围或方式待定 | `redberry-verification` |
| 复查复杂变更 | `redberry-code-review` |
| 根因未明 | `redberry-debugging` |

沿用有效选型时核对约束与接入是否匹配；新增候选或约束变化时再选型。纯说明、文档纠错直接处理并核对。

## 验证与修复

验收方式与分流判据以 `redberry-verification` 为准。实现者与验收者分工，避免双方重复执行同一套检查。

发现问题后：

1. 保留触发条件、根因证据和失败判据；根因不清再排障。
2. 修法明确且依据有效时直接修复；只有技术事实或方案取舍未明时才调研，接口或范围变化时才回设计／需求。
3. 重验原失败、受影响行为及必要回归，复用未受影响的证据。局部修复不重启整套流程；独立复验通常交原验收者。
4. 复查最终差异；约定必需项通过、必修问题关闭且证据适用于最终实现即交付。通过后仅因新增变化、失败或未解决风险扩大验证。

## 记录与交付

- 短任务在对话中记录；跨轮次维护一份当前摘要：目标、验收条件、有效决定、已完成／待办、证据路径。恢复时先读摘要，缺少事实再查历史，按当前状态更新而非追加完整过程。
- 详细日志落文件，工具输出优先给结果及失败片段。仅在并发改动、审计或来源歧义时补足基准证据；按实际风险记录必要证据，常规任务不要求重复报告或每轮全量采集。
- 交付改动、实际验证结果及未验证项；行为结论须有行为证据，测试数量与构建成功不能替代。
- 用户只要求某阶段时在该阶段收尾；已有授权内持续推进，仅澄清无法查明且影响结果的用户选择。提交、发布及外部操作遵循用户授权。
