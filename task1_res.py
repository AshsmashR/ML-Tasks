# -*- coding: utf-8 -*-
"""TASK1 RES

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zuVxKDRPZdT9awVL1evN0-0UR5GM2SKL
"""

#Task 1

#Objective: Build a machine learning model to predict the
#aggregate rating of a restaurant based on other features.


#Task: Predict Restaurant Ratings

#lets import our dataset

import pandas as pd
df = pd.read_csv("/content/resturaant.csv")
df.head()

#SUMMARY OF THE DATASET

df.info()
df.describe()
df.describe(include=['object'])

df.isnull().sum()

#CUISINES HAVE NULL VALUES, DROP

# Filling missing values
df['Cuisines'].fillna(df['Cuisines'].mode()[0], inplace=True)

df.isnull().sum()

#NOW NO MISSINNG VALUES

num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {num_duplicates}")
df = df.drop_duplicates()

#NO DUPLICATES

#NOW LETS DO EDA

#EDA
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
sns.countplot(x=df['Aggregate rating'], palette="viridis")
plt.title("Class Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

#hue is our target variable
plt.figure(figsize=(8, 5))
sns.countplot(x=df['Price range'], hue=df['Aggregate rating'], palette="viridis", legend=False)
plt.title("Class Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

#checking skewness  after class distributions
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

rating_skewness = df['Aggregate rating'].skew()
rating_kurtosis = df['Aggregate rating'].kurtosis()

rating_counts = df['Aggregate rating'].value_counts().sort_index()
print("Rating Counts:\n", rating_counts)

expected_ratings = np.arange(df['Aggregate rating'].min(), df['Aggregate rating'].max() + 0.5, 0.5)
missing_ratings = set(expected_ratings) - set(df['Aggregate rating'].unique())
print("Missing Ratings:", missing_ratings)

df['Aggregate rating'] = df['Aggregate rating'].replace(missing_ratings, np.nan)
df['Aggregate rating'] = df['Aggregate rating'].interpolate(method='linear')

plt.figure(figsize=(8,5))
sns.histplot(df['Aggregate rating'], bins=20, kde=True, color='blue')
plt.title("Updated Distribution of Ratings (After Handling Missing Bins)")
plt.xlabel("Rating")
plt.show()

print("Skewness of Ratings:", rating_skewness)
print("Kurtosis of Ratings:", rating_kurtosis)

df['Aggregate rating'] = df['Aggregate rating'].replace(0.0, np.nan)
df['Aggregate rating'] = df.groupby('Restaurant Name')['Aggregate rating'].transform(lambda x: x.fillna(x.mean()))
df['Aggregate rating'] = df['Aggregate rating'].fillna(df['Aggregate rating'].mean())

df['Aggregate rating_log'] = np.log1p(df['Aggregate rating'])  # log1p ensures no issues with log(0)

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
sns.histplot(df['Aggregate rating'], bins=20, kde=True, color='blue')
plt.title("Distribution of Aggregate ratings (Before Log Transformation)")

plt.subplot(1,2,2)
sns.histplot(df['Aggregate rating_log'], bins=20, kde=True, color='green')
plt.title("Distribution of Aggregate ratings (After Log Transformation)")

plt.show()

print("Missing values after processing:\n", df.isnull().sum())

""" Insights from Aggregate Rating Distributions (Before & After Log Transformation)
1️⃣ Before Log Transformation (Left Plot)
The distribution is slightly right-skewed, meaning lower ratings (e.g., 3.0) are more frequent.
The peak around 3.5 suggests that most restaurants are rated between 3.0 and 4.0.
Some extreme values exist at the higher end (e.g., 4.5+), which could affect model performance.
2️⃣ After Log Transformation (Right Plot)
The log transformation successfully normalizes the data by reducing skewness.
The peak remains centered around 1.5, but the data is now more evenly spread.
The extreme values at the higher end are compressed, making the distribution more suitable for linear models.


"""

df.columns

numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

# Display results
print("Numerical Columns:\n", numerical_columns)
print("\nCategorical Columns:\n", categorical_columns)

unique_cuisines = df['Cuisines'].unique()
print("Unique Cuisines (First  Samples):\n", unique_cuisines[:10])

df_cuisine_encoded = df.copy()  # Create a copy to avoid modifying the original dataframe

# One-Hot Encoding for Cuisines
df_cuisine_encoded = df_cuisine_encoded.join(df_cuisine_encoded['Cuisines'].str.get_dummies(sep=', '))

# Drop original Cuisines column after encoding
df_cuisine_encoded.drop(columns=['Cuisines'], inplace=True)

# Display the first few rows to verify encoding
print("\nTransformed Dataset with Encoded Cuisines:\n", df_cuisine_encoded.head())

#NEED TO CONVERT TO BINARY-0/1

binary_columns = ['Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu']
df[binary_columns] = df[binary_columns].replace({'Yes': 1, 'No': 0})
print("Updated Binary Encoded Columns:\n", df[binary_columns].head())

'Rating color', 'Rating text

rating_mapping = {
    'Not rated': 0,
    'Poor': 1,
    'Average': 2,
    'Good': 3,
    'Very Good': 4,
    'Excellent': 5
}

df['Rating Category'] = df['Rating text'].map(rating_mapping)
df.drop(columns=['Rating color', 'Rating text'], inplace=True)
print("Transformed Rating Category:\n", df[['Rating Category']].head())

df.head(2)

pairplot_features = ['Has Table booking', 'Has Online delivery', 'Is delivering now',
                     'Switch to order menu', 'Price range', 'Votes',
                     'Aggregate rating_log', 'Rating Category']

sns.pairplot(df[pairplot_features + ['Aggregate rating']], hue='Aggregate rating', palette="coolwarm")

plt.show()

"""### **📊 Insights from the Pairplot Analysis**

The **pairplot** provides a detailed **pairwise comparison** of numerical features with **`Aggregate rating` as the hue**. Here are the key observations:

---

### **1️⃣ Strong Correlations**
- **Votes vs. Aggregate Rating:**
  - Restaurants with **higher votes tend to have higher ratings**.
  - This indicates that **popular restaurants (high votes) generally receive better ratings**.
  - Some **outliers** exist where low-vote restaurants have high ratings.

- **Price Range vs. Aggregate Rating:**
  - Higher price range restaurants tend to have **better ratings**.
  - Suggests that **higher-priced restaurants might be associated with better quality and service**.

- **Aggregate Rating (Log) vs. Rating Category:**
  - As expected, `Aggregate rating_log` and `Rating Category` have a **strong positive correlation**.

---

### **2️⃣ Weak or No Correlation**
- **Has Table Booking, Has Online Delivery, Is Delivering Now, Switch to Order Menu vs. Aggregate Rating:**
  - No strong trend is visible.
  - This suggests that **whether a restaurant has table booking or online delivery does not significantly impact the rating**.
  - However, there are **clusters** indicating certain preferences.

---

### **3️⃣ Interesting Clusters & Patterns**
- **Low Ratings (Blue) Are More Spread Out:**
  - Lower-rated restaurants are **spread across different price ranges and vote counts**.
  - This suggests that **poor ratings can occur at any restaurant type**, irrespective of popularity.

- **Higher Ratings (Red) Form Distinct Clusters:**
  - Restaurants with high ratings (4.5+) are **densely clustered in high vote & price range areas**.
  - **Implication:** Customers prefer **high-rated** restaurants that are already popular.

---

### **4️⃣ Potential Outliers**
- Some **restaurants with a high number of votes have low ratings**.
- Similarly, some **low-price range restaurants have very high ratings**.
- These could be **niche restaurants or highly specialized places with loyal customer bases**.


"""

num_features = ['Has Table booking', 'Has Online delivery', 'Is delivering now',
                     'Switch to order menu', 'Price range', 'Votes',
                     'Aggregate rating_log', 'Rating Category']

plt.figure(figsize=(12, 6))
for i, feature in enumerate(num_features, 1):
    plt.subplot(1, len(num_features), i)
    sns.boxplot(y=df[feature], color='lightblue')
    plt.title(f"Boxplot of {feature}")

plt.tight_layout()
plt.show()


#AS WE CAN SEE OUTLIERS FROM OUR BOXPLOT WE NEED TO REMOVE

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)  # 25th percentile
    Q3 = df[column].quantile(0.75)  # 75th percentile
    IQR = Q3 - Q1  # Interquartile Range

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return df_filtered


for feature in num_features:
    df = remove_outliers(df, feature)

plt.figure(figsize=(20, 20))
for i, feature in enumerate(num_features, 1):
    plt.subplot(1, len(num_features), i)
    sns.boxplot(y=df[feature], color='lightgreen')
    plt.title(f"Boxplot After Removing Outliers: {feature}")

plt.tight_layout()
plt.show()

print("Dataset Shape After Outlier Removal:", df.shape)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_regression


#FOR FEATURE IMPORTANCE
df = pd.read_csv("cleaned_restaurant_data.csv")
df_numeric = df.select_dtypes(include=['number'])
plt.figure(figsize=(10, 6))
sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Features")
plt.show()

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_regression
import seaborn as sns
import matplotlib.pyplot as plt

categorical_columns = ['Restaurant Name', 'City', 'Address', 'Locality', 'Locality Verbose',
                       'Cuisines', 'Currency']
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le



#NOW MIF SCORES FOR FEATURE IMPORTANCE
numerical_features = df.columns.drop("Aggregate rating")
target_variable = "Aggregate rating"

mi_scores = mutual_info_regression(df[numerical_features], df[target_variable])
mi_scores_df = pd.DataFrame({'Feature': numerical_features, 'Mutual Info Score': mi_scores})
mi_scores_df = mi_scores_df.sort_values(by="Mutual Info Score", ascending=False)

plt.figure(figsize=(12, 6))
plt.barh(mi_scores_df['Feature'], mi_scores_df['Mutual Info Score'], color='skyblue')
plt.xlabel("Mutual Information Score")
plt.ylabel("Feature")
plt.title("Feature Importance (Mutual Information Scores)")
plt.gca().invert_yaxis()
plt.show()
mi_scores_df

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, f_regression

categorical_columns = ['Restaurant Name', 'City', 'Address', 'Locality', 'Locality Verbose',
                       'Cuisines', 'Currency']

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Step 3: Define the target variable and feature set
target_variable = "Aggregate rating"
X = df.drop(columns=[target_variable])
y = df[target_variable]



#NOW LETS FO SELECTKBEST - SELECT TOP 15 FEATURES WITH HIGH SCORE OF F_REGRESSION
num_features_to_select = 15
selector = SelectKBest(score_func=f_regression, k=num_features_to_select)
X_selected = selector.fit_transform(X, y)

selected_features = X.columns[selector.get_support()]
selected_features_df = pd.DataFrame({"Selected Features": selected_features})
print("Top 10 Selected Features for Model Training:")
print(selected_features_df)
df.to_csv("processed_restaurant_data.csv", index=False)

columns_to_drop = ['Address', 'Locality', 'Latitude', 'Longitude', 'Restaurant ID','Country Code','City']
df = df.drop(columns=columns_to_drop, errors='ignore')
print("Updated Columns after Dropping Unnecessary Features:")
print(df.columns)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


#NOW I NEED TO TRAIN A ML REGRESSOR MODEL

target_variable = "Aggregate rating"
X = df.drop(columns=[target_variable])
y = df[target_variable]

#SPLITTING DATA FOR TRAIN AND TEST

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xgb_model = XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=5)
xgb_model.fit(X_train, y_train)
y_pred = xgb_model.predict(X_test)



