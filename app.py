
import streamlit as st
import csv
import math

st.set_page_config(
    page_title = "Heart Disease task_1",
    layout="wide"
)

st.title(" Heart Disease Prediction Task 1")
st.write("Dataset viewer with manual parsing, sorting and pagination")


file_path = "heart.csv"

with open(file_path,"r",encoding="utf-8") as file:
    first_line = file.readline()

possible_delimiters = [",", ";", "\\t", "|"]

delimiter = ","

for d in possible_delimiters:
    if d in first_line:
        delimiter = d
        break

st.info(f"Detected delimiter: {repr(delimiter)}")

# -----------------------------
# Manually read CSV
# -----------------------------

data = []

with open(file_path, "r", encoding="utf-8") as file:

    reader = csv.reader(file, delimiter=delimiter)

    rows = list(reader)

    headers = rows[0]

    for row in rows[1:]:

        if len(row) == len(headers):

            record = {}

            for i in range(len(headers)):
                record[headers[i]] = row[i]

            data.append(record)

st.success(f"Total records: {len(data)}")

# -----------------------------
# Sorting
# -----------------------------

st.subheader("Sort Dataset")

sort_column = st.selectbox(
    "Select column",
    headers
)

sort_order = st.radio(
    "Sort order",
    ["Ascending", "Descending"],
    horizontal=True
)

def sort_key(row):
    value = row[sort_column]

    try:
        return float(value)
    except:
        return value.lower()

sorted_data = sorted(
    data,
    key=sort_key,
    reverse=(sort_order == "Descending")
)

# -----------------------------
# Pagination
# -----------------------------

st.subheader("Dataset")

rows_per_page = st.selectbox(
    "Rows per page",
    [5, 10, 20, 50],
    index=1
)

total_rows = len(sorted_data)

total_pages = math.ceil(total_rows / rows_per_page)

page_number = st.number_input(
    "Page number",
    min_value=1,
    max_value=max(1, total_pages),
    value=1,
    step=1
)

start_index = (page_number - 1) * rows_per_page

end_index = start_index + rows_per_page

page_data = sorted_data[start_index:end_index]

# -----------------------------
# Display dataset
# -----------------------------

st.dataframe(
    page_data,
    use_container_width=True
)

st.write(
    f"Showing rows {start_index + 1} "
    f"to {min(end_index, total_rows)} "
    f"of {total_rows}"
)

st.write(
    f"Page {page_number} of {total_pages}"
)

