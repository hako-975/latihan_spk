import sys

from colorama import Fore, Style
from models import Base, SportsCar, House
from engine import engine

from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

def review_data():
    query = select(SportsCar)
    for car in session.scalars(query):
        print(car)

def get_data():
    query = select(SportsCar)
    return [{'brand': car.brand, 'type': car.type, 'origin_country': car.country, 'top_speed': car.top_speed} for car in session.scalars(query)]


class SimpleAdditiveWeighting():

    def __init__(self):
        # 1-5
        self.raw_weight = {'developer': 5, 'lt': 3, 'lb': 2, 'price': 4}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k,v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(House)
        return [{'developer': DEV_SCALE[house.developer], 'lt': house.lt, 'lb': house.lb, 'price': house.price} for house in session.scalars(query)]
    
    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        developers = [] # max
        lts = [] # max
        lbs = [] # max
        prices = [] # min
        for data in self.data:
            developers.append(data['developer'])
            lts.append(data['lt'])
            lbs.append(data['lb'])
            prices.append(data['price'])

        max_developer = max(developers)
        max_lt = max(lts)
        max_lb = max(lbs)
        min_price = min(prices)

        return [
            {
                'developer': data['developer']/max_developer, # benefit
                'lt': data['lt']/max_lt, # benefit
                'lb': data['lb']/max_lb, # benefit
                'price': min_price/data['price'] # cost
                }
            for data in self.data
        ]

    @property
    def final_result(self):
        weight = self.weight
        return [
            round(row['developer'] * weight['developer'] +
            row['lt'] * weight['lt'] +
            row['lb'] * weight['lb'] +
            row['price'] * weight['price'], 2)
            for row in self.normalized_data
            ]


class WeightedProduct():
    pass


def run_saw():
    saw = SimpleAdditiveWeighting()
    # {'developer': 5, 'lt': 3, 'lb': 2, 'price': 4}
    print('result:', saw.final_result)

def run_wp():
    wp = WeightedProduct()
    pass

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')