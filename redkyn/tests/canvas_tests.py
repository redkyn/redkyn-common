from redkyn.tests.utils import TestCase

from redkyn.canvas import CanvasAPI
from redkyn.canvas.exceptions import AuthenticationFailed, CourseNotFound, NameResolutionFailed

from requests.exceptions import HTTPError

class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class CanvasTestCase(TestCase):
    def setUp(self):
        self.mock_requests = self._create_patch("redkyn.canvas.requests", autospec=True)
        self.mock_get = self._create_patch("redkyn.canvas.requests.get")

    def test_urls_are_https(self):
        api = CanvasAPI("test token", "mst.instructure.com")
        self.assertEqual("https://mst.instructure.com", api.website_root)

    def test_http_urls_are_httpsified(self):
        api = CanvasAPI("test token", "http://mst.instructure.com")
        self.assertEqual("https://mst.instructure.com", api.website_root)

    def test_courses_auth_failure(self):
        self.mock_get.side_effect = HTTPError(response=FakeResponse(401))

        api = CanvasAPI("test token", "mst.instructure.com")
        with self.assertRaises(AuthenticationFailed):
            api.get_instructor_courses()

    def test_students_auth_failure(self):
        self.mock_get.side_effect = HTTPError(response=FakeResponse(401))

        api = CanvasAPI("test token", "mst.instructure.com")
        with self.assertRaises(AuthenticationFailed):
            api.get_course_students(420)

    def test_course_not_found(self):
        self.mock_get.side_effect = HTTPError(response=FakeResponse(404))

        api = CanvasAPI("test token", "mst.instructure.com")
        with self.assertRaises(CourseNotFound):
            api.get_course_students(420)

    def test_failed_dns(self):
        self.mock_get.side_effect = HTTPError("Name or service not known")

        api = CanvasAPI("test token", "mst.instructure.com")

        with self.assertRaises(NameResolutionFailed):
            api.get_instructor_courses()

        with self.assertRaises(NameResolutionFailed):
            api.get_course_students(420)

    def test_retries_on_5xx(self):
        self.mock_get.side_effect = HTTPError(response=FakeResponse(503))

        api = CanvasAPI("test token", "mst.instructure.com")
        with self.assertRaises(HTTPError):
            api.get_instructor_courses()

        self.assertEqual(5, self.mock_get.call_count)
