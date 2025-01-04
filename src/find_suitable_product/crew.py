import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# Check our tools documentations for more information on how to use them
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List, Dict

from src.find_suitable_product.tools.brave_search import BraveSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

search_tool = BraveSearchTool(api_key=os.getenv("BRAVE_API_KEY"))
scrape_website_tool = ScrapeWebsiteTool()


class ProductRequirement(BaseModel):
    purpose: str = Field(..., description="Mục đích sử dụng")
    budget: float = Field(..., description="Ngân sách")
    necessary_features: List[str] = Field(..., description="Danh sách tính năng cần có")
    preference: str = Field(..., description="Ưu tiên cá nhân")


class ProductCandidate(BaseModel):
    name: str = Field(..., description="Tên sản phẩm")
    specs: Dict[str, str] = Field(..., description="Thông số kỹ thuật chi tiết")
    price: float = Field(..., description="Giá cả")
    promotions: List[str] = Field([], description="Các ưu đãi (nếu có)")
    reviews: List[Dict[str, str]] = Field([], description="Danh sách đánh giá")
    availability: str = Field(..., description="Độ khả dụng")
    shipping_time: str = Field(..., description="Thời gian giao hàng")


class ProductComparison(BaseModel):
    feature_comparisons: List[Dict[str, str]] = Field(..., description="So sánh các tính năng")
    value_for_money: float = Field(..., description="Giá trị trên chi phí")
    expected_performance: str = Field(..., description="Hiệu suất dự kiến")
    pros_cons: List[Dict[str, str]] = Field(..., description="Danh sách  ưu, nhược điểm")


class ProductCandidateList(BaseModel):
    candidates: List[ProductCandidate] = Field(..., description="Danh sách sản phẩm ứng viên")


class ProductComparisonList(BaseModel):
    comparisons: List[ProductComparison] = Field(..., description="Danh sách so sánh sản phẩm")


@CrewBase
class FindSuitableProduct():
    """FindSuitableProduct crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_analyst'],
            verbose=True
        )

    @agent
    def evaluation_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluation_analyst'],
            tools=[
                search_tool,
                scrape_website_tool,
            ],
            verbose=True
        )

    @agent
    def suggestion_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['suggestion_expert'],
            verbose=True
        )

    @task
    def analyze_requirement_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_requirement_task'],
            output_json=ProductRequirement
        )

    @task
    def collect_candidate_task(self) -> Task:
        return Task(
            config=self.tasks_config['collect_candidate_task'],
            output_json=ProductCandidateList
        )

    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task'],
            output_json=ProductComparisonList
        )

    @task
    def suggest_task(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FindSuitableProduct crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
