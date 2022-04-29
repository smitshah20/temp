import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from django.shortcuts import render


data = pd.read_excel('C:/Users/aagjo/OneDrive/Desktop/WebApp/Cohort/authentication/Online Retail_5k.xlsx')

data.head(5)

def explore(x):
    divider = "*_*"
    print("\n {} \n".format((divider*20))) 
    print("Dataframe Makeup \n") 
    x.info() 
    
    print("\n {} \n".format((divider*20))) 
    print("Descriptive Statistics \n\n", x.describe().round(2))
    print("\n {} \n".format((divider*20))) 
    print("Shape of dataframe: {}".format(x.shape)) 
    print("\n {} \n".format((divider*20))) 
    return

explore(data)

def missing_data(x):
    return x.isna().sum()

missing_data(data)

cleaned_data = data.dropna(subset=['CustomerID'])

explore(cleaned_data)
cleaned_data.head()

def get_month(x):
    return dt.datetime(x.year, x.month, 1)

cleaned_data['InvoiceMonth'] = cleaned_data['InvoiceDate'].apply(get_month)

cleaned_data['CohortMonth'] = cleaned_data.groupby('CustomerID')['InvoiceMonth'].transform('min')

def get_date(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day

invoice_year, invoice_month, _ = get_date(cleaned_data, 'InvoiceMonth') 

#invoice_month[:30]
#invoice_year[:30]

cohort_year, cohort_month, _ = get_date(cleaned_data, 'CohortMonth')

year_diff = invoice_year - cohort_year
month_diff = invoice_month - cohort_month

cleaned_data['CohortIndex'] = year_diff * 12 + month_diff + 1

cohort_data = cleaned_data.groupby(
    ['CohortMonth', 'CohortIndex'])['CustomerID'].apply(pd.Series.nunique).reset_index()

cohort_count = cohort_data.pivot_table(index = 'CohortMonth',
                                    columns = 'CohortIndex',
                                    values = 'CustomerID')
                
cohort_size = cohort_count.iloc[:,0] 
retention = cohort_count.divide(cohort_size, axis=0) 
retention.round(3)

plt.figure(figsize = (11,9))
plt.title('Cohort Analysis - Retention Rate')
sns.heatmap(data = retention, 
            annot = True, 
            fmt = '.0%', 
            vmin = 0.0,
            vmax = 0.5,
            cmap = "YlGnBu")
plt.show()
        