import json
from typing import List, Callable, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import AgentLog, UserHabit
from app.schemas import AgentLogResponse, AgentTriggerResponse, PlanetStateResponse
from agents.registry import agent_registry, ADKAgentRegistry
from agents.coordinator import RealityCoordinatorAgent

router = APIRouter(prefix="/agents", tags=["Agents"])

# Global hook to allow broadcasting logs to active websockets
broadcast_callback: Optional[Callable[[dict], None]] = None

def register_broadcast_callback(cb: Callable[[dict], None]):
    global broadcast_callback
    broadcast_callback = cb

def get_agent_registry() -> ADKAgentRegistry:
    """Dependency injection provider for the ADK agent registry."""
    return agent_registry

def get_coordinator(registry: ADKAgentRegistry = Depends(get_agent_registry)) -> RealityCoordinatorAgent:
    """Dependency injection provider to resolve the Reality Coordinator agent."""
    return registry.get_agent("Reality Coordinator")

@router.get("/logs", response_model=List[AgentLogResponse])
def get_agent_logs(limit: int = 100, db: Session = Depends(get_session)):
    """Retrieve agent execution and orchestration cycles history."""
    statement = select(AgentLog).order_by(AgentLog.timestamp.desc()).limit(limit)
    logs = db.exec(statement).all()
    
    response = []
    for log in logs:
        try:
            impact_dict = json.loads(log.impact_summary or "{}")
        except Exception:
            impact_dict = {}
            
        response.append(
            AgentLogResponse(
                id=log.id,
                agent_name=log.agent_name,
                cycle_id=log.cycle_id,
                action=log.action,
                status=log.status,
                rationale=log.rationale,
                impact_summary=impact_dict,
                timestamp=log.timestamp
            )
        )
    return response

@router.post("/trigger", response_model=AgentTriggerResponse)
def trigger_agent_cycle(
    db: Session = Depends(get_session),
    registry: ADKAgentRegistry = Depends(get_agent_registry),
    coordinator: RealityCoordinatorAgent = Depends(get_coordinator)
):
    """
    Manually triggers the 10-agent orchestration sequence.
    Pulls recent user habit actions, runs the coordination workflow, and commits the state.
    Uses dependency injected agent registry and coordinator dependencies.
    """
    try:
        # 1. Fetch habits logged
        habits_statement = select(UserHabit).order_by(UserHabit.timestamp.desc()).limit(50)
        habits = db.exec(habits_statement).all()
        
        # We hook into logging to intercept logs and stream them to websockets in real time
        old_log_execution = coordinator.log_execution
        captured_logs = []
        
        def intercepted_log_execution(db_sess: Session, cycle_id: str, action: str, status: str, rationale: str, impact: dict):
            # Call original logger
            log_entry = old_log_execution(db_sess, cycle_id, action, status, rationale, impact)
            
            # Form response payload
            log_payload = {
                "id": log_entry.id,
                "agent_name": log_entry.agent_name,
                "cycle_id": log_entry.cycle_id,
                "action": log_entry.action,
                "status": log_entry.status,
                "rationale": log_entry.rationale,
                "impact_summary": impact,
                "timestamp": log_entry.timestamp.isoformat()
            }
            captured_logs.append(
                AgentLogResponse(
                    id=log_entry.id,
                    agent_name=log_entry.agent_name,
                    cycle_id=log_entry.cycle_id,
                    action=log_entry.action,
                    status=log_entry.status,
                    rationale=log_entry.rationale,
                    impact_summary=impact,
                    timestamp=log_entry.timestamp
                )
            )
            
            # Broadcast to web socket if available
            if broadcast_callback:
                broadcast_callback(log_payload)
                
            return log_entry
        
        # Intercept logging on all registered agents dynamically resolved from registry
        for name, agent in registry.list_agents().items():
            agent.log_execution = intercepted_log_execution
        
        # Run coordinator cycle injecting the registry as a dependency
        planet_state = coordinator.run_cycle(db, habits, registry=registry)
        
        try:
            proj_dict = json.loads(planet_state.simulation_projection or "{}")
        except Exception:
            proj_dict = {}
            
        new_state_response = PlanetStateResponse(
            id=planet_state.id,
            forest_health=planet_state.forest_health,
            ocean_health=planet_state.ocean_health,
            finance_health=planet_state.finance_health,
            focus_health=planet_state.focus_health,
            overall_equilibrium=planet_state.overall_equilibrium,
            last_updated=planet_state.last_updated,
            agent_version=planet_state.agent_version,
            simulation_projection=proj_dict
        )
        
        return AgentTriggerResponse(
            success=True,
            cycle_id=captured_logs[0].cycle_id if captured_logs else "unknown",
            new_state=new_state_response,
            logs=captured_logs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent coordination run failed: {str(e)}")
