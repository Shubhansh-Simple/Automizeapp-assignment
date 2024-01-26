def validate_reg(data: dict):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    rep_password = data.get('rep_password')
    if first_name and last_name and email and password and rep_password:
        if password == rep_password:
            return True
    return False


def validate_login(data: dict):
    email = data.get('email')
    password = data.get('password')
    if email and password:
        return True
    return False


def convert_timestamp( data, format="%d %B,%Y" ):
    return data.strftime(format)


def count_bad_reviews(df):
    '''Count and return total bad reviews'''

    # Note: CONSIDERING rating < 3 as BAD 
    total_bad_reviews = 0
    for rating in df['Review_Stars']:
        if rating < 3: 
            total_bad_reviews += 1
        else: 
            break   # Will optimize the counting

    return total_bad_reviews


def get_top_five_positive_reviews( df, length ):
    '''Return the top five reviews with rating > 2'''

    good_reviews = []

    for i in range( length-1, length-6, -1):
        try:
            data = df.iloc[i]
        except IndexError:
            break
        else:
            if data['Review_Stars'] > 2:
                data = data.to_dict()
                data['Review_Date'] = convert_timestamp(data['Review_Date'])
                good_reviews.append( data )
            else: break

    return good_reviews


def get_top_five_negative_reviews( df, length ):
    '''Return the top five reviews with rating < 3'''

    bad_reviews = []

    for i in range(0,length):
        try:
            data = df.iloc[i]
        except IndexError:
            break
        else:
            if data['Review_Stars'] < 3:
                data = data.to_dict()
                data['Review_Date'] = convert_timestamp(data['Review_Date'])
                bad_reviews.append( data )
            else: break

    return bad_reviews


def get_good_bad_percentage( total_bad_reviews, total_reviews ):
    '''Calculate good and bad percentages for pie-chart animation''' 

    bad_percentage  = (total_bad_reviews * 100) // total_reviews
    good_percentage = 100 - bad_percentage

    return good_percentage, bad_percentage


def prepare_reviews( good_reviews, 
                     bad_reviews, 
                     total_reviews, 
                     total_bad_reviews ):
    '''Prepare reviews data for sentiment_analysis template'''

    good_percentage, bad_percentage = get_good_bad_percentage( total_bad_reviews, total_reviews )

    return  { 
            'good_reviews'    : good_reviews, 
            'bad_reviews'     : bad_reviews,
            'good_percentage' : good_percentage, 
            'bad_percentage'  : bad_percentage 
    }


