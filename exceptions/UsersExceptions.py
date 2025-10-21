class UserException(Exception):
    def __init__(self,message:str):
        self.message=message
        super().__init__(message)
    
class UserNotFoundException(UserException):
    def __init__(self,message:str|None=None):
        if message is None:
            message="User ot found exception"
        super().__init__(message)
        
class UserAlreadyExistException(UserException):
    def __init__(self,message:str|None=None):
        if message is None:
            message="User already exist"
        super().__init__(message)

class UserPasswordNotEquals(UserException):
    def __init__(self,message:str|None=None):
        if message is None:
            message="User password not equals"
        super().__init__(message)