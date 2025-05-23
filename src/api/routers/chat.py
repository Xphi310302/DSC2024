"""
This module defines FastAPI endpoints for chat.
"""

from fastapi import (status,
                     Depends,
                     APIRouter,
                     HTTPException)

from src.services.service import Service
from src.api.dependencies.dependency import get_service
from src.api.schemas.chat import (RequestChat,
                                  ResponseChat)


chat_router = APIRouter(
    tags=["Chat"],
    prefix="/chat",
)


@chat_router.post(
    '/chatDomain',
    status_code=status.HTTP_200_OK,
    response_model=ResponseChat
)
async def chat_domain(
    request_chat: RequestChat,
    service: Service = Depends(get_service)
) -> ResponseChat:
    """
    Endpoint to handle chat queries and retrieve responses from the chat engine.

    Args:
        request_chat (RequestChat): An object containing the chat query.
        service (Service, optional): Dependency injection for the service layer.
                                     Defaults to Depends(get_service).

    Returns:
        ResponseChat: An object containing the chat response and a flag  
                      indicating if the query was out of the expected domain.
    """
    if not request_chat.query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query is required"
        )
    try:
        result = await service.retrieve_chat_engine.preprocess_query(
            query=request_chat.query
        )
        await service.chat_repository.add_chat_domains(
            query=request_chat.query,
            answer=result.response,
            retrieved_nodes=result.retrieved_nodes,
            is_out_of_domain=result.is_outdomain
        )
        return ResponseChat(
            response=result.response,
            is_outdomain=result.is_outdomain
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)) from e
