# 第 1 轮独立验收

结论：部分完成，不能判定本轮验收通过。A、B、C、E 通过；D 的缓存清除和带缓存重复退出失败。全部 A—E 判据均已实际执行，无未执行的必需项。

## 身份、范围与源码基准

- 验收者：`/root/clean_loop_trial/acceptance_round1`，本轮新建的独立验收上下文，未参与实现或修复，未递归派发。
- 工作目录：`/tmp/redberry-clean-acceptance-90yw4a9h/fixture`。
- 已实际读取：夹具 `AGENTS.md`、`requirements.md`、`store.py`、`test_store.py`；安装路径 `/home/mapleafgo/Projects/OpenProject/red-berry-kit/skills/` 下的 `redberry-verification/SKILL.md` 和 `using-redberry/SKILL.md`。
- 未读取：任务过程记录、Skills 测试及其他历史材料。没有复用历史检查结论。
- 范围：当前内存会话缓存，完整 A—E；不增加持久化或依赖。
- 业务源码：`store.py`，SHA256 为 `410a16f5880a0680eb33f307a1e23c361110417d10977c9aafa8fa90c47e4042`。测试前、测试后及复现后均核对一致；未修改业务源码、需求或 Skills。
- 环境：Python 3.14.8；Linux x86_64，详细版本见 [环境日志](round1-environment.log)。

## 从需求建立的验收表

表中测试方法均在 `test_acceptance_round1.AcceptanceRound1` 下，由实际入口 `python3 -m unittest discover -v` 执行；完整输出见 [原始测试日志](round1-unittest.log)。测试按 A—E 独立建立，既有单条测试仅作为附加回归。

| 判据 | 实际入口与场景 | 验证方式 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| A 初始状态 | 新建 SessionStore | `test_A_initial_state` 同时检查 user 为 None、cache 为空 | 通过 | round1-unittest.log |
| B 建立身份 | 新实例调用 set_user("a") | `test_B_set_identity` 检查 user | 通过 | round1-unittest.log |
| B 相同身份保留缓存 | a 写入两个键，再 set_user("a") | `test_B_same_identity_preserves_all_cache` 检查身份与完整缓存 | 通过 | round1-unittest.log |
| B 不同身份清除缓存 | a 写入两个键，再 set_user("b") | `test_B_different_identity_clears_all_cache` 检查新身份、空缓存及逐键读取 | 通过 | round1-unittest.log |
| C 写入与读取 | 相同键逐次写入字符串、0、False、空字符串、None、字典 | `test_C_put_get_and_overwrite` 检查读取值与键存在 | 通过 | round1-unittest.log |
| C 缺少键 | 空缓存、已有其他键的缓存分别读取 missing | `test_C_missing_returns_none` 检查 None 且其他键保持 | 通过 | round1-unittest.log |
| D 清除身份 | a 写入缓存后 logout | `test_D_logout_clears_identity` 检查 user 为 None | 通过 | round1-unittest.log |
| D 清除全部缓存 | a 写入两个键后 logout | `test_D_logout_clears_all_cache` 检查缓存；直接复现补充 get 结果 | 失败，R1-001 | round1-unittest.log、round1-reproduction.log |
| D 重复退出保持退出状态 | 分别在无缓存、有缓存时连续 logout 两次 | `test_D_repeat_logout_keeps_exited_state` 检查身份、缓存与读取 | 无缓存通过；有缓存失败，R1-001 | round1-unittest.log、round1-reproduction.log |
| E 同一用户重新登录 | a 写入两个键，logout，再 set_user("a") | `test_E_same_user_relogin_has_no_previous_cache` 检查身份、缓存和旧键读取 | 通过 | round1-unittest.log、round1-reproduction.log |

## 命令及原始证据

所有命令在夹具根目录执行。

```bash
python3 -m unittest discover -v
```

退出码 1；共 11 个测试方法（新增 10 个、已有 1 个），2 处失败。完整标准输出与错误输出合并保存于 [round1-unittest.log](round1-unittest.log)，没有删减失败信息。

```bash
python3 -c 'exec(open("reports/reproduce_round1.py").read())'
```

退出码 0；这是状态打印脚本，退出码不代表业务验收通过。原始状态见 [round1-reproduction.log](round1-reproduction.log)，脚本见 [reproduce_round1.py](reproduce_round1.py)。测试源码见 [test_acceptance_round1.py](../test_acceptance_round1.py)。

## 问题 R1-001

- 对应判据：D。
- 触发：创建实例，set_user("a")，写入 first="private" 和 second=0，调用 logout；随后重复 logout。
- 预期：第一次及重复退出后 user 均为 None，cache 为空，get("first") 和 get("second") 均为 None。
- 实际：身份为 None，但两次退出后 cache 均仍为 `{'first': 'private', 'second': 0}`；get("first") 仍返回 `'private'`，get("second") 仍返回 `0`。
- 复现稳定证据：独立测试的两个失败点与直接调用脚本输出一致。
- E 独立结果：随后同一用户重新登录，缓存为空，旧键读取为 None；E 通过不能替代 D 的退出即时清除要求。
- 本报告仅陈述可观察失败，不指定修复方案。

## 未验项与交接

A—E 没有未验项。持久化、第三方服务、并发语义未被需求要求，未纳入范围。既有测试已重新执行，没有以开发者摘要替代验收证据。

将 R1-001 和本轮证据交回主 agent 按已授权的修复闭环处置；修复后交新的干净验收上下文核对完整 A—E。本轮不能进入完成交付结论。
