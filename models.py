from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Date, Enum
from datetime import datetime, timedelta, timezone, date
from pydantic import BaseModel


# Database Section
URL_DATABASE = "postgresql+psycopg2://admin:Pass0rd1@172.16.0.9:5434/computer_inventory"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=True)
    date_created = Column(Date, nullable=True)
    last_updated = Column(Date, nullable=True)


class Laptops(Base):
    __tablename__ = "laptop"

    laptop_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    laptop_br = Column(String, nullable=True)
    laptop_ml = Column(String, nullable=True)
    laptop_ct = Column(String, nullable=True)
    laptop_sn = Column(String, nullable=True)
    laptop_in = Column(String, nullable=True)
    laptop_hdc = Column(String, nullable=True)
    laptop_mc = Column(String, nullable=True)
    laptop_ps = Column(String, nullable=True)
    laptop_pt = Column(String, nullable=True)
    laptop_cn = Column(String, nullable=True)
    laptop_mac = Column(String, nullable=True)
    laptop_os = Column(String, nullable=True)
    laptop_mov = Column(String, nullable=True)
    laptop_anti = Column(String, nullable=True)
    laptop_pdf = Column(String, nullable=True)
    laptop_wsd = Column(Date, nullable=True)
    laptop_wed = Column(Date, nullable=True)
    laptop_dd = Column(Date, nullable=True)
    laptop_dpd = Column(Date, nullable=True)
    laptop_rd = Column(Date, nullable=True)
    division_id = Column(Integer, nullable=True)
    status_id = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)

class Tablets(Base):
    __tablename__ = "tablet"

    tablet_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    division_id = Column(Integer, nullable=True)
    tablet_br = Column(String, nullable=True)
    tablet_ml = Column(String, nullable=True)
    tablet_sn = Column(String, nullable=True)
    tablet_imei = Column(String, nullable=True)
    tablet_os = Column(String, nullable=True)
    tablet_ver = Column(String, nullable=True)
    tablet_in = Column(String, nullable=True)
    tablet_hdc = Column(String, nullable=True)
    tablet_mc = Column(String, nullable=True)
    tablet_wsd = Column(Date, nullable=True)
    tablet_wed = Column(Date, nullable=True)
    tablet_dd = Column(Date, nullable=True)
    tablet_dpd = Column(Date, nullable=True)
    tablet_rd = Column(Date, nullable=True)
    status_id = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)


class Mouses(Base):
    __tablename__ = "mouse"

    mouse_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    division_id = Column(Integer, nullable=True)
    mouse_br = Column(String, nullable=True)
    mouse_ml = Column(String, nullable=True)
    mouse_sn = Column(String, nullable=True)
    mouse_in = Column(String, nullable=True)
    mouse_dd = Column(Date, nullable=True)
    mouse_dpd = Column(Date, nullable=True)
    status_id = Column(Integer, nullable=True)
    ctype_id = Column(Integer, nullable=True)    
    comments = Column(String, nullable=True)
    
    


# Pydantic Models #####################################################################################

class CreateUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    role_id: int
    active: bool
    date_created: date
    last_updated: date

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class laptopDevice(BaseModel):
    laptop_br: str | None = None
    laptop_ml: str | None = None
    laptop_ct: str | None = None
    laptop_sn: str | None = None
    laptop_in: str | None = None
    laptop_hdc: str | None = None
    laptop_mc: str | None = None
    laptop_ps: str | None = None
    laptop_pt: str | None = None
    laptop_cn: str | None = None
    laptop_mac: str | None = None
    laptop_os: str | None = None
    laptop_mov: str | None = None
    laptop_anti: str | None = None
    laptop_pdf: str | None = None
    laptop_wsd: date | None = None
    laptop_wed: date | None = None
    laptop_dd: date | None = None
    laptop_dpd: date | None = None
    laptop_rd: date | None = None
    division_id: int | None = None
    status_id: int | None = None
    comments: str | None = None


class tabletDevice(BaseModel):
    division_id: int | None = None
    tablet_br: str | None = None
    tablet_ml: str | None = None
    tablet_sn: str | None = None
    tablet_imei: str | None = None
    tablet_os: str | None = None
    tablet_ver: str | None = None
    tablet_in: str | None = None
    tablet_hdc: str | None = None
    tablet_mc: str | None = None
    tablet_wsd: date | None = None
    tablet_wed: date | None = None
    tablet_dd: date | None = None
    tablet_dpd: date | None = None
    tablet_rd: date | None = None
    status_id: int | None = None
    comments: str | None = None


class mouseDevice(BaseModel):
    division_id: int | None = None
    mouse_br: str | None = None
    mouse_ml: str | None = None
    mouse_sn: str | None = None
    mouse_in: str | None = None
    mouse_dd: date | None = None
    mouse_dpd: date | None = None
    status_id: int | None = None
    ctype_id: int | None = None   
    comments: str | None = None