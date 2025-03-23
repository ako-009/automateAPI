# automateAPI

Project Overview
All possible names are extracted from an undocumented autocomplete API at http://35.200.185.69:8000 in this project. The API’s behavior is explored, constraints are managed, and results are documented without official guidance.

Requirements
Python 3.7+ is required.
The requests library is installed via pip install requests.

Approach
Setup:
A requests.Session is utilized for efficient HTTP connections.
Code is structured within an APIAutocompleteExtractor class for organization.

Exploration:
The endpoint /v1/autocomplete?query=<string> is tested with single-letter queries (a to z).
Additional endpoints /v2/autocomplete and /v3/autocomplete are investigated.
API responses are analyzed to deduce structure and behavior.

Extraction:
All lowercase alphabets (a to z) are queried initially, with prefixes expanded dynamically (e.g., a to ap).
Unique names are collected in a set and sorted for output.

Constraints Handling:
Rate limiting is addressed with a 0.1s delay between requests and exponential backoff (1s, 2s, 4s) on 429 errors.
HTTP errors, connection issues, and unexpected failures are managed with retries (up to 3 attempts).
Progress is tracked to avoid duplicate queries.

Optimization:
A queue-based approach is implemented to systematically explore prefixes.
Redundant requests are skipped using a visited set.

Findings
Endpoints:
/v1/autocomplete is confirmed as the starting point.
/v2/autocomplete and /v3/autocomplete are also tested.

Response Format:
JSON with a "results" key is assumed, containing a list of names.

Constraints:
Rate limiting (429) is anticipated and handled.
Possible result limits per query are mitigated by expanding prefixes.

Features:
Dynamic prefix generation is observed as a key mechanism for exhaustive extraction.

Running the Code
Dependencies are installed with: pip install requests.
The script is executed with: python script.py.
Results are printed to the console for v1, v2, and v3.

Output:
v1: Found 260 names with 52 requests
v2: Found 360 names with 166 requests
v3: Found 419 names with 156 requests

Code Quality
Robustness: Errors and rate limits are handled comprehensively.
Efficiency: A queue and visited set minimize unnecessary requests.
Readability: Code is structured with clear variable names and logic flow.
