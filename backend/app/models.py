from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class UserHabit(SQLModel, table=True):
    """
    Stores logs of daily user activities and habits.
    Categories: focus, wellness, finance, health, etc.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    activity: str
    value: float
    raw_metadata: Optional[str] = Field(default="{}", description="JSON string of extra context")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PlanetState(SQLModel, table=True):
    """
    Evolving status of the 3D realityverse planet.
    Governed by agents analyzing user habits.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    forest_health: float = Field(default=0.5, description="Scale of 0.0 to 1.0")
    ocean_health: float = Field(default=0.5, description="Scale of 0.0 to 1.0")
    finance_health: float = Field(default=0.5, description="Scale of 0.0 to 1.0")
    focus_health: float = Field(default=0.5, description="Scale of 0.0 to 1.0")
    overall_equilibrium: float = Field(default=0.5, description="Scale of 0.0 to 1.0")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    agent_version: Optional[str] = Field(default="v1.0.0")
    simulation_projection: Optional[str] = Field(default="{}", description="JSON representation of simulation forecasts")

class AgentLog(SQLModel, table=True):
    """
    Real-time log of agent executions and actions taken during a run cycle.
    Provides data to the frontend's Agent Activity Panel.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_name: str
    cycle_id: str
    action: str
    status: str  # RUNNING, SUCCESS, WARNING, FAILED
    rationale: str
    impact_summary: Optional[str] = Field(default="{}", description="JSON of state fields affected")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
