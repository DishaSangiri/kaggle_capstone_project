from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel

class HabitCreate(BaseModel):
    category: str
    activity: str
    value: float
    raw_metadata: Optional[Dict[str, Any]] = None

class HabitResponse(BaseModel):
    id: int
    category: str
    activity: str
    value: float
    raw_metadata: Dict[str, Any]
    timestamp: datetime

    class Config:
        from_attributes = True

class PlanetStateResponse(BaseModel):
    id: int
    forest_health: float
    ocean_health: float
    finance_health: float
    focus_health: float
    overall_equilibrium: float
    last_updated: datetime
    agent_version: str
    simulation_projection: Dict[str, Any]

    class Config:
        from_attributes = True

class AgentLogResponse(BaseModel):
    id: int
    agent_name: str
    cycle_id: str
    action: str
    status: str
    rationale: str
    impact_summary: Dict[str, Any]
    timestamp: datetime

    class Config:
        from_attributes = True

class AgentTriggerResponse(BaseModel):
    success: bool
    cycle_id: str
    new_state: PlanetStateResponse
    logs: list[AgentLogResponse]
