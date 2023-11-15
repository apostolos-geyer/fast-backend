from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, detail: str, additional_detail: str = None):
        if additional_detail:
            detail = f"{detail}: {additional_detail}"
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundError(BaseAPIException):
    def __init__(self, additional_detail: str = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail="User not found",
                         additional_detail=additional_detail)


class UserCreationError(BaseAPIException):
    def __init__(self, additional_detail: str = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Could not create user",
                         additional_detail=additional_detail)

class UserUpdateError(BaseAPIException):
    def __init__(self, additional_detail: str = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Could not update user",
                         additional_detail=additional_detail)


class UserAuthorizationError(BaseAPIException):
    def __init__(self, additional_detail: str = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Not Authorized",
                         additional_detail=additional_detail)



