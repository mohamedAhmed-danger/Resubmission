"""
Dummy data for Resubmission Copilot
Run: python create_dummy_data.py
"""
from pymongo import MongoClient
from datetime import datetime
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["resubmission_db"]

# ── 1. VISITS ──────────────────────────────────────────────────
db.visits.drop()
visits = [
    {
        "visit_id": "V001",
        "patient": {"id": "P001", "name": "Ahmed Hassan", "dob": "1985-03-12", "class": "VIP"},
        "visit_date": "2024-01-15",
        "specialty": "Psychiatry",
        "diagnosis": {"code": "F32.1", "description": "Major depressive disorder"},
        "services": [
            {"service_id": 1, "name": "Psychiatric Examination", "code": "90837",
             "amount": 850.0, "status": "Denied", "denial_reason": "Pre-authorization required"}
        ],
        "insurance": {"provider": "Bupa", "policy_number": "514891001", "member_id": "BUP-001234"},
        "provider": {"name": "Dr. Khalil", "facility": "Mind Clinic"},
        "created_at": datetime(2024, 1, 15)
    },
    {
        "visit_id": "V002",
        "patient": {"id": "P002", "name": "Sara Ali", "dob": "1990-07-22", "class": "VIP+"},
        "visit_date": "2024-01-20",
        "specialty": "Endocrinology",
        "diagnosis": {"code": "E11.9", "description": "Type 2 Diabetes"},
        "services": [
            {"service_id": 1, "name": "Endocrinology Consultation", "code": "99214",
             "amount": 600.0, "status": "Denied", "denial_reason": "Not covered under plan"},
            {"service_id": 2, "name": "HbA1c Lab Test", "code": "83036",
             "amount": 200.0, "status": "Denied", "denial_reason": "Requires pre-authorization"}
        ],
        "insurance": {"provider": "NCCI", "policy_number": "842", "member_id": "NCC-005678"},
        "provider": {"name": "Dr. Jones", "facility": "Alex Clinic"},
        "created_at": datetime(2024, 1, 20)
    },
    {
        "visit_id": "V003",
        "patient": {"id": "P003", "name": "Mohamed Karim", "dob": "1978-11-05", "class": "Gold"},
        "visit_date": "2024-02-01",
        "specialty": "Cardiology",
        "diagnosis": {"code": "I10", "description": "Hypertension"},
        "services": [
            {"service_id": 1, "name": "Cardiology Consultation", "code": "99213",
             "amount": 500.0, "status": "Denied", "denial_reason": "Charged above allowed limit"},
            {"service_id": 2, "name": "ECG", "code": "93000",
             "amount": 150.0, "status": "Approved", "denial_reason": None}
        ],
        "insurance": {"provider": "Bupa", "policy_number": "514891001", "member_id": "BUP-009999"},
        "provider": {"name": "Dr. Hassan", "facility": "Cairo Medical Center"},
        "created_at": datetime(2024, 2, 1)
    },
    {
        "visit_id": "V004",
        "patient": {"id": "P004", "name": "Layla Nour", "dob": "1995-02-28", "class": "VIP"},
        "visit_date": "2024-02-10",
        "specialty": "Maternity",
        "diagnosis": {"code": "Z34.0", "description": "Normal pregnancy supervision"},
        "services": [
            {"service_id": 1, "name": "Obstetrics Consultation", "code": "99215",
             "amount": 700.0, "status": "Denied", "denial_reason": "Duplicate claim submission"},
            {"service_id": 2, "name": "Ultrasound", "code": "76805",
             "amount": 400.0, "status": "Denied", "denial_reason": "Missing referral"}
        ],
        "insurance": {"provider": "NCCI", "policy_number": "842", "member_id": "NCC-007777"},
        "provider": {"name": "Dr. Ali", "facility": "Nile Hospital"},
        "created_at": datetime(2024, 2, 10)
    },
]
db.visits.insert_many(visits)
print(f"✓ Inserted {len(visits)} visits")

