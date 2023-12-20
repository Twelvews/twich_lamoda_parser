"""
container.py: File, containing container that describe all dependencies in the project.
"""


from application.dependencies.twich.token_dependency import TwichAPIToken
from application.services.lamoda.products_service import LamodaProductsService
from application.services.twich.game_service import TwichGameService
from application.services.twich.stream_service import TwichStreamService
from application.services.twich.user_service import TwichUserService
from common.config.base.settings import settings
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton
from infrastructure.connections.elastic.database import ElasticSearchDatabase
from infrastructure.connections.mongo.database import MongoDatabase
from infrastructure.repositories.lamoda.elastic.products_repository import (
    LamodaProductsElasticRepository,
)
from infrastructure.repositories.lamoda.mongo.products_repository import (
    LamodaProductsMongoRepository,
)
from infrastructure.repositories.twich.elastic.game_repository import TwichGameElasticRepository
from infrastructure.repositories.twich.elastic.stream_repository import TwichStreamElasticRepository
from infrastructure.repositories.twich.elastic.user_repository import TwichUserElasticRepository
from infrastructure.repositories.twich.mongo.game_repository import TwichGameMongoRepository
from infrastructure.repositories.twich.mongo.stream_repository import TwichStreamMongoRepository
from infrastructure.repositories.twich.mongo.user_repository import TwichUserMongoRepository
from presentation.controllers.lamoda.products_controller import LamodaProductsController
from presentation.controllers.twich.game_controller import TwichGameController
from presentation.controllers.twich.stream_controller import TwichStreamController
from presentation.controllers.twich.user_controller import TwichUserController


class Container(DeclarativeContainer):
    """
    Container: Class, that describe all dependencies in the project.

    Args:
        DeclarativeContainer (_type_): Base superclass for a Container class.
    """

    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            'presentation.api.v1.endpoints.rest.lamoda.products',
            'presentation.api.v1.endpoints.rest.twich.game',
            'presentation.api.v1.endpoints.rest.twich.user',
            'presentation.api.v1.endpoints.rest.twich.stream',
        ],
    )

    # ------------------------------------ Databases ----------------------------------------------

    mongo: Singleton = Singleton(
        MongoDatabase,
        db_name=settings.DB_MONGO_NAME,
        username=settings.DB_MONGO_USERNAME,
        password=settings.DB_MONGO_PASSWORD,
        host=settings.DB_MONGO_HOST,
        port=settings.DB_MONGO_PORT,
        authentication_source=settings.DB_MONGO_AUTH_SOURCE,
    )

    elastic: Singleton = Singleton(
        ElasticSearchDatabase,
        # add config
    )

    # ------------------------------------- Other --------------------------------------------------

    twich_api_token: Singleton = Singleton(
        TwichAPIToken,
    )

    # ---------------------------------- Repositories ----------------------------------------------

    lamoda_products_mongo_repository: Factory = Factory(
        LamodaProductsMongoRepository,
        db=mongo,
    )

    twich_game_mongo_repository: Factory = Factory(
        TwichGameMongoRepository,
        db=mongo,
    )

    twich_user_mongo_repository: Factory = Factory(
        TwichUserMongoRepository,
        db=mongo,
    )

    twich_stream_mongo_repository: Factory = Factory(
        TwichStreamMongoRepository,
        db=mongo,
    )

    lamoda_products_elastic_repository: Factory = Factory(
        LamodaProductsElasticRepository,
        db=elastic,
    )

    twich_game_elastic_repository: Factory = Factory(
        TwichGameElasticRepository,
        db=elastic,
    )

    twich_user_elastic_repository: Factory = Factory(
        TwichUserElasticRepository,
        db=elastic,
    )

    twich_stream_elastic_repository: Factory = Factory(
        TwichStreamElasticRepository,
        db=elastic,
    )

    # ----------------------------------- Services -------------------------------------------------

    lamoda_products_w_service: Factory = Factory(
        LamodaProductsService,
        repository=lamoda_products_mongo_repository,
    )

    lamoda_products_r_service: Factory = Factory(
        LamodaProductsService,
        repository=lamoda_products_mongo_repository,  # change to elastic from mongo
    )

    twich_game_w_service: Factory = Factory(
        TwichGameService,
        repository=twich_game_mongo_repository,
        token=twich_api_token,
    )

    twich_game_r_service: Factory = Factory(
        TwichGameService,
        repository=twich_game_mongo_repository,  # change to elastic from mongo
        token=twich_api_token,
    )

    twich_user_w_service: Factory = Factory(
        TwichUserService,
        repository=twich_user_mongo_repository,
        token=twich_api_token,
    )

    twich_user_r_service: Factory = Factory(
        TwichUserService,
        repository=twich_user_mongo_repository,  # change to elastic from mongo
        token=twich_api_token,
    )

    twich_stream_w_service: Factory = Factory(
        TwichStreamService,
        repository=twich_stream_mongo_repository,
        token=twich_api_token,
    )

    twich_stream_r_service: Factory = Factory(
        TwichStreamService,
        repository=twich_stream_mongo_repository,  # change to elastic from mongo
        token=twich_api_token,
    )

    # ---------------------------------- Controllers -----------------------------------------------

    lamoda_products_w_controller: Factory = Factory(
        LamodaProductsController,
        service=lamoda_products_w_service,
    )

    lamoda_products_r_controller: Factory = Factory(
        LamodaProductsController,
        service=lamoda_products_r_service,
    )

    twich_game_w_controller: Factory = Factory(
        TwichGameController,
        service=twich_game_w_service,
    )

    twich_game_r_controller: Factory = Factory(
        TwichGameController,
        service=twich_game_r_service,
    )

    twich_user_w_controller: Factory = Factory(
        TwichUserController,
        service=twich_user_w_service,
    )

    twich_user_r_controller: Factory = Factory(
        TwichUserController,
        service=twich_user_r_service,
    )

    twich_stream_w_controller: Factory = Factory(
        TwichStreamController,
        service=twich_stream_w_service,
    )

    twich_stream_r_controller: Factory = Factory(
        TwichStreamController,
        service=twich_stream_r_service,
    )
