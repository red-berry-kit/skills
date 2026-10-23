# Red Plum Skills 独立验收与审查报告

## 结论与范围

本轮验收通过，代码审查未发现必须修复的问题。此结论限定为当前 10 份 SKILL.md 与 README 的流程规则可执行性、一致性、授权边界、退出条件以及指定静态检查；不代表在真实业务项目中执行过五轮场景，也不保证任意模型或客户端始终遵守这些规则。

README 首段在本轮早期补充了流程与验收规则职责指针；接到通知后重新阅读全文并核对哈希，当前内容已被本报告记录的源码哈希覆盖。该补充与入口和 verification 的定义一致，没有新增授权或改变阶段出口。

验收者：新建独立子 agent `/root/clean_skills_acceptance_1`。本会话未获得父会话历史；仅读取派发范围、当前源码及项目规则。未阅读 `tests/workflow/` 的历史结论或父目录 `before`。没有递归派发 agent，没有修改产品文件。报告与原始检查记录仅写入 `/tmp/redplum-clean-acceptance-90yw4a9h/skills-audit/`。

环境：Linux 文件系统、bash、python3、git；仓库 `/home/mapleafgo/Projects/OpenProject/red-plum-kit/skills`。范围为 using-redplum、redplum-verification、redplum-research、redplum-code-review、redplum-coding、redplum-debugging、redplum-planning，以及 redplum-requirements、redplum-design、redplum-proof-of-concept 和 README。补充读取检查脚本、docs/conventions.md、docs/design.md，并检索关联规范的流程用语；未将技术框架规范当成阶段流程的另一份定义。

## 实际检查证据

以下命令均在 Skills 仓库实际执行，保存到 `static-checks.json`，不是文字推演。

| 命令 | 退出码 | 实际结果 |
| --- | --- | --- |
| `python3 scripts/check-skills.py` | 0 | 检查 10 个 Skills，0 个问题 |
| `python3 scripts/sync-references.py --check` | 0 | 发现漂移：0 个文件 |
| `git diff --check` | 0 | 无标准输出或错误输出 |

静态检查脚本已人工阅读：check-skills 检查 frontmatter、英文 description、名称引用与包内 Markdown 链接；sync-references 的 `--check` 只比较 docs 与已有 references 的内容，不改写文件。`git diff --check` 主要覆盖已跟踪差异，不能替代新增文件审查；本轮直接读取了范围内所有 SKILL.md 与 README，包括未跟踪文件。

## 逐项判据

以下位置以当前文件行号表示，均相对仓库根目录。

| 判据 | 结果 | 实际证据与判断 |
| --- | --- | --- |
| 入口负责路由，专业 Skill 负责阶段内容 | 通过 | `using-redplum/SKILL.md:18` 的路由表与各阶段输入、执行、出口对应；`README.md:3` 和 `docs/design.md:75` 将阶段流程唯一来源限定到 SKILL.md。 |
| 需求、设计、计划不混为编码 | 通过 | requirements 第 8、17 行起定义行为判据；design 第 10、17 行起定义职责、状态与定案；planning 第 10、17 行起定义任务和验证映射；各阶段缺口有交接去向。 |
| 调研、POC 与正式验收边界清楚 | 通过 | research 第 17、21 行区分方案依据和必须查证的外部事实；POC 第 8、20 行将可行性返回设计，正式实现另验收；verification 第 8、21 行禁止用 POC 等替代行为验收。 |
| 单独使用专业阶段能获得本阶段产出 | 通过 | 9 个专业 Skill 均包含输入、执行和出口；requirements:8、design:21、planning:21、research:27、POC:22、debugging:21、verification:30、code-review:22 明确限定调用目的；coding:20 明确交付实现及自检材料，整体完成另交验收。README:7 说明名称交接不等于下游已安装或执行。 |
| 已授权工作无需反复确认 | 通过 | using-redplum:37、debugging:21、planning:19、design:21 明确复用授权并继续；requirements:14 仅将无法查明且改变结果的业务选择交用户决定。 |
| 阶段切换不扩大授权 | 通过 | using-redplum:34、43、52、54，code-review:22，verification:30 均保留仅阶段任务的出口与修复/发布授权边界；没有以进入流程为由授权安装、发布、修改业务或外部操作。 |
| 纯文案不强制走软件实施全流程 | 通过 | using-redplum:35 直接处理文档纠错；coding:22 允许低风险文案仅核对实际差异及适当检查，无需新增镜像测试。正式实现的独立验收要求不会把入口已排除的纯说明任务重新纳入软件实施链。 |
| 正式验收必须是干净且新的执行者 | 通过 | verification:12 明确关闭继承、`fork_turns: "none"`、不复用旧验收者，且已派发验收者不递归派发；using-redplum:41 与 coding:20 一致。 |
| 验收隔离与证据来源明确 | 通过 | verification:14、16 规定原始材料、避免预设结论、固定源码、禁止验收者改实现；verification:21 明确复用证据需核对源码与环境；验收报告要求轮次、标识与源码基准。 |
| 失败后持续调研、修复、重新独立验收 | 通过 | using-redplum:43–48 明确问题记录、必要排障、方案依据、实施、新验收者及审查循环；research:19、21 允许机械修复用本地证据简写，但不能省略理由。 |
| 后续发现的受影响入口必须覆盖 | 通过 | planning:13、coding:13、verification:22、code-review:13 均追踪共享入口；using-redplum:48、50 要求完整清单、受影响项与必要回归，不以上一缺陷关闭替代整体通过。 |
| 完成与阻断条件明确且不降标 | 通过 | using-redplum:50、52、54 规定全部必需项、必修问题关闭、审查完成、最终源码证据；verification:28、30 规定完成与部分完成；缺环境只能保留缺项。 |
| 阶段结束不会错误宣称实现完成 | 通过 | requirements:21、design:21、POC:20、coding:20、verification:28 明确各自结论范围；research:25、planning:19 交付已证明内容与未决项。 |
| 英文 description、中文正文 | 通过 | 静态检查覆盖 10 个 description；人工逐份读取正文，说明与规则为中文，技术名称、代码标识和命令保持原样。 |
| 包内引用可解析、规范副本一致 | 通过 | check-skills 0 问题、sync-references --check 0 漂移；README:7 正确区分相对文件链接与跨 Skill 阶段名称。 |

