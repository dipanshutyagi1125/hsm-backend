from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from ..models.attendance import AttendanceStatus

class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    employee_id: str

class AttendanceResponse(AttendanceBase):
    id: int
    employee_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AttendanceListResponse(BaseModel):
    id: int
    date: date
    status: AttendanceStatus
    employee_id: str
    employee_name: str
    employee_department: str

    class Config:
        from_attributes = True
