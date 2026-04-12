## Project Overview
Project Name:
HR Agentic AI-powered onboarding system
Project Type: Agentic AI solution

## Project Objective
Replace manual HR onboarding with an autonomous AI-driven workflow
Collects employee documents via email
- Performs AI document classification and validation
- Conducts gap analysis
- Sends automated followup emails
- Enables HR approval workflow (human in the loop)
- Maintains compliance and audit trail

## Business Problem
Current onboarding challenges:
Manual document tracking
Email dependency
Missing document follow-ups
HR workload overload
No real-time status visibility

## Solution
Deploy Agentic AI solution capable of managing onboarding end-to-end, while keeping a human in the loop mechanism.

## Directory Structure
etl_pipline
 dags
  excel_etl_dag.py
 excel_offer_tracker
  Offer_tracker.xlsx
 src
  _init__.py
 config
  config.py
  _init__.py
 extract
  excel_reader.py
  _init__.py
 _init__.py
 load
  db_loader.py
  _init__.py
 models
  automap.py
  _init__.py
  schema.py
 transform
  hash_generator.py
  _init__.py
  schema_mapper.py
  transformer.py
 utils
  db.py
  _init__.py
  logger.py
 tests

ai_onboarding_brain
 - config
  _init__.py
 src
  constants
   _init_.py
  controller
   _init_.py
  core
   _init_.py
  data
   _init__.py
  _init__.py
  models
   _init__.py
  repository
   _init__.py
  routes
   _init_.py
  schemas
   _init__.py
  services
   _init__.py
  utils
  _init_.py
 validations
   _init__.py
 static
email_attachments
 CIN123
  education
  employment
  personal_details
  unmatched

main.py

mcp_server
 config
  dev.properties
  _init__.py
 constants
  common_functions.py
  constants.py
  _init__.py
  _ pycache_
 _init__.py
 main_server.py
 ocr_classification
  engine
   helper_func.py
   _init__.py
  _init__.py
  tests
   test_ocr.py
  tools
   _init__.py
   ocr_classify.py
  utils
   ocr.py
 read_inbox
  engine
   helper_func.py
   _init__.py
   _pycache_
  _init__.py
  _pycache-
  tests
   _init_.py
   _pycache_
   test_read_inbox_integration.py
   test_read_inbox.py
  tools
   _init__.py
   read_inbox.py
 save_attachment
  engine
   helper_func.py
   _init__.py
   _pycache_
  _init__.py
  _pycache_
  tests
   _init__.py
   _pycache_
   test_db_connection.py
   test_fetch_attachments.py
   test_save_attachment_integration.py
   test_save_attachment.py
  tools
   _init.py
   save_attachment.py

 send_email
  api.py
  engine
   db_engine.py
   _init__.py
   mail_engine.py
   _pycache_
  _init__.py
  pycache_
  tests
   _init__.py
   _pycache_
   test_db_engine.py
   test_dummy_send_email.py
   test_send_email.py
  tools
   _init__.py
   _pycache_
   send_email.py

prompts
 followup.txt

pyproject.toml

pytest.ini

README.md

