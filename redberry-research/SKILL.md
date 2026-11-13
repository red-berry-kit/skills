---
name: redberry-research
description: Use when a Red Berry decision depends on technical facts, existing solutions, library behavior, dependency maintenance, technology suitability, or a remedy for an acceptance or review finding.
---

# 红莓调研

根据待回答的问题、需求约束、目标版本与已有证据查证决策依据；需求范围和业务选择交 `redberry-requirements`。

## 执行

1. 阅读相关实现、已定方案和历史实验，明确问题及决策标准。旧结论先核对版本、环境和范围，仍适用时复用。
2. 按[依赖现有能力优先](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#依赖现有能力优先)查当前版本对具体场景的完整推荐用法，不只检索孤立API是否存在。按项目约定使用文档与检索工具，优先官方文档、对应版本源码、发布记录，再结合实际采用案例。关键事实附具体来源和适用条件；来源冲突或资料缺失明确保留，不用宣传、星数或版本号替代适配证据。
3. 比较候选与现有能力，核对需求匹配、维护状态、接入及运维成本，保留适配及缺口依据。涉及前端能力选型时，读取所安装 ui 模块 `README.LLMS.md` 的全部适用前端规则，按其候选顺序与选型判据调研。分别标记来源事实、项目推断和待实测假设；资料未说明某能力，只能判定证据不足。
4. 对必须实测的问题，给出候选、目标环境、最小真实接入范围及通过/失败判据。没有条件执行时保留缺项，不把待验推荐升级为最终选型。

完成条件：每个候选都带来源、适用条件与结论归属（事实／推断／待实测），结论能直接支持或否定一个待决方案；必须实测的项已给出目标环境与通过判据。

## 验收与审查问题的方案选择

逐项关联问题编号、根因证据和不可降低的验收判据。比较最小根因修复与其他合理方案，依据正确性、安全边界、兼容性、维护和运维成本选择当前项目最合适的方案，记录取舍与回归验证去向；不把“最新”“流行”或“改动最少”单独当成最佳依据。

本地源码、规范和复现足以确定的机械性修复，用这些证据简述方案即可；依赖库、协议或外部行业实践的判断必须查对应权威来源。已有依据复核后引用；证据不足时标注假设待验，必要时交 `redberry-proof-of-concept`。

## 出口与交接

交付：**问题的答案与状态、来源及适用条件、未决问题与验证去向**，更新同一任务记录。证据足以支持当前决定时结束调研；资料受限时说明缺失证据阻断哪个决定，继续可独立查证的部分。

新方案交 `redberry-design`；初步设计已有、关键适配需实测时交 `redberry-proof-of-concept`，实测后返回设计定案。只要求查询或调研时在本阶段收尾，报告范围清楚即可，不自动安装依赖或实施方案。

复用型材料存入项目已有过程资料区；主方案仅写最终有效规则。参考规范按需阅读[开发约定](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md)。
