# nonebot_plugin_todo_nlp

一款自动识别提醒内容，可生成todo图片并定时推送的nonebot插件

消息响应器集合：add_todo, finish_todo,remove_todo,change_todo, get_todo_pic

### 插件特点：

* 允许多样化的日期描述方法，可以在语句中包含“明天”、“9月1日”等日期提示
* 自动识别语句中的事项

### 触发关键词：

* 增加事项: '提醒', 'nonebot_todo'
* 完成事项: '完成'
* 删除事项（支持正则）: '删除', '去掉'
* 修改事项时间: '更正', '改'
* 获取图片: '获取todo'

> 若要强调事件名称（nlp有的时候会犯蠢，比如在示例中机器人没能识别出“中秋假期”这一关键词）：使用英文双引号括上事项名称

### 推送配置方法：

```
TODO_QQ_FRIENDS=[864341840]
TODO_SEND_TIME=[{"HOUR":08,"MINUTE":00}]
```

### TODO：
- [ ] 迁移到postgre数据库
- [ ] 增加优先级相关功能
- [ ] 增加完成todo统计，对完成状况进行跟踪
- [ ] 增加todo项目复用功能（比如每日/每周某天的提醒可以复用）
- [ ] 完善相关log

### 示例：

![1.png](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/1.png)

![2.jpg](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/2.jpg)