## Database Schema
CANDIDATE_INFO CANDIDATE ID NUMBER 22
CANDIDATE_INFO CIN VARCHAR2 50
CANDIDATE_INFO RECRUITER_NAME VARCHAR 100
CANDIDATE_INFO CV_SOURCED_DATE DATE 7
CANDIDATE_INFO JD_PUBLISHED_DATE DATE 7
CANDIDATE_INFO PREFIX VARCHAR2 20
CANDIDATE_INFO VERTICAL VARCHAR2 50
CANDIDATE_INFO BU VARCHAR2 150
CANDIDATE_INFO SOURCE_BASE VARCHAR2 58
CANDIDATE_INFO SOURCE VARCHAR2 100
CANDIDATE_INFO CONSULTANT_NAME VARCHAR2 100
CANDIDATE_INFO DESIGNATION_TO_BE_PRINTED_ON_THE_OFFER_LETTER VARCHAR2 100
CANDIDATE_INFO PREVIOUS_EXPERIENCE VARCHAR2 1
CANDIDATE_INFO GRADE VARCHAR2 20
CANDIDATE_INFO TECHNOLOGY VARCHAR2 100
CANDIDATE_INFO REF_NO VARCHAR2 50
CANDIDATE_INFO OFFER_RELEASE_DATE DATE 17
CANDIDATE_INFO EXPECTED_DOJ_WRT_TO_NP DATE 17
CANDIDATE_INFO MONTH_OF_JOINING VARCHAR2 20
CANDIDATE_INFO CURRENT_STATUS VARCHAR2 50
CANDIDATE_INFO PERSONAL_EMAIL_ID VARCHAR2 100
CANDIDATE_INFO CONTACT_NUMBER VARCHAR2 28
CANDIDATE_INFO CURRENT_RESIDENTIAL_ADDRESS VARCHAR2 200
CANDIDATE_INFO CURRENT_PLACE_OF_STAY VARCHAR2 100
CANDIDATE_INFO REPORTING_LOCATION VARCHAR2 100
CANDIDATE_INFO WORK_BASE_LOCATION VARCHAR2 100
CANDIDATE_INFO NP NUMBER 22
CANDIDATE_INFO EMPLOYMENT_TENURE VARCHAR2 30
CANDIDATE_INFO TOTAL_TAT NUMBER 22
CANDIDATE_INFO TAT_3D_PUBLISHED_TO_OFFER_RELEASE NUMBER 22
CANDIDATE_INFO TAT_OFFER_RELEASED_TO_DOJ_OF_THE_CANDIDATE NUMBER 22
CANDIDATE_INFO REASON_FOR_DROP_OUT VARCHAR2 200
CANDIDATE_INFO PO_NAME VARCHAR2 100
CANDIDATE_INFO MANAGER_NAME VARCHAR2 100
CANDIDATE_INFO BUDDY VARCHAR2 100
CANDIDATE_INFO CONVERSION_COMMENTS VARCHAR2 500
CANDIDATE_INFO RATE_CARD_K_PM NUMBER 22
CANDIDATE_INFO DP VARCHAR2 22
CANDIDATE_INFO ROM_HASH VARCHAR2 100
CANDIDATE_INFO CREATED_ON DATE 7
CANDIDATE_INFO UPDATED_ON DATE 7
CANDIDATE_INFO CANDIDATE_TYPE_ID NUMBER 22
CANDIDATE_INFO CANDIDATE_NAME VARCHAR2 100
CANDIDATE_INFO END_DATE DATE 7
CANDIDATE_INFO GRAD_PG VARCHAR2 50
CANDIDATE_INFO EMPTERM VARCHAR2 50
CANDIDATE_INFO EMPLOYEE_ID VARCHAR2 30
CANDIDATE_INFO PROJECT VARCHAR2 30

CANDIDATE_TYPE_MASTER CANDIDATE_TYPE_ID NUMBER 22
CANDIDATE_TYPE_MASTER CANDIDATE_TYPE VARCHAR2 100
CANDIDATE_TYPE_MASTER CANDIDATE_TYPE_DESCRIPTION VARCHAR2 255
CANDIDATE_TYPE_MASTER CREATED_ON DATE 17
CANDIDATE_TYPE_MASTER UPDATED_ON DATE 7
CANDIDATE_TYPE_MASTER IS_ACTIVE NUMBER 22

DOCUMENT_TRACKER DOCUMENT_TRACKER_ID NUMBER 22
DOCUMENT_TRACKER CANDIDATE_ID NUMBER 22
DOCUMENT_TRACKER DOCUMENT_TYPE_ID NUMBER 22
DOCUMENT_TRACKER DOCUMENT_STORE_ID NUMBER 22
DOCUMENT_TRACKER DOCUMENT_RECIVED_ON DATE 17
DOCUMENT_TRACKER COMMENTS VARCHAR2 500
DOCUMENT_TRACKER STATUS_ID NUMBER 22
DOCUMENT_TRACKER JOB_ID NUMBER 22
DOCUMENT_TRACKER CREATED_ON DATE 17
DOCUMENT_TRACKER UPDATED_ON DATE 7
DOCUMENT_TRACKER IS_ACTIVE NUMBER 22

