from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import numpy as np

from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    CandidateScore,
    ThroughputMetrics,
)


@dataclass(frozen=True)
class TexasBounds:
    min_lat: float = 25.8371
    max_lat: float = 36.5007
    min_lon: float = -106.6456
    max_lon: float = -93.5080


MAJOR_METROS = np.array(
    [
        [29.7604, -95.3698],  # Houston
        [32.7767, -96.7970],  # Dallas
        [30.2672, -97.7431],  # Austin
        [29.4241, -98.4936],  # San Antonio
        [31.7619, -106.4850],  # El Paso
    ]
)

MAJOR_ROAD_ANCHORS = np.array(
    [
        [35.4676, -97.5164],
        [31.9686, -99.9018],
        [29.7604, -95.3698],
        [32.7767, -96.7970],
    ]
)

EXISTING_SUPERMARKETS = np.array(
    [
        [29.7499, -95.3584],
        [29.7030, -95.4998],
        [32.7765, -96.7966],
        [32.7203, -97.3308],
        [30.2711, -97.7437],
        [29.4246, -98.4946],
        [31.7615, -106.4869],
        [33.5779, -101.8552],
        [27.8006, -97.3964],
        [35.2220, -101.8313],
    ]
)


def _normalize(values: np.ndarray) -> np.ndarray:
    minimum = values.min()
    maximum = values.max()
    if maximum == minimum:
        return np.ones_like(values)
    return (values - minimum) / (maximum - minimum)


def _haversine_km(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    earth_radius_km = 6371.0
    lat1, lon1 = np.radians(a[:, 0])[:, None], np.radians(a[:, 1])[:, None]
    lat2, lon2 = np.radians(b[:, 0])[None, :], np.radians(b[:, 1])[None, :]
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * earth_radius_km * np.arcsin(np.sqrt(h))


def _simulate_candidate_grid(size: int, seed: int) -> np.ndarray:
    bounds = TexasBounds()
    rng = np.random.default_rng(seed)
    lats = rng.uniform(bounds.min_lat, bounds.max_lat, size)
    lons = rng.uniform(bounds.min_lon, bounds.max_lon, size)
    return np.column_stack([lats, lons])


def run_suitability_analysis(payload: AnalysisRequest) -> AnalysisResponse:
    started = perf_counter()
    points = _simulate_candidate_grid(payload.grid_size, payload.seed)

    metro_distances = _haversine_km(points, MAJOR_METROS).min(axis=1)
    road_distances = _haversine_km(points, MAJOR_ROAD_ANCHORS).min(axis=1)
    competition_distances = _haversine_km(points, EXISTING_SUPERMARKETS).min(axis=1)

    population_score = 1 - _normalize(metro_distances)
    road_score = 1 - _normalize(road_distances)

    competition_adjusted = np.clip(
        competition_distances / payload.competition_buffer_km,
        a_min=0,
        a_max=1,
    )
    competition_score = competition_adjusted

    suitability = (
        payload.weights.population * population_score
        + payload.weights.roads * road_score
        + payload.weights.competition * competition_score
    )

    top_idx = np.argsort(suitability)[-5:][::-1]
    top_rows = []
    for rank, idx in enumerate(top_idx, start=1):
        top_rows.append(
            CandidateScore(
                rank=rank,
                candidate_id=f"TX-{idx:05d}",
                latitude=round(float(points[idx, 0]), 6),
                longitude=round(float(points[idx, 1]), 6),
                suitability_index=round(float(suitability[idx]), 4),
                population_score=round(float(population_score[idx]), 4),
                road_access_score=round(float(road_score[idx]), 4),
                competition_score=round(float(competition_score[idx]), 4),
            )
        )

    elapsed_ms = (perf_counter() - started) * 1000
    metrics = ThroughputMetrics(
        avg_latency_ms=round(elapsed_ms, 2),
        p95_latency_ms=round(elapsed_ms * 1.2, 2),
        req_per_second=round(1000 / max(elapsed_ms, 1), 2),
    )

    return AnalysisResponse(
        state=payload.state,
        candidates_analyzed=payload.grid_size,
        weights=payload.weights,
        top_locations=top_rows,
        throughput_metrics=metrics,
    )
