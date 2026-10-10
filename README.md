AI-Powered Student Management System
1. Project Information
Project Name: AI-Powered Student Management System
Internship: IBM SkillsBuild Machine Learning & Applied AI
Programming Language: Python
Frontend: Streamlit
Database: SQLite
Machine Learning: Scikit-learn
Data Analysis: Pandas and NumPy
Visualization: Plotly
2. Abstract

The AI-Powered Student Management System is a web application designed to manage student information and analyze academic performance.

The system allows administrators to register students, search records, update information, and view performance statistics.

A Random Forest regression model demonstrates how machine learning can estimate examination marks using attendance, daily study hours, and previous examination marks.

The application also provides data visualizations, model evaluation metrics, and study recommendations.

3. Problem Statement

Managing student records manually can be time-consuming. Teachers and administrators may also need convenient tools to explore academic performance and identify opportunities for additional student support.

This project combines database management, data visualization, and a machine learning demonstration in one application.

4. Objectives
Create and manage student records.
Store student information in an SQLite database.
Display student performance statistics.
Visualize attendance and examination marks.
Demonstrate machine learning-based marks prediction.
Evaluate predictions using standard regression metrics.
Provide general study recommendations.
Export student records to CSV.
5. Features
Student registration.
Student search.
Student record updates and deletion.
Dashboard with performance statistics.
Interactive charts.
Machine learning marks prediction.
MAE, RMSE, and R² evaluation metrics.
CSV downloads.
6. Dataset

The included students.csv contains fictional student records created for demonstration.

The columns include:

student_id
name
student_class
attendance
study_hours
previous_marks
final_marks

The dataset is small and synthetic. It should not be used to claim reliable real-world predictive performance.

7. Machine Learning Methodology

The project uses a Random Forest regression model.

Input Features
Attendance percentage.
Daily study hours.
Previous examination marks.
Target Variable
Final examination marks.
Evaluation

The dataset is split into training and test subsets. The model is evaluated using:

Mean Absolute Error (MAE).
Root Mean Squared Error (RMSE).
R² score, when available.

The metrics are calculated from the current data. No model accuracy is assumed in advance.

8. Installation

Install Python on your computer.

Open a terminal in the project directory and execute:

pip install -r requirements.txt

9. Initialize the Database

Run:

python database.py


The students.db file will be created automatically.

10. Run the Application

Execute:

streamlit run app.py


Open the local address shown in the terminal.

11. Project Structure
AI_Student_Management_System/
├── app.py
├── database.py
├── model.py
├── requirements.txt
├── README.md
├── students.csv
└── students.db

12. Limitations
The sample dataset is small and synthetic.
Model predictions are demonstrations, not guaranteed examination results.
Study recommendations use simple rules.
The application does not include user authentication.
Student information must be protected when deploying the application.
13. Future Scope
Add secure administrator authentication.
Import student records from CSV.
Use a larger, suitable real-world dataset.
Compare multiple machine learning algorithms.
Add attendance alerts.
Generate downloadable student performance reports.
Improve privacy and access controls.
14. Conclusion

The project demonstrates how Python, SQLite, Streamlit, and Scikit-learn can be combined to create a student management application with basic analytics and a machine learning demonstration.

It is intended for educational purposes and can be extended with more robust data, model evaluation, and security features.