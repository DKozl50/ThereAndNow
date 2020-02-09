import pandas as pd
import numpy as np
import os

MaxFlightPrice = 100000 #30000
MaxHotelPrice = 100000 #20000
MaxRandDays = 5
MaxHotels = 100
MaxFlights = 1000000

countries = np.array([895, 4, 8, 12, 16, 20, 24, 660, 10, 28, 32, 51, 533, 36, 40, 31, 44, 48, 50, 52, 112, 56, 84, 204, 60, 64, 68, 535, 70, 72, 74, 76, 92, 96, 100, 854, 108, 116, 120, 124, 132, 136, 140, 148, 152, 156, 170, 174, 178, 184, 188, 384, 191, 192, 531, 196, 203, 408, 626, 180, 208, 86, 262, 212, 214, 218, 818, 222, 226, 232, 233, 231, 238, 234, 242, 246, 250, 260, 254, 258, 266, 270, 268, 276, 288, 292, 300, 304, 308, 312, 316, 320, 831, 324, 624, 328, 332, 340, 344, 348, 352, 356, 360, 364, 368, 372, 833, 376, 380, 388, 392, 832, 400, 398, 404, 296, 410, 414, 417, 418, 428, 422, 426, 430, 434, 438, 440, 442, 446, 450, 454, 458, 462, 466, 470, 580, 584, 474, 478, 480, 484, 583, 498, 492, 496, 499, 500, 504, 508, 104, 516, 520, 524, 528, 540, 554, 558, 562, 566, 570, 574, 807, 578, 512, 896, 586, 585, 275, 591, 598, 600, 604, 608, 612, 616, 620, 630, 634, 638, 642, 643, 646, 652, 654, 659, 662, 666, 666, 670, 882, 674, 678, 682, 686, 688, 690, 694, 702, 534, 663, 703, 705, 90, 706, 710, 728, 724, 744, 144, 729, 740, 748, 752, 756, 760, 158, 762, 834, 764, 768, 772, 776, 780, 788, 792, 795, 796, 798, -2147483648, 800, 804, 784, 826, 850, 840, 858, 860, 548, 336, 862, 704, 876, 732, 887, 894, 716, -2147483648])

ZeroDate = pd.to_datetime('2/8/2020')

class Environment:
    def gen_dataset(self):
        k = dict()
        hotels = ['Baba', 'Bubu', 'Kata']
        hotel_ind = 0
        start_date = ZeroDate

        print('Generating country_to_hotels dataset...')
        
        for i in countries:
            country_to_hotels = {'name' : [], 'day_price': [], 'available_from' : [], 'available_to' : [], 'x':[], 'y':[]}
            currx, curry = 0, 0
            if i == 40:
                currx, curry = 52.35, 13.4
            elif i == 616:
                currx, curry = 52.24, 21.0
            elif i == 36:
                currx, curry = 50.84, 4.38 
            elif i == 276:
                currx, curry = 52.5, 13.4
            elif i == 56:
                currx, curry = 50.84, 4.38 
            for _ in range(MaxHotels):
                country_to_hotels['name'].append('{}_{}'.format(hotels[hotel_ind % 3], hotel_ind))
                country_to_hotels['day_price'].append(np.random.randint(MaxHotelPrice))
                delta1 = np.random.randint(MaxRandDays - 4)
                delta2 = np.random.randint(MaxRandDays)
                country_to_hotels['available_from'].append(start_date + pd.DateOffset(days = delta1))
                country_to_hotels['available_to'].append(start_date + pd.DateOffset(days = delta1 + delta2))
                country_to_hotels['x'].append(currx + 2 * np.random.random_sample() - 1)
                country_to_hotels['y'].append(curry + 2 * np.random.random_sample() - 1)
                hotel_ind+=1

            k[i] = pd.DataFrame(data=country_to_hotels)
            
        self.country_to_hotels_ = k
        
    def __init__(self, country_to_hotels = None):
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
            self.gen_dataset()
        else:
            self.country_to_hotels_ = country_to_hotels
        
        
        print('Done')
        
    def get_tickets(self, time1, time2):
        return self.planes_timetable_[time1 : time2]
    
    def get_hotels(self, country_id, time1, time2): #datetime!!!
        return self.country_to_hotels_[country_id][
            (time1 >= self.country_to_hotels_[country_id]['available_from']) &
            (time2 <= self.country_to_hotels_[country_id]['available_to'])] 