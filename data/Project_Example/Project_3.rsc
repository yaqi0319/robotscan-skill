{
    "calibWorkflowinfo": {
        "loopChecked": false,
        "loopMode": 1,
        "loopTime": "1",
        "procedureName": "1_default"
    },
    "deviceinfo": [
        {
            "deviceItem": [
                {
                    "btnEnabled": true,
                    "btnName": "trakProW",
                    "checked": true,
                    "cmd": "addDevice",
                    "defaultAdd": true,
                    "deviceName": "",
                    "devicePropertyQml": "qrc:Shining3dTrakWproperty.qml",
                    "deviceStatusImg": "qrc:/images/scansoft_R_TrakProL.svg",
                    "deviceUniqueID": "1",
                    "devicetype": "scansoft",
                    "hoverInfo": [
                        {
                            "onLine": 0,
                            "text": "Traker"
                        },
                        {
                            "onLine": 0,
                            "text": "Scanner"
                        }
                    ],
                    "imgText": "SHINING 3D_FreeScan Trak ProW",
                    "onLine": 2,
                    "picPath": "qrc:/images/scansoft_R_TrakProL.svg",
                    "properties": {
                        "deviceSerialNum": "xxxxxxxx",
                        "exeName": "D:/huangchi/release_freetrak_sdk_v2.2_509_cc689104/bin/FreeScan Trak.exe"
                    },
                    "topicWorkflow": ""
                }
            ],
            "devicetype": "scansoft",
            "pageName": "扫描仪"
        },
        {
            "deviceItem": [
                {
                    "btnEnabled": false,
                    "btnName": "dazuE05",
                    "checked": true,
                    "cmd": "addDevice",
                    "defaultAdd": true,
                    "deviceName": "HuayanRobot",
                    "devicePropertyQml": "qrc:DazuRobotDeviceE05.qml",
                    "deviceStatusImg": "qrc:/images/device_robot_status.svg",
                    "deviceUniqueID": "2",
                    "devicetype": "robot",
                    "imgText": "huayan",
                    "onLine": 2,
                    "picPath": "qrc:images/robot_R_dazuS20.svg",
                    "properties": {
                        "ip": "192.168.0.10",
                        "port": "10003"
                    },
                    "topicWorkflow": "RobotRequest"
                }
            ],
            "devicetype": "robot",
            "pageName": "机械臂"
        }
    ],
    "info": {
        "version": "2.0.2.0"
    },
    "workflowinfo": {
        "loopChecked": true,
        "loopMode": 1,
        "loopTime": "10000",
        "procedureName": "1_default"
    }
}
