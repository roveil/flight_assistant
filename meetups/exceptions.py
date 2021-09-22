from typing import Optional, Any, Dict

from fastapi.exceptions import HTTPException


class BoardingPassAlreadyUsed(HTTPException):
    status_code = 400

    def __init__(self, invitation_code: int, headers: Optional[Dict[str, Any]] = None):
        detail = f"Boarding pass with invitation code '{invitation_code}' already used"
        super().__init__(self.status_code, detail=detail, headers=headers)
