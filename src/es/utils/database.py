import logging
from typing import Any, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import Boolean, Column, Date, Float, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, NCHAR, PrimaryKeyConstraint, String, TEXT, Table, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2, MONEY, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

from es.utils import config


config = config.config
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class ArtikelnummernLieferanten(Base):
    __tablename__ = 'Artikelnummern_Lieferanten'
    __table_args__ = (
        PrimaryKeyConstraint('ArtikelNummer', name='Artikelnummern_Lieferanten$PrimaryKey'),
        Index('Artikelnummern_Lieferanten$ArtikelNummer', 'ArtikelNummer')
    )

    ArtikelNummer: Mapped[str] = mapped_column(Unicode(255), primary_key=True)
    SSMA_TimeStamp: Mapped[bytes] = mapped_column(TIMESTAMP)
    Bezeichnung: Mapped[Optional[str]] = mapped_column(Unicode)
    EKNetto: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    VKBrutto: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Art: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Bemerkung: Mapped[Optional[str]] = mapped_column(Unicode)
    Feld1: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    Feld2: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Bild: Mapped[Optional[str]] = mapped_column(String(8000, 'SQL_Latin1_General_CP1_CI_AS'))
    Link: Mapped[Optional[str]] = mapped_column(Unicode(255))


t_Artikelstamm_ES = Table(
    'Artikelstamm_ES', Base.metadata,
    Column('ID', Unicode(255), nullable=False),
    Column('Bezeichnung', Unicode(255)),
    Column('VerkaufsPreis', MONEY, server_default=text('((0))')),
    Column('Gruppe', Unicode(255)),
    Column('Bemerkung', Unicode(255))
)


class EntnahmeArtikel(Base):
    __tablename__ = 'Entnahme_Artikel'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='3_Entnahme_Artikel$PrimaryKey'),
        Index('3_Entnahme_Artikel$ArtikelID', 'ArtikelNummer'),
        Index('3_Entnahme_Artikel$ArtikelNummer', 'ID'),
        Index('3_Entnahme_Artikel$RechnungsNummer', 'RechnungsNummer')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SSMA_TimeStamp: Mapped[bytes] = mapped_column(TIMESTAMP)
    ArtikelNummer: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Anzahl: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RechnungsNummer: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Stückpreis: Mapped[Optional[Any]] = mapped_column(MONEY)
    Rabatt: Mapped[Optional[float]] = mapped_column(Float(53))
    Einheit: Mapped[Optional[str]] = mapped_column(NCHAR(10))
    Anmerkung: Mapped[Optional[str]] = mapped_column(Unicode(255))


class KundenÜbersicht(Base):
    __tablename__ = 'Kunden_Übersicht'
    __table_args__ = (
        PrimaryKeyConstraint('KundenNummer', name='Kunden_Übersicht$PrimaryKey'),
    )

    KundenNummer: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Nachname: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Vorname: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Straße: Mapped[Optional[str]] = mapped_column(Unicode(255))
    PLZ: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Ort: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Land: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Firmenname: Mapped[Optional[str]] = mapped_column(Unicode(255))

    Rechnung_Kunde: Mapped[List['RechnungKunde']] = relationship('RechnungKunde', back_populates='Kunden_Übersicht')


class LieferantES(Base):
    __tablename__ = 'Lieferant_ES'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Lieferant_ES$PrimaryKey'),
        Index('Lieferant_ES$Artikelnummer', 'Artikelnummer'),
        Index('Lieferant_ES$Nummer', 'Nummer')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Artikelnummer: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Lieferant: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Bewertung: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    Nummer: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


