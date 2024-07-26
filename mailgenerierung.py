import json
from datetime import datetime
import locale
import os

# Set the locale to de-DE
locale.setlocale(locale.LC_TIME, 'de_DE')

# Prompt the user for their choice
user_choice = input("Choose an option (1 for 'Sitzungsankündigung', 2 for 'Zoomsession'): ")

# Validate the user's choice
if user_choice not in ["1", "2"]:
    print("Invalid choice. Please choose 1 or 2.")
    exit()

# Determine the file names based on the user's choice
if user_choice == "1":
    input_file_name = "sitzungsankuendigung_template.html"
    output_file_name = "sitzungsankuendigung_output.html"
else:
    input_file_name = "zoomsession_template.html"
    output_file_name = "zoomsession_output.html"

# Create the "output" folder if it doesn't exist
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the data from the JSON file
input_folder = "input"
sensitive_data_file_path = os.path.join(input_folder, 'sensitive_data.json')
if not os.path.exists(sensitive_data_file_path):
    print("sensitive_data.json not found in input folder. Please consider README.md for the required preparation steps.")
else:
    with open(sensitive_data_file_path) as file:
        sensitive_data = json.load(file)

# Format the date values
datumNaechsteSitzung = datetime.strptime(sensitive_data["datumNaechsteSitzung"], "%Y-%m-%d").strftime("%A, %d. %B %Y")
datumLetzteSitzung = datetime.strptime(sensitive_data["datumLetzteSitzung"], "%Y-%m-%d").strftime("%A, %d. %B %Y")
datumGeschaeftsordnung = datetime.strptime(sensitive_data["datumGeschaeftsordnung"], "%Y-%m-%d").strftime("%A, %d. %B %Y")

# Create a variable to hold the data
data_object = {
    "datumNaechsteSitzung": datumNaechsteSitzung,
    "datumLetzteSitzung": datumLetzteSitzung,
    "datumGeschaeftsordnung": datumGeschaeftsordnung,
    "linkZumProtokoll": sensitive_data["linkZumProtokoll"],
    "zoomUhrzeit": sensitive_data["zoomUhrzeit"],
    "zoomMeetingId": sensitive_data["zoomMeetingId"],
    "zoomSchnelleinwahlMobil": sensitive_data["zoomSchnelleinwahlMobil"],
    "zoomEinwahlNachAktuellemStandort": sensitive_data["zoomEinwahlNachAktuellemStandort"],
    "zoomOrtseinwahlSuchen": sensitive_data["zoomOrtseinwahlSuchen"],
    "zusaetzlicheInfos": sensitive_data["zusaetzlicheInfos"],
    "sprecherinnen": sensitive_data["sprecherinnen"],
    "nameLag": sensitive_data["nameLag"],
    "uhrzeitNaechsteSitzungStart": sensitive_data["uhrzeitNaechsteSitzungStart"],
    "uhrzeitNaechsteSitzungEnde": sensitive_data["uhrzeitNaechsteSitzungEnde"],
    "linkZurTagesordnung": sensitive_data["linkZurTagesordnung"],
    "linkZurSignalGruppe": sensitive_data["linkZurSignalGruppe"],
    "linkZuDiscourse": sensitive_data["linkZuDiscourse"],
    "linkZuUnterarbeitsgruppen": sensitive_data["linkZuUnterarbeitsgruppen"],
    "linkZurGeschaeftsordnung": sensitive_data["linkZurGeschaeftsordnung"],
    "linkZumKalender": sensitive_data["linkZumKalender"]
}

# Load the HTML template file
with open(os.path.join(input_folder, input_file_name), 'r') as file:
    html_template = file.read()

# Replace the placeholders with the values from data_object
for key, value in data_object.items():
    placeholder = "{{" + key + "}}"
    if key == "zoomSchnelleinwahlMobil" and isinstance(value, list):
        replacement = "<br />".join(value) + "<br />"
        html_template = html_template.replace(placeholder, replacement)
    elif key == "zoomEinwahlNachAktuellemStandort" and isinstance(value, list):
        replacement = "<br />".join("&nbsp;&nbsp;&nbsp;" + item for item in value) + "<br />"
        html_template = html_template.replace(placeholder, replacement)
    elif key == "zoomOrtseinwahlSuchen":
        if value:
            replacement = f'Ortseinwahl suchen: <a href="{value}" target="_blank" ref="noopener" class="a" style="font-weight: 900; color: #FFFFFF;"><span class="a__text" style="color: #FFFFFF;">{value}</span></a>'
            html_template = html_template.replace(placeholder, replacement)
        else:
            html_template = html_template.replace(placeholder, "")
    elif key == "zusaetzlicheInfos" and isinstance(value, list):
        if value:
            replacement = "".join(
                f'<p class="text p" style="display: block; margin: 14px 0; font-size: 16px; line-height: 20px; color: #201D1B; font-family: PT Sans,Arial,sans-serif;">{item}</p>'
                for item in value
            )
            html_template = html_template.replace(placeholder, replacement)
        else:
            html_template = html_template.replace(placeholder, "")
    elif key == "sprecherinnen" and isinstance(value, list):
        replacement = ""
        for i, item in enumerate(value):
            replacement += f'<a href="mailto:{item["email"]}" class="a" style="font-weight: 900; color: #201D1B;"><span class="a__text" style="color: #201D1B;">{item["name"]}</span></a>'
            if i < len(value) - 2:
                replacement += ",&nbsp;"
            elif i == len(value) - 2:
                replacement += "&nbsp;und&nbsp;"
        html_template = html_template.replace(placeholder, replacement)
    else:
        html_template = html_template.replace(placeholder, value)

# Define the output file path
output_file_path = "output/output.html"

# Write the modified HTML content to the output file
output_file_path = os.path.join(output_folder, output_file_name)
with open(output_file_path, 'w') as file:
    file.write(html_template)

print("HTML content has been written to", output_file_path)
