from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, Float
from sqlalchemy import Integer, BigInteger, String, Text, LargeBinary, DateTime, Boolean, Float
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from es.utils.utils import get_project_root

# Create an SQLAlchemy engine
engine = create_engine("sqlite:///" + str(get_project_root()) + "/es.db", echo=False)

# Create a base class to define all the database subclasses
TableDeclarativeBase = declarative_base()

# Bind the engine to the base class
TableDeclarativeBase.metadata.bind = engine

# Create a Session class able to initialize database sessions
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)


class Customer(TableDeclarativeBase):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, nullable=True)
    prename = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    street = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    invoices = relationship("Invoice", viewonly=True)

    def __repr__(self):
        if self.company_name:
            return f"Customer {self.id} - {self.company_name}"
        return f"Customer {self.id} - {self.prename} {self.surname}"


class Shipping(TableDeclarativeBase):

    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    name_english = Column(String, nullable=True)
    insured = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    weight_up_to = Column(Float, nullable=True)
    country_class = Column(String, nullable=True)
    dimension_1 = Column(Float, nullable=True)
    dimension_2 = Column(Float, nullable=True)
    dimension_3 = Column(Float, nullable=True)

    def __repr__(self):
        return f"Shipping {self.id} {self.name} {self.price}"


class Invoice(TableDeclarativeBase):

    __tablename__ = "invoices"

    id = Column(String, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    price = Column(Float, nullable=False)
    cash = Column(Boolean, nullable=False, default=False)
    invoice_date = Column(DateTime(timezone=True), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=True)
    shipping_id = Column(Integer, ForeignKey('shipping.id'))
    shipping_price = Column(Float, nullable=True)

    customer = relationship("Customer")
    shipping = relationship("Shipping")
    products = relationship("ProductsSold", viewonly=True)

    def __repr__(self):
        return f"Invoice {self.id}, {self.invoice_date}, {self.customer}"


class ESProduct(TableDeclarativeBase):

    __tablename__ = "es_products"

    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    gross_selling_price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    sellers = relationship("ESSupplier", viewonly=True)

    def __repr__(self):
        return f"ES-Product {self.id} - {self.name}"


class ESSupplier(TableDeclarativeBase):

    __tablename__ = "es_supplier"

    es_product_id = Column(String, ForeignKey("es_products.id"), primary_key=True)
    seller_product_id = Column(String, ForeignKey("supplier_products.id"), primary_key=True)
    rating = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False, default=1)

    es_product = relationship("ESProduct")
    seller_product = relationship("SupplierProduct")

    def __repr__(self):
        return f"ES Product {self.es_product} bought as {self.seller_product_id}"


class ProductsSold(TableDeclarativeBase):

    __tablename__ = "products_sold"

    invoice_id = Column(String, ForeignKey("invoices.id"), primary_key=True)
    product_id = Column(String, ForeignKey("es_products.id"), primary_key=True)
    name = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    price_per_item = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    note = Column(String, nullable=True)

    invoice = relationship("Invoice")
    product = relationship("ESProduct")

    def __repr__(self):
        return f"{self.amount}x {self.product.id} sold in invoice {self.invoice.id}"


class Supplier(TableDeclarativeBase):

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)
    banking_details = Column(String, nullable=True)

    invoices = relationship("Receipt", viewonly=True)

    def __repr__(self):
        return f"Seller {self.id} - {self.name}"


class Receipt(TableDeclarativeBase):

    __tablename__ = "receipts"

    id = Column(String, primary_key=True)
    seller_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    price = Column(Float, nullable=False)
    cash = Column(Boolean, nullable=False, default=False)
    category = Column(String, nullable=True)
    invoice_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), default=func.now())
    payment_date = Column(DateTime(timezone=True), nullable=True)
    invoice_receipt = Column(String, nullable=True)
    payment_receipt = Column(String, nullable=True)

    seller = relationship("Supplier")
    products = relationship("ProductsBought", viewonly=True)


class SupplierProduct(TableDeclarativeBase):

    __tablename__ = "supplier_products"

    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    net_price = Column(Float, nullable=False)
    gross_selling_rec = Column(Float, nullable=True)
    category = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    url = Column(String, nullable=True)

    def __repr__(self):
        return f"Seller product {self.id} - {self.name}"


class ProductsBought(TableDeclarativeBase):

    __tablename__ = "products_bought"

    invoice_id = Column(String, ForeignKey("receipts.id"), primary_key=True)
    product_id = Column(String, ForeignKey("supplier_products.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    invoice = relationship("Receipt")
    product = relationship("SupplierProduct")

    def __repr__(self):
        return f"Product {self.product_id} sold in {self.invoice_id}"


TableDeclarativeBase.metadata.create_all(bind=engine)
