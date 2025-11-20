from fastapi import APIRouter, Depends

from geonames.infrastructure.persistence.unit_of_work.sql_alchemy_geonames_unit_of_work import SqlAlchemyGeoNamesUnitOfWorkFactory
from geonames.application.mappers.country_output_mapper import CountryOutputMapper
from geonames.presentation.api.dependencies import get_uow_factory


router = APIRouter()

@router.get("/countries", tags=["countries"])
def get_countries(uow_factory: SqlAlchemyGeoNamesUnitOfWorkFactory = Depends(get_uow_factory)):
    with uow_factory() as uow:
        entities = uow.country_geoname_repo.find_all()
        dtos = CountryOutputMapper.to_dto_list(entities)
        return dtos
