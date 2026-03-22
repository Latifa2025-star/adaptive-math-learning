import pandas as pd
import re
import random
import streamlit as st

# -----------------------------
# Dataset Loader
# -----------------------------

def load_asdiv_dataset():

    # small built-in sample dataset for now
    data = [
        {
            "grade": "1",
            "problem": "Tom has 3 apples. His friend gives him 2 more apples. How many apples does Tom have now?",
            "answer": "5",
            "operation": "addition"
        },
        {
            "grade": "2",
            "problem": "Sarah has 10 candies. She eats 4 candies. How many candies are left?",
            "answer": "6",
            "operation": "subtraction"
        },
        {
            "grade": "3",
            "problem": "There are 4 bags with 3 marbles in each bag. How many marbles are there in total?",
            "answer": "12",
            "operation": "multiplication"
        }
    ]

    df = pd.DataFrame(data)

    return df


# -----------------------------
# Adaptation Generator
# -----------------------------

def generate_adaptive_versions(problem, answer, operation):

    adhd_problem = f"Let's solve this step by step! {problem}"
    ell_problem = f"Read carefully. {problem}"
    id_problem = f"{problem} Think about each number slowly."

    teacher_solution = f"The correct answer is {answer}. The operation used is {operation}."

    adhd_explanation = f"Focus on the numbers and follow the steps to find {answer}."
    ell_explanation = f"We use the math operation {operation} to solve the problem."
    id_explanation = f"Start with the numbers. Use {operation}. The answer is {answer}."

    illustration_plan = {
        "type": "counters",
        "a": random.randint(2,5),
        "b": random.randint(1,4)
    }

    return {
        "teacher_solution": teacher_solution,
        "adhd_problem": adhd_problem,
        "ell_problem": ell_problem,
        "id_problem": id_problem,
        "adhd_explanation": adhd_explanation,
        "ell_explanation": ell_explanation,
        "id_explanation": id_explanation,
        "illustration_plan": illustration_plan
    }


# -----------------------------
# Illustration Renderer
# -----------------------------

def render_illustration(plan):

    if plan["type"] == "counters":

        a = plan["a"]
        b = plan["b"]

        st.write("Visual representation:")

        st.write("🔵 " * a)
        st.write("🟢 " * b)

        st.write(f"Total objects: {a + b}")


# -----------------------------
# Evaluation
# -----------------------------

def evaluate_adaptation(original, adapted):

    def extract_numbers(text):
        return re.findall(r"\d+", text)

    return {
        "numbers_preserved": extract_numbers(original) == extract_numbers(adapted),
        "original_word_count": len(original.split()),
        "adapted_word_count": len(adapted.split())
    }
