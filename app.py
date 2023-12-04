import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.sidebar.title("Log Exporter")
uploaded_file = st.sidebar.file_uploader("Upload a file")

st.title("Steps required")
st.text("Step 1: Upload the log txt file")
st.text("""Step 2: Click Download button to export result in Excel.""")

if uploaded_file is not None:
    

    file = open('log1.txt', "r")
    lines = file.readlines()

    l = []
    for i in lines:
        if (i.find("Query") != -1 or i.find("recycle") != -1) and i.find("took") == -1:
            l.append(i)  

    timestamps, query_num, recycles, pLDDTs, pTMs, ipTMs, tols, length = [], [], [], [], [], [], [], []

    for i in l:
        if i.find("Query") != -1:
            query_match = re.search(r'Query (\d+)', i)
            if query_match:
                query_number = query_match.group(1)
            length_match = re.search(r'length (\d+)', i)
            if length_match:
                length_value = length_match.group(1)
        else:
            match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).*recycle=(\d+) pLDDT=([\d.]+) pTM=([\d.]+) ipTM=([\d.]+)( tol=([\d.]+))?", i)
            if match:
                timestamps.append(match.group(1))
                recycles.append(float(match.group(2)))
                pLDDTs.append(float(match.group(3)))
                pTMs.append(float(match.group(4)))
                ipTMs.append(float(match.group(5)))
                tols.append(float(match.group(7)) if match.group(7) else None)
                query_num.append(float(query_number))
                length.append(float(length_value))
    # Create a DataFrame
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Query_num': query_num,
        'Length' : length,
        'Recycle': recycles,
        'pLDDT': pLDDTs,
        'pTM': pTMs,
        'ipTM': ipTMs,
        'Tol': tols
    })
    def convert_to_ts(str):
        return datetime.strptime(str, "%Y-%m-%d %H:%M:%S,%f")
    df['Timestamp_final'] = df['Timestamp'].apply(convert_to_ts)
    df.drop(columns=["Timestamp"] , inplace = True)
    
    csv = df.to_csv(index = False).encode('utf-8')

    st.text("Sample Excel")

    st.dataframe(df.head(8))    
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Data-Export.csv',
    mime='text/csv')
