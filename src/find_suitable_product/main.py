#!/usr/bin/env python
import sys
import warnings

from find_suitable_product.crew import FindSuitableProduct

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'product': 'Màn hình',
        'requirement': 'Tôi muốn mua 1 màn hình 24 inch 1k hoặc 2k, phục vụ cho công việc lập trình, ngân sách khoảng 3 triệu, ưu tiên màn bảo vệ mắt. Có loa và có cổng usb type c thì càng tốt nhưng không bắt buộc.',
        'location': 'Vietnam'
    }
    FindSuitableProduct().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'product': 'laptop'
    }
    try:
        FindSuitableProduct().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FindSuitableProduct().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        'product': 'laptop'
    }
    try:
        FindSuitableProduct().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
