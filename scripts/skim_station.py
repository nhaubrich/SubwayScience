#iterate through sorted MTA file and accumulate list of date-time/riders
import csv
import sys
import pandas as pd
import numpy as np
import holidays
import pdb
USholidays = holidays.US()

def readOneHour(fname):
    with open(fname,"r") as csvfile:
        datareader = csv.reader(csvfile)
        thisRow = next(datareader)
        while datareader:
            groupedRows = [thisRow]
            try:            
                nextRow = next(datareader)
            except:
                yield groupedRows

            while thisRow[0]==nextRow[0]:
                groupedRows.append(nextRow)
                try:
                    nextRow=next(datareader)
                except:
                    yield groupedRows
                    return
            thisRow=nextRow
            yield groupedRows 
        return


#let's add more features:
#24H, day of week, month
#Do fourier encoding https://stats.stackexchange.com/questions/126230/optimal-construction-of-day-feature-in-neural-networks
def fourierEncode(unit,period):
    return round(np.cos(2*np.pi*unit/period),8),round(np.sin(2*np.pi*unit/period),8)

#bonus: python holidays https://pypi.org/project/holidays/
timestamp,ridership = [],[]
hourX,hourY = [],[]
dayOfWeekX,dayOfWeekY = [],[]
monthX,monthY = [],[]
isHoliday = []


subwayStationIDs = set(['501', '502', '100', '101', '103', '10', '107', '108', '109', '110', '111', '113', '114', '118', '119', '120', '122', '123', '124', '125', '126', '127', '129', '130', '131', '13', '133', '134', '135', '136', '137', '138', '141', '14', '143', '144', '145', '146', '147', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '162', '164', '165', '167', '168', '16', '169', '173', '175', '176', '177', '179', '17', '180', '181', '182', '183', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '1', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '20', '210', '211', '212', '213', '214', '215', '216', '217', '218', '220', '221', '222', '223', '224', '225', '228', '22', '231', '232', '234', '235', '236', '237', '238', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263', '264', '265', '266', '268', '269', '26', '270', '271', '272', '273', '276', '277', '278', '279', '280', '282', '283', '284', '286', '287', '288', '289', '28', '290', '291', '292', '293', '294', '295', '296', '297', '298', '299', '2', '300', '301', '303', '304', '305', '306', '307', '308', '309', '30', '310', '311', '31', '312', '313', '314', '316', '318', '319', '320', '321', '32', '323', '324', '325', '326', '327', '328', '329', '3', '333', '33','334', '336', '337', '339', '340', '341', '343', '344', '34', '345', '346', '347', '348', '349', '350', '351', '352', '353', '354', '35', '355', '356', '357', '358', '359', '360', '361', '362', '363', '364', '365', '366', '367', '368', '369', '36', '370', '371', '372', '373', '374', '375', '376', '377', '37', '378', '379', '380', '381', '382', '383', '384', '385', '386', '387', '388', '38', '391', '392', '393', '394', '395', '396', '397', '398', '399', '39', '403', '404', '405', '407', '409', '413', '414', '416', '41', '417', '418', '419', '420', '421', '422', '423', '424', '425', '426', '427', '428', '429', '42', '430', '431', '432', '433', '434', '436', '437', '438', '439', '43', '440', '441', '442', '443', '444', '445', '446', '447', '448', '449', '44', '450', '451', '452', '453', '455', '456', '457', '458', '459', '45', '460', '461', '463', '464', '46', '471', '475', '476', '477', '47', '48', '49', '4', '50', '51', '52', '5', '53', '54', '55', '56', '57', '58', '59', '601', '602', '603', '604', '605', '606', '607', '608', '609', '60', '610', '611', '612', '613', '614', '61', '615', '616', '617', '618', '619', '620', '621', '622', '623', '624', '62', '625', '626', '627', '628', '629', '630', '635', '636', '6', '64', '65', '66', '67', '68', '69', '70', '71', '72', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '8', '86', '87', '88', '89', '90', '91', '93', '94', '9', '95', '96', '97', '98', '99', 'TRAM1', 'TRAM2'])

stationRidership = { "station_{}".format(station): [] for station in sorted(subwayStationIDs) }
gen=readOneHour(sys.argv[1])
columns = next(gen)[0]
for i,group in enumerate(gen):
    if i%1000==0:
        print(i)
    datetime = pd.to_datetime(group[0][0])
    timestamp.append(str(datetime)) #convert to pandas-default YYYY-MM-DD TIME here

    df = pd.DataFrame(group,columns=columns)
    df = df.astype({'ridership': int})
    #print(df.groupby('station_complex')['ridership'].sum())
    #ridership.append( sum([int(row[7]) for row in group]))
    ridership.append(df['ridership'].sum()) 

    hour =  fourierEncode(datetime.hour,24)
    hourX.append(hour[0])
    hourY.append(hour[1])
    dayOfWeek = fourierEncode(datetime.day_of_week,7)
    dayOfWeekX.append(dayOfWeek[0])
    dayOfWeekY.append(dayOfWeek[1])

    month = fourierEncode(datetime.month,12)
    monthX.append(month[0])
    monthY.append(month[1])

    isHoliday.append( (datetime in USholidays)*1)
    ridershipPerStation = df.groupby('station_complex_id')['ridership'].sum()
    stationsWithData = set(ridershipPerStation.keys())
    missingStationIDs = subwayStationIDs-stationsWithData
    #pdb.set_trace()
    for station in stationsWithData:
        stationRidership["station_{}".format(station)].append( ridershipPerStation[station])
    for station in missingStationIDs:
        stationRidership["station_{}".format(station)].append(0)

    

#fields = ["timestamp","ridership","hourX","hourY","dayOfWeekX","dayOfWeekY","monthX","monthY"]
df = pd.DataFrame({'timestamp': timestamp,'ridership': ridership,
        "hourX":hourX, "hourY":hourY,
        "dayOfWeekX": dayOfWeekX, "dayOfWeekY": dayOfWeekY,
        "monthX": monthX, "monthY": monthY,
        "isHoliday": isHoliday,
        }|stationRidership)
df.to_csv(sys.argv[1].split(".")[0]+"_skimmed_station.csv")



