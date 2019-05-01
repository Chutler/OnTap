#! python3

# import modules
import requests, bs4

# Get HTML from the Saraveza Tap List
res = requests.get('http://fbpage.digitalpour.com/?companyID=51c24092fb890c13d86749af&locationID=1')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
soup = bs4.BeautifulSoup(res.text, 'html.parser')

beverages =[]  # a list to store beer on tap 

# narrow the code to be parsed to the parent 'tapList' div 
taplist = soup.find('div', attrs = {'class':'tapList'}) 

# iterate through each list item that contains info for a tap
for lineitem in taplist.findAll('li'): 
    aBeer = {}  
    aBeer['producer'] = lineitem.find(class_="producerName").get_text().strip() 
    aBeer['beverage'] = lineitem.find(class_="beverageName").get_text().strip()
    aBeer['style'] = lineitem.find(class_="beverageStyle").get_text().strip()
    # aBeer['new'] = lineitem.find(class_="justTapped").get_text() 
    # lineitem['color'] = lineitem.find(class_="kegLevelWrapper").get_style() #color indicates beer left in keg
    beverages.append(aBeer) 

# print(beverages)

onTap = [] # a list to store results when beers searched for are on tap

def match_beer(key, value):
    ''' Iterates through beverages dictionaries looking for key value matches.'''
    for beer in beverages:
        if beer[key].lower() == value.lower():
            onTap.append(beer)

# Call the function to check for beers on tap...        
match_beer('producer', 'Heater Allen')
match_beer('producer', 'Matchless')
match_beer('producer', 'Breakside')

# Check the length of onTap to see if any results were found. 
if len(onTap) == 0:
    print('No matches found')
else:
    print('The beer listed below is on tap now at Saraveza:')

# Print the results list...
for beer in onTap:
    # print(f'{beer['producer']} {beer['beverage']} {beer['style']}') 
    print('{} {} {}.'.format(beer['producer'], beer['beverage'], beer['style']))
    