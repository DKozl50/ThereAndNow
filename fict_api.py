import pandas as pd
import numpy as np
from tqdm import tqdm_notebook

MaxFlightPrice = 40000
MaxHotelPrice = 10000 # for a night
MaxRandDays = 100
MaxHotels = 500
MaxFlights = 100000

ZeroDate = pd.to_datetime('8/2/2020')

class Environment:
    def gen_dataset(self, countries):
        k = dict()
        hotels = ['Alpha_hotel', 'Mega_hotel', 'Super_hotel']
        hotel_ind = 0
        start_date = ZeroDate

        print('Generating country_to_hotels dataset...')
        
        for i in tqdm_notebook(countries):
            country_to_hotels = {'name' : [], 'day_price': [], 'available_from' : [], 'available_to' : []}

            for _ in range(MaxHotels):
                country_to_hotels['name'].append('{}_{}'.format(hotels[hotel_ind % 3], hotel_ind))
                country_to_hotels['day_price'].append(np.random.randint(MaxHotelPrice))

                delta1 = np.random.randint(MaxRandDays)
                delta2 = np.random.randint(MaxRandDays//2)
                country_to_hotels['available_from'].append(start_date + pd.DateOffset(days = delta1))
                country_to_hotels['available_to'].append(start_date + pd.DateOffset(days = delta1 + delta2))

                hotel_ind+=1

            k[i] = pd.DataFrame(data=country_to_hotels)
            
        self.country_to_hotels_ = k
        
    def __init__(self, countries, country_to_hotels = None):
        print('Generating time_to_planes dataset...')
        
        d = {'time' : [], 'price': [], 'from': [], 'to' : []}
        start_date = ZeroDate
        
        for i in range(MaxFlights):
            if i % (MaxFlights // (MaxRandDays * 2)) == 0: 
                start_date += pd.DateOffset(days = 1)
                
            d['time'].append(start_date)
            d['price'].append(np.random.randint(MaxFlightPrice))
            d['from'].append(countries[np.random.randint(countries.size)])
            d['to'].append(countries[np.random.randint(countries.size)])

        self.planes_timetable_ = pd.DataFrame(data=d).set_index('time')
    
        if (country_to_hotels == None):
            self.gen_dataset(countries)
        else:
            self.country_to_hotels_ = country_to_hotels
        
        
        print('Done')
        
    def get_tickets(self, time1, time2):
        return self.planes_timetable_[time1 : time2]
    
    def get_hotels(self, country_id, time1, time2): #datetime!!!
        return self.country_to_hotels_[country_id][
            (time1 > self.country_to_hotels_[country_id]['available_from']) &
            (time2 < self.country_to_hotels_[country_id]['available_to'])] 
