![astrbot_practical_plugin_collection](https://socialify.git.ci/QingFeng-awa/astrbot_practical_plugin_collection/image?description=1&font=KoHo&language=1&name=1&pattern=Solid&theme=Auto)

> [!Warning]
> 当前项目为**早期开发阶段**，可能每个新版本都会存在破坏性变更，请自行做好相关准备。

## 介绍

PracticalPluginCollection 是 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的实用插件合集，旨在集成多个插件并将其封装为一个统一插件，并通过改写代码等实现多功能互联来提供更统一流畅的使用体验。

### ...为什么？

原本我是使用 ZeroBot-Plugin (zbp) 项目的，这个项目是一个 ZeroBot 插件合集，集成了大量插件。\
但毕竟 zbp 是基于 ZeroBot 的，而我更希望使用 AstrBot，我不喜欢同时接入多个机器人框架，容易导致机器人左右脑互搏（功能冲突）；zbp 还将仓库分为了超多仓库/module，可能开发团队这么做有他们的用意，但恕我无法接受改一个功能要翻几个仓库。\
此外 zbp 几乎把日志功能当空气，项目几乎没有日志记录，出现错误直接将错误信息发送给用户，好比：
```py
except Exception as e:
    await event.send(e)
```
错误堆栈一个没有，上下文也没有日志，报个`ERROR: unknown`我怎么知道问题出在哪里？

综上所述，最终我决定创建这个项目，命名为 PracticalPluginCollection，目标就是打造一个 AstrBot 版本的 zbp。

## 功能

> 详细文档目前仍处于计划中。

- 核心 (Core) 功能
  - [x] 封禁系统
  - [ ] 经济系统
  - And More...
- 模块 (Module) 功能
  - [x] 加群自动审核（group_request_review）：提供了基于正则表达式的加群自动处理功能，能够通过正则判断入群答案从而自动同意/拒绝请求，支持等级/速率限制等筛选条件。
  - [ ] 简易入群人机验证（simple_captcha）
  - [ ] 群老婆（qq_wife）
  - [ ] 今日人品（daily_luck）
  - [ ] 我超，盒！（box）
  - And More...

## 鸣谢

- [FloatTech/ZeroBotPlugin](https://github.com/FloatTech/ZeroBot-Plugin) 提供了本项目部分功能想法及实现思路/代码。
- [Zhalslar/astrbot_plugin_box](https://github.com/Zhalslar/astrbot_plugin_box) 提供了本项目模块 `box` 的想法来源。
- [qiqi55488/astrbot_plugin_appreview](https://github.com/qiqi55488/astrbot_plugin_appreview) 提供了本项目模块 `group_request_review` 的想法来源。
- [huntuo146/astrbot_plugin_Group-Verification_PRO](https://github.com/huntuo146/astrbot_plugin_Group-Verification_PRO) 提供了本项目模块 `simple_captcha` 的想法来源。
- [sealdice/sealdice-core](https://github.com/sealdice/sealdice-core) 本项目模块 `daily_luck` 的想法来源。
