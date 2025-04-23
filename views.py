import structlog
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

LOGGER = structlog.get_logger()


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def mcp(request):
    LOGGER.info("mcp", request=request, data=request.data)
    method = request.data.get("method")
    params = request.data.get("params")
    LOGGER.info("mcp", method=method, params=params)
    # {'jsonrpc': '2.0', 'id': 0, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {'sampling': {}, 'roots': {'listChanged': True}}, 'clientInfo': {'name': 'mcp-inspector', 'version': '0.10.2'}}}}}

    res = {
        "jsonrpc": "2.0",
        "id": request.data.get("id"),
        "result": {},
    }
    if method == 'initialize':
        res = {
          "jsonrpc": "2.0",
          "id": request.data.get("id"),
          "result": {
            # "protocolVersion": "2025-03-26", # causes issues with the inspector?
            'protocolVersion': '2024-11-05',
            "capabilities": {
              "logging": {},
              # "prompts": {
              #   "listChanged": true
              # },
              # "resources": {
              #   "subscribe": true,
              #   "listChanged": true
              # },
              "tools": {
                "listChanged": False 
              }
            },
            "serverInfo": {
              "name": "Example",
              "version": "0.1.0"
            },
            "instructions": "Example Instructions"
          }
        }
    elif method == 'tools/list':
        res = {
          "jsonrpc": "2.0",
          "id": request.data.get("id"),
          "result": {
            "tools": [
              {
                "name": "echo",
                "description": "get the term back",
                "inputSchema": {
                  "type": "object",
                  "properties": {
                    "word": {
                      "type": "string",
                      "description": "what to echo"
                    }
                  },
                  "required": []
                }
              }
            ],
            # "nextCursor": "next-page-cursor"
          }
        }
    elif method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name == "echo":
            word = arguments.get("word")
            res = {
              "jsonrpc": "2.0",
              "id": request.data.get("id"),
              "result": {
                "content": [
                  {
                    "type": "text",
                    "text": f"echo {word}"
                  }
                ],
                "isError": False 
              }
            }
    elif method == 'ping':
        res = {
            "jsonrpc": "2.0",
            "id": request.data.get("id"),
            "result": {},
        }

    LOGGER.info("mcp", res=res)
    return Response(res, status=status.HTTP_200_OK)

# Errors
# {
#   jsonrpc: "2.0";
#   id: string | number;
#   result?: {
#     [key: string]: unknown;
#   }
#   error?: {
#     code: number;
#     message: string;
#     data?: unknown;
#   }
# }

