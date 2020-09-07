from redkyn.exceptions import RedkynError
from requests.exceptions import HTTPError


def raiseAuthenticationFailed(err: HTTPError):
    if err.response.status_code != 401:
        return

    raise AuthenticationFailed(err)


class AuthenticationFailed(RedkynError):
    pass


def raiseCourseNotFound(err: HTTPError):
    if err.response.status_code != 404:
        return

    raise CourseNotFound(err)


def raiseStudentNotFound(err: HTTPError):
    if err.response.status_code != 404:
        return

    raise StudentNotFound(err)


class CourseNotFound(RedkynError):
    pass


class AssignmentNotFound(RedkynError):
    pass


class StudentNotFound(RedkynError):
    pass


def raiseNameResolutionFailed(err: HTTPError):
    if err.response is not None:
        return

    if err.request is not None:
        return

    if "Name or service not known" not in str(err):
        return

    raise NameResolutionFailed(err)


class NameResolutionFailed(RedkynError):
    pass
