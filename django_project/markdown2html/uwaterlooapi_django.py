from uwaterlooapi import UWaterlooAPI
uw = UWaterlooAPI(api_key="a07ba3fa921ba4e468a0ed2ad0e0c062")
error = "Course Information Not Found"


def find_course(subject, number):
    subject = subject.upper()
    number = str(number)
    for course in uw.courses():
        if course['subject'] == subject:
            if course['catalog_number'] == number:
                return course['title']

    return error