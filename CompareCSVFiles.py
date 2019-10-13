import pandas as pd
import csv
import os, sys
from pathlib import Path

class CompareCSVFiles:

    def __init__(self):
    """Constructor. Loads the values from Fruits.csv and Vegetables.csv"""

        self._vegetable_set = set()
        self._fruit_set = set()
        self.load_fruit_values()
        self.load_vegetable_values()
        print('The fruit and vegetable values have been loaded!')

    @property
    def vegetables(self):
        return self._vegetable_set

    @vegetables.setter
    def vegetables(self, value):
        self._vegetable_set = value

    @property
    def fruits(self):
        return self._fruit_set

    @fruits.setter
    def fruits(self, value):
        self._fruit_set = value

    def load_fruit_values(self, use_ID_field=False):
        """ Loads Fruits.csv values into vegetable set.

        Parameters:
            use_ID_field
                Set to true so that we can use the CSV's ID field in Pandas dataframe.
        """
        df_fruits = pd.read_csv("./Fruits.csv", usecols=[0,1])

        #If ID field is needed, we use the Pandas dataframe instead of using a set to store values
        if use_ID_field:
            return df_fruits

        for i in df_fruits.iloc[:,1].str.strip():
            self.fruits.add(i)


    def load_vegetable_values(self, use_ID_field=False):
        """ Loads Vegetables.csv values into vegetable set.

        Parameters:
            use_ID_field
                Set to true so that we can use the CSV's ID field in Pandas dataframe.
        """

        df_vegetables = pd.read_csv("./Vegetables.csv", usecols=[0,1])

        if use_ID_field:
            return df_vegetables

        for i in df_vegetables.iloc[:,1].str.strip():
             self.vegetables.add(i)

    def clear_value_sets(self):
        """ Clear the set values, used for debugging."""

        self._vegetable_set.clear()
        self._fruit_set.clear()

    def print_vegetable_values(self):
        """ Print the values from Vegetables.csv"""

        print('These are the values from the vegetables csv file:')
        print(self.vegetables)
        print('Size of csv values: %d\r\n' %len(self.values_to_compare))

    def print_fruit_values(self):
        """ Print the values from Fruits.csv"""

        print('These are the values from the fruit csv file:')
        print(self.fruits)
        print('Size of csv Values: %d\r\n' %len(self.existing_values))

    def compare_to_fruit_values(self):
        """ Show the results of comparison of vegetable values to fruit values."""

        print('\r\nThese vegetables were not found in the fruit values:\r\n')
        print(str(self.vegetables - self.fruits))
        print('\r\nThese vegetables WERE ALSO FOUND in the fruit values %s: \r\n' %(self.vegetables & self.fruits))
        self.clear_value_sets()

    def compare_to_vegetable_values(self):
        """ Show the results of comparison of fruit values to vegetable values."""

        print('\r\nThese fruits were not found in the vegetable values:\r\n')
        print(self.fruits - self.vegetables)
        print('\r\nThese fruits WERE ALSO FOUND in the vegetable values %s: \r\n' %(self.vegetables & self.fruits))
        self.clear_value_sets()

    def show_fruits_vegetables(self):
        """ Show the union of vegetable values and fruit values."""

        print('\r\nThese are the fruit and vegetable values:\r\n')
        print(self.fruits | self.vegetables)
        self.clear_value_sets()

    def merge(self):
        """Displays all ID and fruit and vegetable values, using Pandas merge function."""

        df_vegetables = self.load_vegetable_values(use_ID_field = True)
        df_fruits = self.load_fruit_values(use_ID_field = True)
        print('Result of merged values of fruits and vegetables...\r\n')
        print(pd.merge(df_vegetables, df_fruits, on='ID'))

def print_commands():
    """ Show available commands."""

    print('\r\nThese commands are available:\r\n')
    print('compare_to_fruit_values')
    print('-Compares the vegetable values to fruit values.\r\n')
    print('compare_to_vegetable_values')
    print('-Compares the fruit values to vegetable values.\r\n')
    print('show_fruits_vegetables')
    print('-Shows all the fruit and vegetable values.\r\n')
    print('merge')
    print('-Merge the vegetable and fruit spreadsheet files and show all their ID\'s and values.\r\n')

def parse_arguments(compare_csv_files, input_command):
    """ Parses available commands and calls appropriate function in compare_csv_files object."""

    if input_command == 'compare_to_fruit_values':
        compare_csv_files.compare_to_fruit_values()
    elif input_command == 'compare_to_vegetable_values':
        compare_csv_files.compare_to_vegetable_values()
    elif input_command == 'show_fruits_vegetables':
        compare_csv_files.show_fruits_vegetables()
    elif input_command == 'merge':
        compare_csv_files.merge()

def main():
    """ Main program. Ensures that user provides correct csv directory path and processes CSV's
    when user has provided correct command."""
    
        _directory = input('Enter the directory location that contains the two CSV files that you want to compare: e.g. c:/csvfolder/\r\n')

        if Path(_directory).exists():
            csv_files = list(Path(_directory).glob('**/*.csv'))

            print('Number of CSV files found: %d' %len(csv_files))

            if len(csv_files) == 2:

                compare_csv_files = CompareCSVFiles()

                commands = ('compare_to_fruit_values', 'compare_to_vegetable_values',
                    'show_fruits_vegetables', 'merge')

                print_commands()
                command = input('Enter the command that you want.\r\n')

                while command not in commands:
                    print('Your entered an invalid command! Try entering another command.')
                    print_commands()
                    command = input('Enter the command that you want.\r\n')

                if command in commands:
                    parse_arguments(compare_csv_files, command)

            else:
                print('You need to provide the two csv files in order to compare them!')
        else:
            print('You need to enter a valid directory!')

if __name__ == '__main__':
    main()
