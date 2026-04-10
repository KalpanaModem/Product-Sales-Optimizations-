import pandas as pd
import random
from collections import defaultdict
from itertools import combinations

products = [
    ("Milk","Dairy",40,0.12),("Bread","Bakery",30,0.10),("Butter","Dairy",50,0.15),
    ("Eggs","Dairy",60,0.18),("Cheese","Dairy",80,0.20),("Rice","Grocery",70,0.12),
    ("Oil","Grocery",120,0.22),("Sugar","Grocery",45,0.10),("Tea","Beverage",90,0.25),
    ("Coffee","Beverage",150,0.30),("Biscuits","Snacks",20,0.08),("Chips","Snacks",25,0.09),
    ("Chocolate","Snacks",60,0.20),("Soap","Personal Care",35,0.15),("Shampoo","Personal Care",120,0.25)
]

rows=[]
tid=1000
while len(rows)<10000:
    for p in random.sample(products, random.randint(2,6)):
        if len(rows)>=10000: break
        rows.append([tid,p[0],p[1],p[2],p[3]])
    tid+=1

df=pd.DataFrame(rows,columns=["Transaction_ID","Product","Category","Unit_Price","Profit_Margin"])
df.to_csv("retail.csv",index=False)

print("\nDATASET CREATED:",len(df),"rows")

transactions=df.groupby("Transaction_ID")["Product"].apply(list).tolist()

graph=defaultdict(lambda: defaultdict(int))
for t in transactions:
    for p1,p2 in combinations(set(t),2):
        graph[p1][p2]+=1
        graph[p2][p1]+=1

print("\nACO Recommendations for Milk:")
for item,score in sorted(graph["Milk"].items(),key=lambda x:x[1],reverse=True)[:5]:
    print("Milk ->",item,"|",score)

profit_map={r["Product"]:r["Unit_Price"]*r["Profit_Margin"] for _,r in df.drop_duplicates("Product").iterrows()}

def support(bundle):
    return sum(set(bundle).issubset(set(t)) for t in transactions)

def profit(bundle):
    return sum(profit_map[p] for p in bundle)

def fitness(b):
    return support(b)*profit(b)

products_list=df["Product"].unique().tolist()

def rand_bundle(): return random.sample(products_list,3)

pop=[rand_bundle() for _ in range(20)]

for _ in range(30):
    pop=sorted(pop,key=fitness,reverse=True)
    new=pop[:5]
    while len(new)<20:
        p1,p2=random.choice(pop[:10]),random.choice(pop[:10])
        child=list(set(p1+p2))
        child=random.sample(child if len(child)>=3 else products_list,3)
        if random.random()<0.3:
            i=random.randint(0,2)
            child[i]=random.choice(products_list)
        new.append(child)
    pop=new

best=max(pop,key=fitness)

print("\nBEST BUNDLE:",best)
print("Fitness:",fitness(best))
