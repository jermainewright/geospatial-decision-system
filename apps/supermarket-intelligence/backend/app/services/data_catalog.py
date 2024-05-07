from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetSource:
    name: str
    provider: str
    usage: str
    url: str


DATASETS = [
    DatasetSource(
        name="Population Density",
        provider="US Census (TIGER + ACS)",
        usage="Demand estimation by census tract or block group",
        url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
    ),
    DatasetSource(
        name="Existing Supermarkets",
        provider="OpenStreetMap Overpass",
        usage="Competition pressure and avoidance zones",
        url="https://overpass-turbo.eu/",
    ),
    DatasetSource(
        name="Road Network",
        provider="TxDOT / TIGER Roads",
        usage="Accessibility and logistics scoring",
        url="https://www.txdot.gov/data-maps.html",
    ),
]
