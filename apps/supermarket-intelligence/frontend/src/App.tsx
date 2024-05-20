import { useEffect, useState } from "react";
import { runAnalysis } from "./api/client";
import { TopLocationsTable } from "./components/TopLocationsTable";
import type { AnalysisResponse } from "./types";

function RollingObjects() {
  return (
    <div className="rolling-field" aria-hidden="true">
      <span className="roller roller-a" />
      <span className="roller roller-b" />
      <span className="roller roller-c" />
      <span className="roller roller-d" />
    </div>
  );
}

export default function App() {
  const [data, setData] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    runAnalysis()
      .then(setData)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <main className="loading">
        <RollingObjects />
        <div>
          <div className="pulse" />
          <div>Building suitability heat signal...</div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="error-box">
        <RollingObjects />
        <h2>Unable to render dashboard</h2>
        <p>{error}</p>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <RollingObjects />
      <section className="hero">
        <h1>Texas Supermarket Site Intelligence Dashboard</h1>
        <p className="subtitle">
          Multi-criteria geospatial ranking using demand density, road accessibility, and competition avoidance scoring.
        </p>

        <div className="metrics-grid">
          <article className="metric-card">
            <p className="metric-title">Candidates Evaluated</p>
            <p className="metric-value">{data?.candidates_analyzed}</p>
          </article>
          <article className="metric-card">
            <p className="metric-title">Average Latency</p>
            <p className="metric-value">{data?.throughput_metrics.avg_latency_ms} ms</p>
          </article>
          <article className="metric-card">
            <p className="metric-title">P95 Latency</p>
            <p className="metric-value">{data?.throughput_metrics.p95_latency_ms} ms</p>
          </article>
          <article className="metric-card">
            <p className="metric-title">Req/Sec</p>
            <p className="metric-value">{data?.throughput_metrics.req_per_second}</p>
          </article>
        </div>
      </section>

      <section className="panel">
        <h2>Top 5 Candidate Locations</h2>
        {data && <TopLocationsTable rows={data.top_locations} />}
      </section>
    </main>
  );
}
