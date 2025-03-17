from pylord.orm import Table, Column, ForeignKey


class Category(Table):
    name = Column(str)


class Blog(Table):
    name = Column(str)
    description = Column(str)
    about = Column(str)
    category = ForeignKey(Category)


class User(Table):
    username = Column(str)
    email = Column(str)
    password_hash = Column(str)


