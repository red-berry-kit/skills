# 干净子 agent 验收闭环验证

本文保留历史试验与证据；当前是否需要独立验收，以 [验收方式分流](../../redberry-verification/SKILL.md#选择验收方式) 为准。

日期：2026-10-20。范围：Skills 验收流程规范，不修改 auth 或用户服务。当前状态：规范的独立验收与审查通过；真实夹具完成两轮干净验收及一次问题调研、修复闭环，当前范围无必修缺项。

## 需求与判据

- 正式实现验收与实现者上下文分离；每轮使用新的干净子 agent。
- 交接包含完整判据、当前源码及运行条件，排除实现者自评和预设结论；验收者实际运行检查。
- 问题查证后调研适合当前约束的方案，修复自检后再独立验收。
- 每轮核对完整范围；完整必验项通过、必修问题关闭、审查完成且证据对应最终实现才交付。
- 保持仅验收、仅审查等授权边界；能力与环境缺口保留未完成状态；文案纠错不套软件实施全流程。

## 改写前行为证据

全新上下文 `/root/acceptance_baseline` 读取修改前的入口、验收和审查 Skills，推演“当前自检全绿、审查发现已知根因和修法、用户授权继续到完成”的场景。没有提供目标答案，未修改文件或运行虚构测试。

其回答明确选择：“编码修复 → 受影响范围补验 → 代码复查 → 汇总交付”；指出三份 Skill 没有要求独立验收，选择由当前 agent 连续完成修复、补验和复查。该结果重现两个缺口：允许实现者自验；已知修法直接编码，没有修复方案调研交接。

这是一例修改前行为推演，不是统计效果比较。此前主 agent 对 auth 的自验也不追溯记为干净子 agent 验收。

## 改写范围

入口维护闭环及退出条件；验收 Skill 定义干净上下文、派发材料、实际执行、冻结源码和结果证据；调研 Skill 定义修复方案比较与证据深度。编码、计划、排障、审查改为交接到这些权威规则，不复制整套流程。README 仅提供入口。

## 验证安排

1. 独立验收会话核对 Skills 当前文字、五种边界场景与仓库检查，不读取历史结果。场景推演和静态检查分别报告。
2. 独立协调会话在临时 Python 会话缓存项目中实际使用新版流程。原始需求包含初始化、身份切换、缓存读写、退出与退出后重登录；初始现有测试只覆盖账户切换。协调会话获得原始需求和源码，不获得预设缺陷或修法。
3. 记录实际子 agent 交接与失败、调研、修复、复验，检查是否满足上述判据；观察到规范问题则修正后交新的干净验收者再验。

临时夹具位置：`/tmp/redberry-clean-acceptance-90yw4a9h/fixture`。源码、测试与正式证据已归档到 [fixture](acceptance-loop-evidence/fixture/task.md)，报告中的临时路径保留为原执行环境记录。

## Skills 独立验收结果

验收者 `/root/clean_skills_acceptance_1` 使用 `fork_turns: "none"`，未读取实现会话、历史测试结论或修改前快照。其逐项核对 10 个 Skills、README 与相关规范，未发现必修问题；五种边界的文字推演全部符合要求，报告明确区分推演与实际业务执行。

本轮实际运行：

- `python3 scripts/check-skills.py`：10 个 Skills，0 个问题。
- `python3 scripts/sync-references.py --check`：0 个漂移。
- `git diff --check`：退出码 0。
- 主 agent 另外逐个执行系统 `quick_validate.py`：10 个 Skills 全部有效。

验收范围的聚合 SHA-256：`68d1b4d46c12123285dacb8573310bb98da3b3f72bb8727e1387405340fbdc3f`。README 在验收早期补充职责指针后，验收者重新核对当前内容；最终稳定性检查无变化。

证据：[独立报告](acceptance-loop-evidence/skills-audit/report.md)、[实际检查原始结果](acceptance-loop-evidence/skills-audit/static-checks.json)、[源码哈希](acceptance-loop-evidence/skills-audit/source-hashes.json)、[稳定性检查](acceptance-loop-evidence/skills-audit/source-stability.json)。

## 真实夹具闭环结果

协调与实现者为 `/root/clean_loop_trial`，以不继承父会话的方式创建。它按新版入口分别创建以下验收者，两次均实际设置 `fork_turns: "none"`；验收时业务源码保持固定。第二轮交接完整需求、运行条件和原始复现日志，未传调研方案或实现者自评。

| 阶段 | 实际执行者与结果 | 证据 |
| --- | --- | --- |
| 第一轮独立验收 | `/root/clean_loop_trial/acceptance_round1`；核对完整 A—E，11 项测试中 2 处失败，发现 D 退出及重复退出仍残留缓存；未修改业务实现 | [首轮报告](acceptance-loop-evidence/fixture/reports/round1.md)、[原始日志](acceptance-loop-evidence/fixture/reports/round1-unittest.log) |
| 调研与修复 | 协调者依据源码和复现比较三种处理方式；选择退出时无条件原地清空缓存，保留身份及接口约定，增加 `cache.clear()` | [方案依据](acceptance-loop-evidence/fixture/reports/remedy.md) |
| 编码自检 | 同一测试入口 11 项通过；明确标记为自检，未据此交付 | [自检日志](acceptance-loop-evidence/fixture/reports/coding-selfcheck.log) |
| 第二轮独立验收 | 新验收者 `/root/clean_loop_trial/acceptance_round2`；重新核对 A—E，补充 5 项测试，16 项全部通过；原失败复现已关闭，无范围内未验项 | [复验报告](acceptance-loop-evidence/fixture/reports/round2.md)、[原始日志](acceptance-loop-evidence/fixture/reports/round2-unittest.log) |
| 最终审查 | 协调者检查全部公开入口、状态及证据，无剩余必修问题；源码与第二轮基准一致 | [审查报告](acceptance-loop-evidence/fixture/reports/review.md) |

最终夹具 `store.py` SHA-256：`43ecd19f0fba425e2f5e954c7eb0995225c55e4f61cd207dd80362754b94da68`。实际审查由协调与实现者执行，未将其表述为另一轮独立行为验收。

## 结论与限制

本次观察到新流程在一个真实可执行夹具中完成“干净验收发现问题 → 调研比较 → 修复自检 → 新干净验收者全量核对 → 审查交付”；规范的独立审查及静态检查也通过。相关源码和原始失败记录均保留，没有删用例或缩小 A—E 判据。

这是一次真实夹具闭环及五种边界推演，未进行统计重复抽样；不能保证所有模型长期遵循。多次修复后又发现新缺陷、能力缺失和部署阻断仅做规则推演，未在真实环境中逐一制造。auth 本轮未重验，之前自验报告仍不代表满足新的独立验收要求。
