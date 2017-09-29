from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    path = Column(String(50), nullable = False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
            }

engine = create_engine('sqlite:///files.db')
Base.metadata.create_all(engine)

