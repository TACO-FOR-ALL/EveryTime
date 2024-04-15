class ResponseContent(object):
    """
        Developer: 박찬빈
        기능: 모든 View Function의 Return을 표준화하기 위한 Class
    """
    @staticmethod
    def success(data=None,
                data_field_name: str="data",
                status_code: int=0):
        if data:
            result = {
                "status": status_code,
                data_field_name: data
            }
        else:
            result = {
                "status", status_code
            }
        return result
    @staticmethod
    def fail(error_msg: str="",
             status_code: int=1):
        return {
            "status": status_code,
            "error_msg": error_msg
        }