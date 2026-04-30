###############Copper-Demand_Analysis################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import adfuller
from sqlalchemy import create_engine
import statistics

# Load data
df = pd.read_excel(r"D:\Project 1\data_set (1).xlsx", sheet_name='copper_futures_data', engine='openpyxl')


# Clean column names (optional)
df.columns = [col.strip().replace(' ', '_') for col in df.columns]

#Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Convert numeric columns (remove commas, symbols, etc.)
numeric_cols = ['Open', 'High', 'Low', 'Close']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Impute nulls in numeric columns with median
for col in numeric_cols:
    median_value = df[col].median()
    df[col].fillna(median_value, inplace=True)


print("Remaining nulls:\n", df.isnull().sum())


# Check again
print(df.dtypes)
print(df.head())

# Try converting again (this time store in new column to debug)
df['Parsed_Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Check if any failed
print("Number of unparsed dates:", df['Parsed_Date'].isna().sum())

# Drop rows where conversion failed
df = df.dropna(subset=['Parsed_Date'])

# Now replace original Date column
df['Date'] = df['Parsed_Date']
df.drop(columns=['Parsed_Date'], inplace=True)



# Calculate statistics
mean = df.mean()
median = df.median()
mode = df.mode().iloc[0]

print("Mean:\n", mean)
print("\nMedian:\n", median)
print("\nMode:\n", mode)




print("====== Variance / Standard Deviation / Range ======")

for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    variance = df[col].var()
    std_dev = df[col].std()
    data_range = df[col].max() - df[col].min()
    
    print(f"\n{col}:")
    print(f"  Variance     = {variance:.2f}")
    print(f"  Std Dev      = {std_dev:.2f}")
    print(f"  Range        = {data_range:.2f}")





#Outlier Detection

#Boxplots



# Boxplot for all numeric columns
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[['Open', 'High', 'Low', 'Close', 'Volume']])
plt.title("Outlier Detection via Boxplot")
plt.xticks(rotation=45)
plt.show()

#Using IQR Method

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1

# Define outliers
outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))

# Show how many outliers in each column
print(outliers.sum())

#Time Series Analysis: Stationary vs Non-Stationary
#Kwiatkowski-Phillips-Schmidt-Shin (KPSS)



# KPSS Test on 'Close' column
# Ensure no NaNs in the series passed to KPSS
close_clean = df['Close'].dropna()

statistic, p_value, n_lags, critical_values = kpss(close_clean, regression='c', nlags='auto')

print('KPSS Statistic:', statistic)
print('p-value:', p_value)
print('Lags Used:', n_lags)
print('Critical Values:', critical_values)

if p_value < 0.05:
    print("Series is likely non-stationary (Reject H₀).")
else:
    print("Series is likely stationary (Fail to reject H₀).")

#Augmented Dickey-Fuller (ADF) Test


# Apply ADF test to 'Close' prices
# Clean 'Close' series before passing
close_clean = df['Close'].replace([float('inf'), float('-inf')], pd.NA).dropna()

# Run ADF test
result = adfuller(close_clean)

print("ADF Statistic:", result[0])
print("p-value:", result[1])

if result[1] < 0.05:
    print("Data is likely stationary.")
else:
    print("Data is likely non-stationary.")
    
#Visualization for Time Series

plt.figure(figsize=(14,6))
plt.plot(df['Close'], label='Close Price')
plt.title('Copper Futures - Close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()



# Univariate Analysis

# List of columns for univariate analysis
columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Summary statistics
print("===== Summary Statistics =====")
print(df[columns].describe())

# Histograms & KDE plots
for col in columns:
    plt.figure(figsize=(10, 4))
    sns.histplot(df[col], kde=True, bins=30, color='skyblue')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Boxplots for outlier detection
for col in columns:
    plt.figure(figsize=(6, 3))
    sns.boxplot(x=df[col], color='salmon')
    plt.title(f'Boxplot of {col}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Skewness and Kurtosis
print("\n===== Skewness & Kurtosis =====")
for col in columns:
    skew = df[col].skew()
    kurt = df[col].kurt()
    print(f"{col}: Skewness = {skew:.2f}, Kurtosis = {kurt:.2f}")
    
#Bivariate Analysis

# Compute correlation
corr_matrix = df[['Open', 'High', 'Low', 'Close', 'Volume']].corr()

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()
    

# Volume vs Close
sns.scatterplot(data=df, x='Volume', y='Close')
plt.title('Volume vs Close Price')
plt.xlabel('Volume')
plt.ylabel('Close Price')
plt.show()

# Open vs Close
sns.scatterplot(data=df, x='Open', y='Close')
plt.title('Open vs Close Price')
plt.xlabel('Open Price')
plt.ylabel('Close Price')
plt.show()


# List of columns to plot histograms for
columns_to_plot = ['Open', 'High', 'Low', 'Close', 'Volume']

# Loop through each column to create separate histograms
for col in columns_to_plot:
    plt.figure(figsize=(8, 6))  # Create a new figure for each histogram
    plt.hist(df[col], bins=50, edgecolor='black', alpha=0.7)
    plt.title(f'Histogram of {col} Prices')
    plt.xlabel(f'{col} Price (USD)' if col != 'Volume' else 'Volume')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()



#Correlation of Metals

# Load Excel with all sheets
file_path = "D:\Project 1\data_set (1).xlsx"
xls = pd.ExcelFile(file_path)

# Check sheet names
print(xls.sheet_names)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
xls = pd.ExcelFile("D:/Project 1/data_set (1).xlsx")

# Create an empty DataFrame to merge all 'Close' prices
price_df = pd.DataFrame()

# Loop through each sheet and extract cleaned Close price
for sheet in xls.sheet_names:
    df = xls.parse(sheet)
    
    # Proceed only if 'Date' and 'Close' columns exist
    if 'Date' in df.columns and 'Close' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Convert Close to numeric (invalids like ' ', '--', etc. will become NaN)
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        
        # Drop rows with missing Date or Close
        df = df[['Date', 'Close']].dropna()
        
        # Rename Close column based on sheet name
        df = df.rename(columns={'Close': f"{sheet}_Close"})
        
        # Merge into the master price_df
        if price_df.empty:
            price_df = df
        else:
            price_df = pd.merge(price_df, df, on='Date', how='outer')

# Set Date as index and sort
price_df.sort_values('Date', inplace=True)
price_df.set_index('Date', inplace=True)

# Forward fill and drop remaining missing values
price_df = price_df.fillna(method='ffill').dropna()

#Correlation
corr = price_df.corr()

#Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation of Closing Prices Across Metals")
plt.tight_layout()
plt.show()

df.to_csv("D:/Project 1/cleaned_copper_futures.csv", index=False)

# Re-load to test
df_check = pd.read_csv("D:/Project 1/cleaned_copper_futures.csv")
print(df_check.head())

