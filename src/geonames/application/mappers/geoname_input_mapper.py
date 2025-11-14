from src.geonames.domain.geoname import GeoName


class GeoNameInputMapper:
    
    @staticmethod
    def from_dict(row: dict) -> GeoName:

        return GeoName(
            geoname_id=int(row["geoname_id"]),
            name=row["name"],
            asciiname=row["asciiname"],
            alternatenames=row["alternatenames"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            feature_class=row["feature_class"],
            feature_code=row["feature_code"],
            country_code=row["country_code"],
            cc2=row.get("cc2", ""),
            admin1_code=row["admin1_code"],
            admin2_code=row["admin2_code"],
            admin3_code=row.get("admin3_code", ""),
            admin4_code=row.get("admin4_code", ""),
            population=int(row["population"]) if row["population"] else 0,
            elevation=int(row["elevation"]) if row["elevation"] else None,
            dem=int(row["dem"]) if row["dem"] else None,
            timezone=row["timezone"],
            modification_date=row["modification_date"],
        )
