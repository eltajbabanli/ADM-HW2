import pandas
import matplotlib.pyplot
from collections import defaultdict

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

#We create dictonarys with as keys different time ranges that we will use to count the rides starting in these time zones
time_slots_broughs = {name:{'6-10':0, '10-12':0,'12-15':0,'15-17':0,'17-22':0,'22-6':0} for name in broughs.keys()}

time_slots = {'6-10':0, '10-12':0,'12-15':0,'15-17':0,'17-22':0,'22-6':0}

#We define a function that counts the number of trip in a data frame and put them in a dictonary
def time_slotter(taxi_df, times_dict):
#We extract, from the list of departing time, a list containing two int: one give us the year of the trip, the other the hour of the day for the trip
    for t in map(lambda x: [x[2:4],int(x[11:13])], taxi_df["tpep_pickup_datetime"].values.tolist()): 
#We ignor trips not done in the 2018 (example: wrongly registered, registered in other years)
        if t[0] == '18':
            if 6<t[1]<=10:
                times_dict['6-10']+=1
            elif 10<t[1]<=12:
                times_dict['10-12']+=1
            elif 12<t[1]<=15:
                times_dict['12-15']+=1
            elif 15<t[1]<=17:
                times_dict['15-17']+=1
            elif 17<t[1]<=22:
                times_dict['17-22']+=1
            elif 22<t[1] or t[1]<=6:
                times_dict['22-6']+=1
    return times_dict

#Now we read the files month by month to don't overload the memory and call our function time_slotter on it
for month in taxi_data:

    taxi = pandas.read_csv(month,sep=',', encoding='ISO-8859-1')

#We call the function defined above to count the total number of rides
    time_slots = time_slotter(taxi, time_slots)

#and we call it iteratively on the different broughs
    for brough in time_slots_broughs.keys():
        time_slots_broughs[brough] = time_slotter(taxi.loc[taxi['PULocationID'].isin(broughs[brough])],time_slots_broughs[brough])
    
del taxi, month, brough

#We plot the total number of rides on a histogram
matplotlib.pyplot.bar(time_slots.keys(), time_slots.values(), color='yellow')

#and in another, on a logarithmic scale, the rides for the single broughs
pandas.DataFrame(time_slots_broughs).loc[:,[brough for brough in time_slots_broughs.keys()]].iloc[:].plot(kind='bar', logy = True, figsize = (15,15))