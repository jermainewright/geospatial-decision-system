export type AnalysisWeights = {
  population: number;
  roads: number;
  competition: number;
};

export type Candidate = {
  rank: number;
  candidate_id: string;
  latitude: number;
  longitude: number;
  suitability_index: number;
  population_score: number;
  road_access_score: number;
  competition_score: number;
};

export type AnalysisResponse = {
  state: string;
  candidates_analyzed: number;
  weights: AnalysisWeights;
  top_locations: Candidate[];
  throughput_metrics: {
    avg_latency_ms: number;
    p95_latency_ms: number;
    req_per_second: number;
  };
};
