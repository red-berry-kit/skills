# 模块使用说明改造验证

日期：2026-11-11。范围：模块说明归属、Skills 发现流程、CLI 模板与文档随源码交付。未提交或发布版本，未安装额外文档工具。

## 首轮方案（历史记录）

以下记录清理前的验证范围；最终文件名与规范清理结果见末节。

模块根 `llm.md` 是使用入口，链接实际 README／使用专题；维护规则在源码仓库的 `AGENTS.md`，同仓库模块不强制重复建立维护文件。通用 Skills 先定位真实来源、实现与版本，再读取对应使用说明并复用已有能力；具体 API 用法不复制进通用 Skill。规范保留跨模块契约与交付判据。

本轮涉及五个现有模块（boot、database、cache、auth、user）、CLI full/minimal 应用与模块模板，以及 Skills 索引和相关规范。运行时 API 与业务逻辑未因本轮文档改造而修改。

## 改造前对照

只读 agent `32e60545-5263-4d21-8062-ed3f5035e8a5` 实际读取入口、编码 Skill、API／模块规范和 query README：

- 能正确选择纯分页而不添加示例 Enabled 字段，也能推出本地来源优先；这两项不是失败。
- 缺少明确的使用／维护说明发现顺序，不能从文档确认依赖说明加载机制。
- 公共分页调用细节同时存在模块 README 与通用 API 规范，更新接口时需同步两份；缺少明确的唯一维护归属。

CLI 实施 agent `39c980c2-25e2-4905-a4ff-11837a3902ab` 在改模板前运行新测试，实际发现 full/minimal 缺发现步骤、CreateModule 缺根 README。此前唯一示例说明位于默认被过滤的 examples 下，无法作为安装后的使用入口。

## 本轮结果

### 行为推演

独立只读 agent `460504c9-b486-4066-bcba-aabe26da951d` 读取改造后的本地文件及 boot 使用链，推演五个场景：纯分页不复制业务字段；本地 sources 与线上 main 不一致时选实际来源；缺 llm 时报告交付缺口而不把 AGENTS 当回退；具体 API 示例归模块而非通用 Skill；必要链接越出交付包即不通过。

发现并关闭两项问题：工作区使用入口还指向已移除的 modules 仓库级 llm；“文档不会自动加载”的措辞未区分使用文档与客户端维护指令注入。修复后由同一 agent 只重读相关两处确认，不重跑无关场景。

这是行为推演，不是完整代理成功率评估，也不代表安装执行结果。审阅期间部分文件仍有外部更新，验收者已记录并重读受影响规则。

### 实际创建与安装

CLI 的 `internal/scaffold/module_docs_test.go` 从真实 CreateApp／CreateModule 产物执行依赖管理入口，覆盖：

- full/minimal 两套应用的使用与维护入口，以及后续 locked install 不覆盖业务自定义正文。
- 本地来源的实际目录／版本与文档即时更新。
- tag 0.1.0 的精确提交和多层 docs 文档，默认分支修改不污染锁定版本。
- 受管副本删除后的 locked 恢复，以及文档参与源码摘要校验。
- examples 默认过滤不影响 llm、README 与必要专题交付。

实施 agent 实际执行并报告退出码 0：

```sh
go test ./internal/scaffold -run 'Test(CreateAppModuleDocumentationDiscovery|CreatedModuleDocumentationDelivery)$' -count=1 -v
task test
task check
task build
git diff --check
```

`task test` 覆盖 CLI 全仓 Go race 测试与 26 项 Python 测试；`task check` 覆盖源码约束、staticcheck 与 go vet。无需修改生产复制逻辑：它原本递归保留未被显式过滤的文件，修复集中在模板、说明和回归测试。

### 静态与链接检查

主 agent 执行 `python3 scripts/check-skills.py`，10 个 Skills、0 个问题。对五模块实际交付范围检查 19 份 Markdown 的必要文件及本地链接：没有缺失目标、越出模块目录或指向被过滤 examples 的链接；该检查不验证远程 URL 或代码示例运行行为。三个仓库 `git diff --check` 通过。

## 验证边界

未运行全量浏览器、真实 PostgreSQL/MySQL/Redis 或部署验收；这轮没有改运行时，不以之前 API 封装任务的测试结果冒充本轮业务验证。CLI 使用隔离本地来源／Git tag 夹具验证交付机制，不代表远程发布或所有客户端会自动加载文档。现有模块使用说明只能保证本轮检查范围，客户端仍需显式按入口读取。

## 后续清理：统一 llm.txt

用户确认只需在通用入口说明“使用模块前，先读取该模块的 `llm.txt`”，不重复已有的复用原则，也不为各类模块说明保留独立跳转规范。

本轮删除 standards 中 api、cli、config、migrations、modules、structure、status 七份文件并清除有效引用。API 协议归入 boot 的 docs/api.md；配置与迁移补入各自 README；模块编写与目录协议归 CLI 自有文档。状态页重复的仓库说明与验证要求已有 README／阶段 Skill 承担，不留替代页。历史验收记录保持原判定，失效链接改为当时的路径说明或已有审阅快照。

五个模块、示例应用、CLI、工作区和三套创建模板统一采用 llm.txt，不保留旧名回退。CLI 执行者先将实际创建测试改为新文件名，确认 full/minimal/mod 因缺文件失败，再迁移模板；随后真实创建、本地来源、tag 安装、锁定恢复与旧名不存在断言通过。CLI 的 task check、task test、task build 全部通过，最后对新断言重跑 scaffold 定向 race 测试通过；这些结果来自本轮执行，不沿用首轮成绩。

主 agent 再次执行 Skills 检查（10 项、0 问题）与三个仓库的 diff --check，通过；清理后现行 Skills 文档和索引不再引用已删文件。未发布，远程规范内容的可访问性不属于本地检查通过范围。

