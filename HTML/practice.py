testcaseInfo = {'123': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 123"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "PASS",
                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '234': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 234"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "FAIL",
                                 "Actual CAMM Message": "Hello this the CAMM Message",
                                 "Actual FIX Message": "Hello this is the FIX Message."}},
                '345': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 345"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "PASS",
                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '456': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 456"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                            "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                            "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                            {
                                "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                                "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                            },
                        "Result": {"OverallResult": "PASS",
                                  "Actual CAMM Message": "Hello this the CAMM Message",
                                  "Actual FIX Message": "Hello this is the FIX Message."}}
                }

print(list(testcaseInfo.values())[0]["CAMM Responses"])
print(list(testcaseInfo.values())[0]["FIX Responses"])

for len in range(2):
    for item in list(testcaseInfo.values())[len]["CAMM Responses"]:
        print(list(testcaseInfo.values())[len]["CAMM Responses"][item])
    for item in list(testcaseInfo.values())[len]["FIX Responses"]:
        print(list(testcaseInfo.values())[len]["FIX Responses"][item])