DOCUMENT_TYPE_MASTER DOCUMENT_TYPE_ID NUMBER 22
DOCUMENT_TYPE_MASTER DOCUMENT_NAME VARCHAR2 100
DOCUMENT_TYPE_MASTER PRESHER NUMBER 22
DOCUMENT_TYPE_MASTER EXPERIENCE NUMBER 22
DOCUMENT_TYPE_MASTER DEV_PARTNER NUMBER 22
DOCUMENT_TYPE_MASTER CREATED_ON DATE 17
DOCUMENT_TYPE_MASTER UPDATED_ON DATE 17
DOCUMENT_TYPE_MASTER IS_ACTIVE NUMBER 22

JOB_TRACKER JOB_ID NUMBER 22
JOB_TRACKER JOB_TYPE_ID NUMBER 22
JOB_TRACKER START_TIME TIMESTAMP(6) 11
JOB_TRACKER END_TIME TIMESTAMP(6) 11
JOB_TRACKER HUMAN_ACTION_REQUIRED NUMBER 22
JOB_TRACKER ACTION_DATE DATE 17
JOB_TRACKER DRAFT_MAIL CLOB 4000
JOB_TRACKER REMARK VARCHAR2 500
JOB_TRACKER CANDIDATE_ID NUMBER 22
JOB_TRACKER STATUS_ID NUMBER 22
JOB_TRACKER HUMAN_ACTION VARCHAR2 255
JOB_TRACKER UPDATED_ON DATE 7

JOB_TYPE_MASTER JOB_TYPE_ID NUMBER 22
JOB_TYPE_MASTER JOB_TYPE VARCHAR2 100
JOB_TYPE_MASTER JOB_SUBTYPE VARCHAR2 100
JOB_TYPE_MASTER JOB_DESCRIPTION VARCHAR2 255
JOB_TYPE_MASTER CREATED_ON DATE 7
JOB_TYPE_MASTER UPDATED_ON DATE 17
JOB_TYPE_MASTER IS_ACTIVE NUMBER 22

MAIL_TYPE_MASTER MAIL_TYPE_ID NUMBER 22
MAIL_TYPE_MASTER MAIL_TYPE VARCHAR2 100
MAIL_TYPE_MASTER MAIL_DESCRIPTION VARCHAR2 255
MAIL_TYPE_MASTER CREATED_ON DATE 17
MAIL_TYPE_MASTER UPDATED_ON DATE 17
MAIL_TYPE_MASTER IS_ACTIVE NUMBER 22

## Database Constraints

CONSTRAINT TYPE | TABLE NAME |COLUMN NAME

