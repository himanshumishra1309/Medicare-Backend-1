from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware 
import models
import database
from sqlalchemy.orm import Session
from pydantic import BaseModel


models.database.Base.metadata.create_all(bind=database.engine)

# Basic template
class Doctor(BaseModel):
    name: str
    email: str
    qualification: str
    experience: int
    hashed_password: str


class Student(BaseModel):
    name: str
    email: str
    roll_no: str
    year: str
    hostel: str
    room_no: int
    password: str


class Medicine(BaseModel):
    name: str
    price: float
    quantity: int


class Appointment(BaseModel):
    doctor_id: int
    student_id: int
    date: Optional[str] = None
    time: Optional[str] = None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["medicare-frontend-kaeh3122n-himanshu-mishras-projects-2e5f4b1d.vercel.app", "https://medicare-frontend-lyart.vercel.app/"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
) 

# Signup part for doctor
@app.post('/doctor')
def create_doctor(request: Doctor, db: Session = Depends(database.get_db)):
    new_doctor = models.Doctor_Info(**dict(request))
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@app.post('/student')
def create_student(request: Student, db: Session = Depends(database.get_db)):
    # Directly store the plain password (NOT recommended in a real-world scenario)
    student_data = request.dict()
    student_data["hashed_password"] = student_data.pop("password")  # Rename key
    new_student = models.Student_Info(**student_data)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# Fetching doctors on the basis of their IDs
@app.get('/doctor/{id}')
def get_doctor(id: int, db: Session = Depends(database.get_db)):
    doctor = db.query(models.Doctor_Info).filter(models.Doctor_Info.id == id).first()
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Doctor with id {id} not found"
            )
    return doctor


@app.get('/doctors/')
def get_doctors(db: Session = Depends(database.get_db)):
    doctors = db.query(models.Doctor_Info).all()
    return doctors


@app.get('/student/{id}')
def get_student(id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.Student_Info).filter(models.Student_Info.id == id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
            )
    return student


@app.get('/students/')
def get_students(db: Session = Depends(database.get_db)):
    students = db.query(models.Student_Info).all()
    return students


@app.delete('/doctor/{id}')
def delete_doctor(id: int, db: Session = Depends(database.get_db)):
    doctor = db.query(models.Doctor_Info).filter(models.Doctor_Info.id == id).first()
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Doctor with id {id} not found"
            )
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}


@app.delete('/student/{id}')
def delete_student(id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.Student_Info).filter(models.Student_Info.id == id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
            )
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


@app.put('/doctor/{id}')
def update_doctor(id: int, request: Doctor, db: Session = Depends(database.get_db)):
    doctor = db.query(models.Doctor_Info).filter(models.Doctor_Info.id == id).first()
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Doctor with id {id} not found"
        )
    
    # Convert the request to a dictionary while excluding unmodifiable fields
    update_data = request.dict(exclude_unset=True)
    
    # Perform the update
    db.query(models.Doctor_Info).filter(models.Doctor_Info.id == id).update(update_data)
    db.commit()
    
    return {"message": "Doctor updated successfully"}


@app.put('/student/{id}')
def update_student(id: int, request: Student, db: Session = Depends(database.get_db)):
    student = db.query(models.Student_Info).filter(models.Student_Info.id == id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
            )
    
    # Exclude fields that should not be updated
    update_data = request.dict(exclude_unset=True)
    
    # Only update the fields that are allowed
    allowed_fields = ['name', 'email', 'roll_no', 'year', 'hostel', 'room_no']
    update_data = {k: v for k, v in update_data.items() if k in allowed_fields}
    
    db.query(models.Student_Info).filter(models.Student_Info.id == id).update(update_data)
    db.commit()
    return {"message": "Student updated successfully"}



@app.post('/medicine')
def create_medicine(request: Medicine, db: Session = Depends(database.get_db)):
    new_medicine = models.Medicine(**dict(request))
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine


@app.get('/medicines/')
def get_medicines(db: Session = Depends(database.get_db)):
    medicines = db.query(models.Medicine).all()
    return medicines


@app.get('/medicine/{id}')
def get_medicine(id: int, db: Session = Depends(database.get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Medicine with id {id} not found"
            )
    return medicine


@app.delete('/medicine/{id}')
def delete_medicine(id: int, db: Session = Depends(database.get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Medicine with id {id} not found"
            )
    db.delete(medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}


@app.put('/medicine/{id}')
def update_medicine(id: int, request: Medicine, db: Session = Depends(database.get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id == id).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Medicine with id {id} not found"
            )
    db.query(models.Medicine).filter(models.Medicine.id == id).update(**dict(request))
    db.commit()
    return {"message": "Medicine updated successfully"}


@app.get('/medicine/{name}')
def get_medicine_by_name(name: str, db: Session = Depends(database.get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.name == name).first()
    if medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Medicine with name {name} not found"
            )
    return medicine

@app.get('/doctor_login/{email},{password}')
def doctor_login(email: str, password: str, db: Session = Depends(database.get_db)):
    doctor = db.query(models.Doctor_Info).filter(models.Doctor_Info.email == email).first()
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Doctor with email {email} not found"
            )
    if doctor.hashed_password != password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return doctor


@app.get('/student_login/{email},{password}')
def student_login(email: str, password: str, db: Session = Depends(database.get_db)):
    student = db.query(models.Student_Info).filter(models.Student_Info.email == email).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with email {email} not found"
            )
    if student.hashed_password != password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return student


@app.post('/appointment')
def create_appointment(request: Appointment, db: Session = Depends(database.get_db)):
    new_appointment = models.Appointment(**dict(request))
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@app.get('/appointments/')
def get_appointments(db: Session = Depends(database.get_db)):
    appointments = db.query(models.Appointment).all()
    return appointments

@app.get('/appointment/{doc_id}')
def get_appointment(doc_id: int, db: Session = Depends(database.get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.doctor_id == doc_id).all()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Appointment with id {id} not found"
            )
    return appointment

@app.get('/appointment/{stu_id}')
def get_appointment(stu_id: int, db: Session = Depends(database.get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.student_id == stu_id).all()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Appointment with id {id} not found"
            )
    return appointment

@app.delete('/appointment/{id}')
def delete_appointment(id: int, db: Session = Depends(database.get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Appointment with id {id} not found"
            )
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}

@app.put('/appointment/{id}')
def update_appointment(id: int, request: Appointment, db: Session = Depends(database.get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Appointment with id {id} not found"
            )
    db.query(models.Appointment).filter(models.Appointment.id == id).update(**dict(request))
    db.commit()
    return {"message": "Appointment updated successfully"}

