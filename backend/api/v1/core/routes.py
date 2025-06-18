from fastapi import APIRouter, HTTPException, status, Path, Query, Response
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import json

# Local imports
from c_service.models import Notes
from api.v1.core.models import NotesNew, NotesDetails, NotesUpdate
from api.v1.models import ProcessFeedback

router = APIRouter(tags=["core"])


@router.get("/", name="List of available notes")
async def get_notes_available() -> list[NotesDetails]:
    """Fetch available notes"""
    query = Notes.objects.all()
    status.HTTP_200_OK
    return [notes.model_dump() async for notes in query]


@router.post("/add", name="Add new notes")
async def add_new_notes(new_notes: NotesNew): #-> NotesDetails:
    """Add new notes"""
    notes = await Notes.objects.acreate(**new_notes.model_dump())
    await notes.asave()  # Save the new note to the database
    return Response(str(notes.model_dump()),status.HTTP_201_CREATED)
    #return NotesDetails(**notes.model_dump(), message="Notes created successfully!", status_code=status.HTTP_201_CREATED)


@router.get("/{id}", name="Get notes details by ID")
async def get_notes_by_id(
    id: Annotated[int, Path(description="Notes id")]
) -> NotesDetails:
    """Fetch a specific note by ID"""
    try:
        notes = await Notes.objects.aget(id=id)
        status.HTTP_200_OK
        return NotesDetails(**notes.model_dump())
    except Notes.DoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Notes with id {id} does not exist!",
        )


@router.delete("/{id}", name="Delete a specific note")
async def delete_notes(
    id: Annotated[int, Path(description="Notes id")]
) -> ProcessFeedback:
    """Delete a particular note"""
    try:
        notes = await Notes.objects.aget(id=id)
        await notes.adelete()
        return ProcessFeedback(detail=f"Notes with id {id} deleted successfully!", status_code=status.HTTP_204_NO_CONTENT)
    except Notes.DoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Notes with id {id} does not exist!",
        )


@router.patch("/{id}", name="Update a note")
async def update_notes(
    id: Annotated[int, Path(description="Notes id")],
    updated_data: NotesDetails
) -> NotesDetails:
    """Update an existing note"""
    try:
        notes = await Notes.objects.aget(id=id)
        for attr, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(notes, attr, value)
        await notes.asave()
        return NotesDetails(**notes.model_dump())
    except Notes.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notes with id {id} does not exist!",
        )
    
@router.get("/search", name="Search notes by query")
async def search_notes(
    query: Annotated[str, Query(description="Search query for notes")]
) -> list[NotesDetails]:
    """Search notes by a query string"""
    notes = await Notes.objects.filter(title__icontains=query).all()
    if not notes:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No notes found matching the query '{query}'",
        )
    return [NotesDetails(**note.model_dump()) for note in notes]