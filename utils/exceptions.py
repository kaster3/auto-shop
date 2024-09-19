from fastapi import HTTPException, status


def not_found_by_id(item_id: int, item: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": f"{item} not found with id {item_id}"}
    )