# RobotScan Agent (LangGraph)

这是一个基于 **LangGraph** 构建的 RobotScan 自动化扫描控制 Agent，旨在为 3D 扫描流程提供智能化的决策与执行能力。

## 架构说明
- **语言**: Python 3.9+
- **环境管理**: [uv](https://docs.astral.sh/uv/)
- **核心框架**: LangGraph (ReAct Agent)
- **通讯协议**: TCP (msgBegin{JSON}msgEnd)

## 核心架构 (Conceptual Architecture)

本项目遵循“智能体第一性原理”，将功能划分为以下核心概念：

- **大脑 (Brain - `agent.py`)**: 基于 LangGraph 的推理核心，集成了通信协议知识，负责决策与调度。
- **感官与工具 (Senses & Tools - `src/tools/`)**: 
  - **专业技能 (`robot.py`)**: 3D 扫描特有的硬核能力（状态监测、指令控制）。
  - **基础感知 (`system.py`)**: 对项目环境的观察力（文件浏览、安全读取）。
- **身体 (Body - `client.py`)**: 底层 TCP 通讯协议的 Python 实现，负责与 RobotScan Control 硬件进行物理信息交换。
- **记忆 (Memory)**: 具备会话级别的 Checkpointer，确保 Agent 能够理解复杂的连续任务指令。
- **知识库 (Knowledge - `manual/`)**: 各种 Markdown 格式的技术手册，Agent 会根据需要动态摄入知识。
- **配置与数据 (Config & Data)**: 
  - `config/`: 路径与系统配置。
  - `data/`: 实际的扫描项目与日志数据。

## 安装与运行

1. **安装 uv** (如果尚未安装):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **配置环境**:
   ```bash
   uv sync
   ```

3. **设置环境变量**:
   在根目录创建 `.env` 文件或设置环境变量：
   ```bash
   OPENAI_API_KEY=your_key
   OPENAI_API_BASE=your_base_url
   OPENAI_MODEL_NAME=gpt-4o
   ```

4. **运行演示**:
   ```bash
   uv run python -m src.main
   ```

## 功能特性
- **智能诊断**: 自动读取日志并分析设备状态。
- **模板管理**: 能够定位并加载 `.scanTemplate` 文件。
- **知识问答**: 遇到操作问题时，Agent 会自动查阅 `manual/` 中的文档进行回答。

