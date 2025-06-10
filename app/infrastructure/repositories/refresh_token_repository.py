from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        """Create a new refresh token for a user"""
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
        
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        
        return refresh_token
    
    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get a refresh token by its value"""
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
    
    def revoke(self, token: str) -> bool:
        """Revoke a refresh token"""
        refresh_token = self.get_by_token(token)
        
        if not refresh_token:
            return False
        
        refresh_token.revoked = True
        self.db.commit()
        
        return True
