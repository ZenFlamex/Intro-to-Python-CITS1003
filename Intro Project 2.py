#Author: Wong Alton Xuan Er
#Student Number: 23840745
#Main function
def main(csvfile):
    output_test = {}
    output_nest = {}
    try:
        Org_id, Name, Website, Country, Founded, Category, Num_Employee, Med_Sal, Prof20, Prof21 = readfile(csvfile)
        #Reading the file and putting them to their own list
        output_test = normal(Num_Employee, Med_Sal, Country, Prof20, Prof21)
        #Making the dictionary for t-test score & minkowski distance
        output_nest = nested(Org_id, Num_Employee, Prof20, Prof21, Category)
        #Making the nested dictionary for category
        return output_test, output_nest
    except (ZeroDivisionError,FileNotFoundError,ValueError,TypeError,NameError,IndexError,KeyError):
        return output_test, output_nest
    
    
def readfile(csvfile):
    Org_id = []
    Name = []
    Website = []
    Country = []
    Founded = []
    Category = []
    Num_Employee = []
    Med_Sal = []
    Prof20 = []
    Prof21 = []
    
    encountered_org_id = set()
    
    with open(csvfile,'r') as f:
        data = f.readlines()
        data = data[1:]
        
        for line in data:
            values  = line.split(',')
            if (len(values) != 10 # Ensure there are 10 values in each row
                or values[0] in encountered_org_id #Ensure that there will be no identical Orginisation Ids
                or not values[0] # Check if Org_id is empty or null
                or not values[1] # Check if Name is empty or null
                or not values[5] # Check if Category is empty or null
                or float(values[4]) <=0 #Check if Founded is zero or negative
                or float(values[6]) <= 0 # Check if Num_Employee is zero or negative
                or float(values[7]) <= 0 # Check if Med_Sal is zero or negative
                or float(values[8]) <= 0 # Check if Prof20 is zero or negative
                or float(values[9]) <= 0): # Check if Prof21 is zero or negative
                continue
            encountered_org_id.add(values[0])
            Org_id.append(values[0].lower())
            Name.append(values[1].lower())
            Website.append(values[2].lower())
            Country.append(values[3].lower())
            Founded.append(float(values[4]))
            Category.append(values[5].lower())
            Num_Employee.append(float(values[6]))
            Med_Sal.append(float(values[7]))
            Prof20.append(float(values[8]))
            Prof21.append(float(values[9]))
    return Org_id, Name, Website, Country, Founded, Category, Num_Employee, Med_Sal, Prof20, Prof21 

def normal(Num_Employee, Med_Sal, Country, Prof20, Prof21):
    output = {}
    country_data = {}
    
    for i in range(len(Country)):
        employees = Num_Employee[i]
        median_salary = Med_Sal[i]
        country = Country[i]
        prof20 = Prof20[i]
        prof21 = Prof21[i]
        
        if country not in country_data:
            country_data[country] = {'employee_data':[],'salary_data':[], 'prof20_data':[], 'prof21_data':[]}
        
        country_data[country]['employee_data'].append(employees)
        country_data[country]['salary_data'].append(median_salary)
        country_data[country]['prof20_data'].append(prof20)
        country_data[country]['prof21_data'].append(prof21)
        
    for country, data in country_data.items():
        employee_data = data['employee_data']
        salary_data = data['salary_data']
        prof20_data = data['prof20_data']
        prof21_data = data['prof21_data']
                        
        n = len(employee_data)
        
        mean20 = sum(prof20_data)/n
        mean21 = sum(prof21_data)/n
        
        squared20 = 0
        squared21 = 0
        for x in prof20_data:
            squared20 += (x - mean20) ** 2
        for y in prof21_data:
            squared21 += (y - mean21) ** 2
        sd20 = (squared20/(n - 1))**0.5
        sd21 = (squared21/(n - 1))**0.5
        
        t_test_score = round((mean20 - mean21)/(((sd20**2)/n)+((sd21**2)/n))**0.5,4)
        
        
        #Calculate Minkowski Distance
        minkowski_dist = 0
        for i in range(n):
            minkowski_dist += abs(employee_data[i] - salary_data[i]) ** 3
        minkowski_dist = round(minkowski_dist ** (1/3),4)
        
        output[country] = [t_test_score, minkowski_dist]
    return output


def nested(Org_id, Num_Employee, Prof20, Prof21, Category):
    collect={}
    #creating the first dictionary
    for i in range(len(Org_id)):
        org = Org_id[i]
        employees = int(Num_Employee[i])
        prof20 = Prof20[i]
        prof21 = Prof21[i]
        percentage = round((abs(prof20 - prof21)/prof20)*100,4)
        same_category = []
        #sorting based on number of employees and profit change
        for j in range(len(Org_id)):
            if Category[j] == Category[i]:
                same_category.append(Org_id[j])
        #Calculating the rank based on descending number of employees and descending profit change if num employee is the same
        same_category.sort(key=lambda x: (Num_Employee[Org_id.index(x)], percentage),reverse=True)
        rank = same_category.index(org) + 1
            
        collect[org] = [employees, percentage, rank]

    #creating the second dictionary
    organize_cat = {}
    for i in range (len(Org_id)):
        org = Org_id[i]
        category = Category[i]
        if category not in organize_cat:
            organize_cat[category] = {}
        organize_cat[category][org] = collect[org]
    
    return organize_cat




