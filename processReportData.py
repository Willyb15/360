from pprint import pprint

def processReportData(report,friendlyValues,verticaConn,vTableName,startDate,reportSuite):

    reportData = report['data']
    if len(reportData) == 1:
        reportRow = "'" + startDate + "','" + reportSuite + "','" + friendlyValues['segment'] + "','" + friendlyValues['region'] + "','" + friendlyValues['metric'] + "','" + friendlyValues['detail'] + "'," + reportData[0]['counts'][0]
        print(reportRow)
        vcur = verticaConn.cursor()
        vcur.execute("INSERT INTO " + vTableName + " VALUES (" + reportRow + ")")

    if len(reportData) >= 1:
        if friendlyValues['metric'] == '<breakout>':
                for i in range(len(reportData)):
                    reportDataName = reportData[i]['name'].replace("'","")
                    if reportDataName == "::unspecified::": continue
                    if reportDataName == "::uniques_exceeded::": continue
                    reportRow = "'" + startDate + "','" + reportSuite + "','" + friendlyValues['segment'] + "','" + friendlyValues['region'] + "','" + reportDataName + "','" + friendlyValues['detail'] + "'," + reportData[i]['counts'][0]
                    #print(reportRow)
                    vcur = verticaConn.cursor()
                    vcur.execute("INSERT INTO " + vTableName + " VALUES (" + reportRow + ")")

        if friendlyValues['segment'] == '<breakout>':
                for i in range(len(reportData)):
                    reportDataName = reportData[i]['name'].replace("'", "")
                    if reportDataName == "::unspecified::": continue
                    if reportDataName == "::uniques_exceeded::": continue
                    reportRow = "'" + startDate + "','" + reportSuite + "','" + reportDataName + "','" + friendlyValues['region'] + "','" + friendlyValues['metric'] + "','" + friendlyValues['detail'] + "'," + reportData[i]['counts'][0]
                    #print(reportRow)
                    vcur = verticaConn.cursor()
                    vcur.execute("INSERT INTO " + vTableName + " VALUES (" + reportRow + ")")

        if friendlyValues['detail'] == '<breakout>':
                for i in range(len(reportData)):
                    reportDataName = reportData[i]['name'].replace("'", "")
                    if reportDataName == "::unspecified::": continue
                    if reportDataName == "::uniques_exceeded::": continue
                    reportRow = "'" + startDate + "','" + reportSuite + "','" + friendlyValues['segment'] + "','" + friendlyValues['region'] + "','" + friendlyValues['metric'] + "','" + reportDataName + "'," + reportData[i]['counts'][0]
                    #print(reportRow)
                    vcur = verticaConn.cursor()
                    vcur.execute("INSERT INTO " + vTableName + " VALUES (" + reportRow + ")")

        if friendlyValues['region'] == '<breakout>':
                 for i in range(len(reportData)):
                    reportDataName = reportData[i]['name'].replace("'", "")
                    if reportDataName == "::unspecified::": continue
                    if reportDataName == "::uniques_exceeded::": continue
                    reportRow = "'" + startDate + "','" + reportSuite + "','" + friendlyValues['segment'] + "','" + reportDataName + "','" + friendlyValues['metric'] + "','" + friendlyValues['detail'] + "'," + reportData[i]['counts'][0]
                    #print(reportRow)
                    vcur = verticaConn.cursor()
                    vcur.execute("INSERT INTO " + vTableName + " VALUES (" + reportRow + ")")