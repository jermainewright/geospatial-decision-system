from pydantic import BaseModel, Field, model_validator


class AnalysisWeights(BaseModel):
    population: float = Field(ge=0.0, le=1.0)
    roads: float = Field(ge=0.0, le=1.0)
    competition: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_sum(self) -> "AnalysisWeights":
        total = self.population + self.roads + self.competition
        if abs(total - 1.0) > 1e-9:
            raise ValueError("Weights must sum to exactly 1.0")
        return self


class AnalysisRequest(BaseModel):
    state: str = Field(default="TX", min_length=2, max_length=2)
    grid_size: int = Field(default=1400, ge=100, le=20000)
    competition_buffer_km: float = Field(default=5.0, ge=0.5, le=50)
    seed: int = Field(default=42, ge=1, le=99999)
    weights: AnalysisWeights


class CandidateScore(BaseModel):
    rank: int
    candidate_id: str
    latitude: float
    longitude: float
    suitability_index: float
    population_score: float
    road_access_score: float
    competition_score: float


class ThroughputMetrics(BaseModel):
    avg_latency_ms: float
    p95_latency_ms: float
    req_per_second: float


class AnalysisResponse(BaseModel):
    state: str
    candidates_analyzed: int
    weights: AnalysisWeights
    top_locations: list[CandidateScore]
    throughput_metrics: ThroughputMetrics
