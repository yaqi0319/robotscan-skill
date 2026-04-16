# RobotScan Agent (LangGraph)

这是一个基于 **LangGraph** 构建的 RobotScan 自动化扫描控制 Agent，旨在为 3D 扫描流程提供智能化的决策与执行能力。

## 架构说明
- **语言**: Python 3.9+
- **环境管理**: [uv](https://docs.astral.sh/uv/)
- **核心框架**: LangGraph (ReAct Agent)
- **通讯协议**: TCP (msgBegin{JSON}msgEnd)

## 目录结构
- `src/`: 核心源码
  - `agent.py`: LangGraph 定义
  - `tools.py`: Agent 可调用的工具（状态检查、模板加载、扫描控制）
  - `client.py`: 底层 TCP 通讯客户端
  - `main.py`: Demo 运行入口
- `config/`: 配置文件 (`path.json`)
- `manual/`: 知识库（Ageent 会自动通过查询工具摄入这里的知识）
- `data/`: 示例项目数据

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

