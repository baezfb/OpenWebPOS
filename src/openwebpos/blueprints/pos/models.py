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
        category = Category(name='Category 1', description='Category Description')
        category.save()

    def is_active(self):
        return self.active

    def is_used(self):
        return self.items.count() > 0

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.slug is None:
            self.slug = slugify(text=self.name)


class Item(SQLMixin, db.Model):
    __tablename__ = 'items'

    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
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
        item = Item(name='Burger', description='Burger description', price=10.00, category_id=1)
        item.addons = Addon.query.filter_by(item_id=item.id, active=True).all()
        item.options = Option.query.filter_by(item_id=item.id, active=True).all()
        item.save()

    def is_active(self):
        return self.active

    def is_used(self):
        return self.options.count() > 0 or self.addons.count() > 0

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

        if self.slug is None:
            self.slug = slugify(text=self.name)

        if self.price is None:
            self.price = 0.00


class Option(SQLMixin, db.Model):
    __tablename__ = 'options'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    @staticmethod
    def insert_options():
        """
        Add options to the database.
        """
        option = Option(name='Option 1', description='Option Description', price=10.00, item_id=1)
        option.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Option, self).__init__(**kwargs)

        if self.price is None:
            self.price = 0.00


class Addon(SQLMixin, db.Model):
    __tablename__ = 'addons'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    @staticmethod
    def insert_addons():
        """
        Add addons to the database.
        """
        addon = Addon(name='Addon 1', description='Addon Description', price=10.00, item_id=1)
        addon.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Addon, self).__init__(**kwargs)

        if self.price is None:
            self.price = 0.00
