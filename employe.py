

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


class EmployeePeriodPay():
	def __init__(self, employee, company, remaining_pay_period, pay_period_per_year):
		self.employee = employee # list
		self.company = company
		self.remaining_pay_period = remaining_pay_period # Number
		self.pay_period_per_year = pay_period_per_year

		

class Company():
	def __init__(self, CSST_rate, RRQ_rate, RQAP_rate, EI_rate, FSS_rate,):
		self.CSST_rate = csst_rate
		self.RRQ_rate = RRQ_rate
		self.RQAP_rate = RQAP_rate
		self.EI_rate = EI_rate
		self.FSS_rate = FSS_rate




def weekly_company_payment(employee_pays, fees, qst, gst):
	pass

def employee_pay(pay_date, pay_number, employee, hours, brut_pay, net_pay,):
	pass



