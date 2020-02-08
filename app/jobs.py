from datetime import datetime
import http.client
import requests
from requests.exceptions import (
    ConnectionError,
    RequestException,
    Timeout,
    TooManyRedirects,
)

from app import rq
from app.models import Response


@rq.job
def send_request(check, timeout):
    """Send an HTTP GET request for a check."""
    ok = False
    start_time = datetime.utcnow()
    try:
        resp = requests.get(check.url, timeout=timeout)
        ok = resp.ok
        description = "HTTP {code}: {msg}".format(
            code=resp.status_code, msg=http.client.responses[resp.status_code]
        )
    except ConnectionError:
        description = "Error: connection failed"
    except Timeout:
        description = "Error: request timed out"
    except TooManyRedirects:
        description = "Error: too many redirects"
    except RequestException as e:
        description = "Unknown error: {}".format(str(e))
    finally:
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        return Response(
            check_id=check.id,
            start_time=start_time,
            elapsed_ms=elapsed_ms,
            ok=ok,
            description=description,
        )
