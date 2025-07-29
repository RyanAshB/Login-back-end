from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any, Optional, List, Annotated
from jose import jwt, JWTError
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from datetime import datetime, timedelta, timezone, date
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum
from models import *

app = FastAPI()

SECRET_KEY = 'my_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:5173",  # frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



# THIS IS THE SECTION THAT DEFINES FUNCTIONS #################################################################

async def get_current_user(db: db_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        id = payload.get("id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email, )
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.username)
    if user is  None:
        raise credentials_exception
    return user

user_dependency = Annotated[dict, Depends(get_current_user)]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db, email: str):
    return db.query(Users).filter(Users.email == email).first()


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def add_laptop(db: Session, laptop: laptopDevice):
    db_add_laptop = Laptops(**laptop.model_dump())
    db.add(db_add_laptop)
    db.commit()
    db.refresh(db_add_laptop)
    return(db_add_laptop)

def add_tablet(db: Session, tablet: tabletDevice):
    db_add_tablet = Tablets(**tablet.model_dump())
    db.add(db_add_tablet)
    db.commit()
    db.refresh(db_add_tablet)
    return(db_add_tablet)

def add_mouse(db: Session, mouse: mouseDevice):
    db_add_mouse = Mouses(**mouse.model_dump())
    db.add(db_add_mouse)
    db.commit()
    db.refresh(db_add_mouse)
    return(db_add_mouse)



# THIS IS THE SECTION THAT DEFINES API'S ####################################################################

@app.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_model: CreateUserRequest):
    db_user = get_user(db, user_model.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = Users(
            firstname = user_model.firstname,
            lastname = user_model.lastname,
            email = user_model.email,
            password = pwd_context.hash(user_model.password),
            role_id = user_model.role_id,
            active = user_model.active,
            date_created = user_model.date_created,
            last_updated = user_model.last_updated,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}


@app.post("/token")
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "firstname": user.firstname, "lastname": user.lastname, "role": user.role_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=CreateUserRequest)
async def read_users_me(current_user: user_dependency):
    return current_user

@app.post('/test/')
def get_items_view(db: Session=Depends(get_db)):
    return "hello world"

@app.post('/add-laptop/', response_model = laptopDevice)
def add_laptop_view(laptop: laptopDevice, db: Session=Depends(get_db)):
    return add_laptop(db, laptop)

@app.post('/add-tablet/', response_model = tabletDevice)
def add_tablet_view(tablet: tabletDevice, db: Session=Depends(get_db)):
    return add_tablet(db, tablet)

@app.post('/add-mouse/', response_model = mouseDevice)
def add_mouse_view(mouse: mouseDevice, db: Session=Depends(get_db)):
    return add_mouse(db, mouse)



# SECTION FOR ADDING ITEMS #################################################################################





# def authenticate_user(email:str, password:str, db):
#     user = db.query(Users).filter(Users.email == email).first()
#     if not user:
#         return False # no user found
#     if not pwd_context.verify(password, user.password):
#         return False # wrong password
#     return user



# def create_access_token(email: str, user_id: int, expires_delta: timedelta):
#     encode = {'sub': email, 'id': user_id} # encodes user details into token
#     expires = datetime.utcnow() + expires_delta
#     encode.update({'exp': expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): 
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         user_id = payload.get('id')
#         if email is None or user_id is None:
#             raise credentials_exception
#         return{'username': email, 'id': user_id}
#     except JWTError:
#         raise credentials_exception
    
# user_dependency = Annotated[dict, Depends(get_current_user)]


# @app.post("/create-user", status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency, user_model: CreateUserRequest):
#     user = Users(
#             firstname = user_model.firstname,
#             lastname = user_model.lastname,
#             email = user_model.email,
#             password = pwd_context.hash(user_model.password),
#             role_id = user_model.role_id,
#             active = user_model.active,
#             date_created = user_model.date_created,
#             last_updated = user_model.last_updated,
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"message": "User created successfully"}



# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
    
#     access_token = create_access_token(user.email, user.user_id, timedelta(minutes=20)) # encodes user details into token

#     return Token(access_token=access_token, token_type="bearer")



# @app.get("/me", status_code=status.HTTP_200_OK)
# async def user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return{"User": user}













# @app.get("/test-db")
# def test_db_connection():
#     try:
#         engine.connect()
#         return {"Successful"}
#     except SQLAlchemyError as e:
#         return {"message": "Connection failed", "error": str(e)}
    

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173","http://localhost:88","http://172.16.0.7:88"],  # or 8080
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # A SQLAlchemny ORM Item
# class Items(Base):
#     __tablename__ = "Items"

#     Item_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     Brand = Column(String(255), nullable=False)
#     Model = Column(String(255), nullable=False)
#     Serial_Number = Column(String(255), unique=True, nullable=False)
#     Inventory_Number = Column(Integer, unique=True, nullable=False)
#     Delivery_Date = Column(Date, nullable=True)
#     Deployment_Date = Column(Date, nullable=True)
#     System_Status = Column(String(255), nullable=True)

# # Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


# # A Pydantic Place
# class ItemCreate(BaseModel):
#     Brand: str
#     Model: str
#     Serial_Number: str
#     Inventory_Number: int
#     Delivery_Date: date
#     Deployment_Date: date
#     System_Status: str

# class ItemOut(ItemCreate):
#     Item_ID: int


# def get_item_by_sn(db: Session, item_sn: str):
#     return db.query(Items).where(Items.Serial_Number == item_sn).first()

# def get_items_by_brand(db: Session, item_brand: str):
#     return db.query(Items).where(Items.Brand == item_brand).all()

# def delete_item_by_serial_number(db: Session, serial_number: str):
#     item_to_delete = db.query(Items).filter(Items.Serial_Number == serial_number).first()
#     if item_to_delete:
#         db.delete(item_to_delete)
#         db.commit()
#         return("Item Deleted")

# def get_items(db: Session):
#     return db.query(Items).all()

# def create_item(db: Session, item: ItemOut):
#     db_add_item = Items(**item.model_dump())
#     db.add(db_add_item)
#     db.commit()
#     db.refresh(db_add_item)
#     return(db_add_item)

# # Routes
# @app.post('/create_item/', response_model = ItemOut)
# def create_item_view(item: ItemCreate, db: Session=Depends(get_db)):
#     return create_item(db, item)

# @app.get('/get_items/', response_model = List[ItemOut])
# def get_items_view(db: Session=Depends(get_db)):
#     db_items = get_items(db)
#     return db_items

# @app.get('/get_items_by_brand/{brand}', response_model = List[ItemOut])
# def get_items_by_brand_view(brand: str, db: Session=Depends(get_db)):
#     db_items = get_items_by_brand(db, brand)
#     return db_items

# @app.get('/get_item/{sn}')
# def get_item_view(sn: str, db: Session=Depends(get_db)):
#     db_item = get_item_by_sn(db, sn)
#     return db_item

# @app.delete('/delete_item_by_serial_number/{serial_number}')
# def delete_item_by_serial_number_view(serial_number: str, db: Session=Depends(get_db)):
#     db_items = delete_item_by_serial_number(db, serial_number)
#     return db_items