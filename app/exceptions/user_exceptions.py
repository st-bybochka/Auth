class UserAlreadyRegisteredException(Exception):
    detail = "User already registered"


class UserNotFoundException(Exception):
    detail = "User not found"


class UserIncorrectLoginOrPasswordException(Exception):
    detail = "Incorrect login or password"
