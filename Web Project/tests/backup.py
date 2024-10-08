from tradingview_screener import Query, Column
import numpy as np

# for all classes to return, as __str__() determines what value comes out of every function:
global value

# user input:
uInput = input("Enter a stock name (e.g. NVDA): ")
uInput = uInput.upper()
# upper() so that it does not matter if input is lower/upper case, it will always be upper

exact_name_query = (Query()
                    .select('name')
                    .where(Column('name') == uInput)
                    .get_scanner_data())
# exact_name_query is a query for matched exact name, it returns e.g.

# (1,          ticker    name
# 0         NASDAQ:NVDA  NVDA


class NameLike:
    def __init__(self):
        count, self.query = (Query()
                             .select('name')
                             .where(Column('name').like(uInput))
                             .get_scanner_data())
        # self.query would return this as a dataframe at this stage, "count," to remove COUNT(*) at top left e.g.:
        #          ticker  name
        # 0   NASDAQ:NVDA  NVDA
        # 1   NASDAQ:AMZN  AMZN
        # 2   NASDAQ:COIN  COIN

        nested_list = self.query.values.tolist()
        # nested_list returns this:
        # [['NASDAQ:NVDA', 'NVDA'], ['NASDAQ:AMZN', 'AMZN']]

        global namelist
        namelist = []
        # namelist to append after extracting the short names from nested list

        # working steps to extracting the short names
        for each_list in nested_list:  # initial each_list would print e.g. ['NASDAQ:NVDA', 'NVDA']
            for each_element in each_list:
                y = each_list.pop()  # to retrieve the removed short name, assign it to y and append it to namelist
                namelist.append(y)
                # I named each_list.pop() as each_list would print e.g. 'NASDAQ:NVDA', the leftover
                # the positioning of each_list and y acts like (x,y) in the original value of each_list

    def query(self):
        value = self.query
        return value

    def __str__(self):
        try_msg = "I'm sorry, did you mean {0}, {1} or {2}? Try again"
        value = try_msg.format(namelist[0], namelist[1], namelist[2])
        return value


class FromInput:
    def __init__(self, column):
        self.column = column
        self.query = (Query()
                      .select(self.column)
                      .where(Column('name') == uInput)
                      .get_scanner_data())

    def query(self):
        value = self.query()
        return value

    # FromInput(column_name).query returns initial query

    def get_info(self):
        value = self.query
        self.query = list(self.query)
        self.query = self.query.pop()
        value = self.query.at[0, self.column]  # gets whatever value based on column searched
        return value

    # FromInput(column name).get_info() returns value from column e.g.
    # 78.657387

    # self.query.pop() due to the initial query returning:

    # (1, ticker            column_name
    # 0  NASDAQ:NVDA             x    )

    def __str__(self):
        return value


def inputinfo(column):  # to get one specific number/name
    value = FromInput(column).get_info()
    if column == 'Recommend.All':
        if value >= 0.5:
            value = 'Strong Buy'
        elif value >= 0.1:
            value = 'Buy'
        elif value >= -0.1:
            value = 'Neutral'
        elif value >= -0.5:
            value = 'Sell'
        else:
            return 'Strong Sell'
    return value
#  for naming convenience and to format ratings


# loop for if the name of uInput is not matched, will return a try again with 'try' suggestions:
if exact_name_query[0] == 0:
    print(NameLike())
    uInput = input("Enter a stock name (e.g. NVDA): ")

# exact_name_query[0] = (3318, ----> a COUNT(*),
# if there is 0 COUNT(*), the exact name is not found,
# hence prompting the user to try again and showcasing similar stock names

# uIndustry - The parameter describing the industry belonging to uInput (user input)
uIndustry = FromInput('industry').get_info()


def comparedata(column):
    count, df = (Query()
                 .select('price_sales_ratio', 'price_earnings_ttm', 'net_income',
                         'total_revenue', 'price_earnings_growth_ttm', 'dividends_per_share_fq',
                         'earnings_per_share_fq', 'return_on_equity', 'return_on_assets',
                         'debt_to_equity', 'price_free_cash_flow_ttm')
                 .where(Column('industry') == uIndustry)
                 .get_scanner_data())
    # get all the required columns' data
    df = df.dropna()
    # remove rows with even one 'nan' on it
    value = list(df[column])
    # convert to list for easy comparison when using the values within to calculate the mean and standard deviation
    return value


