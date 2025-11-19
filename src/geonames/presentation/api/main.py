from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from geonames.presentation.api.rest import routes
from geonames.presentation.api.graphql.schema import schema


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="GeoNames API",
        version="1.0",
        debug=True,
    )

    # REST routes
    app.include_router(routes.router, prefix="/api")

    # GraphQL endpoint
    app.include_router(GraphQLRouter(schema), prefix="/api/graphql")

    # Root endpoint
    @app.get("/")
    def root():
        return {"message": "The API is running"}

    return app


app = create_app()