t_Merch_Optionen = Table(
    'Merch_Optionen', Base.metadata,
    Column('ID', Integer, nullable=False),
    Column('Text', TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_Projekt_Artikel = Table(
    'Projekt_Artikel', Base.metadata,
    Column('ProjektID', Integer, nullable=False),
    Column('ESArtikel', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Menge', Float(53))
)


t_Projekt_Beschreibung = Table(
    'Projekt_Beschreibung', Base.metadata,
    Column('ID', Integer, nullable=False),
    Column('Name', Unicode(50), nullable=False),
    Column('KundenNummer', Integer),
    Column('Beschreibung', TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('StartDatum', Date),
    Column('Abgerechnet', Boolean)
)


class RechnungLieferant(Base):
    __tablename__ = 'Rechnung_Lieferant'
    __table_args__ = (
        PrimaryKeyConstraint('RechnungsNummer', name='2_Rechnung_Lieferant$PrimaryKey'),
        Index('2_Rechnung_Lieferant$RechnungsNummer', 'Rechnungsdatum')
    )

    RechnungsNummer: Mapped[str] = mapped_column(Unicode(255), primary_key=True)
    SSMA_TimeStamp: Mapped[bytes] = mapped_column(TIMESTAMP)
    Rechnungsdatum: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)
    Zahlungsdatum: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)
    Lieferant: Mapped[Optional[str]] = mapped_column(Unicode(255))
    BetragNetto: Mapped[Optional[Any]] = mapped_column(MONEY)
    BetragBrutto: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Bemerkung: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Art: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Kasse: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    RechnungsbelegDa: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    ZahlungsbelegDa: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    Link: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Versandkosten: Mapped[Optional[float]] = mapped_column(Float(53))
    geprueft: Mapped[Optional[bool]] = mapped_column(Boolean)


t_Versand = Table(
    'Versand', Base.metadata,
    Column('Versandart', Unicode),
    Column('Kosten', MONEY),
    Column('VersichertBis', MONEY),
    Column('Ländergruppe', Integer),
    Column('GewichtBis', Float(53)),
    Column('EnglischerName', Unicode),
    Column('Länge1', Float(53)),
    Column('Länge2', Float(53)),
    Column('Länge3', Float(53))
)


class WareneingangArtikel(Base):
    __tablename__ = 'Wareneingang_Artikel'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='1_Wareneingang_Artikel$PrimaryKey'),
        Index('1_Wareneingang_Artikel$ArtikelNummer', 'ArtikelNummer'),
        Index('1_Wareneingang_Artikel$ID', 'ID'),
        Index('1_Wareneingang_Artikel$RechnungsNummer', 'RechnungsNummer')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SSMA_TimeStamp: Mapped[bytes] = mapped_column(TIMESTAMP)
    RechnungsNummer: Mapped[Optional[str]] = mapped_column(Unicode(255))
    ArtikelNummer: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Anzahl: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    Verkaufspreis: Mapped[Optional[Any]] = mapped_column(MONEY)


class RechnungKunde(Base):
    __tablename__ = 'Rechnung_Kunde'
    __table_args__ = (
        ForeignKeyConstraint(['KundenNummer'], ['Kunden_Übersicht.KundenNummer'], name='FK_4_Rechnung_Kunde_Kunden_Übersicht'),
        PrimaryKeyConstraint('Rechnungsnummer', name='4_Rechnung_Kunde$PrimaryKey'),
        Index('4_Rechnung_Kunde$KundenNummer', 'KundenNummer')
    )

    Rechnungsnummer: Mapped[str] = mapped_column(Unicode(255), primary_key=True)
    Steuer: Mapped[int] = mapped_column(Integer, server_default=text('((0))'))
    Datum: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)
    KundenNummer: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    Betrag: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Versandart: Mapped[Optional[str]] = mapped_column(Unicode(255))
    Versandkosten: Mapped[Optional[Any]] = mapped_column(MONEY)
    Kasse: Mapped[Optional[bool]] = mapped_column(Boolean)
    Zahlungsdatum: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)

    Kunden_Übersicht: Mapped['KundenÜbersicht'] = relationship('KundenÜbersicht', back_populates='Rechnung_Kunde')


engine = create_engine(
    f"mssql+pyodbc://{config.database.username}:{config.database.password.get_secret_value()}@{config.database.server}:1433/{config.database.database}?driver=ODBC+Driver+17+for+SQL+Server"
)
Session = sessionmaker(bind=engine)
session = Session()