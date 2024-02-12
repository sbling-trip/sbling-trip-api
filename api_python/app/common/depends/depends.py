from fastapi import Depends

from api_python.app.user.service.user_service import get_user_seq_by_authorization, \
    get_user_seq_by_authorization_optional

user_seq_dependency = Depends(get_user_seq_by_authorization)
user_seq_dependency_optional = Depends(get_user_seq_by_authorization_optional)