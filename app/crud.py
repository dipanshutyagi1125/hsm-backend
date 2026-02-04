from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from fastapi import HTTPException, status
from datetime import date
from typing import Optional

# --- Employee CRUD ---

def get_employee(db: Session, employee_id: str):
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Check if employee_id exists
    if get_employee(db, employee.employee_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this ID already exists"
        )
    # Check if email exists
    if get_employee_by_email(db, employee.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    db_employee = models.Employee(
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: str):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    db.delete(db_employee)
    db.commit()
    return db_employee

# --- Attendance CRUD ---

def get_attendance_by_date(db: Session, employee_id: str, date_val: date):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id,
        models.Attendance.date == date_val
    ).first()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    # Check if employee exists
    if not get_employee(db, attendance.employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check if attendance exists for this date
    if get_attendance_by_date(db, attendance.employee_id, attendance.date):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance record already exists for this employee on this date"
        )
    
    db_attendance = models.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance_records(db: Session, employee_id: str):
    # Verify employee exists first (optional, but good for 404)
    if not get_employee(db, employee_id):
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return db.query(models.Attendance).filter(models.Attendance.employee_id == employee_id).all()

def get_all_attendance(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    status: Optional[models.AttendanceStatus] = None,
    date_filter: Optional[date] = None
):
    query = db.query(models.Attendance).join(models.Employee)
    
    if status:
        query = query.filter(models.Attendance.status == status)
    
    if date_filter:
        query = query.filter(models.Attendance.date == date_filter)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Employee.full_name.ilike(search_term),
                models.Employee.employee_id.ilike(search_term)
            )
        )
    
    # Order by date descending
    results = query.order_by(models.Attendance.date.desc()).offset(skip).limit(limit).all()
    
    # Map to schema structure since we need flattened response
    response = []
    for attendance in results:
        response.append({
            "id": attendance.id,
            "date": attendance.date,
            "status": attendance.status,
            "employee_id": attendance.employee.employee_id,
            "employee_name": attendance.employee.full_name,
            "employee_department": attendance.employee.department
        })
    return response