def statement(column):  # function for each statement

    # To use in if/else statement:
    def valuefor(column):
        x = round(inputinfo(column), 2)
        return x

    # To add to string statement:
    def stringfor(column):
        x = str(valuefor(column))
        return x

    # standard deviation:
    def sd(column):
        x = float(np.std(comparedata(column)))
        return x

    # standard deviation:
    def mean(column):
        x = float(np.mean(comparedata(column)))
        return x

    # multiplier calculation:
    def calc(column):
        x = str(round(float(inputinfo(column)/mean(column)), 2)) + " of the average stock"
        return x

    # shortening of long variable names
    p_fcf = inputinfo('price_free_cash_flow_ttm')
    roe = inputinfo('return_on_equity')
    roa = inputinfo('return_on_assets')
    dte = inputinfo('debt_to_equity')

    match column:
        # price-to-sales-ratio ($)
        case "price_sales_ratio" if inputinfo('price_sales_ratio') > 0:
            x = "You are paying $" + stringfor('price_sales_ratio') + " per $1 of sales"
            return x
        case "price_sales_ratio" if inputinfo('price_sales_ratio') < 0:
            pass
        case "price_sales_ratio" if inputinfo('price_sales_ratio') == np.nan:
            x = "Data for amount per $1 of sales could not be found"
            return x

        # price-to-earnings-ratio ($)
        case "price_earnings_ttm" if inputinfo('price_earnings_ttm') > 0:
            x = "You are paying $" + stringfor('price_earnings_ttm') + " per $1 of earnings"
            diff = round(inputinfo('price_earnings_ttm') - inputinfo('price_sales_ratio'), 2)
            addition = ", which amounts to $" + str(diff) + " per $1 of expenses"
            x += addition
            return x
        case "price_earnings_ttm" if inputinfo('price_earnings_ttm') < 0:
            x = "You are paying $" + stringfor('price_earnings_ttm') + " per $1 of loss"
            return x
        case "price_earnings_ttm" if inputinfo('price_earnings_ttm') == np.nan:
            x = "Data for amount per $1 of earnings could not be found"
            return x

        # profit-margin (%)
        case "total_revenue" if inputinfo('net_income') > 0:
            profitmargin = round(inputinfo('net_income')/inputinfo('total_revenue') * 100, 2)
            x = "The profit margin of the company is " + str(profitmargin) + "%"
            if profitmargin > 100:
                addition = ", which implies that the company's income is greater than its equity"
                x += addition
            elif 100 > profitmargin > 0:
                pass
            elif profitmargin < 0:
                x = "Profit Margin is at negative by " + abs(profitmargin) + "%"
                return x
            elif profitmargin == np.nan:
                "Data for profit margin could not be found"
            return x
        case "total_revenue" if inputinfo('total_revenue') < 0:
            pass
        case "total_revenue" if inputinfo('total_revenue') == np.nan:
            x = "Data for profit margin could not be found"
            return x

        # price-earnings-to-growth ($)
        case "price_earnings_growth_ttm" if inputinfo('price_earnings_growth_ttm') > 0:
            term = "the stock's price, its earning, and the expected growth of the company"
            x = "You are paying $" + stringfor('price_earnings_growth_ttm') + " premium per $1 of " + term
            return x
        case "price_earnings_growth_ttm" if inputinfo('price_earnings_growth_ttm') < 0:
            term = "the stock's price, its earning, and the expected growth of the company"
            amt = abs(valuefor('price_earnings_growth_ttm'))
            x = "You would get a $" + str(amt) + " discount per $1 of " + term
            return x
        case "price_earnings_growth_ttm" if inputinfo('price_earnings_growth_ttm') == np.nan:
            x = "Data for amount per $1 of premium/discount could not be found"
            return x

        # dividend-payout-ratio (%)
        case "earnings_per_share_fq" if inputinfo('earnings_per_share_fq') > 0:
            divpayout = round(inputinfo('dividends_per_share_fq')/inputinfo('earnings_per_share_fq') * 100, 2)
            x = "The dividend payout of the company is " + str(divpayout) + "%"
            x_2 = ", at $" + str(round(inputinfo('dividends_per_share_fq'),2)) + " per share"
            x += x_2
            if divpayout > 100:
                addition = ", which implies that the company's income is greater than its equity"
                x += addition
            elif 100 > divpayout > 0:
                pass
            elif divpayout < 0:
                x = "There are no dividends this quarter"
            elif divpayout == np.nan:
                x = "Data for dividend payout could not be found"
            return x
        case "earnings_per_share_fq" if inputinfo('earnings_per_share_fq') < 0:
            x = "Data for dividend payout could not be found"
            return x
        case "earnings_per_share_fq" if inputinfo('earnings_per_share_fq') == np.nan:
            x = "Data for dividend payout could not be found"
            return x

        # price-to-free-cash-flow-ratio ($)
        case "price_free_cash_flow_ttm" if p_fcf >= sd('price_free_cash_flow_ttm') + mean('price_free_cash_flow_ttm'):
            x = "The stock is premium by x" + calc('price_free_cash_flow_ttm')
            return x
        case "price_free_cash_flow_ttm" if mean('price_free_cash_flow_ttm') <= p_fcf > 1:
            x = "The stock is fairly priced at x" + calc('price_free_cash_flow_ttm')
            return x
        case "price_free_cash_flow_ttm" if 1 > p_fcf > 0:
            x = "The stock is undervalued at x" + calc('price_free_cash_flow_ttm')
            return x
        case "price_free_cash_flow_ttm" if p_fcf < 0:
            x = "The stock is at a loss by x" + calc('price_free_cash_flow_ttm')
            addition = "\nThis means more cash left a company's bank account than went into it"
            x += addition
            return x
        case "price_free_cash_flow_ttm" if inputinfo('price_free_cash_flow_ttm') == np.nan:
            x = "Data for price-to-free-cash-flow ratio could not be found"
            return x

        # return-on-equity (%)
        case "return_on_equity" if roe > 100:
            x = "The return on equity is " + str(round(roe,2)) + "%"
            addition = ", implying that the income generated by the company is greater than its equity"
            x += addition
            return x
        case "return_on_equity" if 100 > roe > 20:
            x = "The return on equity is " + str(round(roe, 2)) + "%"
            addition = ", implying that the company's management is VERY efficient in generating income and growth"
            x += addition
            return x
        case "return_on_equity" if 20 >= roe > 15:
            x = "The return on equity is " + str(round(roe, 2)) + "%"
            addition = ", implying that the company's management is efficient in generating income and growth"
            x += addition
            return x
        case "return_on_equity" if 5 >= roe > 0:
            x = "The return on equity is " + str(round(roe, 2)) + "%"
            addition = ", implying that the company is in a harmful zone in managing their income and growth"
            x += addition
            return x
        case "return_on_equity" if roe < 0:
            x = "The return on equity is " + str(round(roe, 2)) + "%"
            addition = ", implying that the company, especially the shareholders'(investments), are experiencing a loss"
            x += addition
            return x
        case "return_on_equity" if inputinfo('return_on_equity') == np.nan:
            x = "Data for return on equity could not be found"
            return x

        # return-on-assets (%)
        case "return_on_assets" if 100 > roa > 20:
            x = "The return on assets is " + str(round(roa, 2)) + "%"
            addition = ", implying that the company's management is VERY efficient in generating income via assets"
            x += addition
            return x
        case "return_on_assets" if 20 >= roa > 15:
            x = "The return on assets is " + str(round(roa, 2)) + "%"
            addition = ", implying that the company's management is efficient in generating income via assets"
            x += addition
            return x
        case "return_on_assets" if 5 >= roa > 0:
            x = "The return on assets is " + str(round(roa, 2)) + "%"
            addition = ", implying that the company is in a harmful zone in using assets to generate income"
            x += addition
            return x
        case "return_on_assets" if roa < 0:
            x = "The return on assets is " + str(round(roa, 2)) + "%"
            addition = ", implying that the company is unable to acquire/use its assets optimally to generate profit"
            x += addition
            return x
        case "return_on_assets" if inputinfo('return_on_assets') == np.nan:
            x = "Data for return on assets could not be found"
            return x

        # debt-to-equity (%)
        case "debt_to_equity" if dte >= sd('debt_to_equity') + mean('debt_to_equity'):
            x = "The debt-to-equity of the company is high at " + str(round(dte, 2)) + "%"
            addition = ", implying that the company has been increasing its debt to finance its assets"
            x += addition
            return x
        case "debt_to_equity" if dte < 2:
            x = "The debt-to-equity of the company is at " + str(round(dte, 2)) + "%"
            return x
        case "debt_to_equity" if 2 >= dte > 1:
            x = "The debt-to-equity of the company is at " + str(round(dte, 2)) + "%"
            addition = ", which is favorable"
            x += addition
            return x
        case "debt_to_equity" if 1 >= dte > 0:
            x = "The debt-to-equity of the company is at " + str(round(dte, 2)) + "%"
            addition = ", which is VERY favorable"
            x += addition
            return x
        case "debt_to_equity" if dte < 0:
            x = "The debt-to-equity of the company is at " + str(round(dte, 2)) + "%, which means that the "
            addition = "total value of the company's assets is less than the total amount of debt and other liabilities"
            x += addition
            return x
        case "debt_to_equity" if inputinfo('debt_to_equity') == np.nan:
            x = "Data for debt-to-equity could not be found"
            return x


print(inputinfo('Recommend.All'))  # print out rating first
print(statement('price_sales_ratio'))
print(statement('price_earnings_ttm'))
print(statement('total_revenue'))
print(statement('price_earnings_growth_ttm'))
print(statement('earnings_per_share_fq'))
print(statement('price_free_cash_flow_ttm'))
print(statement('return_on_equity'))
print(statement('return_on_assets'))
print(statement('debt_to_equity'))



