---
name: redberry-debugging
description: Use when a Red Berry project has errors, unexpected behavior, failing tests, performance regressions, or intermittent failures requiring root-cause analysis.
---

# 红莓排障

根据预期与实际行为、问题证据和当前实现定位根因，确定修复边界；技术约束按需读取[开发约定](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md)。

## 执行

1. 固定现象与环境：触发条件、输入、时间顺序及影响，区分用户反馈、实际观测与解释假设。已证实的审查问题复用原证据，不重做无关调查。按[错误反馈与诊断](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/diagnostics.md)区分正常操作错误与程序故障，再关联用户反馈、请求／任务标识、技术原因链和阶段耗时；缺失信息优先通过已有诊断设施取证。
2. 建立失败判据。优先最小可重复场景或测试，确认失败对应原问题并保留结果。无法复现时收集必要日志、请求与上下文；明确缺少的条件，不靠试改把猜测当成根因。
3. 沿实际数据流验证假设，每次检查一个关键因素。涉及共享状态、资源或公共机制时追踪其他读写入口，确定同类触发与受影响的不变量。库行为未知时交 `redberry-research` 查证。
4. 形成最小修复方案，说明根因、修复位置、相关入口及回归场景。需要改变约定行为或模块接口时，分别交需求或设计阶段；不附带无关重构。

完成条件：

- 定位完成：根因能一句话复述，失败判据在修复前可复现，回归场景覆盖受影响入口。
- 修复验收：后续编码、验收阶段确认失败判据在修复后不再出现；仅交付定位结果时标明尚待修复与验证。

## 出口与交接

交付：**现象、失败判据与证据、已确认根因／待验证假设、修复范围、回归判据**，更新同一任务记录。

- 根因和修法明确时直接交 `redberry-coding`；技术事实或取舍未明时才交 `redberry-research`，复用仍有效的依据。
- 其他故障在根因、修复方案明确且已获授权后，交 `redberry-planning` 安排工作（小修复可简写），再交 `redberry-coding` 实施、`redberry-verification` 按风险验证、`redberry-code-review` 复查。
- 修复后核对原失败、受影响行为及必需检查；最小复现的结论限于其覆盖范围。
- 证据不足时继续取证，报告阻断与恢复条件。
- 用户仅要求诊断时交付诊断结论，不自动改代码；已授权修复时按原授权继续。
