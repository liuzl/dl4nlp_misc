# 对话系统 - 智能闲聊🦜

基础闲聊接口提供基于文本的基础聊天能力，可以让您的应用快速拥有具备语义理解能力的机器聊天功能。

### HTTP请求

`POST https://semantics.work/chitchat/api`

### 请求参数

参数 | 描述
--------- | -------
`text` | `字符串`，用户输入的聊天内容，UTF-8格式编码 

### 状态码说明

status | 说明
--------- | -------
`ok` | 查找成功
`fail` | 失败，此时`message`保存错误信息

### 回复信息说明

字段 | 说明 
--- | ---
`message`|智能闲聊回复文本，UTF-8编码
