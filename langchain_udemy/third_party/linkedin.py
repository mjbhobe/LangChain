"""linkedin.py - scraping LinkedIn for profile info"""

import os
import requests
from dotenv import load_dotenv

# load all environment variables
load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles using scrapein.io,
    Manually scrape the information from profile page"""

    # NOTE: we are not using the mock parameter for now

    response = requests.get(
        linkedin_profile_url,
        timeout=10,
    )
    ret = response.json()
    # filter out fields that we are not interested in
    # this is to limit the tokens going to LLM to save costs!!
    ret = {
        k: v
        for k, v in ret.items()
        if (v not in ([], "", None) and k not in ["certifications"])
    }
    return ret


if __name__ == "__main__":
    gist_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
    print(scrape_linkedin_profile(gist_url))
