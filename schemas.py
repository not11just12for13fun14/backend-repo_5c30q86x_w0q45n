"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Digital marketing portfolio schemas

class PortfolioProject(BaseModel):
    """
    Portfolio projects you want to showcase
    Collection name: "portfolioproject"
    """
    title: str = Field(..., description="Project name")
    client: Optional[str] = Field(None, description="Client or brand")
    summary: str = Field(..., description="Short overview of the work and outcome")
    services: List[str] = Field(default_factory=list, description="Services provided")
    cover_url: Optional[HttpUrl] = Field(None, description="Image or video cover URL")
    case_study_url: Optional[HttpUrl] = Field(None, description="Detailed case study link")
    metrics: Optional[dict] = Field(
        default=None,
        description="Key results, e.g., {'impressions': 1_000_000, 'ctr': 4.2}"
    )

class ContactMessage(BaseModel):
    """
    Leads from the contact form
    Collection name: "contactmessage"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    company: Optional[str] = None
    message: str = Field(..., min_length=10, max_length=2000)
    budget: Optional[str] = Field(None, description="Budget range text")
    services: Optional[List[str]] = Field(default=None, description="Requested services")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
