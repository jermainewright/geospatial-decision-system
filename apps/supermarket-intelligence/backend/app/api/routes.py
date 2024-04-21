from fastapi import APIRouter

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.services.data_catalog import DATASETS
from app.services.suitability import run_suitability_analysis

router = APIRouter(prefix="/api/v1", tags=["site-selection"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/datasets")
def datasets() -> list[dict[str, str]]:
    return [d.__dict__ for d in DATASETS]


@router.post("/analysis/run", response_model=AnalysisResponse)
def run_analysis(payload: AnalysisRequest) -> AnalysisResponse:
    return run_suitability_analysis(payload)
