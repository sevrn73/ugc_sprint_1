from http import HTTPStatus
from typing import Optional

from aiokafka import AIOKafkaProducer
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, APIRouter

from broker.kafka_settings import kafka
from api.models.progress_film import ProgressFilmModel
from services.auth import Auth

router = APIRouter(prefix='/ugc/v1', tags=['progress_film'])
security = HTTPBearer()
auth_handler = Auth()


@router.post('/progress_film/')
async def post_event(
    progress_film: ProgressFilmModel,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # TODO auth
    token = credentials.credentials
    # user_id = auth_handler.decode_token(token)
    user_id = "e76f1153-8b6f-4d6d-b44a-4aece3c4ddb9"
    try:
        await kafka.kafka_producer.send(
            topic='views',
            value=progress_film.json().encode(),
            key=f"{user_id}+{progress_film.movie_id}".encode(),
        )
        return {'msg': 'ok'}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=e.args[0].str())
