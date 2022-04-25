# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
data = pd.read_csv(r'C:\Users\samas\Downloads\usa_00002.csv.gz', compression='gzip',
                   error_bad_lines=False)

data.head()
data = data.loc[data['MET2013'] != 0]
data.head()

data.columns
# Dropping unecessary columns
data1 = data.drop(columns = ["SAMPLE","SERIAL","CBSERIAL","CLUSTER","HHWT","STRATA","GQ", "PERNUM",'RACED', 'EDUCD'])
data1['YEAR'].unique()
data1['SEX'].unique()
#1                   White
#2                   Black/African American/Negro
#3                   American Indian or Alaska Native
#4                   Chinese
#5                   Japanese
#6                   Other Asian or Pacific Islander
#7                   Other race, nec
#8                   Two major races
#9                   Three or more major races
#data1 = data1.loc[(data1['RACE'] != 7) & (data1['RACE'] != 8) & (data1['RACE'] != 9)]
data1['RACE'].unique()
# Reduciong the Races classification to Just 5 groups
data1.loc[(data1.RACE == 5),'RACE'] = 4
data1.loc[(data1.RACE == 6),'RACE'] = 4
data1.loc[(data1.RACE == 7),'RACE'] = 5
data1.loc[(data1.RACE == 8),'RACE'] = 5
data1.loc[(data1.RACE == 9),'RACE'] = 5
data1.RACE.isna().sum()
data1.RACE.unique()
# Updated Race groups
#1                   White
#2                   Black/African American/Negro
#3                   American Indian or Alaska Native
#4                   Asian
#5                   Other races
races_percent_metro = data1.groupby(by = ['YEAR', 'MET2013', 'RACE'])['PERWT'].sum().div(data1.groupby(by = ['YEAR', 'MET2013'])['PERWT'].sum())
races_percent = pd.DataFrame(races_percent_metro).reset_index()
white_percent = races_percent.loc[races_percent.RACE == 1].reset_index().drop(columns = ['index'])
black_percent = races_percent.loc[races_percent.RACE == 2].reset_index().drop(columns = ['index'])
native_percent = races_percent.loc[races_percent.RACE == 3].reset_index().drop(columns = ['index'])
asian_percent = races_percent.loc[races_percent.RACE == 4].reset_index().drop(columns = ['index'])
other_percent = races_percent.loc[races_percent.RACE == 5].reset_index().drop(columns = ['index'])
#--------------------------------------------------------------------------------------------------------------------------------------------------

races_final_pct = pd.merge(white_percent, native_percent, how ="outer", on = ["YEAR", "MET2013"])
races_final_pct = pd.merge(races_final_pct, black_percent, how ="outer", on = ["YEAR", "MET2013"])
races_final_pct = pd.merge(races_final_pct, asian_percent, how ="outer", on = ["YEAR", "MET2013"])
races_final_pct = pd.merge(races_final_pct, other_percent, how ="outer", on = ["YEAR", "MET2013"])
races_final_pct.isna().sum()
races_final_pct.fillna(0, inplace = True)
races_final_pct.to_csv(r'C:\Users\samas\Downloads\races_pct_met.csv')
#00                  N/A or no schooling
#01                  Nursery school to grade 4
#02                  Grade 5, 6, 7, or 8
#03                  Grade 9
#04                  Grade 10
#05                  Grade 11
#06                  Grade 12
#07                  1 year of college
#08                  2 years of college
#09                  3 years of college
#10                  4 years of college
#11                  5+ years of college
data1.EDUC.unique()
data1.loc[(data1.EDUC >= 0) & (data1.EDUC < 6), 'EDUC'] = 1
data1.loc[(data1.EDUC == 6), 'EDUC'] = 2
data1.loc[(data1.EDUC >= 7) & (data1.EDUC < 10), 'EDUC'] = 3
data1.loc[(data1.EDUC == 10), 'EDUC'] = 4
data1.loc[(data1.EDUC == 11), 'EDUC'] = 5
data1.EDUC.unique()
# Updated Education groups
#1 schooling or less than highschool or NA
#2 graduated highschool or 12th ongoing
#3 attended/attending college
#4 completed 4 yrs clg or final year
#5 5+ yrs of clg
educ_percent_by_metro = data1.groupby(by = ["YEAR" ,"MET2013","EDUC"])['PERWT'].sum().div(data1.groupby(by = ['YEAR', 'MET2013'])['PERWT'].sum())
educ_pct = pd.DataFrame(educ_percent_by_metro).reset_index()
less_than_highschool = educ_pct.loc[educ_pct.EDUC == 1].reset_index().drop(columns = ['index'])
highschool = educ_pct.loc[educ_pct.EDUC == 2].reset_index().drop(columns = ['index'])
attended_clg = educ_pct.loc[educ_pct.EDUC == 3].reset_index().drop(columns = ['index'])
bachelors = educ_pct.loc[educ_pct.EDUC == 4].reset_index().drop(columns = ['index'])
mas_phd = educ_pct.loc[educ_pct.EDUC == 5].reset_index().drop(columns = ['index'])
#----------------------------------------------------------------------------------------------------------------------
educ_final_pct = pd.merge(less_than_highschool, highschool, how = 'outer', on = ["YEAR", "MET2013"])
educ_final_pct = pd.merge(educ_final_pct, attended_clg, how = 'outer', on = ["YEAR", "MET2013"])
educ_final_pct = pd.merge(educ_final_pct, bachelors, how = 'outer', on = ["YEAR", "MET2013"])
educ_final_pct = pd.merge(educ_final_pct, mas_phd, how = 'outer', on = ["YEAR", "MET2013"])
educ_final_pct.to_csv(r'C:\Users\samas\Downloads\educ_pct_met.csv')


