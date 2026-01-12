from pulp import *
import pandas as pd

diet_df = pd.read_excel("diet.xls",
                     sheet_name="Sheet1")
diet_df.columns = diet_df.columns.str.strip()

#Get min and max nutrient requirements
min_row = pd.to_numeric(diet_df.iloc[-2][3:], errors='coerce')
max_row = pd.to_numeric(diet_df.iloc[-1][3:], errors='coerce')
print("Minimum Nutritional Requirement")
print(min_row)
print("-----------------------------------------------------")
print("Maximum Nutritional Requirement")
print(max_row)


diet_df = diet_df.dropna(subset=['Foods'])
diet_df = diet_df[~diet_df['Foods'].isin(['Minimum', 'Maximum'])]
print(diet_df.head())

#Get foods and costs
foods = diet_df['Foods'].tolist()
print(f"\nWe have {len(foods)} different foods to choose from")

costs = dict(zip(foods, diet_df['Price/ Serving']))

#Get nutrients
nutrients = [col for col in diet_df.columns if col not in ['Foods', 'Price/ Serving', 'Serving Size']]
#Get nutrition info for each food
food_nutrients = {}
for nutrient in nutrients:
    food_nutrients[nutrient] = dict(zip(foods, diet_df[nutrient]))

#Create LP optimization prblm
prob = LpProblem("Diet_Problem", LpMinimize)

#Create continuous variables for food servings
food_vars = {}
for food in foods:
    food_vars[food] = LpVariable(food.replace(" ", "_").replace("/", "_"), lowBound=0)

#Create binary variables to track if a food is selected
food_selected = {}
for food in foods:
    food_selected[food] = LpVariable(f"Selected_{food.replace(' ', '_').replace('/', '_')}", cat='Binary')

#Set objective - what are we minimizing
prob += lpSum([costs[food] * food_vars[food] for food in foods]), "Total_Cost"

#Add nutrition constraints
#1. Checking minimum and maximum constraint
for nutrient in nutrients:
    #Minimum constraint: (servings × nutrient_per_serving) for all foods >= minimum
    prob += lpSum([food_nutrients[nutrient][food] * food_vars[food] 
                   for food in foods]) >= min_row[nutrient], f"Min_{nutrient}"
    
    #Maximum constraint: (servings × nutrient_per_serving) for all foods <= maximum
    prob += lpSum([food_nutrients[nutrient][food] * food_vars[food] 
                   for food in foods]) <= max_row[nutrient], f"Max_{nutrient}"

#2. Atleast 1/10 serving must be chosen if a food is selected
#BIG M Method
M = 1000  
for food in foods:
    # If selected, servings >= 0.1
    prob += food_vars[food] >= 0.1 * food_selected[food], f"Min_serving_{food.replace(' ', '_')}"
    # If not selected, servings = 0 (enforced by upper bound)
    prob += food_vars[food] <= M * food_selected[food], f"Max_serving_{food.replace(' ', '_')}"

#3. Either Celery or Frozen Broccoli but not both 
if 'Celery, Raw' in foods and 'Frozen Broccoli' in foods:
    prob += food_selected['Celery, Raw'] + food_selected['Frozen Broccoli'] == 1, "Celery_XOR_Broccoli"

#4. Atleast 3 kinds of meat/poultry/fish/eggs
meat_foods = ['Roasted Chicken','Poached Eggs','Scrambled Eggs','Bologna,Turkey','Frankfurter, Beef','Ham,Sliced,Extralean','Kielbasa,Prk',
    'Hamburger W/Toppings','Hotdog, Plain','Pork','Sardines in Oil','White Tuna in Water','Chicknoodl Soup','Splt Pea&Hamsoup',
    'Vegetbeef Soup','Neweng Clamchwd','New E Clamchwd,W/Mlk','Beanbacn Soup,W/Watr']

#Filter to only include meat foods that are in our dataset
available_meat = [food for food in meat_foods if food in foods]
print(f"\nAvailable meat/poultry/fish/eggs items: {len(available_meat)}")

if available_meat:
    prob += lpSum([food_selected[food] for food in available_meat]) >= 3, "Min_Meat_Variety"

print("\nSolving the basic diet problem...")
prob.solve()

#Printing results
print("Optimized model - Minimize cost")
print(f"Status: {LpStatus[prob.status]}")
print(f"Total Cost: ${value(prob.objective):.2f} per day")

print("\nFoods to buy:")
for food in foods:
    servings = food_vars[food].varValue
    if servings and servings > 0:  
        print(f"  {food}: {servings:.2f} servings")

print("\nNutrient Totals:")
for nutrient in nutrients:
    total = sum([food_nutrients[nutrient][food] * food_vars[food].varValue 
                 for food in foods])
    print(f"  {nutrient}: {total:.2f} (Min: {min_row[nutrient]}, Max: {max_row[nutrient]})")