from fastapi.responses import JSONResponse
from fastapi import Request
from geonames.domain.exceptions import InvalidGeoNameSelectionError


async def invalid_geoname_selection_handler(request: Request, exc: InvalidGeoNameSelectionError):
    
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
