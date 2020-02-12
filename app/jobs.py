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
from app.models import Response, Status


@rq.job
def send_request(check, timeout):
    """Send an HTTP GET request for a check."""
    start_time = datetime.utcnow()
    try:
        r = requests.get(check.url, timeout=timeout)
        status = Status.SUCCESS if r.status_code < 400 else Status.FAILURE
        description = "HTTP {code}: {msg}".format(
            code=r.status_code, msg=http.client.responses[r.status_code]
        )
    except ConnectionError:
        status = Status.FAILURE
        description = "Error: connection failed"
    except Timeout:
        status = Status.FAILURE
        description = "Error: request timed out"
    except TooManyRedirects:
        status = Status.FAILURE
        description = "Error: too many redirects"
    except RequestException as e:
        status = Status.FAILURE
        description = "Unknown error: {}".format(str(e))
    finally:
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        return Response(
            check_id=check.id,
            start_time=start_time,
            elapsed_ms=elapsed_ms,
            status=status,
            description=description,
        )
