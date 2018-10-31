import pandas
from collections import defaultdict
import scipy.special

#We create a list with the name of the .csv files
taxi_data = ['yellow_tripdata_2018-0'+str(i)+'.csv' for i in range(1,7)]

# %%
#We load the lookup tables with the name of the zone and the rispective codes
zones = pandas.read_csv('taxi _zone_lookup.csv',sep=',', encoding='ISO-8859-1')

broughs = defaultdict(list)

#We create a dictonary with as entry the name of the broughs and as values a list with the IDs of the associated zones
for number,name in list(zip(zones["LocationID"].values,zones["Borough"].values)): 
    broughs[name].append(number)
    
#We delete the IDs associated to unknow zones
broughs.pop('Unknown')
del number, name, zones
# %%

methods = ['Credit card','Cash', 'No charge', 'Dispute', 'Voided trip']

payments_method = {brough:{method: 0 for method in methods} for brough in broughs.keys()}

for month in taxi_data:

    taxi = pandas.read_csv(month,sep=',', encoding='ISO-8859-1')
    taxi = taxi[list(map(lambda x: x[2:4] == '18', taxi["tpep_pickup_datetime"].values))]
        
    for brough in broughs.keys():
        for p in (taxi.loc[taxi['PULocationID'].isin(broughs[brough])])['payment_type'].values.tolist():
            if p == 1:
                    payments_method[brough]['Credit card'] += 1
            elif p == 2:
                    payments_method[brough]['Cash'] += 1
            elif p == 3:
                    payments_method[brough]['No charge'] += 1
            elif p == 4:
                    payments_method[brough]['Dispute'] += 1
            elif p == 6:
                    payments_method[brough]['Voided trip'] += 1
del month, taxi, brough, p

pandas.DataFrame(payments_method).loc[:,[brough for brough in broughs.keys()]].iloc[:].plot(kind='bar', logy= True, figsize = (15,15))
# %%

methods = ['Credit card','Cash', 'No charge', 'Dispute']

O = [[payments_method[brough][method]for method in methods] for brough in broughs.keys()]

r = len(O)
c = len(O[0])
t = sum(sum(O[i][j]for i in range(r)) for j in range(c))

E = [[sum(O[i][k]for k in range(c))*sum(O[k][j]for k in range(r))/t for i in range(r)] for j in range(c)]
E = [[E[j][i] for j in range(c)] for i in range(r)]

chi = sum(sum(((E[i][j]-O[i][j])**2)/E[i][j] for i in range(r)) for j in range(c))
df = (r-1)*(c-1)

del r,c,t, O, E

p = 1-scipy.special.gammainc(df/2,chi/2)

print("The p-value is:",p)

del chi, df