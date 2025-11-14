from fastapi import APIRouter, Query, Depends
from typing import Optional, List
from src.application.use_cases.select_geonames_use_case import SelectGeoNamesUseCase
from domain.geoname_selection_service import GeoNameSelectionService
from src.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work_factory import SqlAlchemyUnitOfWorkFactory
from src.presentation.api.dependencies import get_uow_factory
from application.dtos.geoname_dto import GeoNameDTO
from application.mappers.geoname_output_mapper import GeoNameMapper

router = APIRouter()


@router.get("/geonames/{country_code}", tags=["geonames"])
def get_geonames(
    country_code: Optional[str],
    feature_class: Optional[str] = Query(None, description="Feature class (e.g., 'A', 'P', etc.)",),
    feature_code: Optional[str] = Query(None, description="Feature code (e.g., 'ADM1', 'ADM2', etc.)",),
    min_population: Optional[int] = Query(None, description="Minimum population filter (used when depth_level is None)",),
    uow_factory: SqlAlchemyUnitOfWorkFactory = Depends(get_uow_factory),
):
    filters = {}

    if country_code:
        filters["country_code"] = country_code
    if feature_class:
        filters["feature_class"] = feature_class    
    if feature_code:
        filters["feature_code"] = feature_code
    if min_population:
        filters["min_population"] = min_population

    with uow_factory() as uow:
        service = GeoNameSelectionService(
            geoname_repository=uow.geoname_repo,
            country_repository=uow.country_geoname_repo
        )
        
        use_case = SelectGeoNamesUseCase(
            service=service
        )

        entities = use_case.execute(filters)
        dtos = GeoNameMapper.to_dto_list(entities)
    
    return dtos