"""
Run this ONCE to insert dummy policies into MongoDB via MongoEngine.
Usage: python insert_policies.py
"""
from mongoengine import connect
from datetime import datetime

# Connect same way as models.py
connect(
    db="resubmission_db",
    host="localhost",
    port=27017,
)

# Import models AFTER connect
from src.resubmission.models import Policy, CoverageDetail, NCCI_Policy, PolicyClass, Benefit, CaseCoverage, SubCoverage

# ── 1. Bupa Policy (514891001) ─────────────────────────────────
existing = Policy.objects(policy_number="514891001").first()
if existing:
    existing.delete()
    print("Deleted old Bupa policy")

bupa = Policy(
    policy_number="514891001",
    company_name="Demo Corp",
    policy_holder="Demo Corp HR",
    effective_from=datetime(2024, 1, 1),
    effective_to=datetime(2025, 1, 1),
    coverage_details=[
        CoverageDetail(
            vip_level="VIP",
            overall_annual_limit="1,000,000 SAR",
            inpatient_outpatient_treatment="Covered",
            outpatient_deductible_mpn="20% patient share, max 100 SAR",
            outpatient_deductible_hospitals="20% patient share, max 150 SAR",
            outpatient_deductible_polyclinic="20% patient share, max 100 SAR",
            branded_medication_deductible="20%",
            generic_medication_deductible="10%",
            psychiatric="Covered up to Annual Limit",
            dental_general="2,000 SAR, scaling covered twice per year",
            dental_corrective="Not covered",
            dental_emergency="Covered up to 500 SAR",
            optical="1,000 SAR",
            maternity="Normal delivery 15,000 SAR, C-section 15,000 SAR",
            physiotherapy="Covered up to 5,000 SAR per year",
            dialysis="Covered",
            hearing_aids_audiometry="Covered up to 2,000 SAR",
            congenital="Covered",
            autism="Covered up to 10,000 SAR",
            checkup="Annual checkup covered",
            vaccination="Covered as per MOH schedule",
            network="National Network",
            approval_preauthorization_notes=(
                "No pre-approval required for outpatient & inpatient services "
                "EXCEPT outpatient services with specific limits: dental, optical, "
                "maternity, kidney aids, hearing aids, and dialysis. "
                "Psychiatric services are NOT listed among the exceptions and require no pre-authorization."
            ),
            special_instructions=(
                "Road Traffic Accidents (RTA) are covered. "
                "Pre-existing conditions covered after 6 months waiting period."
            ),
        ),
        CoverageDetail(
            vip_level="VIP+",
            overall_annual_limit="1,000,000 SAR",
            inpatient_outpatient_treatment="Covered",
            outpatient_deductible_mpn="10% patient share, max 50 SAR",
            outpatient_deductible_hospitals="10% patient share, max 100 SAR",
            outpatient_deductible_polyclinic="10% patient share, max 50 SAR",
            branded_medication_deductible="10%",
            generic_medication_deductible="0%",
            psychiatric="Covered up to Annual Limit",
            dental_general="3,000 SAR",
            dental_corrective="1,000 SAR",
            dental_emergency="Covered",
            optical="1,500 SAR, all lens types covered",
            maternity="Normal delivery 20,000 SAR, C-section 20,000 SAR",
            kidney_transplant="250,000 SAR",
            physiotherapy="Covered up to 10,000 SAR per year",
            dialysis="Covered",
            checkup="Annual checkup covered",
            vaccination="Covered as per MOH schedule",
            network="Premium Network",
            approval_preauthorization_notes=(
                "Pre-authorization required for surgeries above 10,000 SAR only. "
                "All outpatient services do not require pre-authorization."
            ),
            special_instructions="VIP+ members have access to premium hospitals.",
        ),
        CoverageDetail(
            vip_level="Gold",
            overall_annual_limit="500,000 SAR",
            inpatient_outpatient_treatment="Covered",
            outpatient_deductible_mpn="20% patient share, max 150 SAR",
            outpatient_deductible_hospitals="20% patient share, max 200 SAR",
            outpatient_deductible_polyclinic="20% patient share, max 150 SAR",
            branded_medication_deductible="30%",
            generic_medication_deductible="20%",
            psychiatric="Covered up to 20,000 SAR per year",
            dental_general="1,500 SAR",
            dental_emergency="Covered up to 300 SAR",
            optical="800 SAR",
            maternity="Normal delivery 10,000 SAR",
            physiotherapy="Covered up to 3,000 SAR per year",
            network="Standard Network",
            approval_preauthorization_notes=(
                "Pre-authorization required for all inpatient admissions. "
                "Cardiology consultation allowed limit: 400 SAR per visit."
            ),
            special_instructions="Road Traffic Accident (RTA) is covered.",
        ),
    ]
)
bupa.save()
print(f"✓ Inserted Bupa policy: 514891001 with 3 VIP levels (VIP, VIP+, Gold)")

