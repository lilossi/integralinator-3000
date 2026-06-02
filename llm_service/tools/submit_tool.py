from langchain_core.tools import tool
from pydantic import BaseModel, Field


class IntegralList(BaseModel):
    expressions: list[str] = Field(description="A list of mathematical expressions for the integrals.")


# global storage
submitted_integrals: set[str] = set()


def reset_submitted_integrals() -> None:
    submitted_integrals.clear()


@tool(args_schema=IntegralList)
def submit_generated_integrals(expressions: list[str]) -> str:
    """Submit the final list of selected integrals. Call this at the end of every turn."""
    old_count = len(submitted_integrals)
    submitted_integrals.update(expressions)
    added_count = len(submitted_integrals) - old_count
    print(f"Submitted {expressions} — {added_count} new, {len(submitted_integrals)} total.")
    return f"Saved {added_count} new expressions (total: {len(submitted_integrals)})."
