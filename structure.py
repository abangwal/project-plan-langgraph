from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import List, Dict, Annotated, TypedDict, Sequence
import operator


class KeyPointsSchema(BaseModel):
    """Key points to consider while conducting market research"""

    steps: List[str] = Field(
        description="Points to consider while market research, points should be in correct order"
    )


class PlanSchema(BaseModel):
    """Detailed plan to achieve the task"""

    plan: List[str] = Field(
        description="Plan to follow to complete a step to achieve the objecetive, plan should be in correct order"
    )


class GraderSchema(BaseModel):
    """Grade and feedback for agents response for reflection"""

    grade: int = Field(
        description="Marks out of 10 based on the response of agent for the given objective"
    )
    feedback: str = Field(description="What is missing and how agent can improve")


class GraphState(TypedDict):
    task: str
    feedback: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    steps: List[str]
    plan: Dict[str, List[str]]
    sender: str
    next_node: str
