"""Pydantic models defining the structured output schema."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    phone_number: Optional[str] = Field(
        default=None, description="Primary phone number for sales or inquiries"
    )
    support_email: Optional[str] = Field(
        default=None, description="Official support or contact email"
    )
    address: Optional[str] = Field(
        default=None, description="Mailing address or headquarters address"
    )


class SocialProfile(BaseModel):
    platform: str = Field(description="Social network or community name")
    url: str = Field(description="Full https URL to the profile")


class ProductSnapshot(BaseModel):
    product_name: Optional[str] = Field(default=None)
    company_name: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    overview: Optional[str] = Field(
        default=None,
        description="Two to three paragraph summary capturing the product purpose",
    )
    elevator_pitch: Optional[str] = Field(
        default=None,
        description="500-700 word overview as specified in source instructions",
    )
    competitive_advantage: Optional[str] = Field(
        default=None,
        description="Summary of differentiators versus competitors",
    )
    product_description_short: Optional[str] = Field(
        default=None,
        description="One to two sentence description",
    )
    founding_year: Optional[int] = Field(default=None)
    hq_location: Optional[str] = Field(default=None)
    industry: List[str] = Field(default_factory=list)
    parent_category: Optional[str] = Field(default=None)
    sub_category: Optional[str] = Field(default=None)
    contact: ContactInfo = Field(default_factory=ContactInfo)
    social_links: List[SocialProfile] = Field(default_factory=list)