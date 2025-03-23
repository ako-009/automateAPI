# autocomplete API

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
Results are printed for v1, v2, and v3.

Output:

v1: Found 260 names with 52 requests
v2: Found 360 names with 166 requests
v3: Found 419 names with 156 requests

Code Quality

Robustness: Errors and rate limits are handled comprehensively. Challenges such as unpredictable network failures and unknown rate limits were faced due to the API’s lack of documentation. These were overcome by implementing a retry mechanism with up to three attempts for failed requests, incorporating exponential backoff delays (1s, 2s, 4s) for 429 rate limit responses, and catching broad exceptions to manage unexpected issues gracefully with logged feedback.

Efficiency: A queue and visited set minimize unnecessary requests. The risk of excessive querying due to an unknown response pattern was encountered, potentially leading to server overload. This was addressed by employing a deque to systematically expand prefixes only when new names were found, and a visited set to skip redundant queries, ensuring minimal requests while covering all possibilities.

Readability: Code is structured with clear variable names and logic flow. The difficulty of maintaining clarity without API documentation was tackled by organizing the solution in a class structure (APIAutocompleteExtractor), using descriptive names (e.g., queue, results), and following a logical queue-based workflow, making the process easy to understand and maintain.
