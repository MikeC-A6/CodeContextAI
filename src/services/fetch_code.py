"""
fetch_code.py

Utility to fetch raw code from GitHub, given the structured output from Gemini.

Gemini returns something like:
[
  {
    "path": "api/src/auth/auth_utils.py",
    "reason": "Explanation of relevance",
    "github_url": "https://github.com/HHS/simpler-grants-gov/blob/main/api/src/auth/auth_utils.py"
  },
  ...
]

We convert each GitHub URL to a raw.githubusercontent.com URL, fetch the file content,
and return a new JSON array (as a string) that includes both the file metadata and the actual code.
"""

import json
import requests

def fetch_code_from_github(gemini_output_json: str) -> str:
    """
    Takes the Gemini JSON output (as a string) and returns a new JSON string
    that includes the "code" for each file.

    :param gemini_output_json: The JSON array from Gemini, e.g.:
        [
          {
            "path": "...",
            "reason": "...",
            "github_url": "..."
          }
        ]
    :return: A JSON array string, enriched with "raw_url" and "code" for each file:
        [
          {
            "path": "...",
            "reason": "...",
            "github_url": "...",
            "raw_url": "...",
            "code": "<raw file content>"
          }
        ]
        or an empty array [] if something goes wrong.
    """

    try:
        file_refs = json.loads(gemini_output_json)
        if not isinstance(file_refs, list):
            return "[]"
    except json.JSONDecodeError:
        return "[]"

    enriched = []
    for ref in file_refs:
        github_url = ref.get("github_url", "")
        raw_url = _make_raw_github_url(github_url)

        code_content = _fetch_raw_file(raw_url)

        enriched.append({
            "path": ref.get("path", ""),
            "reason": ref.get("reason", ""),
            "github_url": github_url,
            "raw_url": raw_url,
            "code": code_content
        })

    return json.dumps(enriched, indent=2)


def _make_raw_github_url(github_url: str) -> str:
    """
    Convert a GitHub link with /blob/ to a raw link.
    e.g. https://github.com/<org>/<repo>/blob/<branch>/path/to/file
         => https://raw.githubusercontent.com/<org>/<repo>/<branch>/path/to/file
    """
    if not github_url.startswith("https://github.com/"):
        return github_url  # If it's not a recognized GitHub link, just return as-is

    raw_url = github_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
    raw_url = raw_url.replace("/blob/", "/")
    return raw_url


def _fetch_raw_file(url: str) -> str:
    """Fetch the raw file content from `url`. Returns a string (the file content or an error message)."""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text
        return f"Error retrieving file (HTTP {resp.status_code}): {url}"
    except requests.RequestException as exc:
        return f"Exception while retrieving file: {str(exc)}"