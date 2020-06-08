import constant

class AnnualTaxableIncome(): # A
    """Annual income formula

    """
    def __init__(self, P, I, F=0, F2=0, U1=0, HD=0, F1=0, L=0):
        
        self.P = P # periode de paye dans l'annee
        self.I = I # salary per pay period
        self.F = F # cotisation a un reer, etc.
        self.F2 = F2 # retenue pour pension
        self.U1 = U1 # paiement syndicat
        self.HD = HD # Deduction pour region, voir formulaire TD1
        self.F1 = F1 # pensions et autres
        
    def calculate(self):
        # [P x (I - F - F2 - U1)] - HD - F1
        result = (self.P * (self.I - self.F - self.F2 - self.U1)) - self.HD - self.F1
        if result <= 0:
            result = self.L
        return result

    def calculate_comission(self):
        pass

class BasicFederalTax(): # T3
    """Formula to calculate the basic federal tax

    """

    def __init__(self, R, A, K, K1, K2Q, K3, K4, TC, P, C, AE, IE):
        self.R = R
        self.A = A
        self.K = K
        self.K3 = K3
        self.K4 = K4
        self.TC = TC
        self.P = P 
        self.C = C
        self.AE = AE
        self.IE = IE

        self.K1 = 0.15 * self.TC  
        if self.P * self.C > 3146.4:
            self.P_C = 3146.4
        else:
            self.P_C = self.P * self.C

        if self.P * self.AE > 650.4:
            self.P_AE = 650.4
        else:
            self.P_AE = self.P * self.AE

        self.P_IE = self.P * self.IE
        if self.P_IE * 0.00494 > 387.79:
            self.P_IE = 387.79


        self.K2Q = ((0.15 * self.P_C) + (0.15 * self.P_AE) + (0.15 * self.P_IE))

    def calculate(self):
        # print(self.R, self.A, self.K, self.K1, 'K2Q', self.K2Q, 'K3', self.K3, self.K4)

        result = (self.R * self.A) - self.K - self.K1 - self.K2Q - self.K3 - self.K4
        if result < 0:
            result = 0
        return result

class AnnualPayableTaxFederal(): # T1
    """docstring for AnnualPayableTaxFederal"""
    def __init__(self, T3, LCF):
        self.T3 = T3
        self.LCF = LCF
    
    def calculate(self):
        self.T3_LCF = self.T3 - self.LCF
        if self.T3_LCF < 0:
            self.T3_LCF = 0

        result = (self.T3_LCF) - 0.165 * self.T3
        if result < 0:
            result = 0
        return result


class FederalTaxRate():
    """Federal tax rate T"""
    def __init__(self, T1, P, L):
        self.T1 = T1
        self.P = P
        self.L = L

    def calculate(self):
        result = (self.T1 / self.P) + self.L
        return result
        