from typing import Type, Dict, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import json


class ConflictDetectionInput(BaseModel):
    evidence_repository: Dict = Field(
        ..., description="Evidence repository JSON"
    )


class ConflictDetectionTool(BaseTool):
    name: str = "Conflict Detection Tool"

    description: str = (
        "Detect conflicting values extracted from patient documents."
    )

    args_schema: Type[BaseModel] = ConflictDetectionInput

    def _run(self, evidence_repository: Dict) -> str:

        conflicts = []

        fields_to_check = [
            "admission_date",
            "discharge_date",
            "principal_diagnosis",
            "secondary_diagnoses",
            "allergies",
            "procedures",
            "follow_up_instructions",
            "discharge_condition"
        ]

        for field in fields_to_check:

            values = []

            for item in evidence_repository.get(field, []):

                value = str(
                    item.get("value", "")
                ).strip()

                if value:
                    values.append(value)

            unique_values = list(set(values))

            if len(unique_values) > 1:

                conflicts.append(
                    {
                        "field": field,
                        "values": unique_values,
                        "type": "conflicting_information"
                    }
                )

        return {
            "conflicts": conflicts
        }