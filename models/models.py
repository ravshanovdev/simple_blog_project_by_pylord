from pylord.orm import Table, Column, ForeignKey


class User(Table):
    username = Column(str)
    email = Column(str)
    password_hash = Column(str)


class Category(Table):
    user = ForeignKey(User)
    name = Column(str)


class Blog(Table):
    user = ForeignKey(User)
    name = Column(str)
    description = Column(str)
    about = Column(str)
    category = ForeignKey(Category)





