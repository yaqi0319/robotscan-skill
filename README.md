# RobotScan OpenClaw Skill

这是一个为 OpenClaw 平台设计的 RobotScan 自动化扫描控制技能。

## 功能特性
- **跨平台运行**：默认使用 Node.js (`scripts/robotscan_client.js`) 以适配 OpenClaw 原生环境，同时保留 Python (`scripts/robotscan_client.py`) 备选。
- **结构化通讯**：采用标准 JSON 格式进行输入输出，确保 AI 准确解析。
- **稳健的 SOP**：内置安全预检、自动标定引导、异常（如服务离线）处理逻辑。
- **多语种手册**：支持 FreeScan、OptimScan_Q 和 Trak 系列。

## 安装与配置
1. 将本项目解压/克隆到 OpenClaw 的 `skill/` 目录下。
2. 确保 RobotScan 服务运行在 `127.0.0.1:18878`（可在 `robotscan_client` 脚本中修改）。
3. 无需额外安装 Python 环境（使用 Node.js 模式）。

## 核心指令
- 获取状态：`node ./scripts/robotscan_client.js --action status`
- 执行扫描：`node ./scripts/robotscan_client.js --action scan --params '{"mode": "detail", "resolution": 0.05}'`
- 标定尝试：`node ./scripts/robotscan_client.js --action start_calib`

## 注意事项
- 扫描前请务必确认“防护门已关闭”且“急停已释放”。
- 当接口返回 `NEED_CALIBRATION` 时，请跟随 AI 的引导进行操作。
