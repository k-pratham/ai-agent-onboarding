# HR Onboarding — Backend API Reference

**Base URL:** `http://localhost:8080/api/v1`  
**Auth:** None (no token required)  
**Content-Type:** `application/json`  
**CORS:** Enabled for all origins

---

## Table of Contents

1. [Dashboard APIs](#1-dashboard-apis)
2. [Candidate APIs](#2-candidate-apis)
3. [Document APIs](#3-document-apis)
4. [Mail APIs](#4-mail-apis)
5. [Existing Action APIs](#5-existing-action-apis)
6. [Status & Type Reference Tables](#6-status--type-reference-tables)

---

## 1. Dashboard APIs

### 1.1 GET `/dashboard/summary`

Returns counts for all 4 dashboard tabs.

**Request:** No body or query params.

**Response:**
```json
{
  "upcoming_count": 12,
  "in_progress_count": 8,
  "completed_count": 45,
  "dropout_count": 3
}
```

| Field | Type | Description |
|-------|------|-------------|
| `upcoming_count` | `int` | Candidates with future DOJ, onboarding not started |
| `in_progress_count` | `int` | Candidates currently going through onboarding steps |
| `completed_count` | `int` | Candidates who completed all 6 steps |
| `dropout_count` | `int` | Candidates marked as dropout |

---

### 1.2 GET `/dashboard/candidates`

Returns paginated candidate list for a specific tab (Candidate Hub table).

**Query Parameters:**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `tab` | `string` | Yes | — | `"upcoming"` \| `"in_progress"` \| `"completed"` \| `"dropout"` |
| `page` | `int` | No | `1` | Page number (1-indexed) |
| `page_size` | `int` | No | `20` | Items per page (max 100) |
| `search` | `string` | No | `null` | Search by candidate name or CIN |

**Example:** `GET /dashboard/candidates?tab=in_progress&page=1&page_size=20&search=john`

**Response:**
```json
{
  "total": 8,
  "page": 1,
  "page_size": 20,
  "total_pages": 1,
  "items": [
    {
      "candidate_id": 101,
      "cin": "20250415_REF001",
      "name": "John Doe",
      "address": "Mumbai, Maharashtra",
      "employee_type": "Experience",
      "date": "2025-06-01",
      "current_step": 3,
      "current_step_label": "Follow-up Mail Drop",
      "candidate_type_id": 2,
      "email": "john.doe@gmail.com",
      "designation": "Senior Software Engineer"
    },
    {
      "candidate_id": 102,
      "cin": "20250416_REF002",
      "name": "Priya Sharma",
      "address": "Pune, Maharashtra",
      "employee_type": "Fresher",
      "date": "2025-06-15",
      "current_step": 2,
      "current_step_label": "Document Required Mail",
      "candidate_type_id": 1,
      "email": "priya.sharma@gmail.com",
      "designation": "Software Engineer"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total` | `int` | Total matching candidates in this tab |
| `page` | `int` | Current page number |
| `page_size` | `int` | Items per page |
| `total_pages` | `int` | Total number of pages |
| `items` | `array` | List of `CandidateHubRow` objects |

**CandidateHubRow fields:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `candidate_id` | `int` | No | Primary key — use this for all candidate API calls |
| `cin` | `string` | No | Candidate Identification Number |
| `name` | `string` | No | Candidate full name |
| `address` | `string` | Yes | Current residential address |
| `employee_type` | `string` | No | `"Fresher"` \| `"Experience"` \| `"Dev Partner"` |
| `date` | `string` | Yes | Expected date of joining (ISO format YYYY-MM-DD) |
| `current_step` | `int` | No | Current stepper position (1–6) |
| `current_step_label` | `string` | No | Human-readable step name |
| `candidate_type_id` | `int` | No | 1=Fresher, 2=Experience, 3=Dev Partner |
| `email` | `string` | Yes | Personal email |
| `designation` | `string` | Yes | Job designation |

---

## 2. Candidate APIs

### 2.1 GET `/candidates/{candidate_id}`

Returns full candidate details for the detail page / step 1 (Offer Released).

**Path Params:** `candidate_id` (int)

**Response:**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "name": "John Doe",
  "email": "john.doe@gmail.com",
  "contact_number": "+91-9876543210",
  "address": "Mumbai, Maharashtra",
  "employee_type": "Experience",
  "candidate_type_id": 2,
  "designation": "Senior Software Engineer",
  "technology": "Java/Spring Boot",
  "grade": "E3",
  "bu": "Digital Engineering",
  "vertical": "Technology",
  "reporting_location": "Mumbai",
  "work_base_location": "Mumbai",
  "offer_release_date": "2025-04-15",
  "expected_doj": "2025-06-01",
  "previous_experience": "5",
  "recruiter_name": "Priya Sharma",
  "po_name": "Amit Patel",
  "manager_name": "Rajesh Kumar",
  "buddy": "Sneha Gupta",
  "current_status": "In Progress",
  "reason_for_dropout": null
}
```

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `candidate_id` | `int` | No | Primary key |
| `cin` | `string` | No | Candidate Identification Number |
| `name` | `string` | No | Full name |
| `email` | `string` | Yes | Personal email ID |
| `contact_number` | `string` | Yes | Phone number |
| `address` | `string` | Yes | Residential address |
| `employee_type` | `string` | No | `"Fresher"` / `"Experience"` / `"Dev Partner"` |
| `candidate_type_id` | `int` | No | 1 / 2 / 3 |
| `designation` | `string` | Yes | Job title |
| `technology` | `string` | Yes | Tech stack |
| `grade` | `string` | Yes | Grade level |
| `bu` | `string` | Yes | Business unit |
| `vertical` | `string` | Yes | Vertical |
| `reporting_location` | `string` | Yes | Reporting office |
| `work_base_location` | `string` | Yes | Work base office |
| `offer_release_date` | `string` | Yes | ISO date |
| `expected_doj` | `string` | Yes | ISO date |
| `previous_experience` | `string` | Yes | Years of experience |
| `recruiter_name` | `string` | Yes | Recruiter |
| `po_name` | `string` | Yes | PO name |
| `manager_name` | `string` | Yes | Reporting manager |
| `buddy` | `string` | Yes | Assigned buddy |
| `current_status` | `string` | Yes | Current HR status |
| `reason_for_dropout` | `string` | Yes | Dropout reason if applicable |

**Errors:** `404` if candidate not found.

---

### 2.2 GET `/candidates/{candidate_id}/stepper`

Returns the 6-step stepper state for the horizontal progress stepper in the UI.

**Path Params:** `candidate_id` (int)

**Response:**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "current_step": 3,
  "steps": [
    {
      "step_number": 1,
      "label": "Offer Released",
      "status": "completed",
      "completed_at": "2025-04-15",
      "job_id": null,
      "has_draft": false
    },
    {
      "step_number": 2,
      "label": "Document Required Mail",
      "status": "completed",
      "completed_at": "2025-04-17",
      "job_id": 201,
      "has_draft": false
    },
    {
      "step_number": 3,
      "label": "Follow-up Mail Drop",
      "status": "in_progress",
      "completed_at": null,
      "job_id": 205,
      "has_draft": true
    },
    {
      "step_number": 4,
      "label": "Document List",
      "status": "pending",
      "completed_at": null,
      "job_id": null,
      "has_draft": false
    },
    {
      "step_number": 5,
      "label": "On-Boarding Mail",
      "status": "pending",
      "completed_at": null,
      "job_id": null,
      "has_draft": false
    },
    {
      "step_number": 6,
      "label": "IT-Admin Mail",
      "status": "pending",
      "completed_at": null,
      "job_id": null,
      "has_draft": false
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `candidate_id` | `int` | Candidate PK |
| `cin` | `string` | CIN |
| `current_step` | `int` | The first incomplete step (1–6). Use this to highlight the active step. |
| `steps` | `array` | Always 6 elements, one per step |

**StepDetail fields:**

| Field | Type | Description |
|-------|------|-------------|
| `step_number` | `int` | 1 through 6 |
| `label` | `string` | `"Offer Released"` / `"Document Required Mail"` / `"Follow-up Mail Drop"` / `"Document List"` / `"On-Boarding Mail"` / `"IT-Admin Mail"` |
| `status` | `string` | `"completed"` / `"in_progress"` / `"pending"` |
| `completed_at` | `string\|null` | ISO date when this step was completed |
| `job_id` | `int\|null` | Associated JOB_TRACKER ID (for steps 2,3,5,6). Pass this to mail/send API. |
| `has_draft` | `bool` | Whether a draft email exists for this step |

**UI Mapping:**
- Step 1 → Show candidate info (from GET `/candidates/{id}`)
- Step 2 → Show compose mail form (call GET `/candidates/{id}/mail/draft?step=2`)
- Step 3 → Show compose mail form (call GET `/candidates/{id}/mail/draft?step=3`)
- Step 4 → Show document table (call GET `/candidates/{id}/documents`)
- Step 5 → Show compose mail form (call GET `/candidates/{id}/mail/draft?step=5`)
- Step 6 → Show compose mail form (call GET `/candidates/{id}/mail/draft?step=6`)

---

### 2.3 POST `/candidates/{candidate_id}/dropout`

Mark a candidate as dropout. Moves them to the Dropout tab.

**Path Params:** `candidate_id` (int)

**Request Body:**
```json
{
  "reason": "Candidate accepted another offer"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | `string` | No | Reason for dropout. Defaults to "Marked as dropout by HR" |

**Response:**
```json
{
  "success": true,
  "message": "Candidate marked as dropout successfully"
}
```

**Errors:** `404` if candidate not found.

---

## 3. Document APIs

### 3.1 GET `/candidates/{candidate_id}/documents`

Returns all tracked documents for a candidate — used to render the Document List table in Step 4.

**Path Params:** `candidate_id` (int)

**Response:**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "candidate_name": "John Doe",
  "candidate_type": "Experience",
  "documents": [
    {
      "document_tracker_id": 501,
      "document_type_id": 1,
      "document_name": "Aadhaar Card",
      "status": "Verified",
      "status_id": 5,
      "submitted": true,
      "received_on": "2025-04-20",
      "comments": null,
      "is_active": true
    },
    {
      "document_tracker_id": 502,
      "document_type_id": 3,
      "document_name": "10th Marksheet",
      "status": "Pending",
      "status_id": 1,
      "submitted": false,
      "received_on": null,
      "comments": null,
      "is_active": true
    },
    {
      "document_tracker_id": 503,
      "document_type_id": 6,
      "document_name": "Experience Letter",
      "status": "Rejected",
      "status_id": 6,
      "submitted": true,
      "received_on": "2025-04-21",
      "comments": "Document is blurry, please resubmit",
      "is_active": true
    },
    {
      "document_tracker_id": 504,
      "document_type_id": 7,
      "document_name": "Relieving Letter",
      "status": "Mail Received",
      "status_id": 4,
      "submitted": true,
      "received_on": "2025-04-21",
      "comments": null,
      "is_active": true
    }
  ]
}
```

**DocumentRow fields:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `document_tracker_id` | `int` | No | Primary key — use this for approve/reject calls |
| `document_type_id` | `int` | No | Document type ID from master table |
| `document_name` | `string` | No | Human-readable document name |
| `status` | `string` | No | `"Pending"` / `"Mail Drafted"` / `"Mail Sent"` / `"Mail Received"` / `"Verified"` / `"Rejected"` / `"Completed"` |
| `status_id` | `int` | No | Numeric status (1–7) |
| `submitted` | `bool` | No | `true` if document was received from candidate |
| `received_on` | `string` | Yes | ISO date when document was received |
| `comments` | `string` | Yes | HR comments or rejection reason |
| `is_active` | `bool` | No | Always `true` for active documents |

**UI Mapping:**
- `submitted: true` → Show green "Submitted" badge
- `submitted: false` → Show red "Not Submitted" badge
- `status_id == 5` (Verified) → Disable Approve/Reject buttons, show green check
- `status_id == 6` (Rejected) → Show rejection reason from `comments`
- Show Approve button and Reject button for documents with `status_id` in (1, 4) i.e. Pending or Mail Received

---

### 3.2 POST `/documents/{document_tracker_id}/approve`

HR approves a single document.

**Path Params:** `document_tracker_id` (int)

**Request Body:**
```json
{
  "comments": "Document verified successfully"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `comments` | `string` | No | Optional approval comments |

**Response:**
```json
{
  "success": true,
  "message": "Document approved successfully",
  "document_tracker_id": 501,
  "new_status": "Verified"
}
```

**Side Effect:** If ALL documents for this candidate become verified after this approval, the backend automatically creates an onboarding mail job (step 5). The stepper will advance accordingly.

**Errors:** `404` if document_tracker_id not found.

---

### 3.3 POST `/documents/{document_tracker_id}/reject`

HR rejects a single document with a mandatory reason.

**Path Params:** `document_tracker_id` (int)

**Request Body:**
```json
{
  "rejection_reason": "Document is blurry, please resubmit a clear copy"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rejection_reason` | `string` | **Yes** | Reason for rejection (shown to candidate) |

**Response:**
```json
{
  "success": true,
  "message": "Document rejected",
  "document_tracker_id": 503,
  "new_status": "Rejected"
}
```

**Errors:** `404` if document_tracker_id not found.

---

### 3.4 POST `/candidates/{candidate_id}/documents/bulk-action`

Bulk approve or reject multiple documents at once.

**Path Params:** `candidate_id` (int)

**Request Body (Bulk Approve):**
```json
{
  "action": "approve",
  "document_tracker_ids": [501, 502, 504],
  "rejection_reason": null
}
```

**Request Body (Bulk Reject):**
```json
{
  "action": "reject",
  "document_tracker_ids": [503, 505],
  "rejection_reason": "Documents are not readable, please resubmit clear copies"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | `string` | **Yes** | `"approve"` or `"reject"` |
| `document_tracker_ids` | `int[]` | **Yes** | Array of document tracker IDs to act on |
| `rejection_reason` | `string` | Only if `action="reject"` | Shared rejection reason for all documents |

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "document_tracker_id": 501,
      "status": "approved",
      "message": "OK"
    },
    {
      "document_tracker_id": 502,
      "status": "approved",
      "message": "OK"
    },
    {
      "document_tracker_id": 504,
      "status": "error",
      "message": "Document not found"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | `true` if all succeeded, `false` if any errors |
| `results` | `array` | Per-document result |
| `results[].status` | `string` | `"approved"` / `"rejected"` / `"error"` |

---

## 4. Mail APIs

### 4.1 GET `/candidates/{candidate_id}/mail/draft`

Get a pre-filled mail draft for the compose form. Used for stepper steps 2, 3, 5, and 6.

**Path Params:** `candidate_id` (int)

**Query Parameters:**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `step` | `int` | **Yes** | — | `2` / `3` / `5` / `6` |
| `regenerate` | `bool` | No | `false` | Force regenerate draft (ignores existing saved draft) |

**Example:** `GET /candidates/101/mail/draft?step=2&regenerate=false`

**Response (Step 2 — Document Required Mail):**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "step": 2,
  "job_id": 201,
  "to": "john.doe@gmail.com",
  "cc": "recruiter.priya@company.com",
  "subject": "Document Submission Required - CIN 20250415_REF001",
  "body": "Dear John Doe,\n\nWelcome to our onboarding process! As part of the joining formalities, we require the following documents from you:\n\n- Aadhaar Card\n- PAN Card\n- 10th Marksheet\n- 12th Marksheet\n- Degree Certificate\n- Experience Letter\n- Relieving Letter\n- Salary Slips\n\nPlease reply to this email with the documents attached. Include your CIN (20250415_REF001) in the subject line for tracking.\n\nRegards,\nHR Onboarding Team",
  "is_editable": true
}
```

**Response (Step 3 — Follow-up Mail):**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "step": 3,
  "job_id": 205,
  "to": "john.doe@gmail.com",
  "cc": "recruiter.priya@company.com",
  "subject": "Follow-up: Pending Document Submission - CIN 20250415_REF001",
  "body": "Dear John Doe,\n\nThis is a reminder regarding your pending onboarding documents...",
  "is_editable": true
}
```

**Response (Step 5 — On-Boarding Mail):**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "step": 5,
  "job_id": 210,
  "to": "john.doe@gmail.com",
  "cc": "rajesh.kumar@company.com, sneha.gupta@company.com",
  "subject": "Welcome Aboard - Joining Confirmation - John Doe",
  "body": "Dear John Doe,\n\nCongratulations! We are pleased to confirm that all your onboarding documents have been received and verified successfully.\n\nYour expected date of joining is 2025-06-01. You will be joining as Senior Software Engineer at Mumbai.\n\nWe will share further details regarding your joining formalities, including reporting time, dress code, and first-day schedule, shortly.\n\nWelcome aboard!\n\nRegards,\nHR Onboarding Team",
  "is_editable": true
}
```

**Response (Step 6 — IT-Admin Mail):**
```json
{
  "candidate_id": 101,
  "cin": "20250415_REF001",
  "step": 6,
  "job_id": null,
  "to": "it-admin@company.com",
  "cc": "rajesh.kumar@company.com",
  "subject": "IT Provisioning Request - John Doe (CIN 20250415_REF001)",
  "body": "Dear IT Admin,\n\nPlease provision the following for a new joiner:\n\nName: John Doe\nCIN: 20250415_REF001\nDesignation: Senior Software Engineer\nTechnology: Java/Spring Boot\nBusiness Unit: Digital Engineering\nReporting Manager: Rajesh Kumar\nLocation: Mumbai\nExpected Date of Joining: 2025-06-01\n\nRequired provisioning:\n- Laptop / Workstation\n- Email account and distribution lists\n- VPN and network access\n- Badge / access card\n- Required software licenses\n\nPlease ensure the setup is complete before the joining date.\n\nRegards,\nHR Onboarding Team",
  "is_editable": true
}
```

**MailDraftResponse fields:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `candidate_id` | `int` | No | Candidate PK |
| `cin` | `string` | No | CIN |
| `step` | `int` | No | Which step this draft is for (2/3/5/6) |
| `job_id` | `int` | Yes | Existing job ID if draft was saved. Pass this back in the send call. |
| `to` | `string` | No | Pre-filled recipient email |
| `cc` | `string` | Yes | Pre-filled CC email(s), comma-separated |
| `subject` | `string` | No | Pre-filled subject line |
| `body` | `string` | No | Pre-filled email body (HR can edit before sending) |
| `is_editable` | `bool` | No | Always `true` — UI should show all fields as editable |

**Pre-fill Summary:**

| Step | `to` | `cc` | Subject Pattern |
|------|------|------|-----------------|
| 2 | Candidate email | Recruiter | "Document Submission Required - CIN {cin}" |
| 3 | Candidate email | Recruiter | "Follow-up: Pending Document Submission - CIN {cin}" |
| 5 | Candidate email | Manager, Buddy | "Welcome Aboard - Joining Confirmation - {name}" |
| 6 | IT Admin email | Manager | "IT Provisioning Request - {name} (CIN {cin})" |

**Errors:** `400` if step is not 2/3/5/6. `404` if candidate not found.

---

### 4.2 POST `/candidates/{candidate_id}/mail/send`

Send the composed mail. HR may have edited the to/cc/subject/body from the draft. This API dispatches the email and updates the database.

**Path Params:** `candidate_id` (int)

**Request Body:**
```json
{
  "step": 2,
  "job_id": 201,
  "to": "john.doe@gmail.com",
  "cc": "recruiter.priya@company.com",
  "subject": "Document Submission Required - CIN 20250415_REF001",
  "body": "Dear John Doe,\n\nAs part of your onboarding..."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `step` | `int` | **Yes** | `2` / `3` / `5` / `6` — which stepper step this mail belongs to |
| `job_id` | `int` | No | Pass the `job_id` from the draft response if available. If null, a new job is created. |
| `to` | `string` | **Yes** | Recipient email (HR may have edited this) |
| `cc` | `string` | No | CC emails, comma-separated |
| `subject` | `string` | **Yes** | Email subject (HR may have edited this) |
| `body` | `string` | **Yes** | Full email body (HR may have edited this) |

**Response:**
```json
{
  "success": true,
  "message": "Successfully sent email to john.doe@gmail.com with subject 'Document Submission Required - CIN 20250415_REF001'",
  "job_id": 201
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | `true` if email was dispatched and DB updated |
| `message` | `string` | Confirmation message |
| `job_id` | `int` | The JOB_TRACKER ID (existing or newly created) |

**Backend Side Effects by Step:**

| Step | What happens after send |
|------|------------------------|
| 2 | Document tracker entries are created for all required documents. A follow-up job is created for 2 days later. Stepper advances to step 3. |
| 3 | A new follow-up job is created for 2 days later. |
| 5 | An IT admin mail job (step 6) is created automatically. Stepper advances to step 6. |
| 6 | No additional side effects. Stepper shows all 6 steps completed. |

**Errors:** `400` if step is not 2/3/5/6. `404` if candidate or job not found. `502` if email dispatch fails.

---

## 5. Existing Action APIs

These are pre-existing endpoints used by the agent workflow. They continue to work unchanged.

### 5.1 GET `/dashboard/pending-drafts`

Returns agent-generated drafts waiting on HR approval.

**Response:**
```json
[
  {
    "job_id": 201,
    "candidate": "John Doe",
    "cin": "20250415_REF001",
    "draft": "Dear John Doe,\n\nAs part of your onboarding..."
  }
]
```

### 5.2 POST `/action/approve-draft`

HR approves an agent-generated draft and triggers email dispatch.

**Request:**
```json
{
  "job_id": 201,
  "candidate_email": "john.doe@gmail.com",
  "subject": "Document Submission Required",
  "approved_content": "Dear John Doe,\n\n...",
  "hr_comments": "Approved with minor edits"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully sent email to john.doe@gmail.com..."
}
```

### 5.3 POST `/action/check-escalation/{candidate_id}`

Checks if escalation is needed (2+ failed follow-ups).

**Response:**
```json
{
  "escalation_needed": true,
  "followup_count": 3,
  "cin": "20250415_REF001",
  "missing_docs": ["Experience Letter", "Salary Slips"]
}
```

### 5.4 POST `/action/complete-onboarding/{candidate_id}`

Creates summary mail to HR + joining mail to candidate.

**Response:**
```json
{
  "cin": "20250415_REF001",
  "summary_drafted": true,
  "joining_drafted": true,
  "documents_completed": 8
}
```

### 5.5 GET `/dashboard/candidate-status/{cin}`

Returns document status by CIN.

**Response:**
```json
{
  "cin": "20250415_REF001",
  "candidate_name": "John Doe",
  "candidate_id": 101,
  "documents": [
    {
      "tracker_id": 501,
      "document_type_id": 1,
      "status": "Verified",
      "status_id": 5,
      "comments": null,
      "received_on": "2025-04-20"
    }
  ]
}
```

---

## 6. Status & Type Reference Tables

### Status IDs (STATUS_MASTER)

| status_id | Status | UI Badge Color |
|-----------|--------|---------------|
| 1 | Pending | Grey |
| 2 | Mail Drafted | Yellow |
| 3 | Mail Sent | Blue |
| 4 | Mail Received | Orange |
| 5 | Verified | Green |
| 6 | Rejected | Red |
| 7 | Completed | Dark Green |

### Candidate Types (CANDIDATE_TYPE_MASTER)

| candidate_type_id | Label |
|-------------------|-------|
| 1 | Fresher |
| 2 | Experience |
| 3 | Dev Partner |

### Stepper Steps

| Step | Label | UI Content |
|------|-------|-----------|
| 1 | Offer Released | Display candidate info (from GET `/candidates/{id}`) |
| 2 | Document Required Mail | Compose form (from GET `/candidates/{id}/mail/draft?step=2`) |
| 3 | Follow-up Mail Drop | Compose form (from GET `/candidates/{id}/mail/draft?step=3`) |
| 4 | Document List | Document table (from GET `/candidates/{id}/documents`) |
| 5 | On-Boarding Mail | Compose form (from GET `/candidates/{id}/mail/draft?step=5`) |
| 6 | IT-Admin Mail | Compose form (from GET `/candidates/{id}/mail/draft?step=6`) |

---

## UI Integration Flow (Screen by Screen)

### Login Page
> Static for now. No backend API. Hardcode credentials in Angular.

### Dashboard Page (4 Tabs)
1. On page load → call `GET /dashboard/summary` to show tab counts
2. On tab click → call `GET /dashboard/candidates?tab={tab_name}` to populate the table
3. Search box → add `&search={text}` to the candidates call
4. Pagination → pass `&page={n}&page_size={n}`
5. "View" button (eye icon) → navigate to candidate detail page using `candidate_id`
6. "Mark as Dropout" button (X icon) → show confirmation dialog → call `POST /candidates/{id}/dropout`

### Candidate Detail Page (6-Step Stepper)
1. On page load → call **both** in parallel:
   - `GET /candidates/{candidate_id}` (for full details)
   - `GET /candidates/{candidate_id}/stepper` (for step states)
2. Render stepper with 6 steps, highlight `current_step`
3. On step click → load the content for that step:

   **Step 1 (Offer Released):**
   - Display data from `GET /candidates/{id}` response

   **Step 2 (Document Required Mail):**
   - Call `GET /candidates/{id}/mail/draft?step=2`
   - Populate To, CC, Subject, Body fields
   - "Send Mail" button → `POST /candidates/{id}/mail/send` with `step: 2`

   **Step 3 (Follow-up Mail Drop):**
   - Call `GET /candidates/{id}/mail/draft?step=3`
   - Same compose form, "Send Mail" → `POST /candidates/{id}/mail/send` with `step: 3`

   **Step 4 (Document List):**
   - Call `GET /candidates/{id}/documents`
   - Render table with columns: Document Name | Submission Status | Approve | Reject | Rejection Reason
   - "Approve" button → `POST /documents/{tracker_id}/approve`
   - "Reject" button → `POST /documents/{tracker_id}/reject` (collect rejection_reason from input)
   - Optional: "Approve All" / "Reject Selected" → `POST /candidates/{id}/documents/bulk-action`
   - After each action, re-fetch the document list to refresh badges

   **Step 5 (On-Boarding Mail):**
   - Call `GET /candidates/{id}/mail/draft?step=5`
   - Compose form, "Send Mail" → `POST /candidates/{id}/mail/send` with `step: 5`

   **Step 6 (IT-Admin Mail):**
   - Call `GET /candidates/{id}/mail/draft?step=6`
   - Compose form, "Send Mail" → `POST /candidates/{id}/mail/send` with `step: 6`

4. After any send/action → re-fetch `GET /candidates/{id}/stepper` to update the stepper state

---

## Error Response Format

All error responses follow this structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

| HTTP Status | Meaning |
|-------------|---------|
| 400 | Bad request (invalid params, invalid step, etc.) |
| 404 | Resource not found (candidate, document, job) |
| 500 | Internal server error |
| 502 | Email dispatch failure |