Primary Key CANDIDATE_INFO CANDIDATE ID Check CANDIDATE TYPE MASTER | CANDIDATE TYPE
Primary Key CANDIDATE TYPE MASTER | CANDIDATE_TYPE_ID Check CANDIDATE TYPE MASTER |CANDIDATE_TYPE_ID Check CANDIDATE TYPE MASTER | IS ACTIVE
Foreign Key DOCUMENT TRACKER CANDIDATE ID Check DOCUMENT TRACKER DOCUMENT TRACKER DOCUMENT TRACKER_ID
Primary Key DOCUMENT TRACKER ID
Foreign Key DOCUMENT TRACKER DOCUMENT TYPE_ID
Check DOCUMENT TRACKER IS ACTIVE
Foreign Key DOCUMENT TRACKER 300_ID
Foreign Key DOCUMENT TRACKER STATUS ID
Check DOCUMENT TYPE MASTER | DOCUMENT NAME
Primary Key DOCUMENT TYPE MASTER | DOCUMENT TYPE ID
Check DOCUMENT TYPE MASTER DOCUMENT_TYPE_ID
Check DOCUMENT TYPE MASTER IS_ACTIVE
Foreign Key JOB TRACKER | CANDIDATE_ID
Check JOB_TRACKER HUMAN_ACTION_REQUIRED
Check JOB_TRACKER JOB ID
Primary Key JOB_TRACKER JOB ID
Foreign Key JOB_TRACKER JOB_TYPE_ID
Foreign Key JOB_TRACKER STATUS_ID
Check JOB_TYPE_MASTER IS ACTIVE
Check JOB_TYPE_MASTER JOB_TYPE
Primary Key JOB_TYPE_MASTER JOB_TYPE_ID
Check JOB_TYPE_MASTER JOB_TYPE_ID
Check MAIL TYPE MASTER IS ACTIVE
Foreign Key MAIL_TYPE_MASTER JOB_TYPE_ID
Check MAIL TYPE MASTER MAIL TYPE
Primary Key MAIL TYPE MASTER MAIL_TYPE_ID
Check MAIL TYPE MASTER MAIL_TYPE_ID
Check STATUS MASTER IS ACTIVE
Primary Key STATUS MASTER STATUS_ID
Check STATUS MASTER STATUS_ID
Check STATUS MASTER STATUS TYPE

### **Process 1: Candidate Data Ingestion and Job Creation**

**Entry Point**:

offer tracker.xlsx in shared folder.

### ETL Pipeline

The ETL pipeline is responsible for moving candidate data from the shared Excel tracker into the database (Candidate_Info table) and creating initial jobs for each candidate.

**Source:**

Excel file offer tracker.xlsx located in the shared folder.

The Excel contains 3 sheets.

Column names may overlap across sheets, but some differ.

New rows may be added or existing rows altered in any sheet.

**Target:**

