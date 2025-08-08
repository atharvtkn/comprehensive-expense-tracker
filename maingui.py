import main
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt

class maingui:
    def __init__(self):
        self.et = main.ExpTracker()
        
        self.root = ctk.CTk()
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('green')
        self.root.geometry('900x700')
        self.root.title('ET')
        self.options = [
            'HOUSING',
            'TRANSPORTATION',
            'FOOD',
            'UTILITIES',
            'HEALTHCARE',
            'MISCELLANEOUS'
        ]

        self.title_label = ctk.CTkLabel(
            self.root,
            text = 'EXPENSE TRACKER',
            font = ('Courier New', 30), 
            text_color = '#DEF5E5'
        )
        self.title_label.pack(pady = (5, 30))

        self.exp_label_name = ctk.CTkLabel(
            self.root,
            text = '⮮ INPUT THE EXPENSE NAME ⮯',
            font = ('Consolas', 16),
            text_color = '#BCEAD5'
        )
        self.exp_label_name.pack(pady = (0,1))

        self.exp_entry_name = ctk.CTkEntry(
            self.root,
            width = 300,
            font = ('Consolas', 16),
            text_color = '#8EC3B0'
        )
        self.exp_entry_name.pack(pady = (0,5))

        self.exp_label_amount = ctk.CTkLabel(
            self.root,
            text = '⮮ INPUT THE EXPENSE AMOUNT ⮯',
            font = ('Consolas', 16),
            text_color = '#BCEAD5'
        )
        self.exp_label_amount.pack(pady = (0,1))

        self.exp_entry_amount = ctk.CTkEntry(
            self.root,
            width = 300,
            font = ('Consolas', 16),
            text_color = '#8EC3B0'
        )
        self.exp_entry_amount.pack(pady = (0,5))

        self.exp_label_category = ctk.CTkLabel(
            self.root,
            text = '⮮ PICK THE EXPENSE CATEGORY ⮯',
            font = ('Consolas', 16),
            text_color = '#BCEAD5'
        )
        self.exp_label_category.pack(pady = (0,1))

        self.choice = ctk.StringVar()
        self.choice.set(self.options[-1]) # sets the default value as misc for the options (looks clean as fuck)

        self.exp_optionmenu_category = ctk.CTkOptionMenu(
            self.root,
            variable = self.choice,
            values = self.options,
            width = 300,
            font = ('Consolas', 16),
            text_color = '#00301E'
        )
        self.exp_optionmenu_category.pack(pady = (0,5))

        self.add_exp_button = ctk.CTkButton(
            self.root,
            text = 'ADD EXPENSE',
            font = ('Consolas', 16),
            text_color = '#00301E',
            command=self.exp_adder
        )
        self.add_exp_button.pack(pady = (10, 5))

        self.show_summary_button = ctk.CTkButton(
            self.root,
            text = 'SHOW EXPENSES SUMMARY',
            font = ('Consolas', 16),
            text_color = '#00301E',
            command=self.summary
        )
        self.show_summary_button.pack(pady = 5)

        self.exp_visualize_button = ctk.CTkButton(
            self.root,
            text = 'VISUALIZE EXPENSES',
            font = ('Consolas', 16),
            text_color = '#00301E',
            command=self.visualize
        )
        self.exp_visualize_button.pack(pady = 5)

        self.close_visualize_button = ctk.CTkButton(
            self.root,
            text = 'CLOSE VISUALIZATION',
            font = ('Consolas', 16),
            text_color = '#00301E',
            command=self.devisualize
        )
        self.close_visualize_button.pack(pady = 5)

        self.exp_clear_button = ctk.CTkButton(
            self.root,
            text = 'RESET ALL EXPENSE DATA',
            font = ('Consolas', 16),
            text_color = '#00301E',
            command=self.clear_data
        )
        self.exp_clear_button.pack(pady = 5)

        self.terminal_label = ctk.CTkLabel(
            self.root,
            text = '⮮ TERMINAL ⮯',
            font = ('Consolas', 16),
            text_color = '#BCEAD5'
        )
        self.terminal_label.pack(pady = (5, 0))

        self.terminal = ctk.CTkTextbox(
            self.root,
            width = 700,
            height = 200,
            font = ('Consolas', 14),
            text_color = '#9ED5C5'
        )
        self.terminal.pack(pady = (0, 5))
        self.terminal.configure(state='disabled')

        self.root.mainloop()
        
    def update_terminal(self, message):
        self.terminal.configure(state='normal')       # enable editing
        self.terminal.delete('1.0', 'end')            # delete previous output
        self.terminal.insert('end', message + '\n')   # append message
        self.terminal.configure(state='disabled')     # make it read-only again

    def exp_adder(self):
        name = self.exp_entry_name.get()
        amount = self.exp_entry_amount.get()
        category = self.choice.get()
        
        checker, message = self.et.add_expense(name, amount, category)
        
        if not checker:
            self.update_terminal(message)
            return
        
        self.update_terminal(message)
    
    def summary(self):
        checker, self.string_df, self.dataframe = self.et.expense_summary()
        
        if not checker:
            self.update_terminal(self.string_df)
            return
        
        total = self.dataframe.iloc[:, 1].astype(float).sum()
        self.string_df += f'\n\nTotal amount of expenses: ${total:.2f}' # add more shit

        self.update_terminal(self.string_df)
    
    def visualize(self):
        if self.et.figure:
            self.update_terminal('Visualization already running - Reopen to see updates.')
            return
        
        self.et.expense_visualization()
        self.update_terminal('Visualized file.')
    
    def devisualize(self):
        if not self.et.figure:
            self.update_terminal('No visualization running.')
            return
        
        plt.close(self.et.figure)
        self.et.figure = None
        self.update_terminal('Closed visualization.')
    
    def clear_data(self):
        confirm = CTkMessagebox(title = 'Reset Expenses File',
                                message = 'Are you sure you want to clear all expense data?',
                                icon='warning',
                                option_1='No',
                                option_2='Yes'   
        )

        if confirm.get() == 'Yes':
            self.et.restart_expense()
            self.update_terminal('Expenses file cleared.')
            return
        
        self.update_terminal('Expenses file NOT cleared.')

if __name__ == '__main__':
    gui = maingui()