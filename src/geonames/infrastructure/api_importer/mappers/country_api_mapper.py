from geonames.domain.country import Country


class CountryApiMapper:
    
    @staticmethod
    def from_api(data: dict) -> Country:
        
        def to_int(v):
            try:
                return int(v) if v not in (None, "", " ") else None
            except (ValueError, TypeError):
                return None

        def to_float(v):
            try:
                return float(v) if v not in (None, "", " ") else None
            except (ValueError, TypeError):
                return None

        return Country(
            geoname_id=to_int(data.get("geonameId")),
            iso_alpha2=data.get("countryCode"),
            country_name=data.get("countryName"),
            iso_alpha3=data.get("isoAlpha3"),
            iso_numeric=to_int(data.get("isoNumeric")),
            fips_code=data.get("fipsCode"),
            capital=data.get("capital"),
            area_sqkm=to_float(data.get("areaInSqKm")),
            population=to_int(data.get("population")),
            continent=data.get("continent"),
            languages=data.get("languages"),
            currency_code=data.get("currencyCode"),
            postal_code_format=data.get("postalCodeFormat"),
        )