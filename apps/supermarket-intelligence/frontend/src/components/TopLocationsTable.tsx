import type { Candidate } from "../types";

type Props = {
  rows: Candidate[];
};

function formatPercent(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function TopLocationsTable({ rows }: Props) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Candidate</th>
            <th>Coordinates</th>
            <th>Suitability</th>
            <th>Population</th>
            <th>Road</th>
            <th>Competition</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.candidate_id}>
              <td>
                <span className="rank-pill">{row.rank}</span>
              </td>
              <td>{row.candidate_id}</td>
              <td>
                {row.latitude}, {row.longitude}
              </td>
              <td>
                <div className="score-bar">
                  <span style={{ width: `${row.suitability_index * 100}%` }} />
                </div>
                {formatPercent(row.suitability_index)}
              </td>
              <td>{formatPercent(row.population_score)}</td>
              <td>{formatPercent(row.road_access_score)}</td>
              <td>{formatPercent(row.competition_score)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
