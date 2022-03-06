import matplotlib.pyplot as plt
import numpy as np
from math import factorial
import pandas as pd

print('Write here which dice you want to roll in the format "xdn + xdn +..." where x is how many dice, n is how many sides')
dice = input()
print("How many advantages. Negative for disadvantages.") #1 advantage = You roll twice, get best value, 0 advantages = You roll once. -1 advantage = Roll twice, get worst value. 2 advantages = Roll three times...
advantage = int(input())

def decodeDice(x): #Function to convert notation into a dictionary of the dice used
    found_d = False
    found_no = False
    numbers = [str(i) for i in range(10)]
    d = 0
    no = 0
    length = len(x)
    i = 0
    dies = {}
    for char in x:
        i += 1
        if found_d == False and found_no == False and char in numbers:
            found_no = True
            no = int(char)
        elif found_d == False and found_no == True and char in numbers:
            no = no*10+int(char)
        elif found_d == False and found_no == True and char == "d":
            found_d = True
            found_no = False
        elif found_d == True and char in numbers and i != length:
            d = d*10+int(char)
        elif found_d == True and char in numbers and i == length:
            d = d*10+int(char)
            dies[d] = no
        elif char == "+":
            found_d = False
            dies[d] = no
            no = 0
            d = 0
    return dies

# Whenever I say "distribution" coming up next, I mean a dictionary of the form {x1:y1,x2:y2,...}, where yi is the chance of getting xi, so therefore any number not listed is 0 (It's a discrete distribution)

def DistributionSum(dist1,dist2): #Sums two different distribution, and returns the sum of them
    newdist = {}
    for z in range(min(dist1)+min(dist2),max(dist1)+max(dist2)+1):
        total = 0
        for y in range(100):
            if y in dist1 and (z-y) in dist2:
                total += dist1[y] * dist2[z-y]
        newdist[z] = total
    return newdist

def DistributionMultiply(dist,m): #Takes a distribution and the value you want to multiply it by, then returns a distribution that is equal to summing itself m times
    newdist = dist
    for i in range(m-1):
        newdist = DistributionSum(dist,newdist)
    return newdist

def MultipleSum(list): #This will take a LIST of distributions and sum them all
    newlist = list[0]
    for x in range(1,len(list)):
        newlist = DistributionSum(list[x],newlist)
    return newlist

dice = decodeDice(dice)
dicenew = []

for x in dice: #We make a list with all the dice used, using the initial input as reference
    x_dist = {}
    for y in range(1,x+1):
        x_dist[y] = 1/x
    dicenew.append(DistributionMultiply(x_dist,dice[x])) #We generated a dictionary that was the form {dice : number_of_occurences,...} so we just go through every member and multiply it by the number of ocurrences

dice = MultipleSum(dicenew) #And then we finally sum the list we just created

# We have the distribution of the sum of all the dice already. Here onwards is to get the advantage 

def Advantage(a, dist):
    if a == 0:
        return dist
    else:
        def L(x,z): #This function is the chance of getting a number lower than x in a distribution z
            chance = 0
            for y in z:
                if y < x:
                    chance += z[y]
            return chance

        def M(x,z): #And this one is the same as L, for for getting a number higher than x
            chance = 0
            for y in z:
                if y > x:
                    chance += z[y]
            return chance

        def A(x, m, function,z): #This applies the advantage to get the probability of rolling "x" when you have "m" advantages, use function "L" for positive advantage and "M" for negative advantage
            m += 1
            chance = 0
            for i in range(1,m):
                chance += factorial(m)/factorial(i)/factorial(m-i)*function(x,z)**i*z[x]**(m-i) #This uses the binomial theorem for probabilities, excluding the case where all numbers are lower/bigger than x
            chance += z[x]**m
            return chance

        advantagedice = {}
        if a > 0: #This applies advantage to the distribution
            for x in dist:
                advantagedice[x] = A(x, a, L, dist)
        else:
            for x in dist:
                advantagedice[x] = A(x, abs(a), M, dist)
        return advantagedice

dice = Advantage(advantage, dice)

# This part is to plot the graph of the distribution with matplotlib

def plotDist(dist):
    xpoints = []
    ypoints = []
    for x in dist:
        xpoints.append(x)
        ypoints.append(dist[x])

    xpoints = np.array(xpoints)
    ypoints = np.array(ypoints)
    plt.plot(xpoints, ypoints, 'o')
    plt.show()

plotDist(dice)

# This part is to export the results as a .tsv using pandas

def export(dist):
    probability_density = {"Number":[],"Probability":[]}
    for x in dist:
        probability_density["Number"].append(x)
        probability_density["Probability"].append(dist[x])

    results = pd.DataFrame(probability_density)
    results.sort_values(by=["Number"], inplace=True)
    results.to_csv(r'Dicerolls.tsv', index = False, sep ="\t")

export(dice)
