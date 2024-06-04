import type { AnalysisResponse } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8081/api/v1";
const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

const demoData: AnalysisResponse = {
  state: "TX",
  candidates_analyzed: 1800,
  weights: { population: 0.5, roads: 0.3, competition: 0.2 },
  top_locations: [
    { rank: 1, candidate_id: "TX-00421", latitude: 30.228355, longitude: -97.71903, suitability_index: 0.93, population_score: 0.9, road_access_score: 0.88, competition_score: 0.96 },
    { rank: 2, candidate_id: "TX-01537", latitude: 29.80741, longitude: -95.41172, suitability_index: 0.91, population_score: 0.92, road_access_score: 0.85, competition_score: 0.89 },
    { rank: 3, candidate_id: "TX-00988", latitude: 32.92651, longitude: -96.73251, suitability_index: 0.89, population_score: 0.9, road_access_score: 0.84, competition_score: 0.86 },
    { rank: 4, candidate_id: "TX-01112", latitude: 29.51817, longitude: -98.43156, suitability_index: 0.88, population_score: 0.85, road_access_score: 0.87, competition_score: 0.88 },
    { rank: 5, candidate_id: "TX-01763", latitude: 27.80203, longitude: -97.40486, suitability_index: 0.86, population_score: 0.83, road_access_score: 0.81, competition_score: 0.9 },
  ],
  throughput_metrics: { avg_latency_ms: 34.8, p95_latency_ms: 41.1, req_per_second: 28.7 },
};

export async function runAnalysis(): Promise<AnalysisResponse> {
  if (DEMO_MODE) {
    return demoData;
  }

  const response = await fetch(`${API_URL}/analysis/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      state: "TX",
      grid_size: 1800,
      competition_buffer_km: 5,
      seed: 42,
      weights: {
        population: 0.5,
        roads: 0.3,
        competition: 0.2,
      },
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to run suitability analysis.");
  }

  return response.json();
}
