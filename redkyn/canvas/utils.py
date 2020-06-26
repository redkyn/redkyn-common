from redkyn.canvas import CanvasAPI
from typing import List, Dict, Tuple, Any
from redkyn.canvas.exceptions import AssignmentNotFound
import logging
import re

logger = logging.getLogger(__name__)


def lookup_canvas_ids(
    courses: List[Dict[str, Any]], canvas: CanvasAPI, hw_name: str
) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Gets the Canvas internal course IDs for all sections of a course (if different sections have their
    own course IDs), in addition to the assignment IDs for a given assignment, within each course
    :param courses: the data containing course IDs and their sections
    :param canvas: an API object
    :param hw_name: the name of the assignment to obtain IDs for
    :return: the list of course ids keyed by the section name, and the list
    of assignment ids corresponding to each section as a dict keyed on the section
    """
    section_ids = {course["section"]: course["id"] for course in courses}
    min_name = re.search("[A-Za-z]+\d+", hw_name).group(0)
    assignment_ids = {}
    for section, course_id in section_ids.items():
        try:
            canvas_assignments = canvas.get_course_assignments(course_id, min_name)
        except Exception as e:
            print(e, type(e))
            logger.error("Failed to pull assignment list from Canvas")
            raise AssignmentNotFound
        if len(canvas_assignments) != 1:
            logger.error(
                "Could not uniquely identify Canvas assignment from name %s and section %s",
                min_name,
                section,
            )
            raise AssignmentNotFound
        assignment_ids[section] = canvas_assignments[0]["id"]
    return (section_ids, assignment_ids)
