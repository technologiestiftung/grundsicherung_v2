
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

plr = gpd.read_file('data/raw-data/lor/lor_planungsraeume.geojson', encoding='utf-8')

# old data: stgbxIIlor.csv
df = pd.read_csv('data/raw-data/lor/2021.csv', sep=";", dtype={'Kennung':str}, na_values=['x'], encoding='utf-8')
df = df.fillna('NA')
df = df.replace(to_replace='.', value=0)

df.set_index('Kennung', inplace=True)

data = df.join(plr.set_index('spatial_name'), rsuffix='_r')

data.rename(columns={
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\ninsgesamt)': '18-64 Jahre insgesamt',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\ninsgesamt)': 'ab 65 Jahre insgesamt',
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\nDeutsche)': '18-64 Jahre Deutsche',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\nDeutsche)': 'ab 65 Jahre Deutsche',
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\nAusländer)': '18-64 Jahre Ausländer',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\nAusländer)': 'ab 65 Jahre Ausländer'
}, inplace=True)

gpd.GeoDataFrame(data).to_file('data/preprocessed_data/xii.geojson', driver='GeoJSON', encoding='utf-8')

full_df = pd.DataFrame()

for i in range (2006, 2022):
    df = pd.read_excel('data/raw-data/lor/{}.xls'.format(str(i)), sheet_name='Tab E1', header=2, na_values=['x'])
    df['jahr'] = i
    full_df = full_df.append(df[df.iloc[:,1] == 'Berlin'], sort=False)

full_df.set_index('jahr', inplace = True)
full_df = full_df.round(2)

full_df.rename(columns={
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\ninsgesamt)': '18-64 Jahre insgesamt',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\ninsgesamt)': 'ab 65 Jahre insgesamt',
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\nDeutsche)': '18-64 Jahre Deutsche',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\nDeutsche)': 'ab 65 Jahre Deutsche',
       ' je 100 der Bevölkerung1)\n(18 - 64 Jahre,\nAusländer)': '18-64 Jahre Ausländer',
       ' je 100 der Bevölkerung1)\n(ab 65 Jahre,\nAusländer)': 'ab 65 Jahre Ausländer'
}, inplace=True)

full_df[['18-64 Jahre insgesamt',
       'ab 65 Jahre insgesamt', '18-64 Jahre Deutsche', 'ab 65 Jahre Deutsche',
       '18-64 Jahre Ausländer', 'ab 65 Jahre Ausländer']].to_csv('timeline.csv', encoding='utf-8')

full_df = full_df.round(2)
full_df.to_csv('data/preprocessed_data/timeline.csv', encoding='utf-8')

# ab 65 Jahre

#initialise empty data frame
df = pd.DataFrame()

#iterate thorugh all the xls files
#header row ist third row // start coutning at 0
#specify speacial Na values with "x" and "."
for i in range (2006, 2022):
    df_temp = pd.read_excel('data/raw-data/lor/{}.xls'.format(str(i)), sheet_name='Tab E1', header=2, na_values=['x'])
    df_temp.rename(columns={' je 100 der Bevölkerung1)\n(ab 65 Jahre,\ninsgesamt)': 'y' + str(i), 
                            'Planungsraum':'Kennung', 'Unnamed: 1':'Name'}, inplace=True)

    #solange es Planungsräume gibt
    df_temp = df_temp[df_temp.Name.notnull() & (df_temp.Name != 'Name')]
    
    #create smaller df
    df_temp = df_temp[['Kennung', 'Name', 'y' + str(i)]]

    df_temp = df_temp.round(2)
    
    print(df_temp.iloc[439:447,])
    
    if df.size == 0:
        df = df_temp
    else:
        df = df.merge(df_temp, how="right")

#replace '.' with 0
df = df.replace(to_replace='.', value=0)
df = df.round(2)
df = df.fillna('NA')


df.to_csv('data/preprocessed_data/timelapse_full.csv', encoding='utf-8')

# this setup expects the rows to always stay in the same order (e.g.: row 6 = "Empfänger/innen insgesamt").
# If the order changes, the outcome data is faulty

df_income = pd.DataFrame()

for i in range (2007, 2022):
    df_temp = pd.read_excel('data/raw-data/monatliche-statistik/grusi_{}.xls'.format(str(i)), sheet_name='Tab E8', header=2, na_values=['x'])
    df_temp.rename(columns={'Unnamed: 15': str(i), 
                            'Unnamed: 0':'nationality'}, inplace=True)
    df_temp = df_temp[df_temp.nationality.notnull() & (df_temp[str(i)].notnull())]

    
    
    if df_income.size == 0:
        df_income = df_temp[['nationality', str(i)]]
        #df.set_index('nationality', inplace = True)
    else:
        df_income[str(i)] = df_temp[str(i)]

df_income = df_income.round(2)
df_income = df_income.fillna('null')

#replace '.' with 0
df_income = df_income.replace(to_replace='.', value=0)

df_income.to_csv('data/preprocessed_data/income.csv', encoding='utf-8')

# this setup expects the rows to always stay in the same order (e.g.: row 6 = "Empfänger/innen insgesamt").
# If the order changes, the outcome data is faulty

df_rent = pd.DataFrame()

for i in range (2007, 2022):
    df_temp = pd.read_excel('data/raw-data/monatliche-statistik/grusi_{}.xls'.format(str(i)), sheet_name='Tab E6', header=3, na_values=['x'])
    df_temp.rename(columns={'Durchschnittliche\nanerkannte\nAufwendungen für\nUnterkunft und\nHeizung in \nEUR pro Monat\n(Spalte 4-17)': str(i), 
                            'Unnamed: 0':'nationality'}, inplace=True)
    df_temp = df_temp[df_temp.nationality.notnull() & (df_temp[str(i)].notnull())]

    
    
    if df_rent.size == 0:
        df_rent = df_temp[['nationality', str(i)]]
        #df.set_index('nationality', inplace = True)
    else:
        df_rent[str(i)] = df_temp[str(i)]

df_rent = df_rent.round(2)
df_rent = df_rent.fillna('null')

#replace '.' with 0
df_rent = df_rent.replace(to_replace='.', value=0)

df_rent.to_csv('data/preprocessed_data/rent.csv', encoding='utf-8')

# get data of income dataFrame
df_joined = df_income.set_index('nationality').T.iloc[:,0:1]
df_joined.rename(columns={'Empfänger/innen insgesamt':'income'}, inplace = True)

# get data of rent dataFrame
df_joined['rent'] = df_rent.set_index('nationality').T.iloc[:,0:1]

df_joined.to_csv('data/preprocessed_data/rent_income.csv', encoding='utf-8')