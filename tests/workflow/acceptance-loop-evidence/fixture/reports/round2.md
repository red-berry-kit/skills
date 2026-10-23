# 第 2 轮正式验收报告

本轮完整 A—E 通过，R1-001 在当前源码上已复验关闭；无新增问题、无范围内未验项。本轮验收完成，可交接 `redberry-code-review`。此结论仅覆盖约定的内存会话缓存，不代表已完成代码审查或发布。

## 身份与基准

- 验收者：`/root/clean_loop_trial/acceptance_round2`，本轮新建独立验收者，未参与实现、修复或前轮验收，未递归派发。
- 项目：`/tmp/redberry-clean-acceptance-90yw4a9h/fixture`。
- 实际读取：`AGENTS.md`、`requirements.md`、指定的 `redberry-verification/SKILL.md`、`store.py`、现有两个测试文件，以及指定的前轮原始日志和复现脚本。
- 未读取 `task.md`、`reports/remedy.md`、前轮验收摘要、Skills/tests、父目录 before 或其他历史任务材料；未采用实现者自检结论。
- Python：`3.14.8`；无第三方依赖，实际入口为 `python3 -m unittest discover -v`。
- `store.py` 执行前后 SHA256 均为 `43ecd19f0fba425e2f5e954c7eb0995225c55e4f61cd207dd80362754b94da68`，与交接值一致。详见 `round2-environment.log`。
- 本轮只新增测试和证据报告，没有修改业务源码、需求或 Skills，没有提交或发布。

## 独立覆盖核对与逐项验收

先独立核对需求、源码和现有测试，再读取前轮原始证据。开发者 `test_store.py` 只覆盖账号切换；现有 `test_acceptance_round1.py` 对 A—E 有基本覆盖。本轮按需求补充五个测试方法并独立执行全部测试，以下每项均有当前执行证据。

| 条件 | 实际入口与场景 | 验证方式 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| A | `SessionStore()` 初始身份与缓存；两个实例独立 | 断言 user 为 None、cache 为空，并确认另一实例写入不污染初始实例 | 通过 | `test_acceptance_round2.py` 的 `test_A_instances_start_empty_and_are_independent`；`round2-unittest.log` |
| B | `set_user` 建立身份；None→a、a→a、a→b、b→a、a→None、None→None | 每次预置两个缓存项，断言身份更新，同身份完整保留，异身份全部清空，并通过 get 核对 | 通过 | `test_B_identity_transitions_preserve_or_clear_every_entry`、前轮 B 三项；`round2-unittest.log` |
| C | `put/get` 写入、覆盖、缺失读取；字符串、0、False、空字符串、None、列表和字典 | 断言返回原写入值，覆盖后仅一个键，缺失读取为 None 且不新增键；前轮测试另覆盖无身份时读写 | 通过 | `test_C_writes_overwrite_and_missing_reads_do_not_mutate`、前轮 C 两项；`round2-unittest.log` |
| D | 有/无身份、有/无缓存的四种组合；单次退出和连续三次退出 | 每次 logout 后立即断言 user 为 None、全部缓存为空、各旧键均不可读取；另外重跑历史复现链 | 通过 | `test_D_logout_clears_immediately_and_is_repeatable`、前轮 D 三项；`round2-unittest.log`、`round2-reproduction.log` |
| E | 退出后同用户再次登录，连续 a、a、b、a 登录退出循环 | 每次重新登录断言无旧缓存，写入后退出再次检查不可读取；前轮同用户多键场景及历史脚本均重跑 | 通过 | `test_E_repeated_relogin_cycles_never_restore_old_values`、前轮 E；`round2-unittest.log`、`round2-reproduction.log` |

## 实际命令与结果

1. `python3 -m unittest discover -v`：退出码 0，16 个测试全部通过，包含现有 11 个测试及本轮新增 5 个测试；子场景由 unittest subTest 执行。原始输出为 `round2-unittest.log`。
2. `python3 -c 'exec(open("reports/reproduce_round1.py").read())'`：退出码 0；一次、二次退出后均为 `user=None`、`cache={}`、旧键读取为 None；同用户重登亦无旧值。原始输出为 `round2-reproduction.log`。该脚本只打印状态，退出码本身不证明通过；本报告逐项核对打印状态，并由完整测试中的断言提供自动判定。
3. 使用 `hashlib.sha256` 在执行前后核对业务源码，同时记录 Python 版本和工作目录，见 `round2-environment.log`。

## 历史证据核实与复用依据

- `round1-unittest.log` 记录 11 项测试中 D 的全部清缓存及重复退出两个失败断言，实际缓存仍包含旧值。
- `round1-reproduction.log` 与 `reproduce_round1.py` 一致：一次和二次退出后身份已清除但缓存及 get 结果残留；同用户重新登录后缓存为空。因此历史 R1-001 明确对应 D，不能仅靠 E 通过判断退出正确。
- 历史日志没有完整源码哈希与环境绑定，本轮仅用于核实原问题和复现步骤，不复用其通过结论，也不据此证明当前实现。
- 复用现有测试代码与复现脚本，是因为实际阅读后确认它们仍直接检验当前 A—E 判据，且无需第三方依赖或环境变更。全部重新执行；没有复用旧运行结果来替代本轮关键场景。

## 问题、未验项与边界

- R1-001：预期 logout 清除身份与全部缓存、重复退出保持此状态；历史实际为缓存残留。原触发条件本轮重新执行，已得到预期结果，当前源码复验通过。
- 新增问题：无。
- 范围内未验项：无。
- 持久化与第三方依赖不适用，用户明确排除。无网络服务、构建产物或部署入口；本轮验证的是 Python 本地真实对象调用链。线程并发、跨进程共享和任意非法输入未作为新增判据，需求未约定这些能力。
