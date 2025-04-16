class UserAlreadyRegisteredException(Exception):
    status_code = 401
    detail = "User already registered"


class UserNotFoundException(Exception):
    status_code = 404
    detail = "User not found"


class UserIncorrectLoginOrPasswordException(Exception):
    status_code = 401
    detail = "Incorrect login or password"


class UserBlockedException(Exception):
    status_code = 403
    detail = "User blocked"


class UserIncorrectLenPasswordException(Exception):
    status_code = 401
    detail = "Incorrect len password"


class UserNotCapitalLetterException(Exception):
    status_code = 401
    detail = "Not capital letter"


class UserNotSmallLetterException(Exception):
    status_code = 401
    detail = "Not small letter"


class UserNotDigitException(Exception):
    status_code = 401
    detail = "Not digit"
