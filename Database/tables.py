from decimal import Decimal

from sqlalchemy import create_engine, Integer, Column, Numeric, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///Database/restourant.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(12,2), nullable=False)

    def __str__(self):
        return f"<b>🏷️ {self.name}</b>\n💰 Цена: <b>{self.price:,.2f}$</b>"

class User(Base):
    __tablename__ = 'user'
    chat_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)

    basket = relationship('Basket', back_populates="user")

class Basket(Base):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.chat_id'), nullable=False)
    foot_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    stock = Column(Integer, nullable=False)

    user = relationship('User', back_populates='basket')
    menu = relationship('Menu')

    def add(self):
        with Session() as session:
            session.add(self)
            session.commit()