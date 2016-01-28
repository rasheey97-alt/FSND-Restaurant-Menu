Menu Notes / SQLAlchemy Notes
-----------------------------

After making the databae_setup.py file
run the file from the terminal with
    $ python database_setup.py
to create the database

the database is made, but empty


Setup 
-----

To put data in the DB with python shell...:

    $ python
    >>> from sqlalchemy import create_engine 
    >>> from sqlalchemy.orm import sessionmaker
imports necessary sqlalchemy files

    >>> from database_setup import Base, Restaurant, MenuItem
imports the objects made in database_setup.py

    >>> engine = create_engine('sqlite:///restaurantmenu.db')
lets the program know what DB we want to communicate with

    >>> Base.metadata.bind = engine
this command makes the connection between the classes and their corisponding tables in the DB

    >>> DBSession = sessionmaker(bind = engine)
establishes a link between the code execution and the engine that was just created

Everything with SQLAlchemy is done in a session.
A session allows you to write down all the commands you want to execute,but not send them to the DB until a commit is called

    >>> session = DBSession()
creates an instance of DBSession() called session
provides you with a staging zone for all objects loaded into DBSession()


Load some Data
--------------
Still in the Python Shell from the previous connection

    >>> myFirstRestaurant = Restaurant(name = "Pizza Palace")
creates an object of class Restaurant

    >>> session.add(myFirstRestaurant)
adds the myFirstRestaurant object to the SQLAlchemy staging zone, ready to commited to the DB

    >>> session.commit()
stores the myFirstRestaurant object to the DB 


View the Data
-------------
Still in the Python Shell from the previous connection


    >>> session.query(Restaurant).all()
asks the session to go into the DB, find the table that corispondes to the restaurant class, and find all the entries in that table, and return in a list
    
    [<database_setup.Restaurant object at 0x8fd740c>]
returns the objects place in memory...


Load a more complex object
--------------------------

    >>> cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made 
    with fair trade local organic gluten free ingredients", course = 
    "Entree", price = "$8.99", restaurant = myFirstRestaurant)
    >>> session.add(cheesePizza)
    >>> session.commit()


Read a Row from the DB
-----------------------

    >>> firstResult = session.query(Restaurant).first()
makes a varible that coorispondes to a single row in the database. 

single row references allow you to extract column entries as method names

    >>> firstResult.name
returns
    u'Pizza Palace'

    >>> session.query(Restaurant).all()

returns the place in memory of every object in the database

Display Data Nicely
-------------------

    >>> items = session.query(MenuItem).all()
makes a varible `items` and sets it equal to the retrival of all menu items

    >>> for item in items:
    ...		print item.name
    ...

prints a list of all menu item names


Update a Record
----------------
Step 1 is to find the correct veggie burger

    >>> veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

stores a list of all veggies burgers in the veggieBurgers varible

    >>> for veggieBurger in veggieBurgers:
    ... 	print veggieBurger.id
    ...		print veggieBurger.price
    ... 	print veggieBurger.restaurant.name
    ...		print "\n" 
    ...		# ^ prints a new line to make results easier to read
this will print a list of all veggie burger id, price, and restaurants

find the one you want to update by id and save it to a varible:

    >>> UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()

the  `.one()` ensures that only one result is being returned

to check your work run:

    >>> print UrbanVeggieBurger.price

to verify it was the one you wanted to change

    >>> UrbanVeggieBurger.price = '$2.99'
    >>> session.add(UrbanVeggieBurger)
    >>> session.commit()

this changes the price of the obect, stages it, and commits it to the DB

Update Many Records
-------------------

    >>> for veggieBurger in veggieBurgers:
    ...		if veggieBurger.price != '$2.99'
    ...			veggieBurger.price = '$2.99'
    ...			session.add(veggieBurger)
    ... 		session.commit()
    ...
this cycles through a for loop of every veggie burger, changes each price, stages the object, then commits it.


Delete a Record
---------------

    >>> spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
    >>> print spinach.restaurant.name
    Auntie Ann's Diner
    >>> session.delete(spinach)
    >>> # stages item for removal
    >>> session.commit()
    >>> # commits removal



INSTRUCTOR NOTES:
-----------------

CRUD Review
Operations with SQLAlchemy

In this lesson, we performed all of our CRUD operations with SQLAlchemy on an SQLite database. Before we perform any operations, we must first import the necessary libraries, connect to our restaurantMenu.db, and create a session to interface with the database:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
CREATE
We created a new Restaurant and called it Pizza Palace:
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()
We created a cheese pizza menu item and added it to the Pizza Palace Menu:
cheesepizza = menuItem(name="Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()
READ
We read out information in our database using the query method in SQLAlchemy:

firstResult = session.query(Restaurant).first()
firstResult.name

items = session.query(MenuItem).all()
for item in items:
    print item.name
UPDATE
In order to update and existing entry in our database, we must execute the following commands:

Find Entry
Reset value(s)
Add to session
Execute session.commit()
We found the veggie burger that belonged to the Urban Burger restaurant by executing the following query:
veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"
Then we updated the price of the veggie burger to $2.99:

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit() 
DELETE
To delete an item from our database we must follow the following steps:

Find the entry
Session.delete(Entry)
Session.commit()
We deleted spinach Ice Cream from our Menu Items database with the following operations:

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit() 







