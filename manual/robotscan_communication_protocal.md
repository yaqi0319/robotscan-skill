# RobotScan Control通信方法论

## 1. 确定RobotScan Control路径
- 1. 检查前置路径配置，如果缺失/不正确，先自己想办法拿到，实在没办法再请求用户帮助：
    - **RobotScan_exe_path**：RobotScan Control.exe程序路径
    - **Log_path**：RobotScan_exe_path同级目录下的'/userlog'文件夹
    - scanTemplate：扫描程序路径
    - rsc：RC工程路径
    - report：检测报告存放的路径
- 2. 路径位置在config/path.json中

## 2. 通过TCP消息控制RC
### 使用步骤
- 1. RC启动后，作为TCP客户端连接本机18878端口
- 2. 通过TCP Socket发送指令
- 3. 核对log路径，需要确定状态时读取log文件，以log作为状态判断的依据

### 现有指令
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