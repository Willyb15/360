import datetime
import dateutil.relativedelta as dateutil

def generatePullDate(cadence,granularity,lookback,lastDate):
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    lookback = int(lookback)
    lastDate = datetime.datetime.strptime(lastDate, "%m/%d/%Y")

    if (cadence.lower() == "month") or (cadence.lower() == "months"):
        cadence = "months"
        endDate = lastDate + dateutil.relativedelta(months=lookback)
        if endDate < yesterday:
            startDate = lastDate + datetime.timedelta(days=1)
        else:
            dateData = "notready"
            return dateData
    elif (cadence.lower() == "day") or (cadence.lower() == "days"):
        cadence = "days"
        endDate = lastDate + dateutil.relativedelta(months=lookback)
        if endDate < yesterday:
            startDate = lastDate + datetime.timedelta(days=1)
        else:
            dateData = "notready"
            return dateData

    if (granularity.lower() == "days") or (granularity.lower() == "day"):
        granularity = "day"
    if (granularity.lower() == "months") or (granularity.lower() == "month"):
        granularity = "month"

    dateData = {'startDate':startDate.strftime("%Y-%m-%d"),'endDate':endDate.strftime("%Y-%m-%d"),'cadence':cadence,'lookback':lookback,'granularity':granularity}

    return dateData