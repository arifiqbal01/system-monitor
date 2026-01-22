from .model import WebsiteFailureTypes

class WebsiteError(Exception):
    failure_type = WebsiteFailureTypes.UNKNOWN
class DnsError(WebsiteError):
    failure_type = WebsiteFailureTypes.DNS
class NetworkError(WebsiteError):
    failure_type = WebsiteFailureTypes.NETWORK
class TimeoutError(WebsiteError):
    failure_type = WebsiteFailureTypes.TIMEOUT
class HttpError(WebsiteError):
    failure_type = WebsiteFailureTypes.HTTP
    def __int__(self, http_code: int):
        self.http_code = http_code
        super().__init__(f"HTTP error {status_code}")

class SemanticError(WebsiteError):
    failure_type = WebsiteFailureTypes.SEMANTIC
class InvalidUrlError(WebsiteError):
    failure_type = WebsiteFailureTypes.INVALID_URL