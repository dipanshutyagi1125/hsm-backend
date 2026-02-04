from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, description="Unique Employee ID")
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    created_at: datetime
    
    class Config:
        from_attributes = True
