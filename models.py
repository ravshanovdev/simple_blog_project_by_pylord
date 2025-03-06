from pylord.orm import Table, Column


class Category(Table):
    name = Column(str)


class Blog(Table):
    name = Column(str)
    description = Column(str)
    about = Column(str)

