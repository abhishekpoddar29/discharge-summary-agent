from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from discharge_summary_agent.tools.medication_reconciliation_tool import MedicationReconciliationTool
from discharge_summary_agent.tools.conflict_detection_tool import ConflictDetectionTool
from discharge_summary_agent.tools.clinician_review_tool import ClinicianReviewTool


@CrewBase
class DischargeSummaryAgentCrew:
    """Discharge Summary Agent Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # =====================================================
    # AGENTS
    # =====================================================
    """
tools=[()]
"""
    @agent
    def document_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["document_analyst"],
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )

    @agent
    def clinical_safety_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["clinical_safety_reviewer"], 
            tools=[
                MedicationReconciliationTool(),
                ClinicianReviewTool(),
                ConflictDetectionTool()],
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )

    @agent
    def discharge_summary_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["discharge_summary_generator"],
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )

    # =====================================================
    # TASKS
    # =====================================================

    @task
    def extract_patient_evidence(self) -> Task:
        return Task(
            config=self.tasks_config["extract_patient_evidence"]
        )

    @task
    def perform_safety_review(self) -> Task:
        return Task(
            config=self.tasks_config["perform_safety_review"]
        )

    @task
    def generate_discharge_summary(self) -> Task:
        return Task(
            config=self.tasks_config["generate_discharge_summary"]
        )

    # =====================================================
    # CREW
    # =====================================================

    @crew
    def crew(self) -> Crew:
        """Creates the Discharge Summary Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False
        )

