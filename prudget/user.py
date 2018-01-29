from prudget import middleware


def current():
    return middleware.get_current_user()
