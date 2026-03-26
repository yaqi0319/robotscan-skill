# RobotScan OpenClaw Skill

这是一个为 OpenClaw 平台设计的 RobotScan 自动化扫描控制技能。

## 功能特性
- **跨平台运行**：默认使用 Node.js (`scripts/robotscan_client.js`) 以适配 OpenClaw 原生环境。
- **结构化通讯**：采用标准 JSON 格式进行输入输出，确保 AI 准确解析。

## 安装与配置
1. 将本项目解压/克隆到 OpenClaw 的 `skill/` 目录下。
2. 确保 RobotScan 服务运行在 `127.0.0.1:18878`（可在 `robotscan_client` 脚本中修改）。
3. 无需额外安装 Python 环境（使用 Node.js 模式）。

