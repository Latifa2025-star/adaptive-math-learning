import pandas as pd
import streamlit as st
import re
import random


# -----------------------------
# Load datasets
# -----------------------------

def load_asdiv_dataset():

    df = pd.read_csv("asdiv_full.csv")

    df = df.rename(columns={
        "question": "problem",
        "answer": "answer"
    })

    df["grade"] = "1-2"
    df["dataset"] = "ASDiv"
    df["operation"] = "basic"

    return df[["problem", "answer", "grade", "dataset", "operation"]]


def load_gsm8k_dataset():

    df = pd.read_csv("gsm8k_test.csv")

    df = df.rename(columns={
        "question": "problem",
        "answer": "answer"
    })

    df["grade"] = "3-8"
    df["dataset"] = "GSM8K"
    df["operation"] = "multi-step"

    return df[["problem", "answer", "grade", "dataset", "operation"]]


# -----------------------------
# Adaptation generator
# -----------------------------

def generate_adaptive_versions(problem, answer, operation):

    adhd_problem = f"Focus time! Let's solve this together.\n\n{problem}"

    ell_problem = f"Read slowly.\n\n{problem}\n\nThink about the numbers."

    id_problem = f"Step 1: Read the problem.\n\n{problem}\n\nStep 2: Use the numbers to solve it."

    teacher_solution = f"The answer is {answer}. The math operation used is {operation}."

    adhd_explanation = f"Look at the numbers carefully. Follow the steps to find {answer}."

    ell_explanation = f"We solve the problem using {operation}. The answer is {answer}."

    id_explanation = f"Start with the numbers. Use {operation}. The answer becomes {answer}."

    illustration_plan = {
        "type": "counters",
        "a": random.randint(2,6),
        "b": random.randint(1,5)
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
# Illustration generator
# -----------------------------

def render_illustration(plan):

    if plan["type"] == "counters":

        a = plan["a"]
        b = plan["b"]

        st.write("### Visual Illustration")

        st.write("🍎 " * a)
        st.write("🍏 " * b)

        st.write(f"Total objects = {a+b}")


# -----------------------------
# Evaluation
# -----------------------------

def evaluate_adaptation(original, adapted):

    def extract_numbers(text):
        return re.findall(r"\d+", text)

    return {
        "numbers_preserved": extract_numbers(original) == extract_numbers(adapted),
        "original_words": len(original.split()),
        "adapted_words": len(adapted.split())
    }