## 五种边界的文字推演

本节是根据当前规则逐步推演的预期动作，不是对真实应用发请求、实施修复或再次派发子 agent 的执行记录。

| 场景 | 推演步骤与退出状态 | 判定及依据 |
| --- | --- | --- |
| 全绿自检后交付 | 编码记录自检原始证据 → 主 agent 派发新的干净验收者 → 完整判据验收 → 代码审查 → 确认最终源码、必需项与问题状态后交付。仅自检绿色不能提前交付。 | 文本推演通过；coding:20，verification:12、21、28，using-redplum:50。 |
| 已知修法的验收失败 | 记录问题与已确认根因 → research 复核本地证据/相关来源，记录当前约束下方案选择理由 → 按需调整计划 → coding 修复自检 → 新干净验收者重验 → 审查。机械修复不要求编造候选或机械联网，仍保留方案判断。 | 文本推演通过；using-redplum:45–48，research:19–21，debugging:19。 |
| 修复后二次验收发现另一受影响入口 | 将新入口关联现有范围及判据，记录新失败；不是沿用第一次已修状态收尾。核实根因/方案，更新计划并修复；再换新验收者，核对完整清单，覆盖原失败、新影响及必要回归。若它属于未经授权的新功能则返回范围决策，不擅自扩展。 | 文本推演通过；using-redplum:48、50，verification:21–23，code-review:13，requirements:12。 |
| 只验收不修复 | 执行允许范围的独立检查，按逐项状态交付报告；失败不授权验收者改业务，不触发主 agent 自动修复或发布。必需项失败则报告部分完成/不通过，但验收报告这一受托产出可交付。 | 文本推演通过；verification:16、30，using-redplum:52。 |
| 无独立子 agent 或必需环境缺失 | 无独立上下文能力时报告能力缺口，已有自检保留为自检；环境不足时寻找不影响用户服务的独立验证方式。继续可执行部分，记录受影响判据、恢复步骤和替代证据范围；不能宣称独立验收或全部完成。 | 文本推演通过；verification:16、24、30，using-redplum:52、54。 |

## 问题、复用与限制

- 已确认必修问题：无。未将风格偏好或没有复现的疑虑当成缺陷。
- 未复用历史验收结论；报告中的三项静态检查是本轮重新执行。为保存原始记录，命令在只读条件下又执行一次，结果一致。
- 没有真实业务应用可供本轮范围内演练，五种边界仅证明规则可解释且彼此一致；不能据此声称真实业务修复链、环境故障恢复或各种客户端的独立会话能力已经实际通过。
- 本轮实际使用了一位独立验收者，未测试所有客户端的 `fork_turns` 等效行为；规则自身要求能力不足必须受阻，覆盖了无法保证独立性的出口。
- 未审查全部技术规范的框架正确性、全部历史变更或未授权发布行为。技术规范的同步一致性由实际静态命令证明；流程相关补充阅读用于检查与 Skills 的冲突。
- 此审查没有库/框架 API 或外部技术事实待查，未发起 Context7 或互联网请求。

## 源码基准

11 份范围文件按相对路径映射到 SHA-256，映射以键排序后 JSON 序列化所得的聚合 SHA-256：

`68d1b4d46c12123285dacb8573310bb98da3b3f72bb8727e1387405340fbdc3f`

每份文件的 SHA-256、Git HEAD、记录时间见 `source-hashes.json`。该文件另包含排除 `.git` 和 `tests/workflow/` 历史目录的文件内容哈希，后者仅用于检测检查期间文件漂移，不代表这些文件全部经过人工审查。最终稳定性核对结果见 `source-stability.json`。
