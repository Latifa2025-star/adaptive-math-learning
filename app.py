import streamlit as st
import pandas as pd
from utils import (
    load_asdiv_dataset,
    generate_adaptive_versions,
    render_illustration,
    evaluate_adaptation
)

st.set_page_config(
    page_title="Adaptive Math Learning",
    layout="wide"
)

st.title("Adaptive Math Learning Studio")
st.caption(
    "AI-powered adaptation of math word problems for ADHD, ELL, and Intellectual Disability learners"
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Controls")

dataset_name = st.sidebar.selectbox(
    "Select Dataset",
    ["ASDiv"]
)

grade_filter = st.sidebar.selectbox(
    "Filter by Grade",
    ["All", "1", "2", "3", "4", "5", "6"]
)

# -----------------------------
# Load Dataset
# -----------------------------

df = load_asdiv_dataset()

if grade_filter != "All":
    df = df[df["grade"] == grade_filter]

problem_list = df["problem"].tolist()

selected_problem = st.sidebar.selectbox(
    "Select a Math Problem",
    problem_list
)

selected_row = df[df["problem"] == selected_problem].iloc[0]

# -----------------------------
# Display Original Problem
# -----------------------------

st.subheader("Original Problem")

col1, col2, col3 = st.columns(3)

col1.metric("Grade", selected_row["grade"])
col2.metric("Answer", selected_row["answer"])
col3.metric("Operation", selected_row["operation"])

st.write(selected_row["problem"])

# -----------------------------
# Generate Adaptations
# -----------------------------

if st.sidebar.button("Generate Adaptive Lesson"):

    with st.spinner("Generating adaptive explanations..."):

        result = generate_adaptive_versions(
            problem=selected_row["problem"],
            answer=selected_row["answer"],
            operation=selected_row["operation"]
        )

    st.divider()

    tabs = st.tabs(["Teacher", "ADHD", "ELL", "ID"])

    # -----------------------------
    # Teacher Tab
    # -----------------------------

    with tabs[0]:

        st.subheader("Teacher Solution")

        st.write(result["teacher_solution"])

        st.markdown("### Evaluation")

        eval_data = evaluate_adaptation(
            selected_row["problem"],
            result["adhd_problem"]
        )

        st.json(eval_data)

    # -----------------------------
    # ADHD Tab
    # -----------------------------

    with tabs[1]:

        st.subheader("ADHD Adaptation")

        st.write(result["adhd_problem"])

        st.markdown("### Explanation")

        st.write(result["adhd_explanation"])

        st.markdown("### Illustration")

        render_illustration(result["illustration_plan"])

    # -----------------------------
    # ELL Tab
    # -----------------------------

    with tabs[2]:

        st.subheader("ELL Adaptation")

        st.write(result["ell_problem"])

        st.markdown("### Explanation")

        st.write(result["ell_explanation"])

        st.markdown("### Illustration")

        render_illustration(result["illustration_plan"])

    # -----------------------------
    # ID Tab
    # -----------------------------

    with tabs[3]:

        st.subheader("ID Adaptation")

        st.write(result["id_problem"])

        st.markdown("### Explanation")

        st.write(result["id_explanation"])

        st.markdown("### Illustration")

        render_illustration(result["illustration_plan"])
