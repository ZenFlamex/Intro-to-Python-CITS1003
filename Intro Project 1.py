#Main function
def main(csvfile, country):
    f = open(csvfile,"r")
    data = f.readlines()
    data = data[1:]

#Assigning 
    Org_id = []
    Name = []
    Country = []
    Founded = []
    Type = []
    Num_Employee = []
    Med_Sal = []
    Prof20 = []
    Prof21 = []
    
    for line in data:
        values  = line.split(',')
        Org_id.append(values[0])
        Name.append(values[1])
        Country.append(values[3])
        Founded.append(float(values[4]))
        Type.append(values[5])
        Num_Employee.append(float(values[6]))
        Med_Sal.append(float(values[7]))
        Prof20.append(float(values[8]))
        Prof21.append(float(values[9]))

#MaxMin
    maximum = 0
    minimum = 10000
    maxName = ""
    minName = ""
    maxMin = []
        
        
    i = 0
    for line in data:
        if Country[i] == country and 1981 <= Founded[i] <= 2000 :
            current = Num_Employee[i]
            cname = Name[i]
            if current >= maximum:
                maximum = current
                maxName = cname
            if current <= minimum:
                minimum = current
                minName = cname
        i += 1
    
    maxMin.append(maxName)
    maxMin.append(minName)
        
#Standard Deviation for country
    total = 0
    i=0
    stdv = []
    stdv_country = 0
    stdv_all = 0
    mean = 0
    squared = 0
    
    Med_sal_country = []
    for i in range(len(data)):
        if Country[i] == country:
            Med_sal_country.append(Med_Sal[i])
            
    local = sum(Med_sal_country)
    mean = local / len(Med_sal_country)
    i=0
    for i in range(len(Med_sal_country)):
        squared += (Med_sal_country[i] - mean)**2
        
    stdv_country = (squared/(len(Med_sal_country) - 1))**(1/2)
    stdv_country = round(stdv_country,4)
    stdv.append(stdv_country)
    
    i = 0
    
#Standard deviation for all
    squared_total = 0
    total = sum(Med_Sal)
    mean_total = total / len(Med_Sal)
    for i in range(len(data)):
        squared_total += (Med_Sal[i] - mean_total)**2
        
    stdv_all = (squared_total/(len(data) - 1))**(1/2)
    stdv_all = round(stdv_all,4)
    stdv.append(stdv_all)
    
    
#Ratio for specific country
    profit = 0
    i = 0
    positive = 0
    negative = 0
    for line in data:
        if Country[i] == country:
            p20 = Prof20[i]
            p21 = Prof21[i]
            profit = p21 - p20
            if profit > 0:
                positive += profit
            if profit < 0:
                negative += profit * (-1)
        i += 1
    ratio = round((positive / negative),4)
    
    

#Correlation coefficient 
    x = []
    y = []

    i = 0
    for line in data:
        if Country[i] == country and Prof21[i] > Prof20[i]:
            x.append(Prof21[i])
            y.append(Med_Sal[i])
        i += 1

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = 0
    denominator_x = 0
    denominator_y = 0

    for i in range(len(x)):
        numerator += (x[i] - mean_x) * (y[i] - mean_y)
        denominator_x += (x[i] - mean_x) ** 2
        denominator_y += (y[i] - mean_y) ** 2

    correlation = numerator / (denominator_x ** 0.5 * denominator_y ** 0.5)
    correlation = round(correlation, 4)

        
    return maxMin, stdv, ratio, correlation
