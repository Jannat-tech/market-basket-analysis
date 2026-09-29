import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

with open("groceries.csv", "r", encoding="utf-8") as file:
    transactions = [line.strip().split(",") for line in file if line.strip()]

transactions = [[item.strip() for item in transaction] for transaction in transactions]

te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)

basket = pd.DataFrame(te_array, columns=te.columns_)

frequent_itemsets = apriori(
    basket,
    min_support=0.01,
    use_colnames=True
)

rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1.0
)

rules = rules.sort_values("lift", ascending=False)

rules.to_csv("association_rules.csv", index=False)

top_rules = rules.head(10).copy()

top_rules["rule"] = top_rules.apply(
    lambda row: f"{', '.join(row['antecedents'])} → {', '.join(row['consequents'])}",
    axis=1
)

plt.figure(figsize=(10, 6))
plt.barh(top_rules["rule"], top_rules["lift"])
plt.xlabel("Lift")
plt.ylabel("Association Rule")
plt.title("Top 10 Association Rules")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("association_rules.png", dpi=300)
plt.show()