Database table: Candidate_Info`.

Key fields include: 'CIN', 'REF_NO', 'Offer_release_date', 'Row_hash', 'Created_on', etc.

**Transformation Logic:**

1. **Row Detection:**
For each row in Excel, compute a 'row_hash using Python's 'hashlib.
If 'row_hash already exists in Candidate_Info, treat as an update.
If 'row_hash does not exist, treat as a new candidate entry.

2. **Column Handling:**
If new columns are found in Excel, pick them up and transform them into the schema expected by CANDIDATE_INFO.

3. **CIN Creation:**
Generate CIN by concatenating offer release date + Ref No.
These values are initially taken from Excel, then stored in CANDIDATE_INFO".

**Row Hash Creation:**
Use hashlib to generate a unique Row hash for each row.
Ensures duplicate detection and idempotency.

5. **Timestamps:**
Populate Created_on with the date/time when the entry is inserted into the DB.

6. **Job Creation:**
For each new candidate entry in CANDIDATE_INFO, append a corresponding record in Job tracker.
Assign a unique job_id.

Set initial job type documents required.
**Execution:**
This workflow is executed via an "Apache Airflow DAG**.
Schedule: "Daily at 10 PM IST**.

DAG tasks:
Extract data from Excel sheets.
Transform according to rules above.
Load into Candidate_Info table.
Create initial jobs in Job tracker.

**Outcome:**
Candidate data from Excel is consistently synchronized into the database.
New candidates are added, existing candidates are updated.
Initial jobs are created in Job tracker with type documents required', ensuring the workflow begins automatically for each candidate.

### **Process 2: Drafting and Sending Initial Email**
**Pre-Send Checks**:

If ActionDate today and Job type mail send and Human Action Required 1 and Human Action Accepted then proceed.

**Draft Preparation:**
Use the "Draft Prepare Tool to generate the draft email.

Tool logic:
Determine Emp_type (Fresher, Experience, Dev Partner) candidate experience.
Fetch document list from Document_Type_Master Table.
Fetch mail template from Mail_Type Master Table.
Generate draft email store in Draft Nail' field of Job tracker.

**UI Interaction:**
HR reviews the draft email generated by the tool.
HR can edit or approve for sending.

**Sending Initial Email:**
Once HR approves, the email is sent to the candidate.

**Post-Send Action**:
Append new entry in Job tracker
Job type Followup_mail.
NextActionDate +2 days.

**Outcome:**
Draft is generated via the Draft Prepare Tool, HR reviews and sends the initial "Documents Required" email, and a follow-up job is scheduled.

### **Process 3: Handling Candidate Replies and Attachments**

**Email Reading**:

Once a reply email from a candidate is received, the follow up entry for that candidate will be deactivated in Job Tracker table (the status field will be updated).

**Attachment Handling**:
New job entry in Job tracker (save attachment").
If attachments exist:
Save them into a directory named after the candidate's CIN.
Append record in Document tracker with metadata:
DOCUMENT TRACKER_ID', CANDIDATE ID, DOCUMENT TYPE ID', 'DOCUMENT_STORE ID",
DOCUMENT RECEIVED ON, COMMENTS, STATUS_ID, JOB_ID,
CREATED ON, UPDATED ON, IS ACTIVE.

**Agent Trigger**:

Agent is triggered immediately after read inbox.
Agent has:
List of documents received.
Path of stored documents.
MCP tools (tool registry).
Context and necessary output of tools for decision making.

**Outcome**: 
Agent triggered for calling other tools like save attachment, and for further analysis (including gap analysis via MCP tool).

### MCP Tools

**save attachment tool**

Saves candidate email attachments into CIN-specific folders.

Updates Document tracker with metadata.
Implements exception handling

Followup Classification Tool

-Uses LLM call to classify candidate reply into a follow-up category.

Extracts explicit dates (150 format) or relative tine expressions ("tomorrow", "in 3 days").

Rule-based logic then determines the next follow-up date.

### OCR Validation Tool

Uses numarkdown-8B-Thinking model.

-Validates whether received documents match expected types (e.g., aadhar.pdf is actually Aadhaar, PAN, marksheets, etc.).

***Segregation Tool

The Segregation Tool organizes candidate attachments into meaningful categories after OCR validation.

**Input:**

Attachments received from candidate emails.

Validation results from the OCR Validation Tool.

**Steps:

1. Create a directory for each candidate based on their CIN

2. For each attachment:

If the document "passes OCR validation"

Place it into the correct subdirectory (education', employment, or personal details"). Rename the file to include the candidate's CIN for traceability.

Example: Aadhar_Card_CIN123.pdf.

If the document fails OCR validation":

Place it into the unmatched directory.

Status in Document_tracker' remains "pending".

**Output:**

Candidate attachments are neatly organized into CIN-specific folders.

Validated documents are categorized and renamed for consistency.

Invalid or mismatched documents are isolated in the unmatched folder, ensuring HR and automation workflows can easily identify what still needs attention.

### Gap Analysis Tool

Think of the Gap Analysis Tool as the "final checker** that keeps track of which candidate documents are still missing and which ones have been successfully received.

Imagine the candidate is supposed to send their "HSC marksheet"" and ""Relieving letter. These are already marked as "pending in the Document tracker table.

Now the candidate replies with attachments: say "Aadhaar card and "PAN card**
The OCR Validation Tool** looks at each file to confirm if it's really what it claims to be.

If Aadhaar is valid its status in Document_tracker changes from "pending to "complete".

If the PAN card file is wrong (e.g., not actually a PAN card, or belongs to someone else) its status stays pending.

The Gap Analysis Tool's job is to update the database accurately**:

Mark validated documents as "complete".

Keep incorrect or missing documents as "pending".

**Outcome**: 
HR and the automation system always have a clear, up-to-date picture of which documents are still outstanding and which ones are done, so they know exactly what to follow up on next.

## Draft Prepare Tool

Generates follow-up email drafts via LLM.
Saves draft into Draft Mail field in Job tracker Table.
Used when candidate hasn't replied or has pending documents.
Agent Agent will have this:
List of documents received.
Path of stored documents.
MCP tools (tool registry).
Context and neccesary output of tools for decision making

### Rules

- Both the models are local and can run on a single GPU.
- airflow instance is on one server and code will be on another server.