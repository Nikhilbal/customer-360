# put near top of file: import statements
import requests
from requests.adapters import HTTPAdapter, Retry
import shutil
import os
from urllib.parse import urlsplit

def download_from_url(url, filename, out_dir="../data/raw", timeout=30):
    """
    Robust downloader: uses browser-like headers, retries, streaming.
    If server returns 403, suggests manual download and where to place file.
    """
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    # Session with retries
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504, 403])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))

    headers = {
        # mimic a real browser user agent
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept": ("text/html,application/xhtml+xml,application/xml;"
                   "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"),
        "Accept-Language": "en-US,en;q=0.9",
        # optionally referer; some servers check this
        "Referer": "https://www.consumerfinance.gov/"
    }

    try:
        with s.get(url, headers=headers, stream=True, timeout=timeout, allow_redirects=True) as r:
            # If still 403 or other client error, raise to be handled below
            r.raise_for_status()

            # Try to derive filename from headers if not provided
            if not filename:
                cd = r.headers.get('content-disposition')
                if cd and 'filename=' in cd:
                    filename = cd.split('filename=')[-1].strip(' "')
                    out_path = os.path.join(out_dir, filename)

            # Stream to file
            with open(out_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        print(f"✅ Saved {filename} to {out_dir}")
        return out_path

    except requests.exceptions.HTTPError as he:
        status = he.response.status_code if he.response is not None else None
        print(f"HTTP error {status} while downloading {url}: {he}")
        if status == 403:
            print("\nThe remote server returned 403 Forbidden. This often means it blocks automated downloads.")
            print("Options:")
            print("  1) Download the file manually with your browser from:")
            print(f"     {url}")
            print(f"     Then place the file at: {out_path}")
            print("  2) Try using curl/wget with a browser User-Agent (commands given below).")
        raise

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        raise
