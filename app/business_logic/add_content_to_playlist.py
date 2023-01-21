from fastapi import HTTPException, status
import models


def content_to_playlist(contents_id: list[int], db):
    contents = []
    for i in contents_id:
        content = db.query(models.Content).filter(models.Content.id == i).first()
        if not content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id: {i} not found')
        contents.append(content)
    return contents
