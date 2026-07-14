
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    DIRECTOR = "director"
    QAHEAD = "qahead"
    DEAN = "dean"
    QAOFFICER = 'qaofficer'
    VICEDEAN = "vicedean"
    CHAIRHOLDER = 'chairholder'
    COURSECHAIR = "coursechair"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    STAFF = "staff"
    USER = "user"


ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        "user.create",
        "user.delete",
        "course.create",
        "course.delete",
    },

    UserRole.STAFF: {
        "course.create",
        "course.update",
    },

    UserRole.STUDENT: {
        "course.view",
    }
}