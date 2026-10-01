import logging
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataAuditLogger:
    def __init__(self):
        self.anomaly_registry: List[Dict[str, Any]] = []

    def log_anomaly(self, record_id: int, raw_record: Dict[str, Any], reason: str):
        """
        Corrupt ya rejected record ko timestamp aur failure reason ke sath track karta hai.
        """
        anomaly_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "record_id": record_id,
            "reason": reason,
            "raw_payload": raw_record
        }
        self.anomaly_registry.append(anomaly_entry)
        logging.warning(f"🚨 DLQ Alert: Record ID {record_id} captured in Anomaly Logs -> {reason}")

    def generate_audit_report(self) -> Dict[str, Any]:
        """
        Poore transformation batch ka summary metrics report ready karta hai.
        """
        return {
            "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_anomalies_caught": len(self.anomaly_registry),
            "rejected_records": self.anomaly_registry
        }
