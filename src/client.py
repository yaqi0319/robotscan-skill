import socket
import json
import logging

class RobotScanClient:
    def __init__(self, ip="127.0.0.1", port=18878):
        self.ip = ip
        self.port = port
        self.timeout = 2.0
        
    def send_command(self, action, params=None):
        """
        Sends a command to the RobotScan RC software via TCP.
        The protocol is: msgBegin{JSON}msgEnd
        """
        if params is None:
            params = {}
            
        action_map = {
            "start": "CommModule_Start",
            "stop": "CommModule_Stop",
            "suspend": "CommModule_Suspend",
            "resume": "CommModule_Resume",
            "open": "CommModule_Open_Template",
        }
        
        cmd_name = action_map.get(action, action)
        payload = {
            "topicWorkflow": "ExtraCommModuleRequest",
            "redirectAutomationCmd": "1",
            "cmd": cmd_name,
            **params
        }
        
        message = f"msgBegin{json.dumps(payload)}msgEnd"
        
        result = {
            "success": False,
            "action": action,
            "sent_payload": payload,
            "response": None,
            "error": None
        }
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((self.ip, self.port))
                s.sendall(message.encode('utf-8'))
                # According to robotscan_client.js, the RC software writes to logs, 
                # not via TCP response, but we'll try to read just in case there's an ack.
                try:
                    data = s.recv(1024)
                    if data:
                        result["response"] = data.decode('utf-8')
                except socket.timeout:
                    pass # Timeout is expected if RC doesn't respond via TCP
                
                result["success"] = True
        except Exception as e:
            result["error"] = str(e)
            
        return result

if __name__ == "__main__":
    # Quick test
    client = RobotScanClient()
    # print(client.send_command("start"))
