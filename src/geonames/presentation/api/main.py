from fastapi import FastAPI
from src.geonames.presentation.api import routes
from src.geonames.presentation.api.error_handlers import invalid_geoname_selection_handler
from src.geonames.domain.exceptions import InvalidGeoNameSelectionError

app = FastAPI(title="GeoNames API", version="1.0", debug=True)

app.include_router(routes.router)

app.add_exception_handler(InvalidGeoNameSelectionError, invalid_geoname_selection_handler)

@app.get("/")
def root():
    return {"message": "The API is running"}
