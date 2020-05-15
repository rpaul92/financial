#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#
# Binomial Tree for Pricing American Call / Put Options
# Richard Paul

import math
import numpy as np

    

'''
underlying: current price
strike: strike of contract
vol: current implied volatility expressed in decimal
riskfree: current risk free interest rate, expressed in decimal
maturity: days to expiration, expressed in years
iterations: amount of nodes
divyield: div yield %, expressed in decimal
divperyear: amount of dividends paid out per year, average
putcall: "P" for put, "C" for call
'''

def binomialpricing(underlying,strike,vol,riskfree,maturity,iterations,divyield,divperyear,putcall):
    dt = maturity / iterations
    u = math.exp(vol * math.sqrt(dt))
    d = 1 / u
    R = math.exp((riskfree - divyield) * dt)
    q = (R - d) / (u - d)
    dq = 1 - q
    
    #How many nodes is the tree?
    N = iterations
    
    #Assumes a continuous dividend
    div = underlying * (divyield/100)
    div = div / divperyear

    #Establishing base prices of the equity to the Nth node
    stockvalue = np.zeros((N+1, N+1))
    stockvalue[0,0] = underlying
    for i in range(1,N+1):
        stockvalue[i,0] = stockvalue[i-1,0] * u
        for j in range(1, i+1):
            stockvalue[i,j] = stockvalue[i-1,j-1] * d 

    #Checks if it is a Put or Call, and calculates the payoff function as the last node of the price tree
    if putcall == "C": 
        optionvalue = np.zeros((N+1, N+1))
        for k in range(N+1):
            optionvalue[N,k] = max(stockvalue[N,k] - strike, 0)
    else:  
        optionvalue = np.zeros((N+1, N+1))
        for k in range(N+1):
            optionvalue[N,k] = max(strike - stockvalue[N,k], 0)

    #Working back to the inital price, the model assumes a continuous dividend
    for i in range(N-1,-1,-1):
        for j in range(i+1):
            value = math.exp(riskfree * dt) * q * optionvalue[i+1,j] + dq * optionvalue[i+1,j+1]
            if putcall == "C":
                exercise = stockvalue[i,j] - strike + div
            else: exercise = strike - stockvalue[i,j] + div
            optionvalue[i,j] = max(value, exercise)
    return optionvalue[0,0]


#print(binomialpricing(282.02,285,.3088,.05,1/365,100,1.98,4,"P"))







