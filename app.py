import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    initialize_database,
    add_student,
    get_students,
    update_student,
    delete_student,
    get_dashboard_stats
)

from model import (
    train_model,
    predict_marks,
    generate_recommendations
)

st.set_page_config(
    page_title="AI Student Management System",
    page_icon="🎓",
    layout="wide"
)

initialize_database()

st.title("🎓 AI-Powered Student Management System")
st.write(
    "Manage student records, analyze academic performance, "
    "and demonstrate machine learning-based marks prediction."
)

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Update Student",
        "Delete Student",
        "Predict Performance",
        "Model Evaluation"
    ]
)


def records_to_dataframe(records):
    return pd.DataFrame(
        [dict(record) for record in records]
    )


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":
    st.header("Student Dashboard")

    stats = get_dashboard_stats()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Students",
        stats["total_students"]
    )

    col2.metric(
        "Average Final Marks",
        f"{stats['average_marks']:.2f}"
    )

    col3.metric(
        "Average Attendance",
        f"{stats['average_attendance']:.1f}%"
    )

    records = get_students()

    if records:
        df = records_to_dataframe(records)

        st.subheader("Student Records")

        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df,
                x="name",
                y="final_marks",
                title="Final Marks by Student",
                labels={
                    "name": "Student",
                    "final_marks": "Final Marks"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.scatter(
                df,
                x="attendance",
                y="final_marks",
                color="student_class",
                hover_name="name",
                title="Attendance vs Final Marks",
                labels={
                    "attendance": "Attendance (%)",
                    "final_marks": "Final Marks"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No student records found. Add a student to begin.")


# ---------------- ADD STUDENT ----------------

elif menu == "Add Student":
    st.header("Register a Student")

    with st.form("add_student_form"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Student Name")
        student_class = st.text_input("Class")

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=80.0
        )

        study_hours = st.number_input(
            "Study Hours Per Day",
            min_value=0.0,
            max_value=24.0,
            value=2.0
        )

        previous_marks = st.number_input(
            "Previous Examination Marks",
            min_value=0.0,
            max_value=100.0,
            value=60.0
        )

        final_marks = st.number_input(
            "Final Examination Marks",
            min_value=0.0,
            max_value=100.0,
            value=65.0
        )

        submitted = st.form_submit_button("Save Student")

        if submitted:
            try:
                add_student(
                    student_id,
                    name,
                    student_class,
                    attendance,
                    study_hours,
                    previous_marks,
                    final_marks
                )

                st.success("Student registered successfully!")

            except Exception as error:
                st.error(f"Could not register student: {error}")


# ---------------- VIEW STUDENTS ----------------

elif menu == "View Students":
    st.header("Student Records")

    search = st.text_input("Search by Student ID or Name")

    records = get_students(search)

    if records:
        df = records_to_dataframe(records)

        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Student Records CSV",
            data=df.drop(columns=["id"]).to_csv(
                index=False
            ).encode("utf-8"),
            file_name="students.csv",
            mime="text/csv"
        )

    else:
        st.info("No matching students found.")


# ---------------- UPDATE STUDENT ----------------

elif menu == "Update Student":
    st.header("Update Student Information")

    records = get_students()

    if not records:
        st.info("No student records available.")
    else:
        df = records_to_dataframe(records)

        selected_id = st.selectbox(
            "Select Student ID",
            df["student_id"].tolist()
        )

        student = df[
            df["student_id"] == selected_id
        ].iloc[0]

        with st.form("update_student_form"):
            name = st.text_input(
                "Student Name",
                value=student["name"]
            )

            student_class = st.text_input(
                "Class",
                value=student["student_class"]
            )

            attendance = st.number_input(
                "Attendance (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(student["attendance"])
            )

            study_hours = st.number_input(
                "Study Hours Per Day",
                min_value=0.0,
                max_value=24.0,
                value=float(student["study_hours"])
            )

            previous_marks = st.number_input(
                "Previous Marks",
                min_value=0.0,
                max_value=100.0,
                value=float(student["previous_marks"])
            )

            final_marks = st.number_input(
                "Final Marks",
                min_value=0.0,
                max_value=100.0,
                value=float(student["final_marks"])
            )

            submitted = st.form_submit_button("Update Record")

            if submitted:
                try:
                    update_student(
                        selected_id,
                        name,
                        student_class,
                        attendance,
                        study_hours,
                        previous_marks,
                        final_marks
                    )

                    st.success("Student record updated.")

                except Exception as error:
                    st.error(f"Update failed: {error}")


# ---------------- DELETE STUDENT ----------------

elif menu == "Delete Student":
    st.header("Delete Student Record")

    records = get_students()

    if not records:
        st.info("No student records available.")
    else:
        df = records_to_dataframe(records)

        selected_id = st.selectbox(
            "Select Student ID to Delete",
            df["student_id"].tolist()
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this record."
        )

        if st.button("Delete Student", type="primary"):
            if confirm:
                try:
                    delete_student(selected_id)
                    st.success("Student record deleted.")

                except Exception as error:
                    st.error(f"Delete failed: {error}")
            else:
                st.warning("Please confirm before deleting.")


# ---------------- PREDICT PERFORMANCE ----------------

elif menu == "Predict Performance":
    st.header("Machine Learning Performance Prediction")

    records = get_students()

    if len(records) < 5:
        st.warning(
            "At least five student records are required "
            "for this demonstration. Add more students first."
        )

    else:
        df = records_to_dataframe(records)

        st.info(
            "The model uses attendance, study hours, and previous "
            "marks to estimate final marks. Predictions are "
            "experimental and should not be used to make "
            "high-stakes decisions about students."
        )

        try:
            model, metrics = train_model(df)

            with st.form("prediction_form"):
                attendance = st.number_input(
                    "Attendance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0
                )

                study_hours = st.number_input(
                    "Study Hours Per Day",
                    min_value=0.0,
                    max_value=24.0,
                    value=3.0
                )

                previous_marks = st.number_input(
                    "Previous Examination Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0
                )

                submitted = st.form_submit_button(
                    "Predict Final Marks"
                )

            if submitted:
                prediction = predict_marks(
                    model,
                    attendance,
                    study_hours,
                    previous_marks
                )

                st.metric(
                    "Estimated Final Marks",
                    f"{prediction:.2f} / 100"
                )

                st.subheader("Study Recommendations")

                for recommendation in generate_recommendations(
                    attendance,
                    study_hours,
                    previous_marks
                ):
                    st.write(f"- {recommendation}")

                st.caption(
                    "This estimate is based on the available "
                    "demonstration dataset, not a guarantee."
                )

        except ValueError as error:
            st.error(str(error))


# ---------------- MODEL EVALUATION ----------------

elif menu == "Model Evaluation":
    st.header("Model Evaluation")

    records = get_students()

    if len(records) < 5:
        st.warning(
            "Add at least five student records to demonstrate "
            "model evaluation."
        )

    else:
        df = records_to_dataframe(records)

        try:
            model, metrics = train_model(df)

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "MAE",
                f"{metrics['MAE']:.2f}"
            )

            col2.metric(
                "RMSE",
                f"{metrics['RMSE']:.2f}"
            )

            if metrics["R2"] is not None:
                col3.metric(
                    "R² Score",
                    f"{metrics['R2']:.3f}"
                )
            else:
                col3.metric("R² Score", "Unavailable")

            st.write(
                "**MAE:** Mean absolute difference between "
                "actual and predicted marks."
            )

            st.write(
                "**RMSE:** Square root of the mean squared "
                "prediction error."
            )

            st.write(
                "**R²:** Measures how well predictions explain "
                "variation in the test-set marks."
            )

            st.warning(
                "These metrics are based on the current dataset. "
                "A small synthetic dataset cannot establish "
                "real-world predictive performance."
            )

        except ValueError as error:
            st.error(str(error))


st.sidebar.divider()

st.sidebar.caption(
    "IBM SkillsBuild Machine Learning & Applied AI Internship"
)