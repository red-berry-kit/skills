---
name: redberry-code-review
description: Use when reviewing Red Berry code for requirement compliance, design issues, project conventions, verification gaps, or regressions after fixes.
---

# 红莓代码审查

输入为需求、已定方案、变更范围、当前源码与验证证据。围绕可定位的实际问题审查。流程由 `using-redberry` 组织；规范按需从[开发约定](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md)进入。

涉及多个应用的资源、路由或交付时，按[独立应用边界](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#独立应用边界)核对声明驱动装配、应用命名、路径冲突与跨应用隔离。

## 执行

1. 固定审查对象。使用可用的 Git 基点与工作区变更，包含新增及未跟踪文件；无 Git 或历史基线时，以文件清单和当前内容固定范围，说明无法判定的历史差异，不因此放弃当前源码审查。
2. 对照需求和方案按[行为过程与生命周期](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#行为过程与生命周期)追踪输入、调用、过渡状态、收尾与结果，核对消费者仍需的数据是否被提前清理、完成条件及后续回调是否一致。检查受影响的模块职责、公开接口、依赖、不变量及失败行为。共享机制变更检查相关调用入口，复查也覆盖修复新影响的行为，不能只看补丁行。涉及失败处理或后端执行时，按[错误反馈与诊断](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/diagnostics.md)分别检查用户能否纠正／恢复、程序故障能否定位及性能耗时是否可查；错误漏报和正常拒绝产生诊断噪声均列为必修问题。
3. 核对项目规则与生成边界，按[原生优先](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#依赖原生模式优先)检查实际状态流、组合方式及生命周期是否遵循适配的官方模式，复用工具已有结果。涉及 UI 组件时，按所安装 ui 模块 `README.LLMS.md` 的全部前端使用规则核查专用组件及交互能力；适用却未使用且无不适配依据的，按该文档组件选型的审查要求补查，补查后仍不充分即列为必修问题，不作为个人偏好或可选建议。涉及参考界面时，按该文档的界面参考与用户文案核查排版偏离、无需求依据的提示和内部流程外露。涉及界面、用户可见的 API 消息或语言格式时，对照[国际化契约](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/i18n.md)核查实现与验收覆盖，定位遗漏的前后端消息、格式或资源装配。按[命名判据](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#命名判据)检查代码／配置名称及界面文案是否从使用场景表达目的、利用上下文省去重复限定、术语是否贯通调用链；将语义错误或歧义与个人词形偏好区分。个人偏好作为可选建议；未查明的风险作为待核实项，不当作已确认缺陷。
4. 前端审查从场景约束重新核对所选 ui 模块 `README.LLMS.md` 的组件选型，分别报告适配问题与行为问题；漏查合理专用候选、排除理由不足及只有功能证据均不得判选型合格；依据充分性与补查顺序按该文档组件选型的审查要求执行。涉及表单时按该文档表单整体设计的完成条件核对任务、布局与验收证据；检查复用结论是否覆盖本次页面变化。核对验收条件与证据范围。可复用模块对照其交付契约，检查默认装配及干净消费应用的 CLI 安装证据；专属接线藏在 examples 中仍是交付缺陷。检查源码、环境和用例是否匹配，识别缺失场景及失败。必要时执行针对性复现；实际结果属于哪个范围就报告哪个范围，测试数量不构成覆盖证明。
5. 按影响排序报告问题，每项附**位置、触发条件、影响、证据、修复或复查方向**。复用原问题清单记录已修、仍存或待验，避免重复报同一根因。

## 出口与交接

输出审查范围、问题及处置状态、实际检查和验证限制，更新同一任务记录。没有发现问题时也说明覆盖边界，不给出全面正确性保证。

仅审查任务在报告处收尾，不修改源码。已有修复授权时，将问题交回 `using-redberry` 的修复闭环；修复后按 `redberry-verification` 依据本轮变更选择直接验证或独立验收者复验，再回本阶段复查，保持同一任务的问题记录。审查意见不能替代行为验收，审查发现的修改同样会影响旧验收证据。实现任务满足入口规定的完成条件后汇总交付，缺项明确保留。
