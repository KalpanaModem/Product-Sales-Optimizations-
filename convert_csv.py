import pandas as pd

# Read full CSV
df = pd.read_csv("retail.csv")

required_cols = ["Transaction_ID", "Product", "Unit_Price", "Profit_Margin"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Group transactions
grouped = df.groupby("Transaction_ID")["Product"].apply(list).reset_index()

# Create profit map
profit_df = df.drop_duplicates(subset=["Product"]).copy()
profit_df["Profit_Value"] = profit_df["Unit_Price"] * profit_df["Profit_Margin"]

product_profit = dict(zip(profit_df["Product"], profit_df["Profit_Value"]))

# Write JS file
with open("transactions.js", "w", encoding="utf-8") as f:
    f.write("const transactions = [\n")
    for _, row in grouped.iterrows():
        items = row["Product"]
        f.write(f'  {{ id: {row["Transaction_ID"]}, items: {items} }},\n')
    f.write("];\n\n")

    f.write("const productProfit = {\n")
    for product, profit in product_profit.items():
        safe_name = str(product).replace("'", "\\'")
        f.write(f"  '{safe_name}': {round(float(profit), 2)},\n")
    f.write("};\n\n")

    f.write(f"const totalRecords = {len(df)};\n")

print("transactions.js created successfully")
print("Total records:", len(df))
print("Total transactions:", len(grouped))
print("Total unique products:", len(product_profit))
