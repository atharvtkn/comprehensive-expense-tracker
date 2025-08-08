import csv
import pandas
from datetime import datetime
import matplotlib.pyplot as plt

class ExpTracker:
    def __init__(self):
        self.path = 'expenses.csv'
        self.figure = None

        self.options = [
                'HOUSING',
                'TRANSPORT',
                'FOOD',
                'UTILITIES',
                'HEALTHCARE',
                'MISC'
            ]

    def add_expense(self, name, amount, category):
        if not name.strip() or not str(amount).strip():
            error_message = 'Please fill in all fields.'
            return False, error_message
        
        try:
            float(amount)
        except ValueError:
            error_message = 'Amount must be a number.'
            return False, error_message
        
        timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        new_row = [name, amount, category, timestamp]
        
        with open(self.path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        
        return True, 'Expense added.'

    def expense_summary(self):
        self.data_list = []

        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.data_list.append(row)

        self.df = pandas.DataFrame(columns=['Expenses', 'Amount', 'Category', 'Date & Time'], data=self.data_list)
        
        if self.df.empty:
            return False, 'No transactions yet.', None
        
        return True, self.df.to_string(index=False), self.df
    
    def expense_visualization(self):
        housing = 0
        transportation = 0
        food = 0
        utilities = 0
        healthcare = 0
        miscellaneous = 0

        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == 'HOUSING':
                    housing += float(row[1])
                elif row[2] == 'TRANSPORTATION':
                    transportation += float(row[1])
                elif row[2] == 'FOOD':
                    food += float(row[1])
                elif row[2] == 'UTILITIES':
                    utilities += float(row[1])
                elif row[2] == 'HEALTHCARE':
                    healthcare += float(row[1])
                elif row[2] == 'MISCELLANEOUS':
                    miscellaneous += float(row[1])
        
        data_labels = self.options
        data_values = [housing, 
                       transportation, 
                       food, 
                       utilities, 
                       healthcare, 
                       miscellaneous]
        colors = ['#DEF5E5', '#BCEAD5', '#9ED5C5', '#8EC3B0', '#73AF99', '#64A38C']

        self.figure = plt.figure()
        plt.bar(data_labels, data_values, color=colors)
        plt.xticks(rotation=30, ha='right')  # rotate labels to prevent overlap
        plt.ylabel('Amount Spent')
        plt.xlabel('EXPENSE CATEGORIES')
        plt.title(f'Spending by Category - Total ${sum(data_values):.2f} spent')
        plt.tight_layout() # adds spacing below and above, accoring to the labels

        for bars in range(len(self.options)):
            plt.text(bars, 
                    data_values[bars] + 0.1,
                    f'${data_values[bars]:.2f}', 
                    ha='center', 
                    va='bottom')

        plt.show(block=False)

    def restart_expense(self):
        open(self.path, 'w').close()