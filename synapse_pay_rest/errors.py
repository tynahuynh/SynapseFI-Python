""" Custom errors for handling HTTP and API errors. """


class SynapsePayError(Exception):
    """Custom class for handling HTTP and API errors."""
    def __init__(self, message, code, response):
        self.message = message
        self.code = code
        self.response = response


class ClientError(SynapsePayError):
    pass


class BadRequestError(ClientError):
    """ Raised on the HTTP status code 400 """
    pass


class UnauthorizedError(ClientError):
    """ Raised on the HTTP status code 401 """
    pass


class RequestDeclinedError(ClientError):
    """ Raised on the HTTP status code 402 """
    pass


class ForbiddenError(ClientError):
    """ Raised on the HTTP status code 403 """
    pass


class NotFoundError(ClientError):
    """ Raised on the HTTP status code 404 """
    pass


class NotAcceptableError(ClientError):
    """ Raised on the HTTP status code 406 """
    pass


class ConflictError(ClientError):
    """ Raised on the HTTP status code 409 """
    pass


class UnsupportedMediaTypeError(ClientError):
    """ Raised on the HTTP status code 415 """
    pass


class UnprocessableEntityError(ClientError):
    """ Raised on the HTTP status code 422 """
    pass


class TooManyRequestsError(ClientError):
    """ Raised on the HTTP status code 429 """
    pass


class ServerError(SynapsePayError):
    """ Raised on a 5xx HTTP status code """
    pass


class InternalServerError(ServerError):
    """ Raised on the HTTP status code 500 """
    pass


class BadGatewayError(ServerError):
    """ Raised on the HTTP status code 502 """
    pass


class ServiceUnavailableError(ServerError):
    """ Raised on the HTTP status code 503 """
    pass


class GatewayTimeoutError(ServerError):
    """ Raised on the HTTP status code 504 """
    pass


class ErrorFactory():
    ERRORS = {
        400: BadRequestError,
        401: UnauthorizedError,
        402: RequestDeclinedError,
        403: ForbiddenError,
        404: NotFoundError,
        406: NotAcceptableError,
        409: ConflictError,
        415: UnsupportedMediaTypeError,
        422: UnprocessableEntityError,
        429: TooManyRequestsError,
        500: InternalServerError,
        502: BadGatewayError,
        503: ServiceUnavailableError,
        504: GatewayTimeoutError
    }

    def from_response(cls, response):
        code = response.status_code
        klass = cls.ERRORS.get(code, SynapsePayError)
        body = response.json()
        message, error_code = cls.parse_error(body)
        return klass(message=message, code=error_code, response=response)

    def parse_error(body):
        if type(body) is dict and type(body['error']) is dict:
            return [body['error']['en'], body['error_code']]
        else:
            return ['', None]