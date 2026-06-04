"""Frontend routes for Avery Production - Simplified"""
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Request, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional

# Get the directory
FRONTEND_DIR = Path(__file__).parent

# Setup templates
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Add custom filters
def now(format_str: str = "%Y") -> str:
    return datetime.now().strftime(format_str)

templates.env.filters["now"] = now

# Create router
router = APIRouter(prefix="", tags=["frontend"])

# Import the simplified context creator
from .dependencies import create_template_context

# Helper function to render templates
async def render(request: Request, template_name: str, extra_context: dict = None):
    """Simple template rendering helper"""
    # Get base context
    context = await create_template_context(request)
    
    # Add extra context if provided
    if extra_context:
        context.update(extra_context)
    
    return templates.TemplateResponse(template_name, context)

@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    return await render(request, "home.html")

@router.get("/about", response_class=HTMLResponse, name="about")
async def about(request: Request):
    return await render(request, "about.html", {"page_title": "About Us"})

@router.get("/contact", response_class=HTMLResponse, name="contact")
async def contact(request: Request):
    return await render(request, "contact.html", {"page_title": "Contact Us"})

@router.post("/subscribe", name="subscribe")
async def subscribe(request: Request):
    """AJAX endpoint for newsletter subscription"""
    try:
        body = await request.json()
        email = body.get("email")
        
        if not email:
            return {"success": False, "message": "Email is required"}
        
        # TODO: Save to database
        print(f"New subscription: {email}")
        
        return {"success": True, "message": "Successfully subscribed!"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "frontend"}

def setup_frontend(app: FastAPI, mount_path: str = "/", enable_static: bool = True):
    """Setup and mount the frontend to a FastAPI application"""
    # Include the router
    app.include_router(router, prefix=mount_path)
    
    # Mount static files
    if enable_static:
        static_dir = FRONTEND_DIR / "static"
        if static_dir.exists():
            static_path = f"{mount_path}/static" if mount_path else "/static"
            app.mount(static_path, StaticFiles(directory=str(static_dir)), name="static")
            print(f"✅ Static files mounted at: {static_path}")
    
    print(f"✅ Frontend mounted at: {mount_path or '/'}")
    return router

def mount_static_files(app: FastAPI, mount_path: str = ""):
    """Mount static files (legacy function for compatibility)"""
    static_dir = FRONTEND_DIR / "static"
    if static_dir.exists():
        static_path = f"{mount_path}/static" if mount_path else "/static"
        app.mount(static_path, StaticFiles(directory=str(static_dir)), name="static")
        print(f"✅ Static files mounted at: {static_path}")
    return router