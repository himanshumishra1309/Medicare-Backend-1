from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, text,  Date, Time
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
import datetime
import database


class Doctor_Info(database.Base):
    __tablename__ = "Doctor"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    qualification = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    experience = Column(Integer, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class Student_Info(database.Base):
    __tablename__ = "Student"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    roll_no = Column(String, unique=True, index=True, nullable=False)
    year = Column(String, unique=True, index=True, nullable=False)
    hostel = Column(String, index=True)
    room_no = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class Medicine(database.Base):
    __tablename__ = "Medicine"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class Appointment(database.Base):
    __tablename__ = "Appointment"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("Doctor.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("Student.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)  # Corrected to use SQLAlchemy's Date type
    time = Column(Time, nullable=False)  # Corrected to use SQLAlchemy's Time type
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    doctor = relationship("Doctor_Info")
    student = relationship("Student_Info")
