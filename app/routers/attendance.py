from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import crud, schemas, database
from ..models.attendance import AttendanceStatus

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance_record(attendance: schemas.AttendanceCreate, db: Session = Depends(database.get_db)):
    return crud.create_attendance(db=db, attendance=attendance)

@router.get("/", response_model=List[schemas.AttendanceListResponse])
def read_all_attendance(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    status: Optional[AttendanceStatus] = None,
    filter_date: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(database.get_db)
):
    if filter_date is None:
        filter_date = date.today()
    return crud.get_all_attendance(db=db, skip=skip, limit=limit, search=search, status=status, date_filter=filter_date)

@router.get("/{employee_id}", response_model=List[schemas.AttendanceResponse])
def read_attendance_records(employee_id: str, db: Session = Depends(database.get_db)):
    return crud.get_attendance_records(db=db, employee_id=employee_id)
