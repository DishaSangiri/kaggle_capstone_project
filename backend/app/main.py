import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.activity import router as activity_router
from app.routes.planet import router as planet_router
from app.routes.agents import router as agents_router, register_broadcast_callback

class ConnectionManager:
    """Manages active WebSocket connections for live agent activity streaming."""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Gracefully skip broken connections
                pass

manager = ConnectionManager()

def broadcast_agent_log(log_payload: dict):
    """Callback triggered whenever an agent records an execution step."""
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.broadcast(log_payload))
    except RuntimeError:
        # No running event loop (e.g. CLI run context), skip websocket broadcast
        pass

# Connect agent executions to WebSocket broadcasts
register_broadcast_callback(broadcast_agent_log)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema
    init_db()
    yield

app = FastAPI(
    title="ECHO: RealityVerse",
    description="FastAPI service controlling the Multi-Agent RealityVerse system.",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for Vite frontend local/production requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register REST endpoints
app.include_router(activity_router, prefix="/api")
app.include_router(planet_router, prefix="/api")
app.include_router(agents_router, prefix="/api")

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket channel that streams real-time agent execution logs to the Agent Activity Panel."""
    await manager.connect(websocket)
    try:
        while True:
            # Maintain socket connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
