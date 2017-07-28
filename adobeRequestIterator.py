import omniture  #Documentation found here: https://github.com/dancingcactus/python-omniture
import csv
import vertica_python
from compileTimingData import generatePullDate
from processReportData import processReportData
import emailFunctions
from pprint import pprint


analytics = omniture.authenticate('analytics:sharecare','9235cea067a79aff9dd6950cfcb038a7')
verticaConnectData = {
    'host':'internal-qh-vertica-eld-1878753073.us-east-1.elb.amazonaws.com',
    'port':5433,
    'user':'brhodes',
    'password':'scanalytics#255',
    'database':'qualityhealth',
    'read_timeout':600
}
verticaConn = vertica_python.connect(**verticaConnectData)
emailLog = ""

with open(r'C:\Users\Mentos\Automated Reports\Provider Monthly Reporting\Input Files\AdobePullSheet.csv','r') as reportInputList:
    reports = csv.reader(reportInputList)
    next(reports, None)
    for row in reports:
        reportName = row[0]
        reportLastDate = row[12]
        if row[11] == "NO":
            emailLog = emailFunctions.addSkipToEmailQueue(emailLog,reportName,'inactive',timing='')
            continue
        #Report request data
        reportElement = row[5].split(", ")
        reportMetric = row[6].split(", ")
        reportSegment = row[7].split(", ")

        #Report timing data
        reportCadence = row[8].lower()
        reportGranularity = row[9].lower()
        reportLookback = row[10]
        if row[14] != "":
            dataPoints = row[14]
        else:
            dataPoints = "5000"
        dateData = generatePullDate(reportCadence,reportGranularity,reportLookback,reportLastDate)
        if dateData == "notready":
            emailFunctions.addSkipToEmailQueue(emailLog,reportName,'notready',reportLastDate)
            continue

        #"Friendly"/Report-Facing Data
        friendlyValues = {'metric':row[1],'segment':row[2],'region':row[3],'detail':row[4]}

        #Set report suite
        reportSuiteString = row[13]
        suite = analytics.suites[reportSuiteString]
        vTableName = row[15]

        #Account for non-existent values.
        if reportMetric[0] == "":
            reportMetric[0] = "na"
        if reportSegment[0] == "":
            reportSegment[0] = "na"
        if reportElement[0] == "":
            reportElement[0] = "na"

        #Account for non-multiple values.
        for i in range(1,3):
            if len(reportMetric) <= i:
                reportMetric.append("na")
            if len(reportSegment) <= i:
                reportSegment.append("na")
            if len(reportElement) <= i:
                reportElement.append("na")

        if dateData['granularity'] == "":
             if dateData['cadence'] == "months":
                report = suite.report \
                    .metric(reportMetric[0]) \
                    .metric(reportMetric[1]) \
                    .metric(reportMetric[2]) \
                    .element(reportElement[0],top=dataPoints) \
                    .element(reportElement[1], top=dataPoints) \
                    .element(reportElement[2], top=dataPoints) \
                    .filter(reportSegment[0]) \
                    .filter(reportSegment[1]) \
                    .filter(reportSegment[2]) \
                    .range(dateData['startDate'],dateData['endDate'],months=dateData['lookback']) \
                    .sync()
             elif dateData['cadence'] == "days":
                report = suite.report \
                    .metric(reportMetric[0]) \
                    .metric(reportMetric[1]) \
                    .metric(reportMetric[2]) \
                    .element(reportElement[0],top=dataPoints) \
                    .element(reportElement[1], top=dataPoints) \
                    .element(reportElement[2], top=dataPoints) \
                    .filter(reportSegment[0]) \
                    .filter(reportSegment[1]) \
                    .filter(reportSegment[2]) \
                    .range(dateData['startDate'],dateData['endDate'],days=dateData['lookback']) \
                    .sync()
        else:
             if dateData['cadence'] == "months":
                report = suite.report \
                    .metric(reportMetric[0]) \
                    .metric(reportMetric[1]) \
                    .metric(reportMetric[2]) \
                    .element(reportElement[0],top=dataPoints) \
                    .element(reportElement[1], top=dataPoints) \
                    .element(reportElement[2], top=dataPoints) \
                    .filter(reportSegment[0]) \
                    .filter(reportSegment[1]) \
                    .filter(reportSegment[2]) \
                    .range(dateData['startDate'],dateData['endDate'],months=dateData['lookback']) \
                    .granularity(dateData['granularity']) \
                    .sync()
             elif dateData['cadence'] == "days":
                report = suite.report \
                    .metric(reportMetric[0]) \
                    .metric(reportMetric[1]) \
                    .metric(reportMetric[2]) \
                    .element(reportElement[0],top=dataPoints) \
                    .element(reportElement[1], top=dataPoints) \
                    .element(reportElement[2], top=dataPoints) \
                    .filter(reportSegment[0]) \
                    .filter(reportSegment[1]) \
                    .filter(reportSegment[2]) \
                    .range(dateData['startDate'],dateData['endDate'],days=dateData['lookback']) \
                    .granularity(dateData['granularity']) \
                    .sync()

        try:
            processReportData(report.report,friendlyValues,verticaConn,vTableName,dateData['startDate'],reportSuiteString)
            emailLog = emailFunctions.addSuccessToEmailQueue(emailLog,reportName)
        except:
             print(reportName + " failed in the processor. Check to ensure everything matches expected Vertica syntax.")
             emailLog = emailFunctions.addErrorToEmailQueue(emailLog,reportName,"Report Processor Failed")

    emailFunctions.sendEmail(emailLog)
    verticaConn.commit()
    verticaConn.close()
