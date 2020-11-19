import csv
import json
import subprocess
import re


# input values to be changed
reader = csv.reader(open('/Users/ericrygh/Desktop/Python/p365_mopub/320x480_fullscreen_interstitial.csv', 'r'))
linItemNamePrefix = "PubMatic OpenWrap" # here you need to put line item name prefix, line items will be generated as "Line Item Name ( 0.05 )" for bid value 0.05
fileName = "/Users/ericrygh/Desktop/Python/p365_mopub/300x250_banner_curl.txt" # name or path of the text file in which you have copied the Curl call of the line item which we need to refer; make sure it is created recently to have a valid csrf token


# read in data from the csv file, and load into a dictonary
d = {}
for row in reader:
   k, v = row
   d[k] = v.replace('\xa0', ' ')


# Here we need to read in a sample curl call to the MoPub system. This is needed for auth-related reasons. This requuest will then be modified.
f = open(fileName, "r")
curlCall = f.read()
f.close()

# grab the JSON post data
postData = re.findall("(--data-binary '(.*?)')", curlCall)
if postData and postData[0] and postData[0][1]:
    postDataJson = json.loads(postData[0][1])
    print(postDataJson)
else:
    print("Curl Call string is not as expected")


# this function will create new line itmes in the MoPub system
def create_line_item_with_keywords(postDataJson, line_item_prefix, price, keyword=None):

    # uses price directly, doesn't average it
    price = float(price)

    # update bid rate value
    print("Executing the MoPub API to create new line item with Bid Rate: %.2f" % (price))
    postDataJson['bid'] = price # Limit to 2 decimal points to get around the float behavior
    postDataJson['name'] = line_item_prefix + (" ( %.2f )" % (price)) # changing line item name

    if keyword:
        postDataJson['keywords'] = keyword.split('\n')
        print('keyword: %s' % keyword.split('\n'))

    # creating a copy of given curl call with new bid rate value
    newCurlCall = re.sub(r'--data-binary \'.*?\'', '--data-binary \'%s\'' % (json.dumps(postDataJson)), curlCall)
    print(newCurlCall)

# #     # execute curl call
#     output = subprocess.Popen(newCurlCall, shell=True, stdout=subprocess.PIPE).stdout.read()
#     print(output)
#     outputJson = json.loads(output)
#
#     # check response; if not successful, inform
#     if outputJson['status'] == "error":
#         print("Something went wrong, stopping the line item creation process. You may need to copy a new CSRF token from the browser and restart the process with firstLineItemBidRate set to %.2f ." % (price))
#     else:
#         print("Line item created successfuly.")



# call the create_line_item_with_keywords function for every pricepoint listed in the csv
for key in d.keys():
    if key != '\ufeff0.3' and key != '\ufeff1':
        create_line_item_with_keywords(postDataJson, linItemNamePrefix, key, d[key])
