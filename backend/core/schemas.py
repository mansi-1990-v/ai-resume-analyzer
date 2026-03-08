from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ExtractedEntity(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    links: List[str] = Field(default_factory=list)

class Education(BaseModel):
    degree: str
    institution: Optional[str] = None
    year: Optional[str] = None

class Experience(BaseModel):
    role: str
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class SkillExtractorResult(BaseModel):
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)

class FullResumeData(BaseModel):
    personal_info: ExtractedEntity
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: SkillExtractorResult
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    raw_text: str = ""

class JobDescriptionInput(BaseModel):
    text: str

class ScoreBreakdown(BaseModel):
    skills_match: float
    experience_match: float
    education_match: float

class JobFitResult(BaseModel):
    overall_score: float
    breakdown: ScoreBreakdown
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str
    evidences: List[str] = Field(default_factory=list)

class QualityScoreResult(BaseModel):
    overall_score: float
    clarity_score: float
    impact_score: float
    suggestions: List[str]

class RolePrediction(BaseModel):
    role: str
    confidence: float

class ResumeAnalysisResponse(BaseModel):
    resume_data: FullResumeData
    quality_evaluation: QualityScoreResult
    predicted_roles: List[RolePrediction]
    recommendations: List[str]
