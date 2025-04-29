import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Basic Configuration
warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Fix for displaying negative signs

# --- Checklist Step 1: Load Data ---
print("\n--- 1. Loading Data ---")
file_path = 'report/Customers churned in telecom services/customer_churn_telecom_services.csv'
try:
    df = pd.read_csv(file_path)
    print(f"Successfully loaded data from {file_path}")
    print("First 5 rows:")
    print(df.head().to_markdown(index=False))
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# --- Checklist Step 2: Initial Inspection ---
print("\n--- 2. Initial Inspection ---")
print("DataFrame Info:")
df.info()
print("\nInitial Missing Values:")
print(df.isnull().sum())

# --- Checklist Step 3: Clean TotalCharges ---
print("\n--- 3. Cleaning TotalCharges ---")
# Convert TotalCharges to numeric, coercing errors (spaces become NaN)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Check how many NaNs were introduced
nan_count = df['TotalCharges'].isnull().sum()
print(f"Found {nan_count} rows with non-numeric TotalCharges (converted to NaN).")

# Investigate NaN rows, often related to tenure=0
nan_rows = df[df['TotalCharges'].isnull()][['tenure', 'MonthlyCharges', 'TotalCharges']]
print("Rows where TotalCharges became NaN:")
if not nan_rows.empty:
    print(nan_rows.to_markdown(index=False))
    # Impute NaN TotalCharges with 0 where tenure is 0
    zero_tenure_nan_indices = nan_rows[nan_rows['tenure'] == 0].index
    if not zero_tenure_nan_indices.empty:
        df.loc[zero_tenure_nan_indices, 'TotalCharges'] = 0
        print(f"Imputed {len(zero_tenure_nan_indices)} NaN TotalCharges with 0 for tenure=0 customers.")
    else:
        print("No NaN TotalCharges found for tenure=0 customers. Further investigation needed if NaNs remain.")
else:
    print("No rows found where TotalCharges became NaN.")


# Verify imputation
print("\nMissing Values After Cleaning TotalCharges:")
print(df.isnull().sum())
# Drop any remaining rows with NaN TotalCharges if they exist (shouldn't based on common cases)
df.dropna(subset=['TotalCharges'], inplace=True)
print(f"DataFrame shape after handling TotalCharges NaN: {df.shape}")


# --- Checklist Step 4: Convert SeniorCitizen ---
print("\n--- 4. Converting SeniorCitizen ---")
df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
print("Converted SeniorCitizen to 'Yes'/'No':")
print(df['SeniorCitizen'].value_counts())

# Add customerID removal - often not useful for analysis itself
if 'customerID' in df.columns:
    print("\nRemoving customerID column.")
    df = df.drop('customerID', axis=1, errors='ignore')


# --- Checklist Step 5 & 6: Overall Churn Rate & Visualization ---
print("\n--- 5 & 6. Overall Churn Rate ---")
churn_rate = df['Churn'].value_counts(normalize=True) * 100
print("Overall Churn Rate (%):")
print(churn_rate)

plt.figure(figsize=(6, 4))
sns.countplot(x='Churn', data=df, palette='viridis')
plt.title('整体客户流失分布')
plt.xlabel('是否流失')
plt.ylabel('客户数量')
plt.tight_layout()
plt.savefig('churn_distribution.png')
print("Saved plot: churn_distribution.png")
# plt.show() # Keep commented out for non-interactive execution

# --- Checklist Step 7: Demographic Analysis vs. Churn ---
print("\n--- 7. Demographic Analysis vs. Churn ---")
demographic_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
fig, axes = plt.subplots(1, len(demographic_cols), figsize=(18, 5), sharey=True)
fig.suptitle('人口统计特征与客户流失关系', fontsize=16)

for i, col in enumerate(demographic_cols):
    sns.countplot(x=col, hue='Churn', data=df, ax=axes[i], palette='viridis')
    axes[i].set_title(f'{col} vs Churn')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('客户数量' if i == 0 else '')
    axes[i].tick_params(axis='x', rotation=10)

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
plt.savefig('demographic_churn_analysis.png')
print("Saved plot: demographic_churn_analysis.png")
# plt.show()