# ── 2. NCCI Policy (842) ───────────────────────────────────────
existing_ncci = NCCI_Policy.objects(policy_number="842").first()
if existing_ncci:
    existing_ncci.delete()
    print("Deleted old NCCI policy")

ncci = NCCI_Policy(
    provider_name="Hai Al Jamea Hospital",
    policy_number="842",
    policy_status="VALID",
    policy_holder_name="Demo Corp 2",
    policy_type="CORPORATE",
    issue_date=datetime(2024, 1, 1),
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2025, 1, 1),
    last_update=datetime(2024, 1, 1),
    coverage="Comprehensive inpatient and outpatient coverage",
    exclusion="Cosmetic procedures, experimental treatments",
    comments="Standard corporate policy",
    classes=[
        PolicyClass(
            class_code="1-VIP-Network Gold",
            class_limit="800,000 SAR",
            room_type="Private Room",
            room_limit="2,000 SAR per night",
            benefits=[
                Benefit(
                    benefit_code="OUTPATIENT",
                    description="Outpatient Services",
                    limit="800,000 SAR",
                    cases=[
                        CaseCoverage(
                            case_name="General Outpatient",
                            patient_share="0%",
                            max_patient_share="0 SAR",
                            max_consultation_fee="500 SAR",
                            approval_threshold="5,000 SAR",
                        )
                    ],
                ),
                Benefit(
                    benefit_code="MATERNITY",
                    description="Pregnancy, Delivery and Miscarriage",
                    limit="500,000 SAR",
                    cases=[
                        CaseCoverage(
                            case_name="Inpatient Maternity",
                            patient_share="0%",
                            max_patient_share="0 SAR",
                            max_consultation_fee="700 SAR",
                            approval_threshold="10,000 SAR",
                        ),
                        CaseCoverage(
                            case_name="Outpatient Maternity",
                            patient_share="20%",
                            max_patient_share="100 SAR",
                            max_consultation_fee="500 SAR",
                            approval_threshold="10,000 SAR",
                        ),
                    ],
                    sub_coverages=[
                        SubCoverage(
                            sub_coverage_code="175",
                            description="Miscarriage / Legal Abortion / Caesarian",
                            limit="15,000 SAR",
                            approval_threshold="10,000 SAR",
                        ),
                        SubCoverage(
                            sub_coverage_code="178",
                            description="Normal Delivery",
                            limit="12,000 SAR",
                            approval_threshold="10,000 SAR",
                        ),
                    ],
                ),
                Benefit(
                    benefit_code="IMAGING",
                    description="Radiology and Imaging",
                    limit="50,000 SAR",
                    cases=[
                        CaseCoverage(
                            case_name="Outpatient Imaging",
                            patient_share="0%",
                            max_patient_share="0 SAR",
                            max_consultation_fee="1,000 SAR",
                            approval_threshold="5,000 SAR",
                        )
                    ],
                    sub_coverages=[
                        SubCoverage(
                            sub_coverage_code="IMG-001",
                            description="Ultrasound - requires referral from treating physician",
                            limit="5,000 SAR",
                            approval_threshold="5,000 SAR",
                        ),
                    ],
                ),
            ],
        )
    ],
)
ncci.save()
print(f"✓ Inserted NCCI policy: 842")

print("\nAll policies inserted successfully! Now run: python flask_app.py")