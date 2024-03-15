# QGIS Workflow: Best Location for a New Supermarket in Texas

This guide walks through a **business-ready site suitability analysis** in QGIS to identify the best locations for a new supermarket in Texas.

---

## 1) Dataset acquisition

### A. Population density (demand proxy)
- **What to get:** Census tract boundaries + population attributes to calculate people per square mile/km.
- **Recommended source:** U.S. Census TIGER/Line (geometry) + ACS population tables (attributes).
  - TIGER/Line landing page: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
  - Texas tract catalog example: https://catalog.data.gov/dataset/tiger-line-shapefile-current-state-texas-census-tract
  - ACS access: https://data.census.gov/
- **Why it matters (business):** Higher nearby population generally means more potential footfall and basket volume.

### B. Existing supermarket locations (competition proxy)
- **What to get:** Point locations of existing supermarkets/grocery stores in Texas.
- **Recommended source:** OpenStreetMap via Overpass Turbo (export as GeoJSON).
  - Overpass Turbo: https://overpass-turbo.eu/
  - Example query (Texas-wide groceries/supermarkets):

```overpass
[out:json][timeout:180];
area["ISO3166-2"="US-TX"][admin_level=4]->.tx;
(
  node["shop"="supermarket"](area.tx);
  way["shop"="supermarket"](area.tx);
  relation["shop"="supermarket"](area.tx);
  node["shop"="grocery"](area.tx);
  way["shop"="grocery"](area.tx);
  relation["shop"="grocery"](area.tx);
);
out center;
```

- **Why it matters (business):** Dense competitor zones can reduce expected market share, especially for standard-format supermarkets.

### C. Road network (accessibility proxy)
- **What to get:** Major roads/highways for access scoring.
- **Recommended source options:**
  1. Texas DOT data/maps hub: https://www.txdot.gov/data-maps.html
  2. TIGER roads (if you need a consistent federal source): https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- **Why it matters (business):** Better road accessibility often improves customer reach, supply logistics, and repeat visits.

---

## 2) QGIS analysis workflow

> Suggested QGIS plugins/tools: **Processing Toolbox**, **Field Calculator**, **Join attributes by location**, **Raster Calculator**.

### Step 2.1 — Prepare data (clean + align)
1. Load all layers in QGIS.
2. Reproject to a Texas-appropriate projected CRS for distance-based work (for example, a state plane or Albers equal area projection used by your org).
3. Clip all layers to your study extent (statewide Texas or selected metro regions).
4. Fix invalid geometries where needed.

**GIS concept: CRS (Coordinate Reference System)**  
CRS defines how geographic coordinates map to a flat surface. Distance and area calculations are unreliable in unprojected lat/long (EPSG:4326), so use a projected CRS before buffering or measuring distance.

### Step 2.2 — Buffer existing supermarkets (avoid competition zones)
1. Run **Buffer** on supermarket points.
2. Create one or multiple competition buffers (e.g., 2 km and 5 km).
3. Convert to a competition score layer:
   - Inside strong-competition buffer → lower suitability.
   - Outside buffer → higher suitability.

**GIS concept: Buffer**  
A buffer is a zone at a fixed distance around features. Here, it represents likely trade-area overlap and competitive pressure.

### Step 2.3 — Distance to major roads
1. Filter/select major roads only (e.g., interstates, U.S. highways, major arterials).
2. Use **Proximity (raster distance)** or **Distance to nearest hub**:
   - For continuous suitability surface, raster distance is preferred.
3. Create a road-access score where closer (but not directly on highway median) is better.

**GIS concept: Euclidean distance surface**  
A raster where each cell stores distance to the nearest target feature (major road). It is a common accessibility proxy.

### Step 2.4 — Population density surface
1. Join ACS population values to tract polygons (using GEOID).
2. Calculate density field:
   - `pop_density = total_population / tract_area`
3. Rasterize tract density to the same cell size as other rasters.

**GIS concept: Choropleth vs analysis raster**  
Population is often polygon-based, but weighted overlay is cleaner when all factors are converted to aligned rasters (same extent, resolution, CRS).

