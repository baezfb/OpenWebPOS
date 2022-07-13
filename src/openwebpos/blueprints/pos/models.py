from openwebpos.extensions import db
from openwebpos.utils import gen_urlsafe_token
from openwebpos.utils.sql import SQLMixin


class Category(SQLMixin, db.Model):
    __tablename__ = 'categories'

    public_id = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
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
        category.description = 'Burger'
        category.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder_4096x2160.png'

        if self.public_id is None:
            self.public_id = gen_urlsafe_token(10)


class Item(SQLMixin, db.Model):
    __tablename__ = 'items'

    public_id = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    category_id = db.Column(db.Integer, db.ForeignKey('categories.public_id'), nullable=False)
    options = db.relationship('Option', backref='item', lazy='dynamic')
    addons = db.relationship('Addon', backref='item', lazy='dynamic')

    @staticmethod
    def insert_items():
        """
        Add items to the database.
        """
        item = Item()
        item.name = 'Burger'
        item.description = 'Burger'
        item.price = 10.50
        item.category_id = Category.query.filter_by(name='Food').first().public_id
        item.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder_4096x2160.png'

        if self.public_id is None:
            self.public_id = gen_urlsafe_token(10)


class Option(SQLMixin, db.Model):
    __tablename__ = 'options'

    public_id = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.public_id'), nullable=False)

    @staticmethod
    def insert_options():
        """
        Add options to the database.
        """
        option = Option()
        option.name = 'Option1'
        option.description = 'Option1 Description'
        option.price = 10.00
        option.item_id = Item.query.filter_by(name='Burger').first().public_id
        option.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Option, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder_4096x2160.png'

        if self.public_id is None:
            self.public_id = gen_urlsafe_token(10)

        if self.price is None:
            self.price = 0.00


class Addon(SQLMixin, db.Model):
    __tablename__ = 'addons'

    public_id = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # relationship
    item_id = db.Column(db.Integer, db.ForeignKey('items.public_id'), nullable=False)

    @staticmethod
    def insert_addons():
        """
        Add addons to the database.
        """
        addon = Addon()
        addon.name = 'Addon1'
        addon.description = 'Addon1 Description'
        addon.price = 10.00
        addon.item_id = Item.query.filter_by(name='Burger').first().public_id
        addon.save()

    def is_active(self):
        return self.active

    def __init__(self, **kwargs):
        super(Addon, self).__init__(**kwargs)
        if self.image is None:
            self.image = 'placeholder_4096x2160.png'

        if self.public_id is None:
            self.public_id = gen_urlsafe_token(10)

        if self.price is None:
            self.price = 0.00
