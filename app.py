
import objects
import federal


# base sur le document: formules pour le calcul des retenues a la source quebec 2020
# 3 Revenu annuel
# 3.1 Calcul de la retenue d'impot sur la base de paiements reguliers
# 3.1.1 Paiement reguliers
# Etape 1 - calcul du revenu annuel


pay_periods = 52
remuneration_per_period = 1464.56
line_19 = 0 # applicable if you live in a remote region or have child support.
remaining_periods = 50
ei_rate = 0.012 # this is for quebec
ei_year_max = 650.4
holiday_rate = 0.06
CEA = 1245 # federal parameter



deduction_employment_income = objects.DeductionForEmploymentIncome(remuneration_per_period, pay_periods)
print('deduction_employment_income = ', deduction_employment_income.calculate())

source_deduction_return = objects.SourceDeductionReturn(pay_periods, line_19, remaining_periods)
print('source_deduction_return = ', source_deduction_return.calculate())

annual_income = objects.AnnualIncome(pay_periods, remuneration_per_period, 0, deduction_employment_income.calculate(), source_deduction_return.calculate(), reduction_source_deductions=0)
print('annual_income =', annual_income.calculate())

remuneration_per_period_reduced = annual_income.calculate() / pay_periods
print('updated remuneration per period:', remuneration_per_period_reduced)

income_tax_year = objects.IncomeTaxYear(I=annual_income.calculate(), K1=0, E=15532, P=pay_periods, Q=0, Q1=0)
print('income_tax_year = ', income_tax_year.calculate())

income_tax_withheld_period = objects.IncomeTaxWithheldPerPeriod(income_tax_year.calculate(), pay_periods, additional_source_deduction=0)
print('income_tax_withheld_period = ', income_tax_withheld_period.calculate())

A5 = objects.QuebecPensionPlan(S3=remuneration_per_period, V=3500, P=52, M=3146.4, A5=0).calculate() * (pay_periods - remaining_periods)
quebec_pension_plan = objects.QuebecPensionPlan(S3=remuneration_per_period, V=3500, P=52, M=3146.4, A5=A5)
print('quebec_pension_plan = ', quebec_pension_plan.calculate())


A6 = objects.QuebecParentalInsurancePlan(S4=remuneration_per_period, N=387.79, A6=0).calculate() * (pay_periods - remaining_periods) # RQAP paid so far
quebec_parental_insurance_plan = objects.QuebecParentalInsurancePlan(S4=remuneration_per_period, N=387.79, A6=A6)
print('quebec_parental_insurance_plan = ', quebec_parental_insurance_plan.calculate())

# Assurance emploi


print('')


T = federal.FederalTaxRate(T1=0, P=pay_periods, L=0)
print('federal tax rate = ', T.calculate())

annual_taxable_income = federal.AnnualTaxableIncome(P=pay_periods, I=remuneration_per_period, F=quebec_pension_plan.calculate(), F2=0, U1=0, HD=0, F1=0, L=0)
print('annual_taxable_income_federal = ', annual_taxable_income.calculate())

A = annual_taxable_income.calculate()
print('A', A)

ei_paid_so_far = federal.EmployementInsurance(insurable_earning=remuneration_per_period, premium_rate=ei_rate, year_max=650.4, paid_this_year=0).calculate() * (pay_periods - remaining_periods)
employement_insurance = federal.EmployementInsurance(insurable_earning=remuneration_per_period, premium_rate=ei_rate, year_max=650.4, paid_this_year=ei_paid_so_far).calculate()
print('employement_insurance =', employement_insurance)


basic_federal_tax = federal.BasicFederalTax(R=0.205, A=A, K=2669, K1=0, K2Q=0, K3=0, K4=0, TC=0, P=52, C=quebec_pension_plan.calculate(), AE=employement_insurance, IE=A, CEA=CEA)
print('basic_federal_tax = ', basic_federal_tax.calculate())

annual_payable_tax_federal = federal.AnnualPayableTaxFederal(T3=basic_federal_tax.calculate(), LCF=750) # T1
print('annual_payable_tax_federal = ', annual_payable_tax_federal.calculate())

federal_tax_per_period = annual_payable_tax_federal.calculate()/pay_periods
print('federal retenue per pay period = ', federal_tax_per_period)

print('total net pay per pay period = ', remuneration_per_period - federal_tax_per_period - quebec_parental_insurance_plan.calculate() - quebec_pension_plan.calculate() - income_tax_withheld_period.calculate() - employement_insurance)

holiday_witholding = remuneration_per_period * holiday_rate
print('Holiday witholding =', holiday_witholding, 'not substracted from salary, just noted')