# ── 2. POLICIES (what the LLM actually reads) ──────────────────
db.policies.drop()
policies = [
    {
        "policy_number": "514891001",
        "provider": "Bupa",
        "company_name": "Demo Corp",
        "effective_from": "2024-01-01",
        "effective_to": "2025-01-01",
        "coverage": {
            "VIP": {
                "overall_annual_limit": "1,000,000 SAR",
                "outpatient": "Covered, 20% patient share, max 100 SAR per visit",
                "psychiatry": "Covered up to Annual Limit, No pre-authorization required for outpatient",
                "maternity": "15,000 SAR for normal delivery",
                "dental": "2,000 SAR, scaling covered twice a year",
                "optical": "1,000 SAR",
                "approval_preauthorization_notes": "No pre-approval required for outpatient & inpatient services except outpatient services with specific limits (dental, optical, maternity, kidney aids, hearing aids, dialysis)"
            },
            "VIP+": {
                "overall_annual_limit": "1,000,000 SAR",
                "outpatient": "Covered, 10% patient share",
                "psychiatry": "Covered up to Annual Limit",
                "kidney_transplant": "250,000 SAR",
                "optical": "1,000 SAR, all lens types covered",
                "approval_preauthorization_notes": "Pre-authorization required for surgeries above 10,000 SAR only"
            },
            "Gold": {
                "overall_annual_limit": "500,000 SAR",
                "outpatient": "Covered, 20% patient share, max 150 SAR per visit",
                "cardiology_consultation_limit": "400 SAR per visit",
                "special_instructions": "Road Traffic Accident (RTA) is covered",
                "approval_preauthorization_notes": "Pre-authorization required for all inpatient admissions"
            }
        },
        # This is the raw text version fed to the LLM as `policy` param
        "policy_text": """Policy Number: 514891001 | Provider: Bupa | Company: Demo Corp
Effective: 2024-01-01 to 2025-01-01

VIP Class:
- Overall Annual Limit: 1,000,000 SAR
- Outpatient: Covered, 20% patient share, max 100 SAR per visit
- Psychiatry: Covered up to Annual Limit
- Maternity: 15,000 SAR normal delivery, 15,000 SAR C-section
- Dental: 2,000 SAR (scaling twice/year)
- Optical: 1,000 SAR
- Approval/Preauthorization Notes: No pre-approval required for outpatient & inpatient services
  EXCEPT outpatient services with specific limits: dental, optical, maternity, kidney aids, hearing aids, dialysis.

VIP+ Class:
- Overall Annual Limit: 1,000,000 SAR
- Outpatient: Covered, 10% patient share
- Psychiatry: Covered up to Annual Limit
- Kidney Transplant: 250,000 SAR
- Optical: 1,000 SAR (all lens types)
- Approval Notes: Pre-authorization required for surgeries above 10,000 SAR only

Gold Class:
- Overall Annual Limit: 500,000 SAR
- Outpatient: Covered, 20% patient share, max 150 SAR per visit
- Cardiology Consultation Limit: 400 SAR per visit
- Special Instructions: Road Traffic Accident (RTA) is covered
- Approval Notes: Pre-authorization required for all inpatient admissions
"""
    },
    {
        "policy_number": "842",
        "provider": "NCCI",
        "company_name": "Demo Corp 2",
        "effective_from": "2024-01-01",
        "effective_to": "2025-01-01",
        "coverage": {
            "VIP": {
                "overall_annual_limit": "800,000 SAR",
                "outpatient": "Covered, 0% patient share",
                "maternity": "Normal delivery 12,000 SAR, C-section 15,000 SAR",
                "approval_preauthorization_notes": "All services above 5,000 SAR require pre-authorization"
            }
        },
        "policy_text": """Policy Number: 842 | Provider: NCCI | Status: VALID
Effective: 2024-01-01 to 2025-01-01

VIP Class:
- Overall Annual Limit: 800,000 SAR
- Outpatient: Covered, 0% patient share
- Maternity: Normal delivery 12,000 SAR, C-section 15,000 SAR
- Imaging (Ultrasound): Covered, requires referral from treating physician
- Approval Notes: All services above 5,000 SAR require pre-authorization.
  Referral required for specialist visits and imaging.
"""
    }
]
db.policies.insert_many(policies)
print(f"✓ Inserted {len(policies)} policies")

# ── 3. RESUBMISSIONS ───────────────────────────────────────────
db.resubmissions.drop()
resubmissions = [
    {"resubmission_id": "R001", "visit_id": "V001", "submitted_date": "2024-02-01",
     "status": "In Progress", "notes": "Gathering prior auth docs"},
    {"resubmission_id": "R002", "visit_id": "V002", "submitted_date": "2024-02-05",
     "status": "In Progress", "notes": "Reviewing coverage for endocrinology"},
    {"resubmission_id": "R003", "visit_id": "V003", "submitted_date": "2024-02-20",
     "status": "Submitted",   "notes": "Resubmitted with corrected amount"},
    {"resubmission_id": "R004", "visit_id": "V004", "submitted_date": "2024-03-01",
     "status": "In Progress", "notes": "Obtaining referral + unique claim ID"},
]
db.resubmissions.insert_many(resubmissions)
print(f"✓ Inserted {len(resubmissions)} resubmissions")

print("\nCollections summary:")
for name in db.list_collection_names():
    print(f"  {name}: {db[name].count_documents({})} documents")

client.close()
print("\nDone! Run the Flask app now.")