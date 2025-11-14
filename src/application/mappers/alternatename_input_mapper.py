from domain.alternatename import AlternateName


class AlternateNameInputMapper:

    @staticmethod
    def from_dict(row: dict) -> AlternateName:

        def to_bool(value):
            return str(value).strip() == "1"

        return AlternateName(
            alternate_name_id=int(row["alternate_name_id"]),
            geoname_id=int(row["geoname_id"]),
            alternate_name=row.get("alternate_name"),
            iso_language=row.get("iso_language"),
            is_preferred_name=to_bool(row.get("is_preferred_name")),
            is_short_name=to_bool(row.get("is_short_name")),
            is_colloquial=to_bool(row.get("is_colloquial", "0")),
            is_historic=to_bool(row.get("is_historic", "0")),
        )