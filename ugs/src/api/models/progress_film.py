import uuid

from pydantic import BaseModel, Field


class ProgressFilmModel(BaseModel):
    movie_id: uuid.UUID = Field(title="идентификатор фильма")
    viewing_progress: int = Field(title="прогресс просмотра фильма")
