import logging
import requests

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

class EnterpriseExtractor:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.trust_env = False 

    def flatten_json(self, nested_json: dict, prefix: str = "") -> dict:
        """
        Recursive function jo multi-level deeply nested JSON ko single-level 
        flat key-value dictionary me convert karta hai.
        """
        flattened = {}
        for key, value in nested_json.items():
            if isinstance(value, dict):
                flattened.update(self.flatten_json(value, f"{prefix}{key}_"))
            else:
                flattened[f"{prefix}{key}"] = value
        return flattened

    def extract_and_flatten(self, endpoint: str):
        """
        Fetches heavy nested records and yields flat dictionary rows.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"Day 3: Deep Nested JSON Extraction starting from {endpoint}...")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            raw_users = response.json()
            
            for raw_user in raw_users:
                flat_user = self.flatten_json(raw_user)
                yield flat_user
                
        except Exception as e:
            logger.error(f"Extraction failed on Day 3: {str(e)}")

if __name__ == "__main__":
    API_URL = "https://jsonplaceholder.typicode.com"
    extractor = EnterpriseExtractor(base_url=API_URL)
    
    print("🚀 Day 3 Pipeline: JSON Flattening Stream Active...\n")
    user_stream = extractor.extract_and_flatten(endpoint="users")
    
    count = 0
    for flat_record in user_stream:
        count += 1
        print(f"👤 Flat User {count} Map:")
        print(f"   -> ID: {flat_record.get('id')}")
        print(f"   -> Name: {flat_record.get('name')}")
        print(f"   -> Full Address: {flat_record.get('address_street')}, {flat_record.get('address_city')}")
        print(f"   -> Geo Lat/Lng: ({flat_record.get('address_geo_lat')}, {flat_record.get('address_geo_lng')})")
        print(f"   -> Company Name: {flat_record.get('company_name')}\n")
        
    print(f"✅ Day 3 Success: Safely flattened and streamed {count} deeply nested records.")