#RESGRESSOR METRICS DIFFERS
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

#results
print("Model Performance Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")

#CLEAR SIGNS OF OVERFITTING AND MODEL NEEDS MORE TRAINING

X_train.columns

df.head(5)

df = df.drop(columns=["Aggregate rating_log"], errors="ignore")

!pip install --upgrade xgboost scikit-learn

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import HistGradientBoostingRegressor

df = pd.read_csv("final_cleaned_restaurant_data.csv")
df = df.drop(columns=["Aggregate rating_log"], errors="ignore")
#WE HAVE REMOVED LOG VALUES


target_variable = "Aggregate rating"
X = df.drop(columns=[target_variable])
y = df[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#TRYING HISTGRADIENT BOOSTING REG
hgb_model = HistGradientBoostingRegressor()

param_grid = {
    "learning_rate": [0.01, 0.05, 0.1],
    "max_iter": [100, 200, 300],  # Equivalent to n_estimators in XGBoost
    "max_depth": [3, 5, 7],
    "min_samples_leaf": [10, 20, 30],
    "l2_regularization": [0.0, 0.1, 0.5]  # Regularization to reduce overfitting
}
grid_search = GridSearchCV(estimator=hgb_model, param_grid=param_grid, scoring="r2", cv=5, verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Best Hyperparameters:", best_params)
print("Best R² Score from Grid Search:", best_score)

#FOUND BEST PARAMS

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


#TUNING FINAL MODEL WITH THE BEST PARAMS

final_hgb_model = HistGradientBoostingRegressor(
    learning_rate=0.05,
    max_depth=5,
    max_iter=200,
    min_samples_leaf=10,
    l2_regularization=0.0
)


final_hgb_model.fit(X_train, y_train)
y_pred = final_hgb_model.predict(X_test)


#Model Performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

#Results
print("Final Model Performance Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")

#GOOD R-Squared Score (R²): 0.6527

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance

df = pd.read_csv("final_cleaned_restaurant_data.csv")
df = df.drop(columns=["Aggregate rating_log"], errors="ignore")

target_variable = "Aggregate rating"
X = df.drop(columns=[target_variable])
y = df[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#TUNING AGAIN A LITTLE
final_hgb_model = HistGradientBoostingRegressor(
    learning_rate=0.05,
    max_depth=7,
    max_iter=200,
    min_samples_leaf=15,
    l2_regularization=0.0
)

final_hgb_model.fit(X_train, y_train)
perm_importance = permutation_importance(final_hgb_model, X_test, y_test, n_repeats=10, random_state=42)


feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': perm_importance.importances_mean
})


feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
plt.figure(figsize=(12, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel("Feature Importance Score")
plt.ylabel("Feature")
plt.title("Feature Importance Analysis (Permutation Importance)")
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()

#NOW THIS IS THE FINAL FEATURE IMPORTANCE ANALYSIS

#I HAVE UPLOADED FILES EVERYTIME BECAUSE OF MY RUNTIME PROBLEM


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("final_cleaned_restaurant_data.csv")
df = df.drop(columns=["Aggregate rating_log"], errors="ignore")
target_variable = "Aggregate rating"
X = df.drop(columns=[target_variable])
y = df[target_variable]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#NOW WE ONLY USE THE SELECTED FEATURES

selected_features = ['Votes', 'Rating Category', 'Cuisines', 'Average Cost for two', 'Restaurant Name']
X_selected = X_train[selected_features]
X_test_selected = X_test[selected_features]
final_hgb_model_selected = HistGradientBoostingRegressor(
    learning_rate=0.05,
    max_depth=5,
    max_iter=200,
    min_samples_leaf=10,
    l2_regularization=0.0
)

final_hgb_model_selected.fit(X_selected, y_train)
y_pred_selected = final_hgb_model_selected.predict(X_test_selected)


mae = mean_absolute_error(y_test, y_pred_selected)
mse = mean_squared_error(y_test, y_pred_selected)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_selected)

#Results
print("Final Model Performance (After Feature Selection):")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("final_cleaned_restaurant_data.csv")
df = df.drop(columns=["Aggregate rating_log"], errors="ignore")
target_variable = "Aggregate rating"


df[target_variable] = pd.cut(df[target_variable], bins=[0, 1, 2, 3, 4, 5], labels=[0, 1, 2, 3, 4])

X = df.drop(columns=[target_variable])
y = df[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
selected_features = ['Votes', 'Rating Category', 'Cuisines', 'Average Cost for two', 'Restaurant Name']

X_selected = X_train[selected_features]
X_test_selected = X_test[selected_features]

final_hgb_model_selected = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_depth=5,
    max_iter=200,
    min_samples_leaf=10,
    l2_regularization=0.0
)

final_hgb_model_selected.fit(X_selected, y_train)
y_pred_selected = final_hgb_model_selected.predict(X_test_selected)

accuracy = accuracy_score(y_test, y_pred_selected)
class_report = classification_report(y_test, y_pred_selected)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(class_report)

#Test Predictions
test_predictions = pd.DataFrame({
    "True Labels": y_test,
    "Predictions": y_pred_selected
})
print("Test Predictions:")
print(test_predictions.head())

#NOW WE CAN SEE ACCURACY AND UNDERSTAND BETTER

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from imblearn.over_sampling import SMOTE

df = df.drop(columns=["Aggregate rating_log"], errors="ignore")
df["Aggregate rating"] = pd.cut(df["Aggregate rating"], bins=[0, 1, 2, 3, 4, 5], right=False, labels=[0, 1, 2, 3, 4])
df["Aggregate rating"] = df["Aggregate rating"].astype(int)

target_variable = "Aggregate rating"
X = df[['Votes', 'Rating Category', 'Cuisines', 'Average Cost for two', 'Restaurant Name']]
y = df[target_variable]

#SCALING
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

#trying smote

smote = SMOTE(sampling_strategy='auto', random_state=42)
X_scaled_resampled, y_resampled = smote.fit_resample(X_scaled, y)
X_train, X_test, y_train, y_test = train_test_split(X_scaled_resampled, y_resampled, test_size=0.2, random_state=42)

#model EXTRA TREES
extra_trees_model = ExtraTreesRegressor(n_estimators=100, random_state=42)
extra_trees_model.fit(X_train, y_train)
y_pred = extra_trees_model.predict(X_test)


#model's performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)


# Display Results
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")
test_predictions = pd.DataFrame({
    "True Labels": y_test,
    "Predictions": y_pred
})
print("Test Predictions (With ExtraTreesRegressor):")
print(test_predictions.head())

from sklearn.metrics import explained_variance_score, max_error

#Additional Performance Metrics
explained_variance = explained_variance_score(y_test, y_pred)
max_err = max_error(y_test, y_pred)
mean_bias = np.mean(y_pred - y_test)

# all performance metrics
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")
print(f"Explained Variance Score: {explained_variance:.4f}")
print(f"Max Error: {max_err:.4f}")
print(f"Mean Bias Deviation (MBD): {mean_bias:.4f}")

#Test Predictions
test_predictions = pd.DataFrame({
    "True Labels": y_test,
    "Predictions": y_pred
})
print("Test Predictions (With ExtraTreesRegressor):")
print(test_predictions.head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from imblearn.over_sampling import SMOTE


df = pd.read_csv("/content/final_cleaned_restaurant_data.csv")

df = df.drop(columns=["Aggregate rating_log"], errors="ignore")

df["Aggregate rating"] = pd.cut(df["Aggregate rating"], bins=[0, 1, 2, 3, 4, 5], right=False, labels=[0, 1, 2, 3, 4])
df["Aggregate rating"] = df["Aggregate rating"].astype(int)

target_variable = "Aggregate rating"
X = df[['Votes', 'Rating Category', 'Cuisines', 'Average Cost for two', 'Restaurant Name']]
y = df[target_variable]
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
sns.boxplot(data=X)
plt.title("Boxplot for Selected Features")

plt.subplot(2, 1, 2)
sns.boxplot(data=y)
plt.title("Boxplot for Aggregate Rating")

plt.tight_layout()
plt.show()

z_scores = np.abs(stats.zscore(X))
outliers = (z_scores > 3).any(axis=1)

X_no_outliers = X[~outliers]
y_no_outliers = y[~outliers]
scaler = RobustScaler()
X_scaled_no_outliers = scaler.fit_transform(X_no_outliers)

X_train, X_test, y_train, y_test = train_test_split(X_scaled_no_outliers, y_no_outliers, test_size=0.2, random_state=42)

smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)



extra_trees_model = ExtraTreesRegressor(n_estimators=100, random_state=42)
extra_trees_model.fit(X_train_resampled, y_train_resampled)
y_pred = extra_trees_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Display Results
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-Squared Score (R²): {r2:.4f}")

# Step 10: Display Test Predictions
test_predictions = pd.DataFrame({
    "True Labels": y_test,
    "Predictions": y_pred
})
print("Test Predictions (With ExtraTreesRegressor):")
print(test_predictions.head())

"""end

"""