data1.SEX.unique()
#1                   Male
#2                   Female
sex_pct_metro = data1.groupby(by = ["YEAR", "MET2013", "SEX"])["PERWT"].sum().div(data1.groupby(by = ['YEAR', 'MET2013'])['PERWT'].sum())
sex_pct = pd.DataFrame(sex_pct_metro).reset_index()
male_pct = sex_pct.loc[sex_pct.SEX == 1].reset_index().drop(columns = ['index'])
male_pct.to_csv(r'C:\Users\samas\Downloads\male_pct_met.csv')

#-----------------------------------------------------------------------------------------------------------------------------
print(len(data1.loc[data1.AGE < 15]))
# Age Groups
#<15 - 0
#16-19 1
#20-24 2
#25-34 3
#35-44 4
#45-54 5
#55-64 6
#65+  7
data1.loc[data1.AGE <= 15, "AGE"] = 0
data1.loc[(data1.AGE >= 16) & (data1.AGE <= 19), "AGE"] = 1
data1.loc[(data1.AGE >= 20) & (data1.AGE <= 24), "AGE"] = 2
data1.loc[(data1.AGE >= 25) & (data1.AGE <= 34), "AGE"] = 3
data1.loc[(data1.AGE >= 35) & (data1.AGE <= 44), "AGE"] = 4
data1.loc[(data1.AGE >= 45) & (data1.AGE <= 54), "AGE"] = 5
data1.loc[(data1.AGE >= 55) & (data1.AGE <= 64), "AGE"] = 6
data1.loc[(data1.AGE >= 65), "AGE"] = 7
#---------------------------------------------------------------------------------------------------------------------------------
data1.AGE.unique()
age_pct_metro = data1.groupby(by = ["YEAR", "MET2013", "AGE"])["PERWT"].sum().div(data1.groupby(by = ['YEAR', 'MET2013'])['PERWT'].sum())
age_pct = pd.DataFrame(age_pct_metro).reset_index()
age_bl_15 = age_pct.loc[age_pct.AGE == 0].reset_index().drop(columns = ['index'])
age_16_19 = age_pct.loc[age_pct.AGE == 1].reset_index().drop(columns = ['index'])
age_20_24 = age_pct.loc[age_pct.AGE == 2].reset_index().drop(columns = ['index'])
age_25_34 = age_pct.loc[age_pct.AGE == 3].reset_index().drop(columns = ['index'])
age_35_44 = age_pct.loc[age_pct.AGE == 4].reset_index().drop(columns = ['index'])
age_45_54 = age_pct.loc[age_pct.AGE == 5].reset_index().drop(columns = ['index'])
age_55_64 = age_pct.loc[age_pct.AGE == 6].reset_index().drop(columns = ['index'])
age_ab_65 = age_pct.loc[age_pct.AGE == 7].reset_index().drop(columns = ['index'])
#---------------------------------------------------------------------------------------------------------------------------------------
age_final_pct = pd.merge(age_bl_15, age_16_19, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_20_24, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_25_34, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_35_44, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_45_54, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_55_64, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct = pd.merge(age_final_pct, age_ab_65, how = "outer", on = ["YEAR", "MET2013"])
age_final_pct.isna().sum()
age_final_pct.to_csv(r'C:\Users\samas\Downloads\age_pct_met.csv')

# Got the Dataset from Vincent, made on Rstudio.
du_dim = pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\df_DIM_DU_annual.csv")

Y = du_dim.DU
X = du_dim.DIM
X = sm.add_constant(X)
initial_model = sm.OLS(Y, X).fit()
initial_model.summary()

race = pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\races_pct_met.csv")
educ = pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\educ_pct_met.csv")
age =  pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\age_pct_met.csv")
sex =  pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\male_pct_met.csv")


dfs = [du_dim, race, educ, age, sex]
dfs = [x.set_index(["YEAR", "MET2013"]) for x in dfs]
final_data = pd.concat(dfs, axis = 1)
final_data.reset_index(inplace = True)

final_data.columns
final_data.drop(columns = ["Unnamed: 0"], inplace = True)
final_data.drop(columns = ["row_total"], inplace = True)

final_data.to_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\final_data.csv")


###########################################################################################################################################################################################################################################


import statsmodels.api as sm
import numpy as np
import pandas as pd
from linearmodels import PanelOLS
from linearmodels import RandomEffects

final_data = pd.read_csv(r"C:\Users\samas\OneDrive\Desktop\Capstone\final_data.csv")
final_data.drop(columns = ['Unnamed: 0'], inplace = True)
final_data.columns
basic_mod = sm.OLS(final_data.DU, sm.add_constant(final_data.DIM)).fit()
basic_mod.summary()

# Adding Control Variables

endog = final_data.DU
exog = sm.add_constant(final_data.drop(['YEAR', 'MET2013','DU','pct_native','schooling', 'bl_15', ], axis = 1))
comprehensive_mod = sm.OLS(endog, exog).fit()
comprehensive_mod.summary()


year = pd.Categorical(final_data.YEAR)
data = final_data.set_index(["YEAR", "MET2013"])
data['year'] = year
exog_vars = sm.add_constant(data.drop(["DU", ]))
