# README.LLMS.md 编写场景

## 输入

为虚构 notify 模块编写中文 README.LLMS.md，面向使用它的 Agent。使用约定清楚，附公共方法列表简注和源码链接，不写代码块。尽量完整，让 Agent 能正确使用，同时避免只得到代码目录。

材料已核实如下，不要求访问实际文件：

- README.md 已介绍 notify 用途。实现使用 Go、Fx、SMTP；框架统一负责安装、发现、配置分组。
- backend/sender.go 的 Sender.Send(ctx, Message) error：调用前按实际接收者检查授权；取消时停止等待；失败由调用者决定是否重试。
- backend/config.go 的 Config：Address 默认 127.0.0.1:2525，Timeout 默认 5s，QueueSize 默认 100。内部 Schema/Validate 钩子自动执行。
- backend/module.go 的 Module：默认装配，后台投递器仅在 serve 运行。
- backend/command.go 已注释 send-once 命令的参数与默认值。
- backend/message.go 的 Message、Template 用于构造消息；秘密不得写入消息或错误日志。
- 本仓库没有短信接口。所有代码注释已包含签名、字段、参数值与用法示例。

## 判据

正文按使用能力组织，明确授权前提、上下文取消、失败重试责任和秘密保护；方法名称配短注与声明文件链接。可以简要注明后台投递仅在服务运行时使用。

不复述技术栈、安装发现流程、未提供的能力、内部钩子、配置值和逐项命令参数；不复制函数签名或示例代码；不退化成目录／方法列表，也不只跳转到 README。不凭空补出发送重试实现或安全保证。

此场景只验证已给定事实的写作判断；源码调查能力、真实链接可达与多次执行稳定性另行验证。
