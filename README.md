# mopub_with_keywords
Reads in data from a csv, sets up line items and custom keywords

Usage:
1) Login to MoPub UI
2) Create new order
3) Open Chrome Dev Tools and go to the Network tab
4) Create a new line item, following the steps on https://community.pubmatic.com/display/IMOB/MoPub+ad+server+setup (iOS) or https://community.pubmatic.com/display/AMOB/MoPub+ad+server+setup (Android)
5) Right-click on "create", then "Copy as CURL"
6) Open a text editor, paste your clipboard from step 5, give it a unique name, and save as .txt
7) Open mopub_with_keywords.py.
8) Edit the link to the CSV file, as well as the .txt file that you just created
9) Run the script
10) Repeat for each Order you need to create
