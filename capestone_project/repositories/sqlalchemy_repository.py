from .base_repository import BaseRepository
from sqlalchemy.orm import Session

class SQLAlchemyRepository(BaseRepository):
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).first()