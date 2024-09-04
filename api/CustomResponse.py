from rest_framework.response import Response

from rest_framework import status

class CustomResponse(Response):
    def __init__(self,data=None,messages="success",status_code=status.HTTP_200_OK,errors=None,**kwargs):
        
        response_data = {
            "status":"success" if status.is_success(status_code) else "error",
            "message":messages,
            "data":data,
            "errors":errors,
        }
        super().__init__(data=response_data,status=status_code,**kwargs)