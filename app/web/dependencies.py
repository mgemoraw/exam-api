"""Frontend-specific dependencies - Simplified"""
from typing import Optional, Dict, Any
from fastapi import Request
from datetime import datetime

class FrontendContext:
    """Manages frontend context data"""
    
    def __init__(self, request: Request):
        self.request = request
    
    async def get_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        token = self.request.cookies.get("auth_token")
        if token:
            # Fetch user from database/service
            return {"id": 1, "name": "John Doe", "email": "john@example.com"}
        return None
    
    async def get_template_context(self) -> Dict[str, Any]:
        """Get all template context variables"""
        user = await self.get_user()
        return {
            "request": self.request,
            "user": user,
            "current_year": datetime.now().year,
            "environment": "production",
            "version": "1.0.0"
        }

# Simple factory function
async def create_template_context(request: Request) -> Dict[str, Any]:
    """Create template context for a request"""
    context = FrontendContext(request)
    return await context.get_template_context()