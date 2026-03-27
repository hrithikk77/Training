from sqlalchemy import select, delete
from sqlalchemy.inspection import inspect
from repositories.base_repository import BaseRepository
from typing import List, Dict, Any, Optional

class SqlAlchemyRepository(BaseRepository):
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def _to_dict(self, obj) -> Optional[Dict[str, Any]]:
        if not obj: return None
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    async def get_all(self, **filters) -> List[Dict[str, Any]]:
        query = select(self.model_class)
        for k, v in filters.items():
            if hasattr(self.model_class, k):
                query = query.filter(getattr(self.model_class, k) == v)
        res = await self.session.execute(query)
        return [self._to_dict(i) for i in res.scalars().all()]

    async def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        res = await self.session.execute(select(self.model_class).filter_by(id=item_id))
        return self._to_dict(res.scalars().first())

    async def create(self, item_data: dict) -> Dict[str, Any]:
        item = self.model_class(**item_data)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return self._to_dict(item)

    async def find_one_by_field(self, field_name: str, field_value: Any) -> Optional[Dict[str, Any]]:
        query = select(self.model_class).filter(getattr(self.model_class, field_name) == field_value)
        res = await self.session.execute(query)
        return self._to_dict(res.scalars().first())

    async def update(self, item_id: int, item_data: dict) -> Optional[Dict[str, Any]]:
        res = await self.session.execute(select(self.model_class).filter_by(id=item_id))
        item = res.scalars().first()
        if not item: return None
        for k, v in item_data.items(): setattr(item, k, v)
        await self.session.commit()
        await self.session.refresh(item)
        return self._to_dict(item)

    async def delete(self, item_id: int) -> bool:
        res = await self.session.execute(delete(self.model_class).filter_by(id=item_id))
        await self.session.commit()
        return res.rowcount > 0