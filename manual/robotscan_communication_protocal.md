# 通过TCP消息控制RC
## 使用步骤
- 1.RC启动后，作为TCP客户端连接本机18878端口
- 2.通过TCP发送指令
## 现有指令
* 结束

```
msgBegin{"topicWorkflow":"ExtraCommModuleRequest","redirectAutomationCmd":"1","cmd":"CommModule_Stop"}msgEnd
```
* 开始

```
msgBegin{"topicWorkflow":"ExtraCommModuleRequest","redirectAutomationCmd":"1","cmd":"CommModule_Start"}msgEnd
```
* 暂停

```
msgBegin{"topicWorkflow":"ExtraCommModuleRequest","redirectAutomationCmd":"1","cmd":"CommModule_Suspend"}msgEnd
```
* 继续

```
msgBegin{"topicWorkflow":"ExtraCommModuleRequest","redirectAutomationCmd":"1","cmd":"CommModule_Resume"}msgEnd
```
* 导入程序

```
msgBegin{"topicWorkflow":"ExtraCommModuleRequest","redirectAutomationCmd":"1","cmd":"CommModule_Open_Template","filename":"plc_2_wait3.scanTemplate","path":"C:/Users/haoyu/Documents/RobotScanControl/Solution/Project_201/programProcedure"}msgEnd
```

*filename字段为节点程序文件名称，path字段为节点程序的不含文件名的绝对路径*