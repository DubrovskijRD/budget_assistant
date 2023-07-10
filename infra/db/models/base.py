from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.types import Float
from domain.vo.amount import Amount


class Base(DeclarativeBase, MappedAsDataclass):
    type_annotation_map = {
        Amount: Float
    }
