import inspect
import sys

from selvpcclient.exceptions import base


class HttpError(base.ClientException):
    """The base exception class for all HTTP exceptions."""
    http_status = 0
    message = "HTTP Error"

    def __init__(self,
                 message=None,
                 details=None,
                 response=None,
                 request_id=None,
                 url=None,
                 method=None,
                 http_status=None,
                 retry_after=0):
        self.http_status = http_status or self.http_status
        self.message = message or self.message
        self.details = details
        self.request_id = request_id
        self.response = response
        self.url = url
        self.method = method
        formatted_string = "%s (HTTP %s)" % (self.message, self.http_status)
        self.retry_after = retry_after
        if request_id:
            formatted_string += " (Request-ID: %s)" % request_id
        super(HttpError, self).__init__(formatted_string)


class HTTPClientError(HttpError):
    """Client-side HTTP error.

    Exception for cases in which the client seems to have erred.
    """
    message = "HTTP Client Error"


class HttpServerError(HttpError):
    """Server-side HTTP error.

    Exception for cases in which the server is aware that it has
    erred or is incapable of performing the request.
    """
    message = "HTTP Server Error"


class BadRequest(HTTPClientError):
    """HTTP 400 - Bad Request.

    The request cannot be fulfilled due to bad syntax.
    """
    http_status = 400
    message = "Bad Request"


class Unauthorized(HTTPClientError):
    """HTTP 401 - Unauthorized.

    Similar to 403 Forbidden, but specifically for use when authentication
    is required and has failed or has not yet been provided.
    """
    http_status = 401
    message = "Unauthorized"


class PaymentRequired(HTTPClientError):
    """HTTP 402 - Payment Required.

    Reserved for future use.
    """
    http_status = 402
    message = "Payment Required"


class Forbidden(HTTPClientError):
    """HTTP 403 - Forbidden.

    The request was a valid request, but the server is refusing to respond
    to it.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(HTTPClientError):
    """HTTP 404 - Not Found.

    The requested resource could not be found but may be available again
    in the future.
    """
    http_status = 404
    message = "Not Found"


class MethodNotAllowed(HTTPClientError):
    """HTTP 405 - Method Not Allowed.

    A request was made of a resource using a request method not supported
    by that resource.
    """
    http_status = 405
    message = "Method Not Allowed"


class NotAcceptable(HTTPClientError):
    """HTTP 406 - Not Acceptable.

    The requested resource is only capable of generating content not
    acceptable according to the Accept headers sent in the request.
    """
    http_status = 406
    message = "Not Acceptable"


class ProxyAuthenticationRequired(HTTPClientError):
    """HTTP 407 - Proxy Authentication Required.

    The client must first authenticate itself with the proxy.
    """
    http_status = 407
    message = "Proxy Authentication Required"


class RequestTimeout(HTTPClientError):
    """HTTP 408 - Request Timeout.

    The server timed out waiting for the request.
    """
    http_status = 408
    message = "Request Timeout"


class Conflict(HTTPClientError):
    """HTTP 409 - Conflict.

    Indicates that the request could not be processed because of conflict
    in the request, such as an edit conflict.
    """
    http_status = 409
    message = "Conflict"


class Gone(HTTPClientError):
    """HTTP 410 - Gone.

    Indicates that the resource requested is no longer available and will
    not be available again.
    """
    http_status = 410
    message = "Gone"


class LengthRequired(HTTPClientError):
    """HTTP 411 - Length Required.

    The request did not specify the length of its content, which is
    required by the requested resource.
    """
    http_status = 411
    message = "Length Required"


class PreconditionFailed(HTTPClientError):
    """HTTP 412 - Precondition Failed.

    The server does not meet one of the preconditions that the requester
    put on the request.
    """
    http_status = 412
    message = "Precondition Failed"


class RequestEntityTooLarge(HTTPClientError):
    """HTTP 413 - Request Entity Too Large.

    The request is larger than the server is willing or able to process.
    """
    http_status = 413
    message = "Request Entity Too Large"

    def __init__(self, *args, **kwargs):
        try:
            self.retry_after = int(kwargs.pop('retry_after'))
        except (KeyError, ValueError):
            self.retry_after = 0

        super(RequestEntityTooLarge, self).__init__(*args, **kwargs)


class RequestUriTooLong(HTTPClientError):
    """HTTP 414 - Request-URI Too Long.

    The URI provided was too long for the server to process.
    """
    http_status = 414
    message = "Request-URI Too Long"


class UnsupportedMediaType(HTTPClientError):
    """HTTP 415 - Unsupported Media Type.

    The request entity has a media type which the server or resource does
    not support.
    """
    http_status = 415
    message = "Unsupported Media Type"


class RequestedRangeNotSatisfiable(HTTPClientError):
    """HTTP 416 - Requested Range Not Satisfiable.

    The client has asked for a portion of the file, but the server cannot
    supply that portion.
    """
    http_status = 416
    message = "Requested Range Not Satisfiable"


class ExpectationFailed(HTTPClientError):
    """HTTP 417 - Expectation Failed.

    The server cannot meet the requirements of the Expect request-header field.
    """
    http_status = 417
    message = "Expectation Failed"


class UnprocessableEntity(HTTPClientError):
    """HTTP 422 - Unprocessable Entity.

    The request was well-formed but was unable to be followed due to semantic
    errors.
    """
    http_status = 422
    message = "Unprocessable Entity"


class InternalServerError(HttpServerError):
    """HTTP 500 - Internal Server Error.

    A generic error message, given when no more specific message is suitable.
    """
    http_status = 500
    message = "Internal Server Error"


# NotImplemented is a python keyword.
class HttpNotImplemented(HttpServerError):
    """HTTP 501 - Not Implemented.

    The server either does not recognize the request method, or it lacks
    the ability to fulfill the request.
    """
    http_status = 501
    message = "Not Implemented"


class BadGateway(HttpServerError):
    """HTTP 502 - Bad Gateway.

    The server was acting as a gateway or proxy and received an invalid
    response from the upstream server.
    """
    http_status = 502
    message = "Bad Gateway"


class ServiceUnavailable(HttpServerError):
    """HTTP 503 - Service Unavailable.

    The server is currently unavailable.
    """
    http_status = 503
    message = "Service Unavailable"


class GatewayTimeout(HttpServerError):
    """HTTP 504 - Gateway Timeout.

    The server was acting as a gateway or proxy and did not receive a timely
    response from the upstream server.
    """
    http_status = 504
    message = "Gateway Timeout"


class HttpVersionNotSupported(HttpServerError):
    """HTTP 505 - HttpVersion Not Supported.

    The server does not support the HTTP protocol version used in the request.
    """
    http_status = 505
    message = "HTTP Version Not Supported"


_code_map = {}

for member in inspect.getmembers(sys.modules[__name__], inspect.isclass):
    name, obj = member

    if hasattr(obj, 'http_status'):
        _code_map[getattr(obj, 'http_status')] = obj


def get_http_exception(status_code, content=None):
    exception = _code_map[status_code](content)
    return exception
