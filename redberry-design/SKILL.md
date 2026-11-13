---
name: redberry-design
description: Use when a Red Berry change needs frontend component or hook selection, architecture, module responsibilities, public interfaces, state transitions, dependencies, or abstraction decisions.
---

# 红莓设计

根据已明确需求、验收条件、现有架构和调研证据制定行为方案，项目规则优先：

- 涉及模块能力时，读取实际安装版本的 `README.LLMS.md`；按全部适用使用契约、选型及完成条件形成实施依据。用户指定参考时，核对实际参考与需求，记录采用方式和有依据的差异。
- 用户界面、用户可见 API 消息或语言格式读取[国际化契约](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/i18n.md)，明确前后端翻译分工、语言状态、资源归属及默认装配。

涉及多个应用的资源、路由或交付时，按[独立应用边界](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md#独立应用边界)核对声明驱动装配、应用命名、路径冲突与跨应用隔离。

## 执行

1. 核对需求与技术事实，按[依赖现有能力优先](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#依赖现有能力优先)先查已有依赖对当前场景的推荐接入模式，再决定职责与状态方案。业务选择缺口交 `redberry-requirements`，技术事实缺口交 `redberry-research`；已有且仍适用的决定直接复用。
2. 按[设计与架构](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md)划分职责、公开接口、依赖方向及装配边界。对公开接口与配置按[命名判据](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#命名判据)检查业务意图、上下文与术语一致性，用实际调用或配置示例验证可理解性。可复用模块按其交付契约设计默认装配，列清必要配置与可选扩展，不能以示例手工接线代替默认能力。说明调用方必须知道的输入、输出、错误与不变量，优先简单直接的方案；新增抽象须对应实际变化点及收益。
3. 按[行为过程与生命周期](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#行为过程与生命周期)沿操作及数据流设计关键行为，明确关键过渡中的可观察状态与不变量。涉及共享状态时列出所有受影响的读写入口，说明状态迁移、资源生命周期及必要的事务、并发与副作用边界；覆盖失败、取消或恢复中本次实际需要的行为。
4. 将方案行为对应到验收条件，分别明确适配依据与行为验证点；已有有效决定按其覆盖范围复用。给出关键取舍、受影响模块、兼容或迁移影响和待验假设。可行性必须实测时，明确候选与通过判据，交 `redberry-proof-of-concept`，结果返回本阶段定案。

## 出口与交接

交付：**职责与接口、关键行为与不变量、验收对应、取舍及限制**，更新同一任务记录。关键决定有依据、范围内行为有验证去向时交 `redberry-planning`；有阻断项则标记初步方案并说明所需证据。

局部修改沿用既有方案时，直接说明局部改法及影响，无需额外设计文档或审批。只要求设计时在方案交付后停止，标明仅完成设计。主文档保留最终有效规则，调研与实验材料留在项目过程资料区。
