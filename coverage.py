# This file converts a range coverage data to variables which can be outputted on the coverage page

from data import publishers_ordered_by_title
from data import get_publisher_stats


def is_number(s):
    """ Tests if a variable is a number.
        Input: s - a variable
        Return: True if v is a number
                False if v is not a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def convert_to_int(x):
    """ Converts a variable to an integer value, or 0 if it cannot be converted to an integer.
        Input: x - a variable
        Return: x as an integer, or zero if x is not a number
    """
    if is_number(x):
        return int(x)
    else:
        return 0


def table():
    """Generate data for the publisher coverage table
    """

    # Loop over each publisher
    for publisher_title, publisher in publishers_ordered_by_title:

        # Store the data for this publisher as a new variable
        publisher_stats = get_publisher_stats(publisher)
        
        # Create a list for publisher data, and populate it with basic data
        row = {}
        row['publisher'] = publisher
        row['publisher_title'] = publisher_title


        # Compute 2014 IATI spend
        iati_2014_spend_total = 0
        transactions_usd = publisher_stats['sum_transactions_by_type_by_year_usd']

        if '2014' in transactions_usd.get('3', {}).get('USD', {}):
            iati_2014_spend_total += transactions_usd['3']['USD']['2014']

        if '2014' in transactions_usd.get('D', {}).get('USD', {}):
            iati_2014_spend_total += transactions_usd['D']['USD']['2014']

        if '2014' in transactions_usd.get('4', {}).get('USD', {}):
            iati_2014_spend_total += transactions_usd['4']['USD']['2014']

        if '2014' in transactions_usd.get('E', {}).get('USD', {}):
            iati_2014_spend_total += transactions_usd['E']['USD']['2014']

        # Convert to millions USD 
        row['iati_spend_2014'] = float( iati_2014_spend_total / 1000000)


        # Compute 2015 IATI spend
        iati_2015_spend_total = 0

        if '2015' in transactions_usd.get('3', {}).get('USD', {}):
            iati_2015_spend_total += transactions_usd['3']['USD']['2015']

        if '2015' in transactions_usd.get('D', {}).get('USD', {}):
            iati_2015_spend_total += transactions_usd['D']['USD']['2015']

        if '2015' in transactions_usd.get('4', {}).get('USD', {}):
            iati_2015_spend_total += transactions_usd['4']['USD']['2015']

        if '2015' in transactions_usd.get('E', {}).get('USD', {}):
            iati_2015_spend_total += transactions_usd['E']['USD']['2015']

        # Convert to millions USD 
        row['iati_spend_2015'] = float( iati_2015_spend_total / 1000000)


        # Set spend ratio score
        """This is manually set at 100% for now. The IATI technical team is still working 
           on compiling reference spend data from disparate sources, in order to assess 
           the spend ratio. See: https://github.com/IATI/IATI-Dashboard/issues/374

           spend_ratio calculation to be modified when this data has been gathered, see:
           https://github.com/IATI/IATI-Dashboard/issues/375
        """
        row['spend_ratio'] = 100


        # Compute coverage score and raise to the top of its quintile
        if row['spend_ratio'] >= 80:
            row['coverage_adjustment'] = 100

        elif row['spend_ratio'] >= 60:
            row['coverage_adjustment'] = 80

        elif row['spend_ratio'] >= 40:
            row['coverage_adjustment'] = 60

        else:
            row['coverage_adjustment'] = 40


        # Return a generator object
        yield row

