import sys
import json
from client import CheckpointSerializer

ckpt = CheckpointSerializer()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-workflow-checkpoint-state-serializer-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "commit_checkpoint",
                        "description": "Saves state snapshot at a given step",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "step_name": {"type": "string"},
                                "state": {"type": "object"}
                            },
                            "required": ["step_name", "state"]
                        }
                    },
                    {
                        "name": "restore_checkpoint",
                        "description": "Restores state dictionary by checkpoint ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "checkpoint_id": {"type": "integer"}
                            },
                            "required": ["checkpoint_id"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "commit_checkpoint":
            res = ckpt.commit_checkpoint(args.get("step_name", ""), args.get("state", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif name == "restore_checkpoint":
            res = ckpt.restore_checkpoint(args.get("checkpoint_id", 1))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
