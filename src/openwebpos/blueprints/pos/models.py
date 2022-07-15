from slugify import slugify

from openwebpos.extensions import db
from openwebpos.utils.sql import SQLMixin


class Category(SQLMixin, db.Model):
    __tablename__ = 'categories'

    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    # relationship
    items = db.relationship('Item', backref='category', lazy='dynamic')

    @staticmethod
    def insert_categories():
        """
        Add categories to the database.
        """
        category = Category()
        category.name = 'Food'
        category.slug = slugify(text='Food')
        category.description = 'Category description'
        category.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.slug is None:
            self.slug = slugify(text=self.name)


class Item(SQLMixin, db.Model):
    __tablename__ = 'items'

    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    options = db.relationship('Option', backref='item', lazy='dynamic')
    addons = db.relationship('Addon', backref='item', lazy='dynamic')

    @staticmethod
    def insert_items():
        """
        Add items to the database.
        """
        item = Item()
        item.name = 'Burger'
        item.slug = slugify(text='Burger')
        item.description = 'Item description'
        item.price = 10.50
        item.category_id = Category.query.filter_by(name='Food').first().id
        item.addons = Addon.query.filter_by(item_id=item.id, active=True).all()
        item.options = Option.query.filter_by(item_id=item.id, active=True).all()
        item.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

        if self.image is None:
            self.image = 'placeholder.png'

        if self.price is None:
            self.price = 0.00


class Option(SQLMixin, db.Model):
    __tablename__ = 'options'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    @staticmethod
    def insert_options():
        """
        Add options to the database.
        """
        option = Option()
        option.name = 'Option1'
        option.description = 'Option1 Description'
        option.price = 10.00
        option.item_id = Item.query.filter_by(name='Burger').first().id
        option.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Option, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder.png'

        if self.price is None:
            self.price = 0.00


class Addon(SQLMixin, db.Model):
    __tablename__ = 'addons'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    @staticmethod
    def insert_addons():
        """
        Add addons to the database.
        """
        addon = Addon()
        addon.name = 'Addon1'
        addon.description = 'Addon1 Description'
        addon.price = 10.00
        addon.item_id = Item.query.filter_by(name='Burger').first().id
        addon.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Addon, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder.png'

        if self.price is None:
            self.price = 0.00
