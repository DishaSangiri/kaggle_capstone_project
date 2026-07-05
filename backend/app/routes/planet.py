import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import PlanetState
from app.schemas import PlanetStateResponse

router = APIRouter(prefix="/planet", tags=["Planet"])

@router.get("/state", response_model=PlanetStateResponse)
def get_current_planet_state(db: Session = Depends(get_session)):
    """Retrieve the most recent 3D planet configuration status."""
    statement = select(PlanetState).order_by(PlanetState.last_updated.desc()).limit(1)
    state = db.exec(statement).first()
    
    if not state:
        # Generate default state if database is empty
        state = PlanetState(
            forest_health=0.5,
            ocean_health=0.5,
            finance_health=0.5,
            focus_health=0.5,
            overall_equilibrium=0.5,
            agent_version="v2.0.0-INIT",
            simulation_projection="{}"
        )
        db.add(state)
        db.commit()
        db.refresh(state)

    try:
        proj_dict = json.loads(state.simulation_projection or "{}")
    except Exception:
        proj_dict = {}

    return PlanetStateResponse(
        id=state.id,
        forest_health=state.forest_health,
        ocean_health=state.ocean_health,
        finance_health=state.finance_health,
        focus_health=state.focus_health,
        overall_equilibrium=state.overall_equilibrium,
        last_updated=state.last_updated,
        agent_version=state.agent_version,
        simulation_projection=proj_dict
    )