OP1, OP2 = main('Organisations.csv')
OP2s = {'transportation': {'fddf45e1defebbc': [9941, 17.0098, 1], 'e5ca6529dcd4030': [9890, 64.8253, 2], '18c26fd0fad73e3': [9655, 74.9636, 3], 'dedd9d0aa6115d3': [9151, 54.3155, 4], '3ed7b5f7c7f2bfe': [8887, 60.6208, 5], 'ecedfb72daeebbc': [8861, 77.5734, 6], 'cbd16b4174ded61': [8841, 11.115, 7], 'c763f85cc571e19': [8471, 36.2271, 8], '958cabb9b17124d': [8250, 19.1039, 9], 'df39abf66ae4d0c': [8213, 58.8421, 10], 'aac4f9abf86eaef': [7994, 2642.0042, 11], 'ebd8bceefc9a560': [7982, 218.6259, 12], 'af3b0dc3a779eb5': [7898, 70.6684, 13], 'b0e440da717eff9': [7825, 1275.1963, 14], 'afee981fbacdbe8': [7809, 19.1986, 15], '487110e58a9b49f': [7806, 32.4814, 16], '6aa8ef34dceed25': [7672, 58.1371, 17], 'd2ef4c24da2d2a7': [7668, 18.2202, 18], '6f8e7fe3ccfcb7c': [7640, 0.0175, 19], 'e9bebd37bfee7bb': [7597, 1014.1936, 20], '2eaa3c5d6cc37b9': [7306, 97.6941, 21], 'a5ffb6afd24d2eb': [7298, 5.0006, 22], '50d48830dc9a8ac': [7286, 273.4816, 23], 'db82eaf8e7a59af': [7188, 24.1508, 24], 'ccd85e8579f9c7e': [6998, 22.7903, 25], 'fde4affceee8f58': [6921, 33.5829, 26], '4dbcfb13cf62f8f': [6594, 151.4915, 27], 'f40fc5a648c53f3': [6515, 5.3627, 28], 'ad103986bdbe6ad': [6472, 35.0741, 29], '3899d932c149e5c': [6403, 234.9487, 30], '4cd5cc59b0aa9c5': [6336, 49.9936, 31], '244f2bdbb45dcbc': [6177, 519.1777, 32], '30aa99fbfaf7ae0': [6139, 20.4869, 33], 'ce017b247db1ede': [6029, 20.221, 34], '6b345d487edf9df': [5533, 203.0828, 35], 'd0b5d62f4ba941f': [5422, 65.3625, 36], 'ebdceaf8b6b2fb5': [5199, 18.3902, 37], 'fdcceeffac73497': [5197, 909.2176, 38], 'ba404ddd2ad309a': [5158, 250.2989, 39], '55cc2d7816506bd': [5096, 171.2146, 40], 'a0dcf3bcf1addea': [4815, 94.1705, 41], 'cc88150b8ecad8c': [4619, 278.3508, 42], 'a8fd24e2bb7d0fd': [4110, 75.0101, 43], '0fbfeda9d5e0b69': [3958, 444.4106, 44], 'db0ecf7ddcc3a7a': [3866, 31.1923, 45], '9f63c73be6a39e9': [3837, 31.5272, 46], 'ddba684d69764eb': [3806, 73.7467, 47], 'a376a6d71f1c36c': [3778, 33.6626, 48], '9dd10a3ccb2b1bd': [3468, 91.2823, 49], 'f73b358bf010f7f': [3101, 3.6208, 50], 'fa302496c8b81de': [2730, 353.9522, 51], '5a1abaad8cf84dc': [1715, 173.0893, 52], '2c676bfb58d9907': [1419, 232.0742, 53], '9eeb46cbf04eeff': [1371, 42.0656, 54], 'e84e97db7bfaded': [1145, 223.9254, 55], 'fe8bbb899efcb06': [959, 78.108, 56], 'ec2dae361f8bb30': [886, 27.0291, 57], 'bcf355a517cb541': [871, 82.0194, 58], 'beef0bf7cabe089': [778, 22.6976, 59], '4eb9d3e5cf79b91': [730, 139.1334, 60], 'ee2d54f3ad9c126': [313, 239.6799, 61], 'fe7fbd9a048c647': [275, 77.6339, 62], 'a1c2b67b5a01adf': [159, 14.7981, 63], 'ea8a779bec3c8ff': [142, 37.3099, 64], '51acf1269e194e8': [1, 1.102, 65]}, 'apparel': {'ffb1a8af4fec7ce': [9751, 148.0152, 1], 'cdbd7720bba0bf5': [9676, 79.8178, 2], 'ed8abdcda9dd862': [9231, 33.8691, 3], '9f8efb3d03193db': [9056, 83.5497, 4], 'c8ee331607f5eba': [8986, 83.7773, 5], '5022c998edeada1': [8940, 76.1092, 6], '6be8a1ef720fd32': [8323, 53.3066, 7], '3deebf49bd2fce7': [8125, 68.3556, 8], 'bbb5ab4b0aad7a3': [8073, 58.4499, 9], 'dffc100fccdc16d': [7720, 8.5224, 10], 'a68bbe2bdba36e4': [7679, 32.7773, 11], '4255e3e4acf7abf': [7374, 208.7767, 12], 'bfa9a7d5cd3ea2c': [7249, 674.8441, 13], 'dfed388e08b676f': [7161, 175.6802, 14], 'bba52b87bb6a32f': [6819, 77.3826, 15], 'bdf0c047e52cdc3': [6639, 208.9649, 16], '9fbf69aa2d9aaf1': [6165, 23.0195, 17], 'a3a8d60af487c75': [6150, 677.836, 18], '4d17fa0d985e0d7': [5942, 113.4418, 19], 'd9b675d794bba4e': [5683, 65.5512, 20], '19d7de485e79df6': [5594, 77.0358, 21], '3abb3f3bb9c1c3c': [5573, 85.5494, 22], 'e4a91c4dae32af6': [4738, 6.6024, 23], 'bf0ebca305efbe4': [4704, 3965.7108, 24], 'e4c640af4aa845a': [4531, 68.4492, 25], '0de4671f41341d6': [4204, 77.8637, 26], '778fb7e29d989a6': [3894, 37.2988, 27], '90bbf5c6d616dbf': [3787, 114.4093, 28], '8a9190a50adf241': [3695, 70.1366, 29], '7afb4a27bf2fcf7': [3547, 75.798, 30], '2ecb7041dc2adf1': [3321, 46.1179, 31], '4ded9e3ff968e7c': [3313, 61.4542, 32], 'ec0e323acd42b6e': [3250, 12.9206, 33], '27eab75ce19c101': [2878, 451.9604, 34], '6de050494d4602b': [2781, 90.8269, 35], 'eb1f0a485ff5c50': [2587, 604.2237, 36], 'b3ea88cb559edd6': [2304, 61.0309, 37], '91ba1665eeb4d22': [1999, 87.3718, 38], '8c4d487cabce6e9': [1740, 420.7197, 39], 'ccb6a3bcccd8bd0': [1339, 27.0469, 40], 'bd5e1a9a3f0f95a': [1213, 268.0361, 41], 'd214d152bdf2f3d': [1175, 86.2326, 42], '0a3ca1e9c01baae': [1021, 204.9677, 43], '3d41753aadac2fb': [956, 67.4287, 44], 'cffbc964c8c205d': [795, 1.6964, 45], 'ecb7aae9a6cb36d': [485, 13.0138, 46], '3c6fd0d86e7baaf': [404, 17.6824, 47], '9ec72158e7c46d2': [219, 248.5721, 48]}, 'accounting': {'a5e8ce5cf97c2ac': [8128, 760.9484, 1], 'df66e70fae1aa5d': [7518, 0.5118, 2], '5e2bb2dace9511e': [7007, 73.0692, 3], '795195c9db5e1c0': [6977, 96.9351, 4], 'a6bc77d5ce07c7b': [6947, 90.4202, 5], 'ca8e1dfba7b1d8d': [6628, 110.683, 6], 'b715731fa4a6cdb': [6429, 970.6279, 7], '8f55cd0ad6dcde2': [6202, 22.6138, 8], 'bcaac3adb10bf1c': [6143, 801.5984, 9], 'c38cf79de2e6b6a': [5784, 125.3964, 10], 'ef56bdce48de5ff': [5523, 597.8386, 11], '0bcebfcd12bcb7e': [5282, 31.2454, 12], 'e0da4a69658eaca': [4491, 120.9667, 13], '27fbc78271f3aa2': [4288, 174.5934, 14], 'd457875b76d0ad8': [3784, 28.912, 15], 'ef7e820bc9f7e49': [2861, 40.1272, 16], 'a45e805db7feee1': [2658, 158.8379, 17], 'a3b8d27d51aae2f': [2135, 64.8933, 18], 'ba907c2acbc34ba': [2090, 13.0396, 19], 'f8a35a4b5d7b2c1': [871, 40.3551, 20]}, 'music': {'6b1bbe5dfdac090': [9915, 201.3362, 1], 'b7b5ca3592086ed': [9684, 706.8407, 2], '05bbfbda2ad8e1a': [8889, 195.0258, 3], '6fb2023d97790c7': [8677, 434.1696, 4], '2fab6dad4afe024': [8562, 36.981, 5], 'a9a62abc02eceeb': [8056, 21.5653, 6], '3a4fd31d16d2a42': [6405, 84.2735, 7], '5b62b5165b3a0c8': [6307, 49.8873, 8], '3edc8528529b302': [6176, 37.5451, 9], 'e7e1d499c94d9dd': [5680, 88.2631, 10], 'd8bf7aebbbaeef0': [5429, 3.6205, 11], '38df1aedef8e004': [5416, 44.1764, 12], 'f9a2fb187bcdc9f': [5082, 17.3066, 13], 'da71cdd001e06d6': [4375, 54.0655, 14], '3ddeb6ddcfc4f51': [3634, 20.8359, 15], 'cb54d184eb3677f': [2776, 91.0025, 16], '3ee4fbffa7150bc': [1587, 2878.6917, 17], 'bec776b6c8ce1ac': [1552, 65.1366, 18], 'acc61a49398bdd4': [1416, 12.1496, 19], 'ea75cd979ec705f': [1243, 756.3287, 20], 'd2b69efedff6f87': [818, 38.9721, 21], '08bccf6da86fba2': [795, 260.5804, 22], 'd343b9db0563a4e': [346, 22.139, 23]}, 'computer hardware': {'b87a9762ff1ecdc': [9808, 45.2578, 1], 'fb20b12fcf3f4be': [9652, 72.1107, 2], 'd253b3cee134fed': [9633, 5.7761, 3], '73ab5e45c1e5b55': [9469, 82.7335, 4], '9aaad5026aa8abf': [8952, 48.0709, 5], '391e22a22e6c77a': [8917, 790.7106, 6], 'c8efd8a1ae4e3cf': [8904, 60.3854, 7], '318c1f58cfcbda9': [8600, 21.4083, 8], '78ea4c2c1cb83ab': [8534, 72.8556, 9], '6f442e8596b4b4e': [8506, 104.7023, 10], '3f665deb1d8d4e9': [8303, 3363.8003, 11], 'c087578943f19e4': [7222, 214.3591, 12], '3851f381ea54d70': [6765, 35.1898, 13], '5a3d438bd544b85': [6676, 70.7411, 14], '6ea03577dc2f3c3': [6644, 31.3992, 15], '44b829ad3abbdf3': [6412, 29.3283, 16], '944bb87fc8a613e': [6412, 1.3267, 17], '32dffb53469ea98': [6330, 26.408, 18], 'a51ffffdb11cff2': [6030, 69.6975, 19], '89adcc6b8715b23': [6016, 217.8243, 20], 'e67e4dead7f7ac8': [5977, 23.4243, 21], '5b77f60c3cc6ae6': [5971, 75.1743, 22], '31aeba479968af3': [5962, 397.8579, 23], 'afeaf6beef0db13': [5687, 1512.9137, 24], '5cb0bbca289679c': [5406, 1225.955, 25], 'f801bac42f9ac1f': [4998, 56.407, 26], '60a7985f64acbaf': [4679, 142.4315, 27], 'bdf1b9f31a0dacb': [4256, 123.5729, 28], '1a1402caa5a1f1c': [4218, 63.29, 29], 'de66a10faf4e5b1': [4176, 31.9235, 30], 'ddce3797f22d3ae': [3985, 4938.4722, 31], 'ffdb822c7597c10': [3925, 355.7076, 32], 'ff4cdcd04bc0da8': [3886, 5.8095, 33], 'fcdbf9ac5f68eaa': [3512, 86.9496, 34], '54fa48043aaacd4': [3118, 97.8323, 35], '97bfc3c2f851b8b': [3081, 132.4173, 36], 'ceab4db1cad0adf': [2828, 6.6571, 37], 'faacec3019bf7f5': [2788, 67.5585, 38], '68aa8ddf26e3aca': [2540, 40.1107, 39], 'c494abe0cdb9c70': [2252, 386.5734, 40], '994aad9baa0bef3': [2251, 28.364, 41], '70eeceee7d6faec': [2240, 31.6066, 42], '7cf53a7abba2ca1': [2191, 317.92, 43], 'd17135fb399dd4c': [2164, 19.8459, 44], 'e7e0efaacc8122d': [1623, 19.5945, 45], 'a0bbb5ab97fe257': [1310, 3.6854, 46], 'c3ba071a2bb4d6f': [1053, 19.789, 47], 'c18b4aad9adf4cf': [1027, 38.3683, 48], 'ee4aa1dc0265e0e': [648, 83.8616, 49], 'a11b2cc54eae95b': [643, 62.2688, 50], 'd1f772a3528ecfc': [338, 58.559, 51], 'c7afe1e7295d09a': [311, 7.3951, 52], '9d7e4c3afd2392c': [157, 43.3793, 53], '0d2d0dc2ddb267c': [28, 29.3696, 54]}, 'biotechnology': {'3c08339af3bb8c8': [8575, 36.4935, 1], '7ade1d82d2ac863': [7205, 140.2845, 2], 'eaf5ae0fcbcb4dd': [6603, 78.062, 3], '139ab569bdfce4f': [3493, 62.6008, 4], 'a483cd7f7b486b4': [3427, 179.344, 5], 'bf1cc30febed38c': [481, 8.9567, 6], 'bde405d2e490ebe': [92, 38.1616, 7]}, 'information technology': {'f735adc8e8d53f4': [9719, 39.9308, 1], '94e7ccbaee6e83a': [9686, 31.5399, 2], '67eeacabcfccb6c': [9666, 142.8388, 3], 'db6109ab9fff8f4': [9510, 202.2082, 4], '722a53cbc046cac': [9503, 22.816, 5], '7647af9d4705c6b': [9497, 75.9206, 6], 'a25549b77e0c766': [9431, 63.875, 7], 'b6cf3a0fe2a5acd': [9286, 63.5874, 8], 'c9d4fb3bebd10bc': [9246, 232.1162, 9], 'c3ea6c9a31edf44': [9240, 84.5056, 10], '41ec4ddd3f62bbc': [9235, 80.317, 11], 'df6af24ee566f49': [9170, 142.357, 12], '96bbbefa9d8daec': [8887, 3.4543, 13], 'b598519fdfc530b': [8830, 177.6645, 14], 'cbe3da81dfae3a3': [8802, 237.7772, 15], 'cdf2e85ca8a7cfa': [8710, 14.9273, 16], 'cfc7683a8cee57d': [8509, 27.9091, 17], 'ff3aeca14f2b61b': [8461, 160.3011, 18], 'cce3b1c5f77bdf1': [8423, 0.526, 19], 'efc5c915acbf437': [8299, 80.9399, 20], 'f8bd41b97f5e96a': [8263, 37.5322, 21], 'dfd2cf9485b11c6': [8249, 70.1079, 22], 'dd7b5cbf5bc8fb8': [8228, 50.1027, 23], 'd8ec443ba5419a7': [8217, 175.474, 24], '1c1bc158dee046b': [8147, 37.5825, 25], 'b81ea4bd32537cf': [7919, 63.8846, 26], '4beaccfec62bbd7': [7755, 66.7427, 27], 'd5a9ace6035f9ce': [7675, 163.4107, 28], 'edbdabfd62cbea7': [7663, 1126.2073, 29], 'aa31e3ecbfb4bb1': [7649, 46.553, 30], 'ee1adb78478bf80': [7532, 5.1785, 31], 'eaa4e1cf00ee3c2': [7349, 1.0778, 32], '22f15be620aa6ae': [7348, 61.496, 33], '3dc422c0ac77de1': [7245, 20.3712, 34], 'afcbe39d8b0b2f6': [7241, 3.7014, 35], '6bdeeb7334ec8a1': [7150, 47.1, 36], 'acc4b161ae09e3e': [7096, 88.4882, 37], 'f56155a0a9ce693': [7082, 82.6334, 38], 'f7d126abdba0cb9': [7067, 69.6428, 39], 'ab2ea15d98b6bd4': [7020, 85.8431, 40], 'a4fecc8bb7aff7b': [7020, 52.3564, 41], '2f31eddf2db9aae': [6991, 67.1851, 42], '9c9ad5abae300f4': [6903, 191.8545, 43], '9e9ec3be1ded6d1': [6822, 13.3905, 44], '41ef2a0f35c4fa7': [6742, 101.2749, 45], 'a0fe365befc1aab': [6607, 82.1188, 46], '0aded4af925c9ec': [6572, 246.8783, 47], '4cfce7fab148cc8': [6458, 221.9198, 48], '788906d5eddabe1': [6403, 386.9079, 49], 'ba4ed05a7e04fec': [6366, 10.4427, 50], 'f32aed40d49de04': [6357, 28.2253, 51], 'c398a370ccfe05f': [6176, 129.1794, 52], '630effa39f6f50d': [6085, 510.4875, 53], '95e2fc82ca04a9b': [5975, 89.3466, 54], 'e3b3a0e923874cf': [5969, 23.0648, 55], '062fdfdc5aa37f9': [5959, 113.6367, 56], 'f6cfebba4acd3ca': [5943, 469.464, 57], '2d66c5bc84d36bf': [5842, 10.5002, 58], '56bdd78bbcdcca4': [5821, 72.2262, 59], 'a7d5585efe783de': [5799, 211.6505, 60], 'f7adb3a0e3553df': [5786, 59.9547, 61], '0aa03de0f49f09d': [5723, 36.9955, 62], '0502b16c90e7072': [5687, 14.3257, 63], '040bddafc73cb32': [5597, 77.9869, 64], 'a7b73fd2d7a38d0': [5338, 180.8178, 65], 'fff54ebcb7f443b': [5299, 6.1177, 66], '2fff9ac231a6768': [5250, 91.9342, 67], '4daeeda7cbc40a1': [5247, 179.976, 68], 'c357e7ecee0ec17': [5201, 64.225, 69], 'dffd5cb3c19fa22': [5042, 42.891, 70], 'f1d537929fa45ad': [4884, 34.3628, 71], 'df3b3ed4193d90f': [4864, 204.1709, 72], '64d0598e6f89c12': [4864, 69.4323, 73], '0aab0baad1d0622': [4813, 56.106, 74], '89d4ed3f2bd8cdc': [4759, 10.0329, 75], 'e898490f4b5ccbb': [4635, 177.1784, 76], 'ebdafefb1fde197': [4606, 19.8805, 77], 'ff0a16aceaad6de': [4604, 2171.5336, 78], '3cce7ee2c078d51': [4587, 148.9817, 79], 'c158808ca005a75': [4556, 84.1118, 80], '0052abdaff57dac': [4544, 10.8048, 81], '71d0fabef420ac6': [4484, 175.6245, 82], 'b4ff489acfe154d': [4470, 121.8325, 83], 'ac3ce792fadcd5f': [4447, 44.089, 84], 'df8e88cfabc1f3d': [4437, 31.6561, 85], '8b43a3446ad871c': [4408, 66.9575, 86], 'ab2db5c6c1a2a36': [4342, 120.4243, 87], '405ee5ec62afbac': [4319, 9.1433, 88], 'c1fbdc26744c6a6': [4238, 40.5603, 89], '2606f29ee3f97f5': [4089, 766.981, 90], 'c3b6dfaaa57f88c': [4077, 228.681, 91], '83f947d8ee5773b': [3985, 74.0814, 92], 'a83b7d8ed965d17': [3842, 57.6523, 93], 'b25ffe2fdbc55d1': [3811, 233.9915, 94], '57a23e8bcf9d340': [3786, 82.737, 95], '073cf1efaada57a': [3702, 10.1733, 96], 'c6eb96acc73baa0': [3619, 185.6986, 97], '53bb589efdb6118': [3399, 2580.3319, 98], '5e75d5cd8beb4da': [3382, 26.7647, 99], '1aee77abf8647f4': [3308, 17.8581, 100], 'ce8feac6b8c8e44': [3289, 85.3747, 101], 'f58be3967e3fa62': [3242, 334.4071, 102], 'c7e8caa3fe0ea9c': [3238, 54.9142, 103], '9e8bdfef88aa4e9': [3233, 2.3956, 104], '47344a0d7ded6a5': [3182, 57.6542, 105], '477cdccc1e02aad': [3162, 111.7113, 106], '736e0c8368e8f3d': [3136, 61.1451, 107], 'c48febcf2558dec': [3123, 44.6014, 108], 'd9a26d0e83cbbce': [3113, 2095.7369, 109], '496ed1c0e85d7f5': [3098, 734.3461, 110], '7dc8c8cd1ff23fe': [3098, 172.2507, 111], 'b419bfbdf7ceb25': [3064, 65.2718, 112], 'a832ebc6811df1a': [2996, 40.317, 113], 'ec1ddbcbd1c649f': [2928, 49.2988, 114], 'eec9cebd4cdfd4e': [2760, 51.4858, 115], 'd1ee04a587a0b6f': [2726, 45.3119, 116], '73fac61efec51cd': [2712, 28.6664, 117], '0c6d831e8dcecfe': [2709, 177.0294, 118], 'a8954a402a90e7f': [2685, 463.545, 119], 'c3c4eadeddcaacb': [2674, 173.0393, 120], '7fdeeff01a742de': [2668, 80.9032, 121], 'fb9ca60b6cef6da': [2624, 7.988, 122], '1f91dfc7bbef29e': [2495, 39.8636, 123], '4fefe84ab8d7ca2': [2368, 3.5675, 124], 'e3f8efc10ad96e9': [2330, 71.0933, 125], 'c44a5cdf9c829e3': [2273, 126.2877, 126], 'f1d5c69dfb934fb': [2268, 46.5977, 127], 'cc45ccf52fec2fe': [2179, 20.8721, 128], 'c2fa8baecc7d0f8': [2101, 143.6145, 129], '8f48cab85ee2dc5': [2050, 10.3483, 130], '4c0ab3fc0bd3e59': [2037, 33.1227, 131], '5bf4d472d771bd2': [1903, 90.9419, 132], '7db53b8ca40ab0d': [1878, 41.7293, 133], 'a3bb544c4f950e5': [1693, 18.2145, 134], 'f6025bcbbd3953e': [1422, 74.7197, 135], 'e86e20273da5da7': [1397, 56.0048, 136], '6bc62f2c0fcfb43': [1312, 24.0842, 137], '2dc933bd78efeca': [1185, 10.169, 138], 'bebdbffb7a060b6': [1132, 52.6751, 139], '61521f79cd45a7b': [321, 23.0634, 140], 'dfcadad69fe1d2a': [305, 25.6996, 141], 'a2a1fceed2eb3c9': [68, 26.1726, 142], '1f8d1eb79aad8e6': [48, 78.9466, 143], '27cebbbbcf4e17f': [36, 50.0813, 144], 'f4bdec9dbc6fd93': [20, 12.1658, 145]}, 'construction': {'699e5b0fe674695': [9686, 12.0395, 1], 'abf8dccabe179f9': [9440, 3.8979, 2], 'ebcf126fe9fdead': [9283, 2.3954, 3], 'e0c34c4c54d52fe': [9069, 105.482, 4], 'beea0cefcd9b53a': [9014, 84.8738, 5], '6a4dad8c40aa962': [8641, 35.079, 6], 'b943aa9d8d33575': [8318, 11.4812, 7], 'dc94cdf6d5bddbd': [7961, 46.9659, 8], 'dc421a3a9b6d50d': [7613, 333.3893, 9], 'f4ba33faae5dcc6': [7607, 63.4315, 10], 'a4c0c42a1ebe6e4': [7429, 29.0803, 11], '3a3d7c279ef39ed': [6864, 153.8779, 12], 'e1dd58a2ced2812': [6847, 158.2616, 13], 'aacadfad1365da3': [6796, 135.2416, 14], '9fb0f575eda185e': [6746, 87.3921, 15], 'b8a269b56c88826': [6597, 10.2233, 16], 'ea29bafac0fd400': [6436, 239.86, 17], '6e2fa3d40fdfdec': [5840, 501.3496, 18], 'ecc3baf0677bf90': [5662, 77.7872, 19], '00b6a6fdc035ff3': [5184, 42.6341, 20], 'b73b0deedeecca0': [5050, 10.5957, 21], 'dad2bd3ae5ce86d': [4878, 655.5911, 22], 'c477dfe441aa317': [4680, 87.7997, 23], 'a428fb0f7d1ada4': [4522, 795.4817, 24], '3ddb89ecd83b533': [4467, 127.3172, 25], 'aeec625ffe6bbcc': [4441, 11.2321, 26], '30a079b41f85cf7': [4156, 95.824, 27], 'a9aace4ae9da4e5': [4066, 284.1802, 28], 'de5fc71de825bfc': [3825, 13.7118, 29], 'd8eae5c3a1f27ef': [3822, 66.0114, 30], '924fc506bd20747': [3215, 42.6462, 31], '136dd17ebfae94f': [3160, 49.3332, 32], '83fb0faf1f3421d': [2882, 16.9106, 33], '513f535882afd7d': [1852, 10.6032, 34], '9ec666e820d8b6c': [1615, 50.4789, 35], '35762be17ca3d47': [1424, 2783.3153, 36], 'e3b672feed6ecba': [1416, 13.1242, 37], '8b901f70eaf1bbe': [1075, 3.5964, 38], '334b91221694b23': [953, 12.0654, 39], '4d6a2a19bf95fc4': [802, 49.1045, 40], 'e5cab57fff6f4bd': [117, 3472.6897, 41]}, 'textiles': {'effe2cb0aacfdfb': [9089, 144.8751, 1], 'a24dfd5ad79c3a7': [8897, 52.6738, 2], 'e82ec3fefc5ac80': [8891, 33.1482, 3], 'cdfbabdd3ae5ca1': [8674, 30.2233, 4], '8bb4d87c9e9b58d': [8578, 441.4196, 5], '2e9eeb3cb58afcd': [7578, 139.3893, 6], 'a98cb22e83aec1a': [6926, 82.0295, 7], '61da9fefc27c3a9': [5982, 43.5416, 8], 'c82cee1027a60e8': [5802, 80.7004, 9], 'b4af39efb508dee': [5800, 88.8559, 10], '9abeb8aafd25e04': [5355, 47.7618, 11], 'ad2eb3c8c24db87': [5105, 62.2994, 12], '8bbc7a4ba6388f6': [4559, 24.1257, 13], 'cbbb2861c47e17d': [4233, 82.3591, 14], '52bc0070051fbf9': [4209, 61.8382, 15], 'eb43ce5cb105fcc': [4031, 30.1232, 16], 'b73e7cac4fae8fe': [3541, 961.2493, 17], 'c9dbfbffffef44c': [3511, 114.8142, 18], '734ae2a83a2c3dc': [3488, 252.5446, 19], '6426a5886e94bcd': [3070, 24.7659, 20], '680dca425fdbb9b': [2895, 145.4461, 21], '82def5c9d6f513d': [2253, 29.0269, 22], '1d1a0fbb82a912b': [2235, 11.1505, 23], 'ab2bfec96f40b9b': [1971, 23.4418, 24], '51ccd5cdfdba968': [1587, 34.1153, 25], '53b148affae7f4c': [1202, 54.0863, 26], '521b3d4a4be241e': [904, 59.1427, 27], '529e8d003d34c28': [876, 120.1727, 28], '50a5cfcded6ad6a': [816, 18.4386, 29], '6fcb10da7e6f9df': [640, 222.0099, 30], '5e94b45be9da540': [599, 429.3757, 31]}, 'insurance': {'46671edec7cf6bf': [9376, 199.5032, 1], 'd2cb5b5e5ac938a': [9343, 0.221, 2], '522809bebbfce43': [9329, 3.586, 3], 'de596ab67e93e2d': [9307, 186.8027, 4], 'dcffb6bcb80bc16': [9256, 71.5118, 5], 'afc46d7facecd9b': [9178, 93.7816, 6], '8f3d5626d7d4f41': [9088, 33.3774, 7], 'fe6b0d849ea1ff8': [9074, 58.862, 8], 'a4ff0d1bed7ad9f': [9013, 322.3183, 9], '183edd689dbde8f': [8873, 23.2489, 10], 'dcbfdc5b5ef0c20': [8788, 185.5415, 11], 'd60eb560ccf800f': [8738, 54.4851, 12], 'ecdbf14f9f876d7': [8644, 5.7268, 13], 'b0bbebb36babb35': [8497, 789.8824, 14], 'badce4b6b7e6ecf': [8491, 357.9448, 15], '98c2ae97c376cfd': [8383, 305.1874, 16], 'f21ac01c1c5f5ff': [8184, 191.8967, 17], '0ab00dcbeb6d7b1': [7978, 35.2286, 18], 'e1e2ede231a49aa': [7913, 872.6033, 19], '60abfeaf173adba': [7846, 6.7194, 20], '0b19f0056c68e6f': [7664, 78.7121, 21], 'f86a2ca7a4def88': [7464, 93.2766, 22], '91fc21f3ff0c6a4': [7454, 89.3544, 23], 'ddce8f6ec509efd': [7175, 116.768, 24], 'f8e394bbabdb0b5': [6932, 46.5593, 25], '94122a41a8a8481': [6922, 197.504, 26], '4f223d5c80a096d': [6839, 7.9915, 27], '3aecbe853d893db': [6826, 21.3344, 28], '23a677cecd2bcac': [6346, 1389.6467, 29], 'd3e19c1c996c3bb': [6151, 20.2041, 30], '624f5e1c3c0f0a0': [6016, 113.0487, 31], '2e92e71eb9e6fb7': [5703, 2.3635, 32], 'bc6adfff45c6bdd': [5650, 4.0556, 33], '14db63a4ea4212f': [5540, 111.8605, 34], 'ed8de6f5f3a97db': [5395, 29.6309, 35], '3fc5f6509b65987': [5253, 18.9749, 36], 'f0a58aa2db37dda': [5052, 34.8692, 37], 'da2fe1267ccbbae': [4929, 30.6814, 38], '47ebb7eafe0b9b8': [4691, 9.0859, 39], 'a66737ce0ccb2c6': [4337, 762.8689, 40], 'c61dd4bb78351a7': [4308, 1284.9094, 41], 'dfa6b1cf6ffbddc': [4243, 1141.6871, 42], 'efec11ca6a7f3a0': [4155, 47.0855, 43], 'f41fddfa46ad4b8': [4118, 250.7502, 44], '2402ecd89b5e16d': [3884, 86.4935, 45], 'ef80e90db608daf': [3583, 339.8333, 46], '78fcb64cb9a9c40': [3410, 6.3041, 47], 'f3da775bab0f1f7': [3269, 101.7186, 48], '06fae819cce7d30': [2987, 21.9864, 49], 'cc06c8c9ac5d4db': [2874, 10.2265, 50], 'ef65aebcdfbc7f2': [2775, 78.4685, 51], '69dcf87b76e8d91': [2660, 135.6256, 52], 'dddbddfcff9f56f': [2616, 92.8693, 53], 'f932fe8fc8bdbb5': [2378, 33.219, 54], 'e35517078fc19db': [2185, 91.5217, 55], 'dc47da5dbd7f9a7': [2008, 1.1601, 56], 'b98b5b8944c73cd': [1905, 38.8879, 57], '61ff50b0caece58': [1545, 44.2283, 58], '4eb2ba5bdadcabb': [1363, 83.595, 59], 'bbd8aa10ddeb16b': [1228, 82.5869, 60], 'dee2ebd7e3cac97': [869, 84.743, 61], 'dc6d6e7ea7deabd': [406, 43.7043, 62]}}
flag = True
print(f'length of OP2: {len(OP2)}. expected length: {len(OP2s)}')
if len(OP2) != len(OP2s):
    flag = False
for idx in OP2:
    for ditem in OP2s[idx]:
        for i in range(len(OP2s[idx][ditem])):
            if OP2s[idx][ditem][i] != OP2[idx][ditem][i]:
                print(f'difference in output at index {idx}, id {ditem}. got {OP2[idx][ditem]}, expected {OP2s[idx][ditem]}')
                flag = False
print(flag)
