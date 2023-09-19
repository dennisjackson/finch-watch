import json
import csv
from datetime import datetime
import sys
import os.path

# Replace 'input.json' with the path to your JSON file
input_file = sys.argv[1]
output_folder = sys.argv[2]

# Read JSON data from the file
with open(input_file, 'r') as json_file:
    json_data = json.load(json_file)

# Create and open a CSV file for writing

for channel_filter in ["STABLE","CANARY","DEV","BETA"]:
    with open(os.path.join(output_folder, f"{channel_filter}_table.csv"), 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the CSV header
        writer.writerow(["Name", "Consistency", "Experiment Name", "Probability Weight", "Enable Feature", "Disable Feature", "Forcing Feature On", "Forcing Feature Off", "Min Version", "Channel", "Platform", "End Date"])

        # Process JSON data and write to CSV
        for obj in json_data['study']:
            name = obj.get("name", "")
            consistency = obj.get("consistency", "")
            experiment = obj.get("experiment", [])
            filter_data = obj.get("filter", {})
            if filter_data:
                min_version = filter_data.get("minVersion", "0")
                channel = ", ".join(filter_data.get("channel", []))
                platform = ", ".join([x.replace("PLATFORM_","") for x in filter_data.get("platform", []) if x is not None])
                end_date = datetime.fromtimestamp(int(filter_data.get("endDate", "1916038763")))

            for exp in experiment:
                exp_name = exp.get("name", "")
                probability_weight = exp.get("probabilityWeight", "")
                feature_association = exp.get("featureAssociation", {})
                if feature_association:
                    enable_feature = ", ".join(feature_association.get("enableFeature", []))
                    disable_feature = ", ".join(feature_association.get("disableFeature", []))
                    forcing_feature_on = feature_association.get("forcingFeatureOn", "")
                    forcing_feature_off = feature_association.get("forcingFeatureOff", "")
                if probability_weight in ["0", "", 0] or int(min_version.split(".")[0]) < 100 or channel_filter not in channel:
                    continue
                else:
                    writer.writerow([name, consistency, exp_name, probability_weight, enable_feature, disable_feature, forcing_feature_on, forcing_feature_off, min_version, channel, platform, end_date])

        print(f"CSV data has been written to {csv_file.name}")