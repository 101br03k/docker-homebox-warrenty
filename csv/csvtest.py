import os
import pandas as pd

host = "http://192.168.0.11:3100"
#host = "https://demo.homebox.software"

# delete the old csv from previous job
if os.path.exists("output2.csv"):
    os.remove("output2.csv")
    print("deleted file output2.csv")
else:
    print("The file output.csv does not exist")

print("starting csv editing")
# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv('input.csv')

# Step 2: Remove rows where the value in the specified column matches the value to be removed
# this removes HB.archived = ja
df = df[df["HB.archived"] != "true"]
if "HB.field.Doos" in df.columns:
    print("HB.field.Doos collum found, removing empty and is not true rows for collum HB.field.Doos")
    # this removes HB.field.doos isnot true
    df = df[df["HB.field.Doos"] != "true"]
    # this removes HB.field.Doos = empty
    df = df.dropna(subset=["HB.field.Doos"])
else:
    print("HB.field.Doos collum not found")
# Step 3: Write the filtered DataFrame back to a new CSV file
#df_filtered3.to_csv('output.csv', index=False)

print("Rows with specified collums values have been removed and the modified data has been saved to 'output1.csv'.")

# Step 4: Delete the specified columns
df.drop('HB.import_ref', axis=1, inplace=True)
df.drop('HB.labels', axis=1, inplace=True)
df.drop('HB.url', axis=1, inplace=True)
df.drop('HB.archived', axis=1, inplace=True)
df.drop('HB.description', axis=1, inplace=True)
df.drop('HB.insured', axis=1, inplace=True)
df.drop('HB.notes', axis=1, inplace=True)
df.drop('HB.purchase_price', axis=1, inplace=True)
df.drop('HB.purchase_from', axis=1, inplace=True)
df.drop('HB.purchase_time', axis=1, inplace=True)
df.drop('HB.manufacturer', axis=1, inplace=True)
df.drop('HB.model_number', axis=1, inplace=True)
df.drop('HB.serial_number', axis=1, inplace=True)
df.drop('HB.lifetime_warranty', axis=1, inplace=True)
df.drop('HB.warranty_details', axis=1, inplace=True)
df.drop('HB.sold_to', axis=1, inplace=True)
df.drop('HB.sold_price', axis=1, inplace=True)
df.drop('HB.sold_time', axis=1, inplace=True)
df.drop('HB.sold_notes', axis=1, inplace=True)

#delete all custom collums (all custom collums start with hb.field.*) except those seperate specified with: and col != 'HB.field.Doos'
columns_to_drop = [col for col in df.columns if col.startswith('HB.field.') and col != 'HB.field.Doos']
df.drop(columns=columns_to_drop, inplace=True)



# Step 6: Write the modified DataFrame back to a new CSV file
df.to_csv('output1.csv', index=False)

print("Columns has been deleted")

# Step 8: Convert the 'HB.warranty_expires' column to datetime format with error handling
df['HB.warranty_expires'] = pd.to_datetime(df['HB.warranty_expires'], errors='coerce', dayfirst=False)

# Try to parse dates and coerce errors to NaT (Not a Time)
invalid_dates = df[df['HB.warranty_expires'].isna()]
if not invalid_dates.empty:
    print("Rows with invalid dates in 'HB.warranty_expires':")
    print(invalid_dates)
    
# Step 9: Filter out rows where 'HB.warranty_expires' is before the specified date
specified_date = pd.to_datetime('2025-01-01')
df = df[df['HB.warranty_expires'] <= specified_date]

#df["HB.asset_id"] = df["HB.asset_id"].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
a = "/a/"
df["HB.asset_id"] = df["HB.asset_id"].apply(lambda x: f'<a href="{host}{a}{x}" target="_blank">{x}</a>')
#print(df["HB.asset_id"])

# Step 5: Rename Collum names to a more clean name:  
df.columns = df.columns.str.replace('^HB\.', '', regex=True)
#df.rename(columns={'HB.warranty_expires': 'quantity'}, inplace=True) #getting errors in this one
df.rename(columns={'HB.field.Doos': 'Doos'}, inplace=True)



# Step 10: Write the filtered DataFrame back to a new CSV file
df.to_csv('output2.csv', index=False)

print("Rows with dates before the specified date have been removed and the modified data has been saved to 'output2.csv'.")
print("csv editing finished")
print("now starting index.html generation")

# Step 11: Read the CSV file into a DataFrame
df = pd.read_csv('output2.csv')

# Step 12: Convert the DataFrame to an HTML table
html_table = df.to_html(escape=False, index=False)

# Save the HTML table to a file
with open('output2.html', 'w') as file:
    file.write(html_table)

print("CSV file has been converted to an HTML table and saved as 'output2.html'.")

#setting style by selecting a css file
style = "homebox" # later implement changin it via docker env var
c1 = '<link rel="stylesheet" href="css/'+style+'.css"></head><body>'
#setting banner file
b1 = open('html-templates/banner/'+style+'.html','r')
# get amount of rows for stats
num_of_rows = len(df)
# add up amount of all items in the collum
total_sum = df["quantity"].sum()

# opening files in read only mode to read initial contents
o1 = open("index.html", 'w')
f1 = open("html-templates/header.html", 'r')
f2 = open("html-templates/header2.html", 'r')
f3 = open("html-templates/footer.html", 'r')
f4 = open("html-templates/header3.html", 'r')
f5 = open("html-templates/header4.html", 'r')
f6 = open("html-templates/header5.html", 'r')
h1 = open("output2.html", 'r')

# appending the contents of the second file to the first file
o1.write(f1.read())
o1.write(c1)
o1.write(b1.read())
o1.write(f2.read())
o1.write(str(num_of_rows))
o1.write(f4.read())
o1.write(str(total_sum))
o1.write(f5.read())
o1.write(str(num_of_rows))
o1.write(f6.read())
o1.write(h1.read())
o1.write(f3.read())

# closing the files
o1.close()
f1.close()
f2.close()
f3.close()
h1.close()

#removing files
print("")
if os.path.exists("output.csv"):
    os.remove("output.csv")
    print("deleted file output.csv")
else:
    print("The file output.csv does not exist")

if os.path.exists("output1.csv"):
    os.remove("output1.csv")
    print("deleted file output1.csv")
else:
    print("The file output1.csv does not exist")

if os.path.exists("output2.html"):
    os.remove("output2.html")
    print("deleted file output2.html")
else:
    print("The file output2.html does not exist")

print("finished html generation")