---
name: redberry-requirements
description: Use when a Red Berry feature needs requirements clarified, its scope changes, or its acceptance criteria and failure behavior are incomplete.
---

# 红莓需求澄清

根据用户请求、现有实现、项目约束和已确认决定明确验收行为，复用已明确内容。单独调用时仅交付需求结果，不进入实现。

## 执行

1. 还原目标：谁在什么条件下做什么，期望看到什么结果。检查已有能力和约束，区分本次范围、明确不做的内容及未决项。涉及用户可见内容或语言格式时，按[国际化契约](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/i18n.md)核对语言范围、既有约定与翻译职责，将受影响行为纳入验收条件。
2. 按用户操作梳理正常、失败和恢复行为。涉及失败反馈或执行诊断时，按[错误反馈与诊断](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/diagnostics.md)明确用户可见原因、纠正／恢复动作与故障及耗时判据。涉及共享状态时列出相关操作及其顺序或并发约束；只展开本次实际受影响的链路，不增加未经要求的功能。
3. 可复用模块将“干净应用通过 CLI 添加并配置后使用默认能力”纳入范围，区分必要配置、业务策略与不应由使用者编写的装配。将每个范围内要求写成可观察判据：**前置条件／动作或事件／预期结果**，包括与任务相关的错误和边界。沿用项目编号或简短标签，便于计划、验收及审查引用。
4. 分开标记已确认要求、可验证假设和待用户决定事项。技术事实交 `redberry-research` 查证；无法从上下文查明且会改变结果的业务选择才询问用户。已有批准继续有效，只补新增缺口。

完成条件：每条范围内要求都有「前置条件／动作或事件／预期结果」三段，且已确认、假设、待决三类没有混在一起。

## 出口与交接

交付目标、范围、逐项验收条件和未决项，并更新当前任务记录。

关键行为已明确时交 `redberry-design`；既有方案可直接复用时交 `redberry-planning`。仍有未知项时指出它阻断哪个决定，推进不依赖它的部分。仅完成需求讨论时，交付状态标为需求阶段完成。
