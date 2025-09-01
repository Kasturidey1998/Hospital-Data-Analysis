import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load data
df = pd.read_csv("Hospital Data.csv")

# Cleaning
df = df[df['Age'] >= 0]
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
df['No-show'] = df['No-show'].map({'Yes': 1, 'No': 0})

# -----------------------------
# Streamlit UI
st.title("Hospital Appointment No-Show Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
age_min, age_max = st.sidebar.slider("Select Age Range", int(df['Age'].min()), int(df['Age'].max()), (0, 100))
sms_filter = st.sidebar.multiselect("SMS Received", options=df['SMS_received'].unique(), default=df['SMS_received'].unique())

# Apply filters
filtered_df = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Age'].between(age_min, age_max)) &
    (df['SMS_received'].isin(sms_filter))
]

# -----------------------------
# Basic stats
st.subheader("Dataset Overview (Filtered)")
st.write(f"Total Records: {filtered_df.shape[0]}")
st.write(f"No-show Rate: {filtered_df['No-show'].mean()*100:.2f}%")
st.dataframe(filtered_df.head())

# Gender vs No-show
st.subheader("Gender vs No-show")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='Gender', hue='No-show', ax=ax)
st.pyplot(fig)

# Age distribution
st.subheader("Age Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df['Age'], bins=30, kde=True, ax=ax)
st.pyplot(fig)

# Waiting days vs No-show
st.subheader("Waiting Days vs No-show")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x='No-show', y='WaitingDays', ax=ax)
st.pyplot(fig)

# SMS reminder effectiveness
st.subheader("SMS Reminder Effectiveness")
fig, ax = plt.subplots()
sns.barplot(data=filtered_df, x='SMS_received', y='No-show', ax=ax)
st.pyplot(fig)

# -----------------------------
# NEW: Medical Conditions
medical_cols = ['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']

st.subheader(" Medical Conditions vs No-show Rate")
for c in medical_cols:
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_df, x=c, y='No-show', ax=ax)
    ax.set_title(f"{c} vs No-show Rate")
    st.pyplot(fig)
