import streamlit as st
import pandas as pd
from io import BytesIO
from LinearProgram import solve_timetabling


# Streamlit UI
st.title("Klausuren Zeitplanungs Solver")

# Create three columns for displaying tables side by side
col1, col2, col3 = st.columns(3)

# Predefined editable tables
def create_editable_table(data, key):
    return st.data_editor(pd.DataFrame(data), key=key, num_rows="dynamic", height=300)

Klausurs_data = {"Klausur": ["Mathematik", "Physik", "Chemie", "Biologie", "Geschichte"]}
students_data = {"Student": ["Alice", "Alice", "Bob", "Bob", "Charlie", "Charlie", "David", "David", "Eva", "Eva", "Frank", "Frank", "Grace", "Grace", "Henry", "Henry", "Irene", "Irene", "Jack", "Jack", "Katie", "Katie", "Liam", "Liam"], "Klausur": ["Mathematik", "Physik", "Mathematik", "Chemie", "Biologie", "Geschichte", "Physik", "Chemie", "Mathematik", "Geschichte", "Physik", "Chemie", "Mathematik", "Biologie", "Chemie", "Geschichte", "Physik", "Geschichte", "Biologie", "Geschichte", "Mathematik", "Chemie", "Physik", "Biologie"]}
time_slots_data = {"Zeitfenster": ["Montag, 09:00", "Montag, 14:00", "Dienstag, 09:00", "Dienstag, 14:00"]}


with col1:
    st.write("### Klausuren")
    Klausurs_df = create_editable_table(Klausurs_data, "Klausurs")
with col2:
    st.write("### Studenten")
    students_df = create_editable_table(students_data, "students")
with col3:
    st.write("### Zeitfenster")
    time_slots_df = create_editable_table(time_slots_data, "time_slots")
    

if st.button("Löse Zeitplanproblem"):
    schedule_df, obj_value = solve_timetabling(Klausurs_df, students_df, time_slots_df)
    if int(obj_value) == 1:
        st.write("### Generierter Zeitplan mit einer Überschneidung.")
    else:
        st.write(f"### Generierter Zeitplan mit {int(obj_value)} Überschneidungen.")
    st.dataframe(schedule_df)
    
    # Convert DataFrame to Excel for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        schedule_df.to_excel(writer, index=False, sheet_name='Schedule')
    output.seek(0)
    
    st.download_button(
        label="Lade Zeitplan herunter",
        data=output,
        file_name="Klausur_schedule.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
