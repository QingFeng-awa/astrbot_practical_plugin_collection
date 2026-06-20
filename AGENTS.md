# AGENTS.md

这是一个运行 AstrBot 上的插件，名为 AstrBot 实用插件合集（AstrBot Practical Plugin Collection）。
> AstrBot 是一个开源的一体化代理聊天机器人平台，与主流即时通讯应用集成。它为个人、开发者和团队提供可靠且可扩展的对话式人工智能基础设施。

插件的目的旨在集成多个插件并将其封装为一个统一插件，并通过改写代码等实现多功能互联来提供更统一流畅的使用体验。

项目目前仍在早期开发阶段。

## 项目结构

> 仅列出于实际开发可能有关的文件。

```
.
├── core/                            # 核心功能模块
│   ├── __init__.py                  # 核心模块导出
│   └── ban.py                       # 封禁系统，基于 aiosqlite 的本地封禁管理
├── module/                          # 插件功能模块
│   ├── __init__.py                  # 导出各模块处理器
│   ├── group_request_review/        # 加群请求自动审核模块
│   └── utils/                       # 模块共享工具
│       ├── __init__.py              # 统一导出工具函数与类
│       ├── api.py                   # ProtocolEndApi：封装 NapCat 协议端 API 调用
│       ├── filter.py                # event_filter：事件类型匹配过滤器
│       └── function.py              # 辅助函数：封禁检查、机器人身份检查
├── main.py                          # 插件入口，定义 PracticalPluginCollection 主类（继承 Star）
├── metadata.yaml                    # AstrBot 插件元数据（名称、版本、作者等）
├── _conf_schema.json                # AstrBot 插件配置项定义（JSON Schema 格式）
├── pyproject.toml                   # 项目配置（依赖、Python 版本、许可证等）
└── uv.lock                          # uv 包管理器锁定文件
```

### 技术栈

| 类别       | 技术                            | 说明                                                    |
| ---------- | ------------------------------- | ------------------------------------------------------- |
| 编程语言   | Python >= 3.13                  | 使用最新 Python 版本，无需考虑旧版兼容                  |
| 机器人框架 | AstrBot >= 4.17.6               | 基于 `Star` 类开发的一体化聊天机器人插件                |
| 协议适配   | aiocqhttp（NapCat / OneBot 11） | 通过 NapCat 协议端与 QQ 交互                            |
| 数据存储   | aiosqlite >= 0.22.1             | 用于核心与模块本地数据持久化                            |
| 包管理器   | uv                              | 现代 Python 包管理器，使用 `pyproject.toml` + `uv.lock` |
| 代码检查   | ruff >= 0.15.13                 | 开发依赖，用于代码风格与质量检查                        |
| 许可证     | AGPL-3.0-or-later               | 强 copyleft 许可证                                      |
| 支持平台   | aiocqhttp                       | 仅考虑支持 NapCat/Onebot 11 协议端                      |
