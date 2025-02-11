import pandas as pd
import pulp

def solve_timetabling(Klausurs_df, students_df, time_slots_df):
    # Extract data
    Klausurs = Klausurs_df["Klausur"].tolist()
    time_slots = time_slots_df["Zeitfenster"].tolist()

    # Student Klausur Registrations (convert DataFrame to dictionary)
    students = {}
    for _, row in students_df.iterrows():
        if row["Student"] not in students:
            students[row["Student"]] = []
        if row["Student"] is None:
            continue
        assert row["Klausur"] is not None and row["Klausur"] != "",  "Student: '" + row["Student"] + "' hat eine Zeile ohne Klausur."
        assert row["Klausur"] in Klausurs, "Klausur: '" + str(row["Klausur"]) + "' von Student: '" + row["Student"] + "' nicht definiert in Klausuren Tabelle"
        students[row["Student"]].append(row["Klausur"])

    # Create PuLP problem
    prob = pulp.LpProblem("Klausur_Timetabling", pulp.LpMinimize)

    # Decision Variables
    x = pulp.LpVariable.dicts("Schedule", [(e, t) for e in Klausurs for t in time_slots], cat=pulp.LpBinary)
    conflict_var = pulp.LpVariable.dicts("Conflict", [(s, t) for s in students for t in time_slots], cat=pulp.LpBinary)
    
    # Objective: Minimize conflicts
    prob += pulp.lpSum(conflict_var[s, t] for s in students for t in time_slots), "Minimize_Conflicts"

    # Constraints
    for e in Klausurs:
        prob += pulp.lpSum(x[e, t] for t in time_slots) == 1, f"One_Slot_{e}"

    for student, registered_Klausurs in students.items():
        for t in time_slots:
            prob += pulp.lpSum(x[e, t] for e in registered_Klausurs) <= 1 + conflict_var[student, t], f"Conflict_{student}_{t}"

    # Solve the problem
    prob.solve()

    # Collect results
    schedule = []
    for e in Klausurs:
        for t in time_slots:
            if pulp.value(x[e, t]) == 1:
                schedule.append((e, t))

    return pd.DataFrame(schedule, columns=['Klausur', 'Zeitfenster']), prob.objective.value(),
