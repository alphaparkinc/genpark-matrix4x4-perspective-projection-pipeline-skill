import sys
import json
import math
from client import TransformPipeline4x4

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-matrix4x4-perspective-projection-pipeline-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "project_point",
                    "description": "Project 3D point into Normalized Device Coordinates (NDC) using perspective matrix",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "point": {"type": "array", "items": {"type": "number"}},
                            "fov_degrees": {"type": "number", "default": 60.0},
                            "aspect_ratio": {"type": "number", "default": 1.0},
                            "near": {"type": "number", "default": 1.0},
                            "far": {"type": "number", "default": 100.0}
                        },
                        "required": ["point"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "project_point":
            pt = args.get("point")
            fov = math.radians(args.get("fov_degrees", 60.0))
            asp = args.get("aspect_ratio", 1.0)
            near = args.get("near", 1.0)
            far = args.get("far", 100.0)
            mat = TransformPipeline4x4.perspective(fov, asp, near, far)
            ndc = TransformPipeline4x4.project_point(mat, pt)
            res = {"content": [{"type": "text", "text": json.dumps({"ndc_point": ndc})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
