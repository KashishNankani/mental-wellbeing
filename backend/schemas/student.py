from typing import Annotated, Optional, Literal
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

EnrollmentNo = Annotated[str, Field(min_length=4, max_length=50, strip_whitespace=True)]
RollNumber = Annotated[Optional[str], Field(default=None, max_length=50, strip_whitespace=True)]
PhoneNum = Annotated[str, Field(min_length=10, max_length=15, pattern=r"^\+?[0-9]+$")]
# restricted to Male/Female to align with gender-specific scoring baselines in GWBS-KADA
GenderStr = Literal['Male', 'Female']

class StudentBase(BaseModel):
    enrollment_no: EnrollmentNo
    roll_number: RollNumber
    name: Annotated[str, Field(min_length=2, max_length=100, strip_whitespace=True)]
    email: EmailStr
    phone: PhoneNum
    gender: GenderStr 
    course: Annotated[str, Field(min_length=2, max_length=100, strip_whitespace=True)]
    semester: Annotated[int, Field(ge=1, le=10)]
    session: Annotated[str, Field(pattern=r"^\d{4}-\d{4}$")]

class StudentUpdate(BaseModel):
    # PATCH schema allowing students to update only editable profile fields
    roll_number: Annotated[Optional[str], Field(default=None, min_length=4, max_length=50, strip_whitespace=True)]
    phone: Optional[PhoneNum] = None
    semester: Annotated[Optional[int], Field(default=None, ge=1, le=10)]

class StudentOut(StudentBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# added for dashboard route
class DashboardSummary(BaseModel):
    total_rsvps: int
    total_quizzes: int

class DashboardOut(BaseModel):
    student: StudentOut
    summary: DashboardSummary