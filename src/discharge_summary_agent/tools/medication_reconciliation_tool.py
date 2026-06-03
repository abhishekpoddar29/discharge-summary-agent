from typing import Type, List, Dict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import json
import re


class MedicationReconciliationInput(BaseModel):
    admission_medications: List[str] = Field(
        ..., description="Admission medications"
    )
    discharge_medications: List[str] = Field(
        ..., description="Discharge medications"
    )


class MedicationReconciliationTool(BaseTool):
    name: str = "Medication Reconciliation Tool"
    description: str = (
        "Compare admission and discharge medications. "
        "Detect additions, removals, dose changes, "
        "frequency changes, and route changes."
    )

    args_schema: Type[BaseModel] = MedicationReconciliationInput

    def _parse_medication(self, medication_text: str) -> Dict:

        medication_text = medication_text.strip()

        name_match = re.match(r"^[A-Za-z0-9\-]+", medication_text)

        medication_name = (
            name_match.group(0).lower()
            if name_match
            else medication_text.lower()
        )

        dose_match = re.search(
            r"(\d+\s*(mg|mcg|g|ml|units))",
            medication_text,
            re.IGNORECASE,
        )

        route_match = re.search(
            r"\b(PO|IV|IM|SC|SQ|Topical|Inhaled)\b",
            medication_text,
            re.IGNORECASE,
        )

        frequency_match = re.search(
            r"\b(QD|BID|TID|QID|PRN|Daily|Weekly)\b",
            medication_text,
            re.IGNORECASE,
        )

        return {
            "name": medication_name,
            "dose": dose_match.group(1) if dose_match else None,
            "route": route_match.group(0).upper()
            if route_match
            else None,
            "frequency": frequency_match.group(0).upper()
            if frequency_match
            else None,
            "raw": medication_text,
        }

    def _run(
        self,
        admission_medications: List[str],
        discharge_medications: List[str],
    ) -> str:

        admission = {
            self._parse_medication(med)["name"]:
            self._parse_medication(med)
            for med in admission_medications
        }

        discharge = {
            self._parse_medication(med)["name"]:
            self._parse_medication(med)
            for med in discharge_medications
        }

        added = []
        removed = []
        modified = []

        admission_names = set(admission.keys())
        discharge_names = set(discharge.keys())

        for med in discharge_names - admission_names:
            added.append(discharge[med])

        for med in admission_names - discharge_names:
            removed.append(admission[med])

        for med in admission_names.intersection(discharge_names):

            admission_med = admission[med]
            discharge_med = discharge[med]

            changes = []

            if admission_med["dose"] != discharge_med["dose"]:
                changes.append(
                    {
                        "type": "dose_change",
                        "before": admission_med["dose"],
                        "after": discharge_med["dose"],
                    }
                )

            if admission_med["frequency"] != discharge_med["frequency"]:
                changes.append(
                    {
                        "type": "frequency_change",
                        "before": admission_med["frequency"],
                        "after": discharge_med["frequency"],
                    }
                )

            if admission_med["route"] != discharge_med["route"]:
                changes.append(
                    {
                        "type": "route_change",
                        "before": admission_med["route"],
                        "after": discharge_med["route"],
                    }
                )

            if changes:
                modified.append(
                    {
                        "medication": med,
                        "changes": changes,
                    }
                )

        result = {
            "added": added,
            "removed": removed,
            "modified": modified,
        }

        return json.dumps(result, indent=2)