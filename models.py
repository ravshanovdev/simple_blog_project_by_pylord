from pylord.orm import Table, Column, ForeignKey


class Category(Table):
    name = Column(str)


class Blog(Table):
    category = ForeignKey(Category)
    name = Column(str)
    description = Column(str)
    about = Column(str)

