from typing import Type, Dict, List, ClassVar
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import json


class ClinicianReviewInput(BaseModel):
    evidence_repository: Dict = Field(
        ..., description="Evidence repository"
    )

    conflicts: List = Field(
        ..., description="Detected conflicts"
    )


class ClinicianReviewTool(BaseTool):
    name: str = "Clinician Review Tool"

    description: str = (
        "Generate clinician review flags for missing fields, "
        "conflicts, and unresolved discharge issues."
    )

    args_schema: Type[BaseModel] = ClinicianReviewInput

    REQUIRED_FIELDS: ClassVar[List[str]] = [
        "admission_date",
        "discharge_date",
        "principal_diagnosis",
        "discharge_medications",
        "follow_up_instructions",
        "discharge_condition"
    ]

    def _run(
        self,
        evidence_repository: Dict,
        conflicts: List,
    ) -> str:

        review_flags = []

        for field in self.REQUIRED_FIELDS:

            if not evidence_repository.get(field):

                review_flags.append(
                    {
                        "type": "missing_required_field",
                        "field": field,
                        "message": f"Missing required field: {field}"
                    }
                )

        for conflict in conflicts:

            review_flags.append(
                {
                    "type": "conflict",
                    "field": conflict["field"],
                    "message": (
                        f"Conflict detected in "
                        f"{conflict['field']}"
                    )
                }
            )

        result = {
            "review_flags": review_flags
        }

        return json.dumps(
            result,
            indent=2
        )