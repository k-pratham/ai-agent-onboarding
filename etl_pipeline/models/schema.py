from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Float, CLOB, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class CandidateTypeMaster(Base):
    __tablename__ = 'CANDIDATE_TYPE_MASTER'

    CANDIDATE_TYPE_ID = Column(Integer, primary_key=True)
    CANDIDATE_TYPE = Column(String(100), nullable=False)
    CANDIDATE_TYPE_DESCRIPTION = Column(String(255))
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    IS_ACTIVE = Column(Integer, nullable=False)

class DocumentTypeMaster(Base):
    __tablename__ = 'DOCUMENT_TYPE_MASTER'

    DOCUMENT_TYPE_ID = Column(Integer, primary_key=True)
    DOCUMENT_NAME = Column(String(100), nullable=False)
    FRESHER = Column(Integer)
    EXPERIENCE = Column(Integer)
    DEV_PARTNER = Column(Integer)
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    IS_ACTIVE = Column(Integer, nullable=False)

class JobTypeMaster(Base):
    __tablename__ = 'JOB_TYPE_MASTER'

    JOB_TYPE_ID = Column(Integer, primary_key=True)
    JOB_TYPE = Column(String(100), nullable=False)
    JOB_SUBTYPE = Column(String(100))
    JOB_DESCRIPTION = Column(String(255))
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    IS_ACTIVE = Column(Integer, nullable=False)

class MailTypeMaster(Base):
    __tablename__ = 'MAIL_TYPE_MASTER'

    MAIL_TYPE_ID = Column(Integer, primary_key=True)
    MAIL_TYPE = Column(String(100), nullable=False)
    MAIL_DESCRIPTION = Column(String(255))
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    IS_ACTIVE = Column(Integer, nullable=False)

class StatusMaster(Base):
    __tablename__ = 'STATUS_MASTER'
    
    STATUS_ID = Column(Integer, primary_key=True)
    STATUS_TYPE = Column(String(100), nullable=False)
    IS_ACTIVE = Column(Integer, nullable=False)


class CandidateInfo(Base):
    __tablename__ = 'CANDIDATE_INFO'

    CANDIDATE_ID = Column(Integer, primary_key=True)
    CIN = Column(String(50))
    RECRUITER_NAME = Column(String(100))
    CV_SOURCED_DATE = Column(Date)
    JD_PUBLISHED_DATE = Column(Date)
    PREFIX = Column(String(20))
    VERTICAL = Column(String(50))
    BU = Column(String(150))
    SOURCE_BASE = Column(String(50))
    SOURCE = Column(String(100))
    CONSULTANT_NAME = Column(String(100))
    DESIGNATION_TO_BE_PRINTED_ON_THE_OFFER_LETTER = Column(String(100))
    PREVIOUS_EXPERIENCE = Column(String(10))
    GRADE = Column(String(20))
    TECHNOLOGY = Column(String(100))
    REF_NO = Column(String(50))
    OFFER_RELEASE_DATE = Column(Date)
    EXPECTED_DOJ_WRT_TO_NP = Column(Date)
    MONTH_OF_JOINING = Column(String(20))
    CURRENT_STATUS = Column(String(50))
    PERSONAL_EMAIL_ID = Column(String(100))
    CONTACT_NUMBER = Column(String(28))
    CURRENT_RESIDENTIAL_ADDRESS = Column(String(200))
    CURRENT_PLACE_OF_STAY = Column(String(100))
    REPORTING_LOCATION = Column(String(100))
    WORK_BASE_LOCATION = Column(String(100))
    NP = Column(Integer)
    EMPLOYMENT_TENURE = Column(String(30))
    TOTAL_TAT = Column(Integer)
    TAT_3D_PUBLISHED_TO_OFFER_RELEASE = Column(Integer)
    TAT_OFFER_RELEASED_TO_DOJ_OF_THE_CANDIDATE = Column(Integer)
    REASON_FOR_DROP_OUT = Column(String(200))
    PO_NAME = Column(String(100))
    MANAGER_NAME = Column(String(100))
    BUDDY = Column(String(100))
    CONVERSION_COMMENTS = Column(String(500))
    RATE_CARD_K_PM = Column(Integer)
    DP = Column(String(22))
    ROW_HASH = Column(String(100))
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    CANDIDATE_TYPE_ID = Column(Integer, ForeignKey('CANDIDATE_TYPE_MASTER.CANDIDATE_TYPE_ID'))
    CANDIDATE_NAME = Column(String(100))
    END_DATE = Column(Date)
    GRAD_PG = Column(String(50))
    EMPTERM = Column(String(50))
    EMPLOYEE_ID = Column(String(30))
    PROJECT = Column(String(30))

class DocumentTracker(Base):
    __tablename__ = 'DOCUMENT_TRACKER'

    DOCUMENT_TRACKER_ID = Column(Integer, primary_key=True)
    CANDIDATE_ID = Column(Integer, ForeignKey('CANDIDATE_INFO.CANDIDATE_ID'))
    DOCUMENT_TYPE_ID = Column(Integer, ForeignKey('DOCUMENT_TYPE_MASTER.DOCUMENT_TYPE_ID'))
    DOCUMENT_STORE_ID = Column(Integer)
    DOCUMENT_RECIVED_ON = Column(Date)
    COMMENTS = Column(String(500))
    STATUS_ID = Column(Integer, ForeignKey('STATUS_MASTER.STATUS_ID'))
    JOB_ID = Column(Integer, ForeignKey('JOB_TRACKER.JOB_ID'))
    CREATED_ON = Column(Date)
    UPDATED_ON = Column(Date)
    IS_ACTIVE = Column(Integer, nullable=False)

class JobTracker(Base):
    __tablename__ = 'JOB_TRACKER'

    JOB_ID = Column(Integer, primary_key=True)
    JOB_TYPE_ID = Column(Integer, ForeignKey('JOB_TYPE_MASTER.JOB_TYPE_ID'))
    START_TIME = Column(TIMESTAMP)
    END_TIME = Column(TIMESTAMP)
    HUMAN_ACTION_REQUIRED = Column(Integer)
    ACTION_DATE = Column(Date)
    DRAFT_MAIL = Column(CLOB)
    REMARK = Column(String(500))
    CANDIDATE_ID = Column(Integer, ForeignKey('CANDIDATE_INFO.CANDIDATE_ID'))
    STATUS_ID = Column(Integer, ForeignKey('STATUS_MASTER.STATUS_ID'))
    HUMAN_ACTION = Column(String(255))
    UPDATED_ON = Column(Date)