# --- Checklist Step 8 & 9: Tenure Analysis vs. Churn ---
print("\n--- 8 & 9. Tenure Analysis vs. Churn ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('客户任期 (Tenure) 与流失关系', fontsize=16)

# Histogram
sns.histplot(data=df, x='tenure', hue='Churn', kde=True, ax=axes[0], palette='viridis')
axes[0].set_title('任期分布 (按是否流失区分)')
axes[0].set_xlabel('任期 (月)')
axes[0].set_ylabel('客户数量')

# Box Plot
sns.boxplot(x='Churn', y='tenure', data=df, ax=axes[1], palette='viridis')
axes[1].set_title('任期箱线图 (按是否流失区分)')
axes[1].set_xlabel('是否流失')
axes[1].set_ylabel('任期 (月)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('tenure_churn_analysis.png')
print("Saved plot: tenure_churn_analysis.png")
# plt.show()

avg_tenure = df.groupby('Churn')['tenure'].mean()
print("\nAverage Tenure by Churn Status:")
print(avg_tenure)

# --- Checklist Step 10: Phone/MultipleLines Analysis vs. Churn ---
print("\n--- 10. Phone Service Analysis vs. Churn ---")
phone_cols = ['PhoneService', 'MultipleLines']
fig, axes = plt.subplots(1, len(phone_cols), figsize=(12, 5), sharey=True)
fig.suptitle('电话服务与客户流失关系', fontsize=16)

for i, col in enumerate(phone_cols):
    sns.countplot(x=col, hue='Churn', data=df, ax=axes[i], palette='viridis')
    axes[i].set_title(f'{col} vs Churn')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('客户数量' if i == 0 else '')
    axes[i].tick_params(axis='x', rotation=10)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('phone_churn_analysis.png')
print("Saved plot: phone_churn_analysis.png")
# plt.show()

# --- Checklist Step 11: Internet Service Analysis vs. Churn ---
print("\n--- 11. Internet Service Analysis vs. Churn ---")
internet_cols = ['InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
n_cols = 3
n_rows = (len(internet_cols) + n_cols - 1) // n_cols # Calculate rows needed
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows), sharey=True)
fig.suptitle('互联网服务与客户流失关系', fontsize=16)
axes = axes.flatten() # Flatten axes array for easy iteration

for i, col in enumerate(internet_cols):
    sns.countplot(x=col, hue='Churn', data=df, ax=axes[i], palette='viridis')
    axes[i].set_title(f'{col} vs Churn')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('客户数量' if i % n_cols == 0 else '')
    axes[i].tick_params(axis='x', rotation=10)

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0.03, 1, 0.97]) # Adjust layout
plt.savefig('internet_churn_analysis.png')
print("Saved plot: internet_churn_analysis.png")
# plt.show()

# --- Checklist Step 12: Account Info Analysis vs. Churn ---
print("\n--- 12. Account Information Analysis vs. Churn ---")
account_cols = ['Contract', 'PaperlessBilling', 'PaymentMethod']
n_cols = 3
n_rows = (len(account_cols) + n_cols - 1) // n_cols
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows), sharey=True)
fig.suptitle('账户信息与客户流失关系', fontsize=16)
axes = axes.flatten()

for i, col in enumerate(account_cols):
    sns.countplot(x=col, hue='Churn', data=df, ax=axes[i], palette='viridis')
    axes[i].set_title(f'{col} vs Churn')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('客户数量' if i % n_cols == 0 else '')
    axes[i].tick_params(axis='x', rotation=15) # Increased rotation for payment method

# Hide unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('account_churn_analysis.png')
print("Saved plot: account_churn_analysis.png")
# plt.show()


# --- Checklist Step 13 & 14: MonthlyCharges Analysis vs. Churn ---
print("\n--- 13 & 14. Monthly Charges Analysis vs. Churn ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('月度费用 (MonthlyCharges) 与流失关系', fontsize=16)

# Histogram
sns.histplot(data=df, x='MonthlyCharges', hue='Churn', kde=True, ax=axes[0], palette='viridis')
axes[0].set_title('月度费用分布 (按是否流失区分)')
axes[0].set_xlabel('月度费用')
axes[0].set_ylabel('客户数量')

# Box Plot
sns.boxplot(x='Churn', y='MonthlyCharges', data=df, ax=axes[1], palette='viridis')
axes[1].set_title('月度费用箱线图 (按是否流失区分)')
axes[1].set_xlabel('是否流失')
axes[1].set_ylabel('月度费用')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('monthlycharges_churn_analysis.png')
print("Saved plot: monthlycharges_churn_analysis.png")
# plt.show()

# --- Checklist Step 15 & 16: TotalCharges Analysis vs. Churn ---
print("\n--- 15 & 16. Total Charges Analysis vs. Churn ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('总费用 (TotalCharges) 与流失关系', fontsize=16)

# Histogram
sns.histplot(data=df, x='TotalCharges', hue='Churn', kde=True, ax=axes[0], palette='viridis')
axes[0].set_title('总费用分布 (按是否流失区分)')
axes[0].set_xlabel('总费用')
axes[0].set_ylabel('客户数量')

# Box Plot
sns.boxplot(x='Churn', y='TotalCharges', data=df, ax=axes[1], palette='viridis')
axes[1].set_title('总费用箱线图 (按是否流失区分)')
axes[1].set_xlabel('是否流失')
axes[1].set_ylabel('总费用')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('totalcharges_churn_analysis.png')
print("Saved plot: totalcharges_churn_analysis.png")
# plt.show()

# --- Checklist Step 17 & 18: Numerical Feature Correlation ---
print("\n--- 17 & 18. Numerical Feature Correlation ---")
numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
correlation_matrix = df[numerical_cols].corr()
print("Correlation Matrix:")
print(correlation_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
plt.title('数值特征相关性热力图')
plt.tight_layout()
plt.savefig('numerical_correlation_heatmap.png')
print("Saved plot: numerical_correlation_heatmap.png")
# plt.show()

print("\n--- Analysis Script Completed ---") 