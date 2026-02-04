from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=List[schemas.EmployeeResponse])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.delete("/{employee_id}", response_model=schemas.EmployeeResponse)
def delete_employee(employee_id: str, db: Session = Depends(database.get_db)):
    return crud.delete_employee(db=db, employee_id=employee_id)
