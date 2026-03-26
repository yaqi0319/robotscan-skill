const net = require('net');

/**
 * RobotScan TCP Client for OpenClaw (JavaScript version)
 * Handles "msgBegin{JSON}msgEnd" protocol.
 */

const TARGET_IP = "127.0.0.1";
const TARGET_PORT = 18878;

const action_map = {
  "start": "CommModule_Start",
  "stop": "CommModule_Stop",
  "suspend": "CommModule_Suspend",
  "resume": "CommModule_Resume",
  "open": "CommModule_Open_Template",
};

async function callRobot(action, params = {}) {
  const cmd_name = action_map[action] || action;
  const payload = {
    topicWorkflow: "ExtraCommModuleRequest",
    redirectAutomationCmd: "1",
    cmd: cmd_name,
    ...params
  };

  const message = `msgBegin${JSON.stringify(payload)}msgEnd`;

  const result = {
    success: false,
    action: action,
    sent_payload: payload,
    response: null,
    error: null
  };

  return new Promise((resolve) => {
    const client = new net.Socket();
    client.setTimeout(2000); // Only timeout if connection or sending fails

    client.connect(TARGET_PORT, TARGET_IP, () => {
      // Send the command and resolve once it's written to the buffer.
      // Status information is written to log files by RC, not via TCP response.
      client.write(message, () => {
        result.success = true;
        client.destroy();
      });
    });

    client.on('error', (err) => {
      result.error = err.message;
      resolve(result);
    });

    client.on('timeout', () => {
      result.error = "Connection/Send Timeout";
      client.destroy();
    });

    client.on('close', () => {
      resolve(result);
    });
  });
}

// CLI handle
if (require.main === module) {
  const args = process.argv.slice(2);
  let action = "";
  let params = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--action") action = args[i + 1];
    if (args[i] === "--params") {
      try {
        params = JSON.parse(args[i + 1]);
      } catch (e) {
        process.stdout.write(JSON.stringify({ success: false, error: "Invalid JSON in --params" }));
        process.exit(1);
      }
    }
  }

  if (!action) {
    process.stdout.write(JSON.stringify({ success: false, error: "Missing --action" }));
    process.exit(1);
  }

  callRobot(action, params).then(res => {
    process.stdout.write(JSON.stringify(res, null, 2));
  });
}
