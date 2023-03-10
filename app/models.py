from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table, DECIMAL
from sqlalchemy.orm import relationship, backref

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    password = Column(String)
    mail = Column(String(50))
    is_staff = Column(Boolean, default=False)
    date_time_registration = Column(DateTime)
    contents = relationship('Content', back_populates='user')
    playlists = relationship('PlayList', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    wallet = relationship('Wallet', back_populates='user', uselist=False)


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    file = Column(String(1000))
    date_time_uploaded = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='contents')
    playlists = relationship("PlayList", secondary="playlists_contents", back_populates="contents")
    comments = relationship('Comment', back_populates='content')
    likes = relationship('Like', back_populates='content')


class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True)
    content = relationship('Content', back_populates='likes')


class PlayList(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    playlist_title = Column(String(50))
    date_time_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='playlists')
    contents = relationship("Content", secondary="playlists_contents", back_populates="playlists")


playlists_contents = Table('playlists_contents', Base.metadata,
                           Column('playlist_id', ForeignKey('playlists.id'), primary_key=True),
                           Column('content_id', ForeignKey('contents.id'), primary_key=True)
                           )


class Subscription(Base):
    __tablename__ = 'subscriptions'
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    youtuber_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(String(200))
    date_time_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='comments')
    content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'))
    content = relationship('Content', back_populates='comments')


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    date_time_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='wallet', uselist=False)


class Check(Base):
    __tablename__ = 'checks'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    date_time_created = Column(DateTime)
    wallet_id_from = Column(Integer, ForeignKey('users.id'))
    wallet_id_to = Column(Integer, ForeignKey('users.id'))
