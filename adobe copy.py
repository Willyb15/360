import omniture
import csv
import vertica_python

analytics = omniture.authenticate('analytics:sharecare','9235cea067a79aff9dd6950cfcb038a7')
# verticaConnectData = {
#     'host':'internal-qh-vertica-eld-1878753073.us-east-1.elb.amazonaws.com',
#     'port':5433,
#     'user':'brhodes',
#     'password':'scanalytics#255',
#     'database':'qualityhealth',
#     'read_timeout':600
# }

print("<<<<<<<<<<The following are the Analytics Report Suites>>>>>>>>>>>\n", analytics.suites)
suite = analytics.suites['sharecareprod']
print ("<<<<<<<<<<The following are is the sharecareprod report suite>>>>>>>>>>\n", suite)
print ("<<<<<<<<<<The following are the metrics>>>>>>>>>>\n", suite.metrics)
print("<<<<<<<<<<The following are the elements>>>>>>>>>>\n", suite.elements)
print("<<<<<<<<<<The following are the segments>>>>>>>>>>\n", suite.segments)
