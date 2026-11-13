---
name: redberry-code-review
description: Use when reviewing Red Berry code for requirement compliance, design issues, project conventions, verification gaps, or regressions after fixes.
---

# 红莓代码审查

对照需求、已定方案、变更范围、当前源码与验证证据审查可定位的实际问题；规范按需读取[开发约定](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md)。

涉及多个应用的资源、路由或交付时，按[独立应用边界](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md#独立应用边界)核对声明驱动装配、应用命名、路径冲突与跨应用隔离。

## 执行

1. 固定审查对象。使用可用的 Git 基点与工作区变更，包含新增及未跟踪文件；无 Git 或历史基线时，以文件清单和当前内容固定范围，说明无法判定的历史差异，不因此放弃当前源码审查。
2. 对照需求和方案检查行为：
   - 按[行为过程与生命周期](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#行为过程与生命周期)追踪输入、调用、过渡状态、收尾与结果；核对消费者所需数据的清理时机、完成条件与后续回调的一致性。
   - 检查受影响的模块职责、公开接口、依赖、不变量及失败行为。共享机制检查相关调用入口；复查覆盖修复新影响的行为。
   - 涉及失败处理或后端执行时，按[错误反馈与诊断](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/diagnostics.md)检查用户纠正／恢复、故障定位及耗时查询；错误漏报和正常拒绝产生诊断噪声均列为必修问题。
3. 按[设计与架构](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md)核对职责与生成边界，按[技术选型](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/stack.md)核对工具、版本及工程检查：
   - 按[依赖现有能力优先](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#依赖现有能力优先)检查实际状态流、组合方式与生命周期是否遵循适配的官方模式，复用工具已有结果。
   - 前端变更按所安装 ui 模块 `README.LLMS.md` 的全部适用前端规则核对任务设计、能力选型与实际接入；涉及参考界面时按其参考与文案规则核对差异依据。选型与行为证据按第4项检查。
   - 界面、用户可见 API 消息或语言格式对照[国际化契约](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/i18n.md)核查实现与验收覆盖，定位遗漏的消息、格式或资源装配。
   - 代码与配置名称及界面文案按[命名判据](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#命名判据)检查是否从使用场景表达目的、利用上下文省去重复限定、术语贯通调用链；语义错误与歧义列问题，个人词形偏好归可选建议，未查明的风险记待核实。
4. 核对验收条件与证据：
   - 从需求约束重新核对能力适配与行为证据，分别报告结果；复用结论须覆盖本次变化。缺少适用候选或排除依据时先补查，不以功能通过判定适配合格；遗漏适用能力且无充分不适配依据的列为必修问题。前端按 ui 模块规范的选型、整体设计及验收判据核对。
   - 可复用模块对照交付契约检查默认装配及干净消费应用的 CLI 安装证据；模块专属接线仅在 examples 中提供的列为交付缺陷。
   - 核对源码、环境与用例是否匹配，记录缺失场景及失败；必要时针对性复现。按实际覆盖范围报告结果，不以测试数量证明覆盖。
5. 按影响排序报告问题，每项附**位置、触发条件、影响、证据、修复或复查方向**。复用原问题清单记录已修、仍存或待验，避免重复报同一根因。

## 出口与交接

输出审查范围、问题及处置状态、实际检查和验证限制，更新同一任务记录。没有发现问题时也说明覆盖边界，不给出全面正确性保证。

仅审查任务在报告处收尾，不修改源码。已有修复授权时，将问题交回 `using-redberry`；修复后按 `redberry-verification` 重核旧证据有效性，选择直接验证或独立验收者复验，再回本阶段复查，维护同一问题记录。行为验收单独完成；实现任务满足入口完成条件后汇总交付，保留缺项。
