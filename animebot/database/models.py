from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

playlist_musiclink = Table('playlist_musiclink', Base.metadata,
    Column('music_link', Integer, ForeignKey('music_link.id')),
    Column('playlist', Integer, ForeignKey('playlist.id'))
)


class MusicLink(Base):
    __tablename__ = 'music_link'
    id = Column(Integer, primary_key=True)
    link = Column(String(70))
    playlist = relationship("Playlist", secondary=playlist_musiclink, backref='music')

    def __repr__(self):
        return "<test(name='%s', fullname='%s')>" % (
                            self.name, self.fullname)


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)