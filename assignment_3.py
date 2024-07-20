import yaml
import pickle

#test.py contains the flow_1, flow_2, and flow_3 dictionaries.
from test import flow_1, flow_2, flow_3

def fetch_urls(data):
    """Fetches all URLs from a nested dictionary."""
    urls = []
    for key, value in data.items():
        if isinstance(value, dict):
            urls.extend(fetch_urls(value))  # Recursive call for nested dictionaries
        elif isinstance(value, str) and value.startswith("http"):
            urls.append(value)
    return urls

def add_entity(data, flow_id, entity_name, prompt):
    """Adds a new entity to a specific flow within the data dictionary."""
    for flow in data.values():
        if flow.get("intent") == flow_id:
            flow["entities"].append({"entity": entity_name, "prompt": prompt})
            return  # Exit after adding to the first matching flow

def update_url(data, new_url):
    """Updates the URL in all flows within the data dictionary."""
    for flow in data.values():
        flow["api_data"]["url"] = new_url

def delete_entity(data, flow_id, entity_name):
    """Deletes an entity from a specific flow within the data dictionary."""
    for flow in data.values():
        if flow.get("intent") == flow_id:
            for i, entity in enumerate(flow["entities"]):
                if entity["entity"] == entity_name:
                    del flow["entities"][i]
                    return  # Exit after deleting from the first matching flow

# Load the data from test.py
data = {
    "flow_1": flow_1,
    "flow_2": flow_2,
    "flow_3": flow_3
}

# Fetch all URLs
urls = fetch_urls(data)
print("Fetched URLs:", urls)

# Add a new entity to flow_3
add_entity(data, "ask_price", "customer_name", "Please enter your name ?")
print("Updated data after adding entity:", data)

# Update URL in all flows
update_url(data, "https://rasatest.free.beeceptor.com/")  
print("Updated data after updating URL:", data)

# Delete the "location" entity from flow_1
delete_entity(data, "product_info", "location")
print("Updated data after deleting entity:", data)

# Save the data to YAML file
with open("data.yaml", "w") as f:
    yaml.dump(data, f)

# Save the data to pickle file
with open("data.pickle", "wb") as f:
    pickle.dump(data, f)

print("Results saved to data.yaml and data.pickle")
