import os
import sys
import argparse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

def run_api_server():
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    print(f"Starting FastAPI on http://{host}:{port} ...")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

def run_mcp_server():
    host = os.getenv("API_HOST", "127.0.0.1")
    mcp_port = int(os.getenv("MCP_PORT", "8001"))
    print(f"Starting FastMCP server on sse://{host}:{mcp_port} ...")
    
    # SSE transport lets other hosts/sub-agents communicate over HTTP
    from mcp.server import mcp
    mcp.run(transport="sse", host=host, port=mcp_port)

def main():
    parser = argparse.ArgumentParser(description="ECHO RealityVerse Runner CLI")
    parser.add_argument(
        "service",
        choices=["api", "mcp", "all"],
        default="api",
        nargs="?",
        help="Specify service: 'api' for FastAPI backend, 'mcp' for FastMCP server, 'all' for starting both."
    )
    args = parser.parse_args()

    if args.service == "api":
        run_api_server()
    elif args.service == "mcp":
        run_mcp_server()
    elif args.service == "all":
        import multiprocessing
        
        p1 = multiprocessing.Process(target=run_api_server)
        p2 = multiprocessing.Process(target=run_mcp_server)
        
        p1.start()
        p2.start()
        
        try:
            p1.join()
            p2.join()
        except KeyboardInterrupt:
            print("\nShutting down servers...")
            p1.terminate()
            p2.terminate()

if __name__ == "__main__":
    main()
