import json

import abstra.workflows as aw
import pandas as pd
from abstra.ai import prompt

file_path = "mock_database.csv"

proposal = aw.get_data("proposal")
proposal_string = json.dumps(proposal)

# open files
df = pd.read_csv(file_path)
products_database = df.to_dict(orient="records")
products_database_string = json.dumps(products_database)

database_products_names = [product["name"] for product in products_database]

match = prompt(
    f"""You will receive a list of products in JSON format that corresponds to a budget. Each product has a 'name' and 'quantity' field and fields for 'price', 'database_match' and 'product_id' initially empty. Additionally, you will receive a product database also in JSON format that corresponds to the product stock. You must, for each product in the budget, find the most similar product in the database and then generate a new budget string, following the previous format and filling in the 'price', 'database_match', and 'product_id' fields with the information from the product found in the database. The output should always be a list of dictionaries delimited by square brackets, even id it is only one product. If you do not find a similar product, you should fill in the 'database_match' field with 'Not found.' and the 'product_id' field with 0. The product list in the budget is as follows:

    Budget: {proposal_string}

    Product list in stock: {products_database_string} """,
    format={
        "updated_proposal": {
            "type": "string",
            "description": "New budget string with fields filled",
        }
    },
    temperature=0.3,
)

updated_proposal = json.loads(match["updated_proposal"])
aw.set_data("updated_proposal", updated_proposal)
for p in updated_proposal:
    print(p)
