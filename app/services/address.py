import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import AddressNotFoundError, DatabaseError
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.services.distance import distance_km

logger = logging.getLogger(__name__)


def get_address_by_id(db: Session, address_id: int) -> Address:
    address = db.get(Address, address_id)
    if address is None:
        raise AddressNotFoundError(address_id)
    return address


def create_address(db: Session, payload: AddressCreate) -> Address:
    address = Address(**payload.model_dump())
    try:
        db.add(address)
        db.commit()
        db.refresh(address)
        logger.info("Created address id=%s name=%s", address.id, address.name)
        return address
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Failed to create address: %s", exc)
        raise DatabaseError("Failed to create address") from exc


def update_address(db: Session, address_id: int, payload: AddressUpdate) -> Address:
    address = get_address_by_id(db, address_id)
    for field, value in payload.model_dump().items():
        setattr(address, field, value)
    try:
        db.commit()
        db.refresh(address)
        logger.info("Updated address id=%s", address.id)
        return address
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Failed to update address id=%s: %s", address_id, exc)
        raise DatabaseError("Failed to update address") from exc


def delete_address(db: Session, address_id: int) -> None:
    address = get_address_by_id(db, address_id)
    try:
        db.delete(address)
        db.commit()
        logger.info("Deleted address id=%s", address_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Failed to delete address id=%s: %s", address_id, exc)
        raise DatabaseError("Failed to delete address") from exc


def search_addresses_by_proximity(
    db: Session,
    latitude: float,
    longitude: float,
    distance: float,
) -> list[Address]:
    if distance <= 0:
        raise ValueError("distance must be greater than 0")

    addresses = db.query(Address).all()
    results: list[Address] = []
    for address in addresses:
        km = distance_km(latitude, longitude, address.latitude, address.longitude)
        if km <= distance:
            results.append(address)

    logger.info(
        "Proximity search at (%.4f, %.4f) within %s km returned %s results",
        latitude,
        longitude,
        distance,
        len(results),
    )
    return results
