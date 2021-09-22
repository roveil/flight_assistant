from typing import Optional, Any, Dict, Type

from fastapi.exceptions import HTTPException

from core.models_base import Base


class ObjectAlreadyExists(HTTPException):
    status_code = 400

    def __init__(self, model_instance: Base, headers: Optional[Dict[str, Any]] = None):
        detail = f"{model_instance.__class__.__name__} already exists"
        super().__init__(self.status_code, detail=detail, headers=headers)


class ObjectDoesNotExists(HTTPException):
    status_code = 404

    def __init__(self, model: Type[Base], key: int, headers: Optional[Dict[str, Any]] = None):
        detail = f"{model.__name__} with key '{key}' does not exists"
        super().__init__(self.status_code, detail=detail, headers=headers)
