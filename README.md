# nonebot-plugin-todo-nlp

一款自动识别提醒内容，可生成todo图片并定时推送的nonebot2插件，v11适配器可用

nlp支持来源于[jionlp](https://github.com/dongrixinyu/JioNLP) （十分便利的nlp库）

图片生成功能来源于nonebot插件[htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender) 
（我们先进的的浏览器制图已经完全超越了老式的PIL制图了（不是））

### 插件特点：

* 允许多样化的日期描述方法，可以在语句中包含“明天”、“9月1日”等日期提示
* 自动识别语句中的事项

### 安装

#### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```
nb plugin install nonebot_plugin_todo_nlp
```

- 使用 poetry

```
poetry add nonebot_plugin_todo_nlp
```

- 使用 pip

```
pip install nonebot_plugin_todo_nlp
```

#### 从 GitHub 安装（不推荐）

```
git clone https://github.com/Jigsaw111/nonebot_plugin_todo.git
```

### 食用方法：

触发关键词：

* 增加事项: '提醒', 'nonebot_todo'
* 完成事项: '完成'
* 删除事项（支持正则表达式）: '删除', '去掉'
* 修改事项时间: '更正', '改'
* 获取图片: '获取todo'

> 若要强调事件名称（nlp有的时候会犯蠢，比如在示例中机器人没能识别出“中秋假期”这一关键词）：使用英文双引号括上事项名称

> **由于nonebot使用uvicorn框架，在windows平台使用时图片的导出可能会出现not implemented error。**\
> 解决方法：将env中的FASTAPI_RELOAD改为false。\
> 见nonebot-plugin-htmlrender [issue#25](https://github.com/kexue-z/nonebot-plugin-htmlrender/issues/25) ;\
> nonebot2文档中对此亦有提及，见[fastapi_reload](https://nb2.baka.icu/docs/tutorial/choose-driver#fastapi_reload) 。

### 配置方法：

在env中添加如同以下格式的配置（多个send time则多次推送，**注意时间首位去0！**）：\
在群聊中使用时，只有管理员和群主可以增删todo项目。
私聊情况下，好友均可使用todo增删功能，此处配置是推送名单。

```
TODO_USERS=["1234567890"]
TODO_GROUPS=["1234567890"]
TODO_SEND_TIME=[{"HOUR":8,"MINUTE":0},{"HOUR":19,"MINUTE":34}]
```

### TODO：

- [ ] 迁移到postgre数据库
- [ ] 增加优先级相关功能支持
- [ ] 增加完成todo统计，对完成状况进行跟踪
- [ ] 增加todo项目复用功能（比如每日/每周某天的提醒可以复用而不用手动再次添加）
- [ ] 完善相关console log
- [ ] 更加优雅的todo使用订阅与推送时间配置
- [ ] （可能后期会加上其他的todo主题？）

### 更新日志

2022-9-4：适配python3.8

2023-1-20: 升级nonebot_plugin_apscheduler依赖

### 示例：

![1.png](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/1.png)

![2.jpg](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/2.jpg)
