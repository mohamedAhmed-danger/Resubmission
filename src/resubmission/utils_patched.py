import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from src.resubmission.models import CoverageDetail, Policy, NCCI_Policy, CaseCoverage, SubCoverage, Benefit, PolicyClass, Endorsement

# ── SFDA drug list ─────────────────────────────────────────────
sf = pd.read_csv(Path("Data") / "sfda_list.csv")

_ = load_dotenv()

# ── Dummy data replaces SQL Server completely ──────────────────
from dummy_sql_data import get_dummy_visits, get_dummy_visit_data


def get_visits_by_date():
    df = get_dummy_visits()
    return df["VisitID"]


def get_policy_details(df, logger):
    policy_number_input = df["ContractorClientPolicyNumber"].iloc[0]
    vip_level_input = normalize_text(df["Contract"].iloc[0])

    policy = _find_policy_by_number(policy_number_input)
    if not policy:
        logger.info("No policy found")
        return None, None, None

    detail, available_levels = _match_coverage_detail(policy, vip_level_input)
    return policy, detail, available_levels


def _find_policy_by_number(policy_number_input):
    policy_numbers = list(
        Policy.objects().only("policy_number").scalar("policy_number")
    )
    for policy_number in policy_numbers:
        if policy_number_input in policy_number:
            return Policy.objects(policy_number=policy_number).first()
    return None


def _match_coverage_detail(policy, vip_level_input):
    coverage_details = policy.coverage_details

    if len(coverage_details) == 1:
        detail = coverage_details[0].to_mongo().to_dict()
        return dict(sorted(detail.items())), None

    matching_coverages = [
        c for c in coverage_details if normalize_text(c.vip_level) == vip_level_input
    ]

    if matching_coverages:
        detail = matching_coverages[0].to_mongo().to_dict()
        return dict(sorted(detail.items())), None

    available_levels = [c.vip_level for c in coverage_details]
    return None, available_levels


def get_visit_data(visit_id, logger):
    df = get_dummy_visit_data(visit_id)
    logger.info(f"Fetched {len(df)} rows for visit {visit_id}")

    if df.empty:
        return None

    df["Contract"] = (
        df["Contract"]
        .fillna("")
        .astype(str)
        .str.split("-", n=1)
        .pipe(lambda p: p.apply(lambda x: x[1].strip() if len(x) > 1 else x[0].strip()))
    )

    df = pd.merge(df, sf, on="Service_Name", how="left")

    if "Start_Date" in df.columns and not df.empty:
        df["Start_Date"] = pd.to_datetime(df["Start_Date"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


def extract_drug_code(text):
    pattern = r"\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?){0,2}"
    codes = re.findall(pattern, text)
    return set(codes)


def processing_thoughts(text):
    pattern = r"<think>(.*?)</think>"
    text_in_between = re.findall(pattern, str(text), re.DOTALL)
    clean_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return clean_text.strip(), text_in_between[0].strip()


def list_files(folder_path: str):
    p = Path(folder_path)
    if not p.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory")
    return [str(f) for f in p.iterdir() if f.is_file()]


def insert(data_source):
    if isinstance(data_source, str):
        with open(data_source, "r") as f:
            data = json.load(f)
    elif isinstance(data_source, dict):
        data = data_source
    else:
        raise TypeError("data_source must be a dict or JSON file path")

    policy_number = data.get("policy_number")
    if not policy_number:
        raise ValueError("Missing required field: 'policy_number'")

    existing = Policy.objects(policy_number=policy_number).first()
    if existing:
        print(f"Policy {policy_number} already exists. Skipping insert.")
        return existing

    coverage_list = [
        CoverageDetail(**coverage) for coverage in data.get("coverage_details", [])
    ]

    policy = Policy(
        policy_number=policy_number,
        company_name=data.get("company_name"),
        policy_holder=data.get("policy_holder"),
        effective_from=(
            datetime.fromisoformat(data["effective_from"]) if "effective_from" in data else None
        ),
        effective_to=(
            datetime.fromisoformat(data.get("effective_to"))
            if data.get("effective_to") not in (None, "") else None
        ),
        coverage_details=coverage_list,
    )
    policy.save()
    print(f"Policy {policy.policy_number} inserted successfully.")


def insert_ncci(data_source):
    if isinstance(data_source, str):
        with open(data_source, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif isinstance(data_source, dict):
        data = data_source
    else:
        raise TypeError("data_source must be a dict or JSON file path")

    policy_number = data.get("policy_number")
    if not policy_number:
        raise ValueError("Missing required field: 'policy_number'")

    existing = NCCI_Policy.objects(policy_number=policy_number).first()
    if existing:
        print(f"Policy {policy_number} already exists. Skipping insert.")
        return existing

    class_list = []
    for cls in data.get("classes", []):
        benefit_list = []
        for benefit in cls.get("benefits") or []:
            cases = [CaseCoverage(**case) for case in (benefit.get("cases") or [])]
            sub_coverages = [SubCoverage(**sub) for sub in (benefit.get("sub_coverages") or [])]
            benefit_list.append(Benefit(
                benefit_code=benefit.get("benefit_code"),
                description=benefit.get("description"),
                limit=benefit.get("limit"),
                cases=cases or None,
                sub_coverages=sub_coverages or None,
            ))
        class_list.append(PolicyClass(
            class_code=cls.get("class_code"),
            class_limit=cls.get("class_limit"),
            room_type=cls.get("room_type"),
            room_limit=cls.get("room_limit"),
            benefits=benefit_list or None,
        ))

    if not class_list:
        raise ValueError("At least one class is required")

    endorsement_list = [
        Endorsement(**e) for e in (data.get("endorsements") or [])
    ]

    policy = NCCI_Policy(
        provider_name=data.get("provider_name"),
        policy_number=policy_number,
        policy_status=data.get("policy_status"),
        policy_holder_name=data.get("policy_holder_name"),
        policy_type=data.get("policy_type"),
        issue_date=datetime.fromisoformat(data["issue_date"]) if data.get("issue_date") else None,
        start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
        end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
        last_update=datetime.fromisoformat(data["last_update"]) if data.get("last_update") else None,
        coverage=data.get("coverage"),
        exclusion=data.get("exclusion"),
        comments=data.get("comments"),
        classes=class_list,
        endorsements=endorsement_list or None,
        additional_information=data.get("additional_information"),
    )
    policy.save()
    print(f"Policy {policy.policy_number} inserted successfully.")
    return policy


def delete(policy_number: str):
    policy = Policy.objects(policy_number=policy_number).first()
    if not policy:
        print(f"Policy {policy_number} not found.")
        return False
    policy.delete()
    print(f"Policy {policy_number} deleted successfully.")
    return True


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    return text.replace(" ", "").replace("–", "").replace("-", "").lower()