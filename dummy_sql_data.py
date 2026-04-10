
import pandas as pd

# ── Dummy visits list (replaces get_visits.sql) ────────────────
DUMMY_VISITS = pd.DataFrame({
    "VisitID": ["V001", "V002", "V003", "V004", "V005"]
})

# ── Dummy visit details (replaces resubmission.sql) ────────────
DUMMY_VISIT_DATA = {
    "V001": pd.DataFrame([
        {
            "VisitID": "V001",
            "Start_Date": "2024-01-15 09:00:00",
            "Med_Dept": "Psychiatry",
            "Specialty_Name": "Psychiatry",
            "ContractorClientPolicyNumber": "514891001",
            "ContractorClientEnName": "Demo Corp",
            "Contract": "VIP",
            "Service_Name": "Psychiatric Examination",
            "ISDRUG": 0,
            "ResponseReasonCode": "BE-001",
            "ResponseReason": "BE-001: Pre-authorization required for this service",
            "Price": 850.0,
            "Diagnose_Name": "Major depressive disorder",
            "ICD10 Code": "F32.1",
        },
        {
            "VisitID": "V001",
            "Start_Date": "2024-01-15 09:00:00",
            "Med_Dept": "Psychiatry",
            "Specialty_Name": "Psychiatry",
            "ContractorClientPolicyNumber": "514891001",
            "ContractorClientEnName": "Demo Corp",
            "Contract": "VIP",
            "Service_Name": "Psychotherapy Session",
            "ISDRUG": 0,
            "ResponseReasonCode": "BE-002",
            "ResponseReason": "BE-002: Benefit limit exceeded",
            "Price": 600.0,
            "Diagnose_Name": "Major depressive disorder",
            "ICD10 Code": "F32.1",
        }
    ]),
    "V002": pd.DataFrame([
        {
            "VisitID": "V002",
            "Start_Date": "2024-01-20 11:00:00",
            "Med_Dept": "Endocrinology",
            "Specialty_Name": "Endocrinology",
            "ContractorClientPolicyNumber": "842",
            "ContractorClientEnName": "Demo Corp 2",
            "Contract": "VIP",
            "Service_Name": "Endocrinology Consultation",
            "ISDRUG": 0,
            "ResponseReasonCode": "CV-001",
            "ResponseReason": "CV-001: Service not covered under plan",
            "Price": 600.0,
            "Diagnose_Name": "Type 2 Diabetes",
            "ICD10 Code": "E11.9",
        },
        {
            "VisitID": "V002",
            "Start_Date": "2024-01-20 11:00:00",
            "Med_Dept": "Endocrinology",
            "Specialty_Name": "Endocrinology",
            "ContractorClientPolicyNumber": "842",
            "ContractorClientEnName": "Demo Corp 2",
            "Contract": "VIP",
            "Service_Name": "Metformin 500mg",
            "ISDRUG": 1,
            "ResponseReasonCode": "CV-003",
            "ResponseReason": "CV-003: Drug not in approved formulary",
            "Price": 120.0,
            "Diagnose_Name": "Type 2 Diabetes",
            "ICD10 Code": "E11.9",
        }
    ]),
    "V003": pd.DataFrame([
        {
            "VisitID": "V003",
            "Start_Date": "2024-02-01 10:00:00",
            "Med_Dept": "Cardiology",
            "Specialty_Name": "Cardiology",
            "ContractorClientPolicyNumber": "514891001",
            "ContractorClientEnName": "Demo Corp",
            "Contract": "Gold",
            "Service_Name": "Cardiology Consultation",
            "ISDRUG": 0,
            "ResponseReasonCode": "BE-005",
            "ResponseReason": "BE-005: Charged amount exceeds allowed limit",
            "Price": 500.0,
            "Diagnose_Name": "Hypertension",
            "ICD10 Code": "I10",
        }
    ]),
    "V004": pd.DataFrame([
        {
            "VisitID": "V004",
            "Start_Date": "2024-02-10 14:00:00",
            "Med_Dept": "Obstetrics",
            "Specialty_Name": "Maternity",
            "ContractorClientPolicyNumber": "842",
            "ContractorClientEnName": "Demo Corp 2",
            "Contract": "VIP",
            "Service_Name": "Obstetrics Consultation",
            "ISDRUG": 0,
            "ResponseReasonCode": "CV-002",
            "ResponseReason": "CV-002: Duplicate claim submission",
            "Price": 700.0,
            "Diagnose_Name": "Normal pregnancy",
            "ICD10 Code": "Z34.0",
        },
        {
            "VisitID": "V004",
            "Start_Date": "2024-02-10 14:00:00",
            "Med_Dept": "Obstetrics",
            "Specialty_Name": "Maternity",
            "ContractorClientPolicyNumber": "842",
            "ContractorClientEnName": "Demo Corp 2",
            "Contract": "VIP",
            "Service_Name": "Ultrasound",
            "ISDRUG": 0,
            "ResponseReasonCode": "BE-003",
            "ResponseReason": "BE-003: Missing referral from treating physician",
            "Price": 400.0,
            "Diagnose_Name": "Normal pregnancy",
            "ICD10 Code": "Z34.0",
        }
    ]),
    "V005": pd.DataFrame([
        {
            "VisitID": "V005",
            "Start_Date": "2024-02-15 09:30:00",
            "Med_Dept": "Orthopedics",
            "Specialty_Name": "Orthopedics",
            "ContractorClientPolicyNumber": "514891001",
            "ContractorClientEnName": "Demo Corp",
            "Contract": "VIP+",
            "Service_Name": "Physiotherapy Session",
            "ISDRUG": 0,
            "ResponseReasonCode": "CV-004",
            "ResponseReason": "CV-004: Annual limit for physiotherapy exhausted",
            "Price": 450.0,
            "Diagnose_Name": "Low back pain",
            "ICD10 Code": "M54.5",
        }
    ]),
}


def get_dummy_visits():
    """Replaces: read_data(visits_query, ...)"""
    return DUMMY_VISITS


def get_dummy_visit_data(visit_id):
    """Replaces: read_data(query, ..., params=(visit_id,))"""
    return DUMMY_VISIT_DATA.get(str(visit_id), pd.DataFrame())