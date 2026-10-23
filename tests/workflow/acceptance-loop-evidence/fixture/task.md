# 会话缓存正式验收与修复任务

## 目标与授权

仅验收并修复当前夹具中的内存会话缓存；不增加持久化或第三方依赖，不修改 Skills、真实业务或 auth，不提交、不发布。按 `requirements.md` 全量核对 A—E，现有测试仅作自检证据。协调者：`/root/clean_loop_trial`。

## 流程与当前阶段

已实际读取 `using-redplum`、`redplum-verification`、`redplum-research`、`redplum-coding`、`redplum-code-review` 及夹具 `AGENTS.md`，并读取 coding 的开发约定索引；实际入口以夹具规则优先。当前阶段：第二轮完整独立验收与代码审查均完成，已达到本任务交付条件。

## 完整验收条件

| 条件 | 行为 |
| --- | --- |
| A | 初始身份为 None，缓存为空 |
| B | 设置身份；相同身份保留缓存，不同身份清空缓存 |
| C | put 写缓存，get 返回缓存值，缺失返回 None |
| D | logout 清除身份和全部缓存，重复调用保持退出状态 |
| E | 退出后同一用户登录不能读取退出前缓存 |

## 原始基准与环境

- 目录：`/tmp/redplum-clean-acceptance-90yw4a9h/fixture`。
- Python：`Python 3.14.8`。
- `store.py` SHA-256：`410a16f5880a0680eb33f307a1e23c361110417d10977c9aafa8fa90c47e4042`。
- 初始 `test_store.py` SHA-256：`cef4ee2f251dca9a7d5bbf81423bc77ee458896b028ec0323a9eea371a69a38f`。
- `requirements.md` SHA-256：`dd122ee13238ea46238454df172d8e46b7b6a6111c778e8fac18ef62e2b7925d`。
- 已执行源码读取、`sha256sum store.py test_store.py requirements.md`、`python3 --version`，退出码均为 0。

## 验收轮次

第一轮验收者 `/root/clean_loop_trial/acceptance_round1`，以 `fork_turns=none` 新建，未参与实现，期间业务源码固定。结果：A、B、C、E 通过，D 失败。实际入口运行 11 个测试、2 处失败、退出码 1；详见 `reports/round1.md` 及原始日志。完整清单全部检查，现有测试没有替代验收清单。

第二轮验收者 `/root/clean_loop_trial/acceptance_round2`，另以 `fork_turns=none` 新建，没有参与实现、修复或前轮验收。交接完整需求与规则、当前源码哈希、运行入口和原始日志，未要求其阅读实现过程或推荐修法。它先核对完整需求，再核实历史失败，重新执行全部关键场景并补充 5 个测试。结果：A—E 全部通过，16 个测试、退出码 0；无必需未验项。源码在验收前后保持一致。报告为 `reports/round2.md`，原始证据为 `reports/round2-unittest.log`、`reports/round2-reproduction.log`、`reports/round2-environment.log`。

## 问题及调研交接

- R1-001：logout 仅清空身份，退出及重复退出仍能读取旧缓存，违反 D。根因由源码与第一轮复现直接确认，无需另行猜测排障。
- `reports/remedy.md` 记录原始来源、三个候选、选择理由和验证去向；选择 logout 中无条件原地清空缓存，与已有 set_user 的清理行为一致。`set_user(None)` 的替代方案不能处理身份已经为 None 而缓存有值的情况。
- 局部计划：只增加退出缓存清理，保留首轮回归测试；自检后另启新干净子 agent 全量验收，再做代码审查。没有职责、接口、依赖变化，无需另开设计或 POC；局部计划记录于此。

## 缺项与下一步

已在 logout 中增加 `self.cache.clear()`；当前 `store.py` SHA256 为 `43ecd19f0fba425e2f5e954c7eb0995225c55e4f61cd207dd80362754b94da68`。编码自检命令 `python3 -m unittest discover -v` 运行 11 个测试，退出码 0；原始证据 `reports/coding-selfcheck.log`。这是自检，不能替代正式验收。夹具没有配置额外格式、类型或构建入口，不新增第三方工具。

R1-001 已经第二轮独立复验关闭。最终代码审查由协调者按 `redplum-code-review` 执行，检查全部公开入口、状态转换、最终源码哈希和完整验收证据，未发现新问题，详见 `reports/review.md`。审查复用对应当前源码的第二轮原始通过证据，没有无理由重复运行。

## 交付状态

已完成：唯一业务改动为 logout 时无条件清空缓存；保留原始测试，新增完整验收与边界回归；问题调研、两轮独立验收原始日志、复现脚本及审查记录均保存在夹具。完整必需验收通过，必修问题关闭，代码审查完成，证据对应最终源码。

实际命令结果：第一轮 `python3 -m unittest discover -v` 为 11 测试、2 失败、退出 1；修复后编码自检为 11 测试通过、退出 0；第二轮同入口为 16 测试通过、退出 0；第二轮原始复现脚本退出 0，打印状态显示退出、重复退出及同用户重登均无旧缓存；最终源码与测试哈希核对退出 0。

无范围内待完成项。限制：本任务仅本地内存缓存，不验证并发、跨进程、持久化或真实部署；未修改夹具外文件、Skills、auth 或真实服务，未提交发布。下一步：交付本夹具代码与证据；继续扩展需求需另行确定范围。
