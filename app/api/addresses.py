import logging

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from app.services import address as address_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Create an address record with validated geographic coordinates.",
)
def create_address(
    payload: AddressCreate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    address = address_service.create_address(db, payload)
    return AddressResponse.model_validate(address)


@router.get(
    "/search",
    response_model=list[AddressResponse],
    summary="Search addresses by proximity",
    description=(
        "Return all addresses within the given distance (kilometers) "
        "from the specified latitude and longitude."
    ),
)
def search_addresses(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Center latitude"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Center longitude"),
    distance: float = Query(..., gt=0, description="Search radius in kilometers"),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    addresses = address_service.search_addresses_by_proximity(
        db, latitude, longitude, distance
    )
    return [AddressResponse.model_validate(a) for a in addresses]


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Get an address by ID",
    description="Retrieve a single address record by its unique identifier.",
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
) -> AddressResponse:
    address = address_service.get_address_by_id(db, address_id)
    return AddressResponse.model_validate(address)


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Update an address",
    description="Replace all fields of an existing address record.",
)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    address = address_service.update_address(db, address_id, payload)
    return AddressResponse.model_validate(address)


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address",
    description="Permanently remove an address record from the database.",
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
) -> None:
    address_service.delete_address(db, address_id)
