from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PropertyStatus(str, Enum):
    AVAILABLE = "available"
    VIEWING_BOOKED = "viewing_booked"
    RESERVED = "reserved"
    CONTRACT_PENDING = "contract_pending"
    RENTED = "rented"
    MOVE_OUT = "move_out"
    INSPECTION = "inspection"


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    STUDIO = "studio"
    ROOM = "room"


class PropertyAmenity(Base):
    __tablename__ = "property_amenities"

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="CASCADE"),
        primary_key=True,
    )

    amenity_id: Mapped[int] = mapped_column(
        ForeignKey("amenities.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    property_type: Mapped[PropertyType] = mapped_column(
        SQLEnum(PropertyType),
        nullable=False,
    )

    rooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    area: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
    )

    rent_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    deposit_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    utilities_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    status: Mapped[PropertyStatus] = mapped_column(
        SQLEnum(PropertyStatus),
        nullable=False,
        default=PropertyStatus.AVAILABLE,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    images: Mapped[list["PropertyImage"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
    )

    amenities: Mapped[list["Amenity"]] = relationship(
        secondary="property_amenities",
        back_populates="properties",
    )


class PropertyImage(Base):
    __tablename__ = "property_images"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    property: Mapped["Property"] = relationship(
        back_populates="images",
    )


class Amenity(Base):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    properties: Mapped[list["Property"]] = relationship(
        secondary="property_amenities",
        back_populates="amenities",
    )