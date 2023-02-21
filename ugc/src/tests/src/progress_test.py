import logging
from http import HTTPStatus

from ugc_api.api.models.progress_film import ProgressFilmModel
from ugc_api.tests.testdata.data import HEADERS, MOVIE_ID, TIMESTAMP_MOVIE


logger = logging.getLogger(__name__)


async def test_success(make_post_request):
    """Test success case."""
    data = ProgressFilmModel(movie_id=MOVIE_ID, timestamp_movie=TIMESTAMP_MOVIE)
    response = await make_post_request(
        "progress_film",
        headers=HEADERS,
        data=data.json(),
    )
    logger.debug("Response: %s %s", response.status, response)
    assert response.status == HTTPStatus.OK
