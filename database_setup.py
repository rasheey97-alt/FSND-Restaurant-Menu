import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(
		String(80), nullable = False)
	id = Column(
		Integer, primary_key = True)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	# Create name of menu item column
	name = Column(
		String(80), nullable = False)
	# Create ID column
	id = Column(
		Integer, primary_key = True)
	# Create course type coulmn
	course = Column(
		String(250))
	# Create description of item column
	description = Column(
		String(250))
	# Create Price
	price = Column(
		String(8))
	# What restaurant makes it
	restaurant_id = Column(
		Integer, ForeignKey('restaurant.id'))
	# Create relationship between Class Restaurant
	restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)