

# company
# 	week_pay(list)
# 		employee(list)
# 			hours
# 			brut_pay
# 			net_pay
# 			adjustment
# 				date_of_
# 				hours
# 				brut_pay
# 				net_pay


class Employee():
	def __init__(self, pay_periods, remuneration_per_period, line_19, remaining_periods, ei_rate, ei_year_max, holiday_rate, CEA):
		self.pay_periods = pay_periods
		self.remuneration_per_period = remuneration_per_period
		self.line_19 = line_19
		self.remaining_periods = remaining_periods
		self.ei_rate = ei_rate
		self.ei_year_max = ei_year_max
		self.holiday_rate =Holiday_rate
		self.CEA = CEA


class WeekPay():
	def __init__(self, employee, company,):
		self.employee = employee
		self.company = company
		

class Company():
	def __init__(self, csst_rate, ):
		self.csst_rate = csst_rate

def weekly_company_payment(employee_pays, fees, qst, gst):
	pass

def employee_pay(pay_date, pay_number, employee, hours, brut_pay, net_pay,):
	pass



