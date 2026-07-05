import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import UserHabit
from app.schemas import HabitCreate, HabitResponse

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("", response_model=HabitResponse)
def create_habit(habit_in: HabitCreate, db: Session = Depends(get_session)):
    """Logs a new habit or activity (e.g. coding, hydration, budget expenses)."""
    try:
        raw_meta = json.dumps(habit_in.raw_metadata or {})
        db_habit = UserHabit(
            category=habit_in.category,
            activity=habit_in.activity,
            value=habit_in.value,
            raw_metadata=raw_meta
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        
        # Prepare response model with dict raw_metadata
        response_data = HabitResponse(
            id=db_habit.id,
            category=db_habit.category,
            activity=db_habit.activity,
            value=db_habit.value,
            raw_metadata=json.loads(db_habit.raw_metadata),
            timestamp=db_habit.timestamp
        )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save habit: {str(e)}")

@router.get("", response_model=List[HabitResponse])
def list_habits(limit: int = 50, db: Session = Depends(get_session)):
    """Retrieve historical list of logged habits."""
    statement = select(UserHabit).order_by(UserHabit.timestamp.desc()).limit(limit)
    habits = db.exec(statement).all()
    
    response_list = []
    for h in habits:
        response_list.append(
            HabitResponse(
                id=h.id,
                category=h.category,
                activity=h.activity,
                value=h.value,
                raw_metadata=json.loads(h.raw_metadata or "{}"),
                timestamp=h.timestamp
            )
        )
    return response_list
