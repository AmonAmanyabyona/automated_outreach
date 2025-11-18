#!/usr/bin/env python3
"""
Demo: Discover 50 cafés in Munich using OpenStreetMap's Overpass API
and save results into a CSV file.
"""

import csv
import overpy

OUTPUT_CSV = "munich_cafes.csv"
LIMIT = 50  # number of cafés to fetch


def fetch_munich_cafes(limit: int = LIMIT):
    """
    Query Overpass for cafés within Munich administrative boundary.
    Returns a list of dicts with core fields and available tags.
    """
    api = overpy.Overpass()

    query = f"""
    [out:json][timeout:25];
    area["name"="München"]["boundary"="administrative"]->.munich;
    node(area.munich)["amenity"="cafe"];
    out {limit};
    """

    result = api.query(query)

    cafes = []
    for node in result.nodes[:limit]:
        cafes.append(
            {
                "osm_id": node.id,
                "name": node.tags.get("name", "Unnamed"),
                "lat": node.lat,
                "lon": node.lon,
                "phone": node.tags.get("phone") or node.tags.get("contact:phone"),
                "website": node.tags.get("website") or node.tags.get("contact:website"),
                "addr_street": node.tags.get("addr:street"),
                "addr_housenumber": node.tags.get("addr:housenumber"),
                "addr_postcode": node.tags.get("addr:postcode"),
                "addr_city": node.tags.get("addr:city"),
            }
        )
    return cafes


def save_to_csv(rows, path=OUTPUT_CSV):
    """
    Save rows to CSV with a fixed column order.
    """
    fieldnames = [
        "osm_id",
        "name",
        "lat",
        "lon",
        "phone",
        "website",
        "addr_street",
        "addr_housenumber",
        "addr_postcode",
        "addr_city",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Wrote {len(rows)} cafés to CSV: {path}")


def main():
    cafes = fetch_munich_cafes(limit=LIMIT)
    if not cafes:
        print("No cafés fetched. Try increasing timeout or limit.")
        return
    save_to_csv(cafes, OUTPUT_CSV)


if __name__ == "__main__":
    main()
