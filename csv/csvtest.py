import os
#import csv
import pandas as pd

print("starting csv editing")
# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv('input.csv')

# Step 2: Remove rows where the value in the specified column matches the value to be removed
# this removes HB.archived = ja
df_filtered = df[df["HB.archived"] != "true"]
# this removes HB.field.Doos = nee
df_filtered2 = df_filtered[df["HB.field.Doos"] != "nee"]
# this removes HB.lifetime_warranty = true
df_filtered3 = df_filtered2[df["HB.field.Doos"] != "true"]

# Step 3: Write the filtered DataFrame back to a new CSV file
#df_filtered3.to_csv('output.csv', index=False)

print("Rows with specified collums values have been removed and the modified data has been saved to 'output1.csv'.")

# Step 4: Read the CSV file into a DataFrame
#df = pd.read_csv('output.csv')
df = df_filtered3
# Step 5: Delete the specified columns
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

# Step 6: Rename Collum names to a more clean name:  
df.rename(columns={'HB.location': 'location'}, inplace=True)
df.rename(columns={'HB.asset_id': 'asset_id'}, inplace=True)
df.rename(columns={'HB.name': 'name'}, inplace=True)
df.rename(columns={'HB.quantity': 'quantity'}, inplace=True)
#df.rename(columns={'HB.warranty_expires': 'warranty_expires'}, inplace=True) getting errors in this one
df.rename(columns={'HB.field.Doos': 'Doos'}, inplace=True)

# Step 7: Write the modified DataFrame back to a new CSV file
df.to_csv('output1.csv', index=False)

print("Columns has been deleted and the modified data has been saved to 'output1.csv'.")

# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv('output1.csv')

# Step 2: Convert the 'HB.warranty_expires' column to datetime format with error handling
# Try to parse dates and coerce errors to NaT (Not a Time)
df['HB.warranty_expires'] = pd.to_datetime(df['HB.warranty_expires'], errors='coerce', dayfirst=False)

# Step 3: Filter out rows where 'HB.warranty_expires' is before the specified date
# Replace '2025-01-01' with the date you want to use for filtering
specified_date = pd.to_datetime('2025-01-01')
df_filtered = df[df['HB.warranty_expires'] <= specified_date]

# Step 4: Write the filtered DataFrame back to a new CSV file
df_filtered.to_csv('output2.csv', index=False)

print("Rows with dates before the specified date have been removed and the modified data has been saved to 'output2.csv'.")
print("csv editing finished")
print("now starting index.html generation")

# Step 1: Read the CSV file into a DataFrame
df = pd.read_csv('output2.csv')

# Step 2: Convert the DataFrame to an HTML table
html_table = df.to_html(index=False)

# Save the HTML table to a file
with open('output2.html', 'w') as file:
    file.write(html_table)

print("CSV file has been converted to an HTML table and saved as 'output2.html'.")


# opening files in read only mode to read initial contents
f1 = open("index.html", 'w')
f2 = open("templates/header.html", 'r')
f3 = open("templates/footer.html", 'r')
c1 = open("output2.html", 'r')
 
# appending the contents of the second file to the first file
f1.write(f2.read())
f1.write(c1.read())
f1.write(f3.read())
 
# closing the files
f1.close()
f2.close()
f3.close()
c1.close()

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

if os.path.exists("output2.csv"):
    os.remove("output2.csv")
    print("deleted file output2.csv")
else:
    print("The file output.csv does not exist")

#if os.path.exists("output2.html"):
#    os.remove("output2.html")
#    print("deleted file output2.html")
#else:
    print("The file output2.html does not exist")

print("finished html generation")