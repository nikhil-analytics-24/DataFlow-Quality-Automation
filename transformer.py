import re
import json
import logging
from typing import Dict, Any, List
from audit_logger import DataAuditLogger 

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

class DataTransformer:
    def __init__(self):
        pass

    def cast_and_clean_fields(self, flat_record: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_record = {}
        try:
            cleaned_record["id"] = int(flat_record.get("id", 0))
            cleaned_record["name"] = str(flat_record.get("name", "Unknown")).strip()
            cleaned_record["username"] = str(flat_record.get("username", "N/A")).strip().lower()
            cleaned_record["email"] = str(flat_record.get("email", "N/A")).strip().lower()
            cleaned_record["geo_lat"] = float(flat_record.get("address_geo_lat", 0.0))
            cleaned_record["geo_lng"] = float(flat_record.get("address_geo_lng", 0.0))
            
            street = flat_record.get("address_street", "")
            city = flat_record.get("address_city", "")
            cleaned_record["full_address"] = f"{street}, {city}".strip(", ") if (street or city) else "Not Available"
            cleaned_record["company_name"] = str(flat_record.get("company_name", "Freelance/Individual")).strip()
            return cleaned_record
        except (ValueError, TypeError):
            return {"id": 0, "error": True}

class EnterpriseDataValidator:
    def __init__(self, audit_engine: DataAuditLogger = None):
        self.email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        self.audit_engine = audit_engine
        logger.info("Day 5 & 6: Strict Schema Enforcement & Audit Logging Engine Active.")

    def is_valid_record(self, cleaned_record: Dict[str, Any]) -> bool:
        rec_id = cleaned_record.get("id", 0)
        
        if rec_id <= 0:
            reason = f"Validation Failed: Invalid ID found -> {rec_id}"
            logger.warning(reason)
            if self.audit_engine:
                self.audit_engine.log_anomaly(record_id=rec_id, raw_record=cleaned_record, reason=reason)
            return False

        email = cleaned_record.get("email", "")
        if not self.email_regex.match(email):
            reason = f"Validation Failed: Corrupt/Invalid Email format -> '{email}'"
            logger.warning(f"{reason} (ID: {rec_id})")
            if self.audit_engine:
                self.audit_engine.log_anomaly(record_id=rec_id, raw_record=cleaned_record, reason=reason)
            return False

        lat = cleaned_record.get("geo_lat", 0.0)
        if not (-90.0 <= lat <= 90.0):
            reason = f"Validation Failed: Out of boundary Latitude ({lat}) detected"
            logger.warning(f"{reason} (ID: {rec_id})")
            if self.audit_engine:
                self.audit_engine.log_anomaly(record_id=rec_id, raw_record=cleaned_record, reason=reason)
            return False

        return True

    def run_transform_and_validate_pipeline(self, raw_data_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        transformer = DataTransformer()
        passed_records = []
        rejected_count = 0
        
        for raw_record in raw_data_batch:
            cleaned = transformer.cast_and_clean_fields(raw_record)
            
            if cleaned.get("error"):
                rejected_count += 1
                if self.audit_engine:
                    raw_id = raw_record.get("id", 0)
                    try: raw_id = int(raw_id)
                    except: raw_id = 0
                    self.audit_engine.log_anomaly(record_id=raw_id, raw_record=raw_record, reason="Casting Error: Raw fields failed data type generation.")
                continue
                
            if self.is_valid_record(cleaned):
                passed_records.append(cleaned)
            else:
                rejected_count += 1
                
        logger.info(f"Batch Execution Over: {len(passed_records)} passed, {rejected_count} anomaly records rejected.")
        return passed_records

def dump_pipeline_state(valid_records: List[Dict[str, Any]], audit_report: Dict[str, Any]):
  
    try:
        with open("clean_transformed_data.json", "w", encoding="utf-8") as valid_file:
            json.dump(valid_records, valid_file, indent=4, ensure_ascii=False)
        logger.info("💾 Success: Valid data cached safely in 'clean_transformed_data.json'.")

        with open("anomaly_dlq_report.json", "w", encoding="utf-8") as dlq_file:
            json.dump(audit_report, dlq_file, indent=4, ensure_ascii=False)
        logger.info("💾 Success: DLQ Anomaly logs dumped in 'anomaly_dlq_report.json'.")
        
    except IOError as e:
        logger.error(f"Storage Dump Failed: System write permissions anomaly -> {str(e)}")


if __name__ == "__main__":
    audit_engine = DataAuditLogger()
    
    mixed_raw_data = [
        {
            "id": "10", 
            "name": "Kunal Sharma", 
            "username": "KunalS",
            "email": "kunal@tier1.com",
            "address_street": "Connaught Place",
            "address_city": "New Delhi",
            "address_geo_lat": "28.6139",
            "address_geo_lng": "77.2090"
        },
        {
            "id": "11",
            "name": "Anomalous Record Email Test",
            "username": "bad_email",
            "email": "plainaddress_no_at_the_rate.com",
            "address_geo_lat": "12.9716",
        },
        {
            "id": "12",
            "name": "Anomalous Record Geo Test",
            "username": "bad_geo",
            "email": "geo@test.com",
            "address_geo_lat": "150.8574", 
        }
    ]
    
    validator = EnterpriseDataValidator(audit_engine=audit_engine)
    print("\n🚀 Day 7: Executing Transform Pipeline & Target File Dumps...\n")
    
    final_pipeline_output = validator.run_transform_and_validate_pipeline(mixed_raw_data)
    report = audit_engine.generate_audit_report()
    
    dump_pipeline_state(valid_records=final_pipeline_output, audit_report=report)
    
    print(f"\n📊 Day 7 Health Metrics: {len(final_pipeline_output)} Transformed Data Written | {report['total_anomalies_caught']} DLQ logs cached.")
