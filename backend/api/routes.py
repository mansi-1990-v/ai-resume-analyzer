from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import tempfile
import asyncio


from backend.core.schemas import (
    ResumeAnalysisResponse, JobFitResult, FullResumeData, 
    SkillExtractorResult, QualityScoreResult, ScoreBreakdown
)
from backend.core.parsers.factory import get_parser
from backend.core.extractor.entities import EntityExtractor
from backend.core.nlp.skill_graph import SemanticSkillGraph
from backend.core.models.role_predictor import RolePredictor
from backend.core.ats.simulator import ATSSimulator
from backend.core.scoring.job_matcher import JobMatcher
from backend.core.xai.explainer import ExplainableAIEngine

router = APIRouter(prefix="/api/v1", tags=["analyzer"])

# Initialize singletons for performance
entity_extractor = EntityExtractor()
skill_graph = SemanticSkillGraph()
role_predictor = RolePredictor()
ats_simulator = ATSSimulator()
job_matcher = JobMatcher()
xai_engine = ExplainableAIEngine()

@router.post("/analyze/resume", response_model=ResumeAnalysisResponse)
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to upload and analyze a resume file (PDF, DOCX, TXT).
    Returns structured data, predicted roles, and quality evaluation.
    """
    allowed_types = [
        "application/pdf", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
        "text/plain"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and TXT are supported.")
    
    # Save file temporarily to parse
    _, ext = os.path.splitext(file.filename)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=ext)
    try:
        with os.fdopen(tmp_fd, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        
        # 1. Parsing
        parser = get_parser(tmp_path)
        raw_text = await asyncio.to_thread(parser.parse, tmp_path)
        
        # 2. Entity Extraction
        entities = await asyncio.to_thread(entity_extractor.extract_all, raw_text)
        
        # 3. Simple Tokenization for skills
        import re
        tokens = re.findall(r'\b[a-zA-Z\.+#-]{2,}\b', raw_text)
        skills_dict = await asyncio.to_thread(skill_graph.extract_and_normalize, tokens)
        
        # 4. Role Prediction
        roles = await asyncio.to_thread(role_predictor.predict, raw_text)
        
        # 5. ATS Simulation
        ats_eval = await asyncio.to_thread(ats_simulator.evaluate, raw_text)
        
        resume_data = FullResumeData(
            personal_info=entities,
            skills=SkillExtractorResult(**skills_dict),
            raw_text=raw_text
        )
        
        quality = QualityScoreResult(
            overall_score=ats_eval["ats_score"],
            clarity_score=ats_eval["ats_score"] * 0.9, # Mocked metric
            impact_score=ats_eval["ats_score"] * 0.85, # Mocked metric
            suggestions=ats_eval["suggestions"]
        )
        
        return ResumeAnalysisResponse(
            resume_data=resume_data,
            quality_evaluation=quality,
            predicted_roles=roles,
            recommendations=["Consider adding a GitHub portfolio link." if not entities.get("links") else "Your links look good."]
        )
    finally:
        os.remove(tmp_path)

@router.post("/analyze/job-fit", response_model=JobFitResult)
async def analyze_job_fit_endpoint(resume_text: str = Form(...), job_description: str = Form(...)):
    """
    Endpoint to compare parsed resume text against a Job Description.
    Returns cosine similarity scores and detailed breakdown.
    """
    import re
    tokens = re.findall(r'\b[a-zA-Z\.+#-]{2,}\b', resume_text)
    
    # Extract candidate skills
    candidate_skills = []
    res = await asyncio.to_thread(skill_graph.extract_and_normalize, tokens)
    candidate_skills.extend(res["technical_skills"])
    candidate_skills.extend(res["soft_skills"])
    candidate_skills.extend(res["tools"])
    
    fit_result = await asyncio.to_thread(job_matcher.evaluate_fit, resume_text, job_description, candidate_skills)
    
    # Generate XAI text
    candidate_skills_with_missing_approx = candidate_skills + fit_result.missing_skills
    explanation = await asyncio.to_thread(
        xai_engine.generate_explanation,
        candidate_skills_with_missing_approx, # approximation of JD
        candidate_skills,
        fit_result.breakdown,
        fit_result.evidences
    )
    fit_result.explanation = explanation
    
    return fit_result
