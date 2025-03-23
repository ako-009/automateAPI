import requests
import time
from collections import deque
import string

class APIAutocompleteExtractor:
    def __init__(self, base_url="http://35.200.185.69:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {'User-Agent': 'AutocompleteExtractor/1.0'}
        
    def extract_names(self, api_version='v1'):
        visited = set()
        queue = deque()
        results = set()
        request_count = 0
        retries = 3
        delay = 1
        
        # Initialize with all possible first characters
        for c in string.ascii_lowercase:
            queue.append(c)
            
        while queue:
            prefix = queue.popleft()
            if prefix in visited:
                continue
            visited.add(prefix)
            
            url = f"{self.base_url}/{api_version}/autocomplete?query={prefix}"
            response = None
            
            for attempt in range(retries):
                try:
                    response = self.session.get(url, headers=self.headers)
                    request_count += 1
                    if response.status_code == 200:
                        break
                    elif response.status_code == 429:
                        time.sleep(delay * (2 ** attempt))
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(delay * (2 ** attempt))
            
            if response and response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    for name in data['results']:
                        clean_name = name.strip().lower()
                        if clean_name not in results:
                            results.add(clean_name)
                            # Generate next level prefixes
                            if len(clean_name) > len(prefix):
                                next_prefix = clean_name[:len(prefix)+1]
                                if next_prefix not in visited:
                                    queue.append(next_prefix)
            
            # Rate limit protection
            time.sleep(0.1)
        
        return sorted(results), request_count

    def save_to_file(self, names, version):
        filename = f"{version}_names.txt"
        with open(filename, 'w') as f:
            f.write('\n'.join(names))
        print(f"Saved {len(names)} names to {filename}")

if __name__ == "__main__":
    extractor = APIAutocompleteExtractor()
    
    # Process and save v1
    v1_names, v1_requests = extractor.extract_names('v1')
    extractor.save_to_file(v1_names, 'v1')
    print(f"v1: Found {len(v1_names)} names with {v1_requests} requests")
    
    # Process and save v2
    v2_names, v2_requests = extractor.extract_names('v2')
    extractor.save_to_file(v2_names, 'v2')
    print(f"v2: Found {len(v2_names)} names with {v2_requests} requests")
    
    # Process and save v3
    v3_names, v3_requests = extractor.extract_names('v3')
    extractor.save_to_file(v3_names, 'v3')
    print(f"v3: Found {len(v3_names)} names with {v3_requests} requests")