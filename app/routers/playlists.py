from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import PlayList, User, AddContentToPlaylist, PlayListResponse
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user
from business_logic.add_content_to_playlist import content_to_playlist

router = APIRouter(tags=['playlists'])


@router.post('/playlists', status_code=status.HTTP_201_CREATED)
def create_playlist(playlist_data: PlayList, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    new_playlist = models.PlayList(**playlist_data.dict(), user_id=current_user.dict().get('id_user'))
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist


@router.get('/playlists', response_model=list[PlayListResponse])
def get_my_playlists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_playlists = db.query(models.PlayList).filter(models.PlayList.user_id == current_user.dict().get('id_user')).all()
    return my_playlists


@router.put('/add-content-to-playlist/{playlist_id}', status_code=status.HTTP_201_CREATED,
            response_model=PlayListResponse)
def add_content_to_playlist(playlist_id: int, playlist_data: AddContentToPlaylist, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    playlist_query = db.query(models.PlayList).filter(models.PlayList.id == playlist_id)
    playlist = playlist_query.first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    if playlist.user_id != current_user.dict().get('id_user'):
        return {'msg': 'нет доступа'}
    contents = content_to_playlist(playlist_data.content_id, db)
    playlist.contents += contents
    db.commit()
    db.refresh(playlist)
    return playlist
