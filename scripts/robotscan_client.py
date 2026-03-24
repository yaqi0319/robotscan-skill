import sys
import socket
import json
import argparse

# RobotScan 协议默认对端（可能是服务也可能是 RC 本身）在本地 18878 端口
TARGET_IP = "127.0.0.1"
TARGET_PORT = 18878

def call_robot(cmd_name, params=None):
    """
    通过 TCP Socket 发送协议指令并返回 JSON 结果。
    """
    if params is None:
        params = {}

    payload = {
        "topicWorkflow": "ExtraCommModuleRequest",
        "redirectAutomationCmd": "1",
        "cmd": cmd_name
    }
    payload.update(params)

    message = f"msgBegin{json.dumps(payload)}msgEnd"
    
    result = {
        "success": False,
        "action": cmd_name,
        "sent_payload": payload,
        "response": None,
        "error": None
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((TARGET_IP, TARGET_PORT))
            s.sendall(message.encode('utf-8'))
            
            try:
                data = s.recv(4096).decode('utf-8', errors='ignore')
                if data:
                    # 简单剥离 msgBegin/msgEnd (如果存在)
                    clean_data = data.replace("msgBegin", "").replace("msgEnd", "")
                    try:
                        result["response"] = json.loads(clean_data)
                    except json.JSONDecodeError:
                        result["response"] = clean_data
                result["success"] = True
            except socket.timeout:
                result["error"] = "Timeout: No response from robot"
                # 有些指令可能没有即时回复
                result["success"] = True 
                
    except Exception as e:
        result["error"] = str(e)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

def main():
    parser = argparse.ArgumentParser(description="RobotScan TCP 客户端控制脚本")
    parser.add_argument("--action", type=str, required=True, 
                        choices=["start", "stop", "suspend", "resume", "open", "scan", "status"],
                        help="执行的动作 (start, stop, suspend, resume, open, scan, status)")
    parser.add_argument("--params", type=str, default="{}", 
                        help="JSON 格式的参数字符串")

    args = parser.parse_args()

    # 指令名映射 (根据协议文档)
    action_map = {
        "start": "CommModule_Start",
        "stop": "CommModule_Stop",
        "suspend": "CommModule_Suspend",
        "resume": "CommModule_Resume",
        "open": "CommModule_Open_Template",
        "scan": "CommModule_Start_Scan",  # 补充可能的扫描指令
        "status": "CommModule_Get_Status"  # 补充可能的状态查询指令
    }

    target_cmd = action_map.get(args.action, args.action)
    
    try:
        params_dict = json.loads(args.params)
    except json.JSONDecodeError:
        print(json.dumps({"success": False, "error": "Invalid JSON in --params"}, indent=2))
        sys.exit(1)

    call_robot(target_cmd, params_dict)

if __name__ == "__main__":
    main()