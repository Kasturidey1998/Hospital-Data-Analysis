import pandas as pd

df = pd.read_csv("Hospital Data.csv")
print(df.head())
print(df.info())
print(df.isnull().sum())
print(df.describe())
print(df.shape)
print(df['PatientId'].nunique())
# 1. Remove negative age
df = df[df['Age'] >= 0]

df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
df['No-show'] = df['No-show'].map({'Yes': 1, 'No': 0})
df.reset_index(drop=True, inplace=True)
print(df.info())
print(df.head())
print(df['No-show'].value_counts())

import matplotlib.pyplot as plt
import seaborn as sns

# 1. No-show distribution
plt.figure(figsize=(5,4))
sns.countplot(data=df, x='No-show')
plt.title("Appointment Attendance (0=Show, 1=No-show)")
plt.show()

# 2. Gender vs No-show
plt.figure(figsize=(6,4))
sns.countplot(data=df, x='Gender', hue='No-show')
plt.title("Gender-wise Attendance")
plt.show()

# 3. Age distribution
plt.figure(figsize=(6,4))
sns.histplot(df['Age'], bins=30, kde=True)
plt.title("Age Distribution of Patients")
plt.show()

# 4. Waiting Days vs No-show
plt.figure(figsize=(6,4))
sns.boxplot(data=df, x='No-show', y='WaitingDays')
plt.title("Waiting Days vs No-show")
plt.show()

no_show_rate = df['No-show'].mean()*100
print(f"No-show Rate: {no_show_rate:.2f}%")

sns.countplot(data=df, x='Gender', hue='No-show')
plt.title("Gender-wise Attendance")
plt.show()

df['AgeGroup'] = pd.cut(df['Age'], bins=[0,12,18,35,60,100],
                        labels=['Child','Teen','Adult','MiddleAge','Senior'])

sns.barplot(data=df, x='AgeGroup', y='No-show')
plt.title("Age Group vs No-show Rate")
plt.show()

sns.boxplot(data=df, x='No-show', y='WaitingDays')
plt.title("Waiting Days vs No-show")
plt.show()

sns.barplot(data=df, x='SMS_received', y='No-show')
plt.title("SMS Reminder Effectiveness")
plt.show()

cols = ['Hipertension','Diabetes','Alcoholism','Handcap']
for c in cols:
    sns.barplot(data=df, x=df[c].astype(str), y='No-show')
    plt.title(f"{c} vs No-show Rate")
    plt.show()
 #   Neighbourhood analysis
top10 = df['Neighbourhood'].value_counts().head(10).index
sns.barplot(data=df[df['Neighbourhood'].isin(top10)],
            x='Neighbourhood', y='No-show')
plt.xticks(rotation=45)
plt.title("Top 10 Neighbourhoods vs No-show Rate")
plt.show()











