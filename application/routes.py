from flask import render_template, request
from application import app
from application.finance import Finance
from application.forms import BasicForm, DebtForm, ComparisonForm
from application.data_provider_service import DataProviderService

# instantiating an object of DataProviderService
DATA_PROVIDER = DataProviderService()


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html', title='ChipIn Home Page')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


# https://www.codecademy.com/learn/learn-flask/modules/flask-templates-and-forms/cheatsheet
# consider using a redirect here so the submit of the form redirects to the template
@app.route('/form', methods=['GET', 'POST'])
def form_input():
    error = ""
    form = BasicForm()

    if request.method == 'POST':
        salary = form.salary.data
        other = form.other.data
        food_drink = form.food_drink.data
        housing = form.housing.data
        energy = form.energy.data
        petrol = form.petrol.data
        train = form.train.data
        bus = form.bus.data
        eating = form.eating.data
        holidays = form.holidays.data
        clothes = form.clothes.data

        if not salary or not housing:
            error = 'Please fill in the required Salary and Housing fields.'
        else:
            new_data = DATA_PROVIDER.add_form_data(salary, other, food_drink, housing, energy, petrol, train, bus, eating, holidays, clothes)
            data = []
            data += [food_drink, housing, energy, petrol, train, bus, eating, holidays, clothes]
            return render_template('dashboard.html', data=data, new_data=new_data)

    return render_template('form.html', title='Form Page', form=form, message=error)


@app.route('/dashboard')
def dashboard():

    dashboard = Finance('dashboard')

    comparison_list = DATA_PROVIDER.get_average_monthly_expense_data_for_graph()
    comparison_list.insert(0, 'UK Average')

    # currently using hard-coded user data to create graphs
    headers_list = ['housing', 'food and drink', 'energy bills', 'petrol or diesel', 'train fares', 'bus fares', 'eating and drinking', 'holidays', 'clothes and footwear']
    pie_user_list = [981, 372, 107, 102, 15, 35, 382, 115, 161]
    user_list = ['My Spending', 981, 372, 107, 102, 15, 35, 382, 115, 161]
    
    # create a pie chart
    dashboard.create_pie(headers_list, pie_user_list)

    # create a stacked bar chart using data pulled from the database
    dashboard.create_stacked_bar(user_list, comparison_list)

    # grab data to create average UK spending table
    av = DATA_PROVIDER.get_average_monthly_expense_data_for_page_table()

    return render_template('dashboard.html', title='Dashboard', uk_average=av) #key=value pairs (my_variable_on_html_page = this_thing_here_on this page)




@app.route('/admin')
def admin():
    average_debt_data = DATA_PROVIDER.average_debt_report() # returns a decimal object
    average_debt = int(average_debt_data) # recast decimal object as an integer
    average = f"{average_debt:,.02f}" # make the integer a formatted string with thousand separator and 2 decimal places for pence
    debt_type_frequency = DATA_PROVIDER.frequency_debt_report()
    print(debt_type_frequency)    
    Finance('report').generate_debt_report(average_debt_data, debt_type_frequency)
    return render_template('admin.html', title='Admin', average_debt_data = average, debt_type = debt_type_frequency)



@app.route('/debt_calculator_form', methods=['GET', 'POST'])
def calculate_debt():
    external_link_investopedia = 'https://www.investopedia.com/terms/d/debt.asp'
    debt_info = []
    error = ''
    form = DebtForm()
    if request.method == 'POST':
        debt_type = form.debt_type.data
        debt_amount = form.debt_amount.data
        debt_interest = form.debt_interest.data
        debt_term = form.debt_term.data
        debt_monthsyears = form.monthsyears.data
        debt_info += [debt_amount, debt_interest, debt_term, debt_monthsyears, debt_type]
        #print(debt_info)
        if not debt_amount or not debt_interest or not debt_term:
            # if any of those are False/ empty
            error = 'please enter values'
        else:
            new_debt_id = DATA_PROVIDER.add_debt_data(debt_amount, debt_type)
            dc = Finance('dc').simple_debt_calculator(debt_info)
            debt_info += [dc, new_debt_id]
            debt_info[5] = f"{debt_info[5]:,.02f}"
            return render_template('debt_calculator.html', debt_info=debt_info)
    return render_template('debt_calculator_form.html', form=form, message=error, external_link_investopedia=external_link_investopedia)



@app.route('/debt_comparison_form', methods=['GET', 'POST'])
def debt_comparison():
    comparison_info = []
    error = ''
    form = ComparisonForm()
    if request.method == 'POST':
        debt1 = []
        debt1_type = form.debt1_type.data
        debt1_amount = form.debt1_amount.data
        min1_repayment = form.debt1_repayment.data
        debt1_interest = form.debt1_interest.data
        debt1 += [debt1_amount, debt1_interest, min1_repayment]

        debt2 = []
        debt2_type = form.debt2_type.data
        debt2_amount = form.debt2_amount.data
        min2_repayment = form.debt2_repayment.data
        debt2_interest = form.debt2_interest.data
        debt2 += [debt2_amount, debt2_interest, min2_repayment]

        debt3 = []
        debt3_type = form.debt3_type.data
        debt3_amount = form.debt3_amount.data
        min3_repayment = form.debt3_repayment.data
        debt3_interest = form.debt3_interest.data
        debt3 += [debt3_amount, debt3_interest, min3_repayment]

        comparison_info += [debt1, debt2, debt3]
        print(comparison_info)
        DATA_PROVIDER.add_debt_data(debt1_amount, debt1_type)
        DATA_PROVIDER.add_debt_data(debt2_amount, debt2_type)
        DATA_PROVIDER.add_debt_data(debt3_amount, debt3_type)
        #Finance('dc').debt_comparison_calc(comparison_info) # Add the name of your function here
        #return render_template('comparison_results.html') # Add the name of your html comparison results page here
    return render_template('debt_comparison_form.html', form=form, message=error)




# Repeated Routes to Different Benefits
@app.route('/<benefit_name>')
def benefits(benefit_name):
    # Grab 3 pieces of information; url-endpoint, how-data and what-data to auto-complete fields
    unpacked_benefit_data_tuple = DATA_PROVIDER.get_benefits_data(benefit_name)
    if benefit_name == 'child-benefit':
        return render_template('articles.html', title='Child Benefit', data=unpacked_benefit_data_tuple)
    elif benefit_name == 'housing-benefit':
        return render_template('articles.html', title='Housing Benefit', data=unpacked_benefit_data_tuple)
    elif benefit_name == 'employment-support-allowance':
        return render_template('articles.html', title='ESA', data=unpacked_benefit_data_tuple)
    elif benefit_name == 'jobseekers-allowance':
        return render_template('articles.html', title='JSA', data=unpacked_benefit_data_tuple)
    elif benefit_name == 'universal-credit':
        return render_template('articles.html', title='Universal Credit', data=unpacked_benefit_data_tuple)
    else:
        return render_template('index.html', title='Home Page')





