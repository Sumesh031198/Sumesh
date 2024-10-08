import requests
import pandas as pd

# create request header
headers = {'User-Agent': "sumesh031198@gmail.com"}

#get all company data 
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers 
)

#review Response / Keys
print(companyTickers.json().keys())

#format response to dictionary and get the first key
firstentry = companyTickers.json()['5']
if isinstance(firstentry, dict):
    print(firstentry)

# If firstentry is a list of dictionaries, print the first dictionary in the list
elif isinstance(firstentry, list) and len(firstentry) > 0:
    print(firstentry[0])

#parse CIk
directCik = companyTickers.json()['5']['cik_str']
directCik = str(int(directCik))
print(directCik)


#create dataframe
companydata = pd.DataFrame.from_dict(companyTickers.json(),orient='index')

companydata['cik_str']= companydata['cik_str'].astype(str).str.zfill(10)
print(companydata[:5])

cik = companydata.iloc[2]['cik_str']
print(cik)

#company specific metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',headers=headers
)

# Convert JSON response to a dictionary
data = filingMetadata.json()

# Print keys and structure for debugging
print("Keys in the JSON response:", data.keys())

# Access the 'filings' key and its sub-keys
if 'filings' in data:
    filings = data['filings']
    print("Keys in 'filings':", filings.keys())
    
    if 'recent' in filings:
        recent_filings = filings['recent']
        print("Keys in 'recent':", recent_filings.keys())
        
        # Convert recent filings to a DataFrame
        allforms = pd.DataFrame.from_dict(recent_filings)
        print("DataFrame columns:", allforms.columns)

        # Display specific columns and rows
        try:
            result = allforms[['accessionNumber', 'reportDate', 'form']].head(50)
            print(result)
        except KeyError as e:
            print(f"KeyError: {e}. Ensure that the specified columns are present in the DataFrame.")
    else:
        print("'recent' key not found in 'filings'.")
else:
    print("'filings' key not found in the JSON response.")

#10-Q Metadata
specific_row = allforms.iloc[14]
print(specific_row)

#get company facts data 
companyFacts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',headers=headers)

facts_data = companyFacts.json()

# Inspect the keys at the top level
print(facts_data.keys())

# Access the 'facts' key
if 'facts' in facts_data:
    facts = facts_data['facts']
    print(facts.keys())
else:
    print("'facts' key not found in the JSON response.")

# filing metadata
try:
    stock_shares_outstanding = facts_data['facts']['dei']['EntityCommonStockSharesOutstanding']
    
    # Print the keys at this level
    print(stock_shares_outstanding.keys())
    
    # Access the 'units' key
    units = stock_shares_outstanding['units']
    print(units.keys())
    
    # Access the 'shares' key
    shares = units['shares']
    print(shares)
    
    # Print the first element in the 'shares' list
    if len(shares) > 0:
        print(shares[0])
    else:
        print("No shares data available.")
except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# Print available keys in 'us-gaap'
us_gaap_facts = companyFacts.json()['facts']['us-gaap']
print(us_gaap_facts.keys())  # Lists all available financial concepts

# Access specific financial concepts
accounts_payable = us_gaap_facts.get('AccountsPayable', {})
revenues = us_gaap_facts.get('Revenues', {})
assets = us_gaap_facts.get('Assets', {})

print('Accounts Payable:', accounts_payable)
print('Revenues:', revenues)
print('Assets:', assets)

# Fetch specific concept data
companyConcept = requests.get(
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json',
    headers=headers
)

# Print the concept data
concept_data = companyConcept.json()
print(concept_data.keys())  # Print keys in the concept data to understand its structure

# Access the data and print it
print(concept_data)

# Load the JSON data
concept_data = companyConcept.json()

# Print the keys to understand the structure
print(concept_data.keys())

# Navigate through the nested structure to get the value
units_data = concept_data.get('units', {})
usd_data = units_data.get('USD', [])
if usd_data:
    # Print the first value, if available
    asset_value = usd_data[0].get('val', 'No value found')
    print('Asset Value:', asset_value)
else:
    print('USD data not found')

assetsData = pd.DataFrame(usd_data)

# Display the DataFrame
print(assetsData.head())

import matplotlib.pyplot as plt

# Review columns
print(assetsData.columns)

# Check 'form' column if it exists
if 'form' in assetsData.columns:
    print(assetsData['form'].unique())

# Get assets data from 10-Q forms and reset index
assets10Q = assetsData[assetsData['form'] == '10-Q']
assets10Q = assets10Q.reset_index(drop=True)

# Plot
if not assets10Q.empty:
    assets10Q.plot(x='end', y='val', kind='line', title='Assets from 10-Q Forms')
    plt.xlabel('End Date')
    plt.ylabel('Value (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No 10-Q forms found in the data.")


