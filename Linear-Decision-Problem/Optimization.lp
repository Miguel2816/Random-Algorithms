\* Optimization *\
Maximize
OBJ: 0.095 Amount_Invested_Xa + 0.08 Amount_Invested_Xb
 + 0.09 Amount_Invested_Xc + 0.09 Amount_Invested_Xd + 0.09 Amount_Invested_Xe
Subject To
Matuarity: Amount_Invested_Xb + Amount_Invested_Xe >= 50000
Return_from_Tax_Free: 0.057 Amount_Invested_Xa + 0.048 Amount_Invested_Xb
 - 0.036 Amount_Invested_Xc + 0.054 Amount_Invested_Xd
 - 0.036 Amount_Invested_Xe >= 0
Risks: Amount_Invested_Xa + Amount_Invested_Xd + Amount_Invested_Xe <= 50000
Tax: Amount_Invested_Xa + Amount_Invested_Xb + Amount_Invested_Xd >= 30000
Total_Available: Amount_Invested_Xa + Amount_Invested_Xb + Amount_Invested_Xc
 + Amount_Invested_Xd + Amount_Invested_Xe = 100000
End