### Step 2.5 — Normalize all criteria to a 0–1 score
Normalize each criterion so scores are comparable.

- **Benefit criterion** (higher is better, e.g., population density):
  - `norm = (x - min) / (max - min)`
- **Cost criterion** (lower is better, e.g., competition intensity or too-far road distance):
  - `norm = (max - x) / (max - min)`

Optional: cap outliers before normalization using percentile clipping (e.g., 5th–95th) to reduce skew.

**GIS concept: Normalization**  
Converts different units (people/km², meters, buffer classes) to a common scale so they can be combined fairly.

### Step 2.6 — Weighted overlay (Suitability Index)
Use Raster Calculator:

```text
Suitability = w_pop * PopNorm + w_road * RoadNorm + w_comp * CompNorm
```

Example business weights:
- `w_pop = 0.50` (demand)
- `w_road = 0.30` (access)
- `w_comp = 0.20` (competition avoidance)
- Constraint: `w_pop + w_road + w_comp = 1.0`

**GIS concept: Weighted linear combination**  
A multi-criteria decision analysis (MCDA) approach where each factor contributes based on business priority.

---

## 3) Generate the final suitability map

1. Style the Suitability raster with a 5-class ramp (Very Low → Very High).
2. Optionally mask out non-developable zones (water bodies, protected land, zoning exclusions).
3. Validate visually against known high-demand corridors.

**Business interpretation:** High suitability cells represent the best balance of demand potential, accessibility, and manageable competitive pressure.

---

## 4) Highlight top 5 best locations

### Method A (raster to points)
1. Use **Raster layer statistics** to find high-value threshold (e.g., top 1% cells).
2. Convert top cells to polygons/points.
3. Run **Minimum distance** rules to avoid clustered picks (e.g., >= 10 km apart).
4. Sort by suitability score and keep top 5.

### Method B (candidate parcels/centroids)
If you have candidate parcels or block-group centroids:
1. Sample suitability raster values at candidate points.
2. Rank descending.
3. Exclude points inside hard constraints.
4. Keep top 5.

**Recommended attributes for top-5 table:**
- Rank
- Latitude/Longitude
- Suitability score
- Distance to nearest major road
- Distance to nearest competitor supermarket
- Nearby population density

---

## 5) Create a professional map layout (QGIS Layout Manager)

Include:
- Clear title: *Texas Supermarket Site Suitability Analysis (Year)*
- Legend (with intuitive classes)
- Scale bar and north arrow
- Source credits (Census, OSM, TxDOT)
- Inset map (Texas context + zoom area)
- Top-5 location callouts with rank labels
- Analyst/date/version note

Cartography tips:
- Use muted basemap colors; keep suitability layer visually dominant.
- Use colorblind-friendly ramps.
- Avoid overly saturated reds/greens for executive audiences.

---

## Why each factor matters for business decisions

1. **Population density (Demand):** Supports sales volume and faster payback period.
2. **Distance to major roads (Access):** Reduces travel friction for customers and last-mile delivery complexity.
3. **Distance from existing supermarkets (Competition):** Helps identify underserved markets and protect margins.
4. **Weighted overlay (Strategy alignment):** Lets leadership explicitly encode strategy (growth-first, margin-first, convenience-first) into site ranking.

---

## Suggested sensitivity test (important)

Run 3 scenarios and compare how top-5 changes:
- **Demand-led:** 0.6 pop / 0.25 road / 0.15 competition
- **Balanced:** 0.5 / 0.3 / 0.2
- **Competition-averse:** 0.4 / 0.25 / 0.35

If the same locations remain top-ranked across scenarios, your decision is more robust.

---

## Deliverables checklist

- [ ] Cleaned and projected input layers
- [ ] Competition buffer map
- [ ] Road distance raster
- [ ] Normalized factor rasters (0–1)
- [ ] Final suitability index raster
- [ ] Top-5 candidate points + attribute table
- [ ] Executive-ready layout PDF

