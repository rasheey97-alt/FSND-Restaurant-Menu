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
    >>> from sqlachemy import create_engine 
    >>> from sqlalchemy.orm import sessionmaker
    >>> # imports necessary sqlalchemy files
    >>> from database_setup import Base, Restaurant, Menu Item
    >>> # imports the objects made in database_setup.py
    >>> engine = create_engine('sqlite:///restaurantmenu.db')
    >>> lets the program know what DB we want to communicate with
    >>> Base.metadata.bind = engine
    >>> # this command makes the connection between the classes
    >>> # and their corisponding tables in the DB
    >>> DBSession = sessionmaker(bind = engine)
    >>> # establishes a link between the code execution and the engine that was just created

Everything with SQLAlchemy is done in a session
A session allows you to write down all the commands you want to execute,
but not send them to the DB until a commit is called

    >>> session = DBSession()
    >>> # creates an instance of DBSession() called session
    >>> # provides you with a staging zone for all objects loaded into DBSession()


Load some Data
--------------
Still in the Python Shell from the previous connection

    >>> myFirstRestaurant = Restaurant(name = "Pizza Palace")
    >>> # creates an object of class Restaurant
    >>> session.add(myFirstRestaurant)
    >>> # adds the myFirstRestaurant object to the SQLAlchemy staging zone,
    >>> # ready to commited to the DB
    >>> session.commit()
    >>> # stores the myFirstRestaurant object to the DB 


View the Data
-------------
Still in the Python Shell from the previous connection


    >>> session.query(Restaurant).all()
    >>> # asks the session to go into the DB, find the table that corispondes
    >>> # to the restaurant class, and find all the entries in that table, and return in a list
    [<database_setup.Restaurant object at 0x8fd740c>]
    >>> # returns the objects place in memory...


Load a more complex object
--------------------------

    >>> cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made with fair trade local organic gluten free ingredients", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
    >>> session.add(cheesePizza)
    >>> session.commit()



