import imp
from typing import Optional,Dict
from fastapi import HTTPException, Request,status
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlow as OAuthFlowsModel

class OAuth2AppBearer(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get(" Authorization")
        print(f"#### {request.headers}")
        # scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer","X_APP_TOKEN" : "","X_REFRESH_TOKEN":""},
                )
            else:
                return None
        return authorization
