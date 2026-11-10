
 
# STEP 1: Emission factors (kg CO2 per unit) 
ELECTRICITY_FACTOR = 0.727   
LPG_FACTOR = 42.6            
FLIGHT_FACTOR = 300          
SHOPPING_FACTOR = 0.012      
INDIA_AVERAGE = 2000         
TREE_ABSORBS = 21            
 
# Tips to reduce emissions, one for each category
TIPS = {
    "Electricity": "Use LED bulbs and 5-star appliances, switch off idle devices, try rooftop solar.",
    "Cooking gas": "Use a pressure cooker, cover pots while cooking, consider induction cooking.",
    "Commute": "Carpool, use bus/metro, or cycle for short distances.",
    "Flights": "Take a train for trips under 500 km and combine trips.",
    "Food": "Eat more plant-based meals, buy local and seasonal food, avoid wasting food.",
    "Shopping": "Buy fewer but durable items, repair or buy second-hand, recycle waste.",
}
 
 
# Helper: safe number input (prevents crashes) 
def get_number(question, minimum=0):
    """Keep asking until the user types a valid number >= minimum."""
    while True:
        try:
            value = float(input(question))
            if value < minimum:
                print("  Please enter a value of at least", minimum)
            else:
                return value
        except ValueError:
            print("  That is not a number. Try again.")
 
 
# Helper: safe menu input 
def get_choice(question, valid_choices):
    """Keep asking until the user picks one of the valid choices."""
    while True:
        choice = input(question)
        if choice in valid_choices:
            return choice
        print("  Invalid choice. Pick one of:", valid_choices)
 
 
#  STEP 2: Ask the user questions 
print("=== CARBON FOOTPRINT CALCULATOR ===")
 
kwh = get_number("Electricity used per month (kWh): ")
cylinders = get_number("LPG cylinders used per month: ")
people = get_number("People in your household: ", minimum=1)   # minimum 1 avoids divide-by-zero
 
print("\nHow do you travel daily?")
print("1. Car   2. Motorbike   3. Bus   4. Train/Metro   5. Walk/Cycle")
mode = get_choice("Choose 1-5: ", ["1", "2", "3", "4", "5"])
km_per_week = get_number("Distance travelled per week (km): ")
flights = get_number("Flights per year (round trips): ")
 
print("\nWhat is your diet?")
print("1. Vegetarian   2. Mixed   3. Non-veg most days")
diet = get_choice("Choose 1-3: ", ["1", "2", "3"])
 
print("\nHow much waste do you recycle?")
print("1. Almost nothing   2. Some   3. Most")
recycle = get_choice("Choose 1-3: ", ["1", "2", "3"])
shopping_rs = get_number("Spending on clothes/gadgets per month (Rs): ")
 
# STEP 3: Turn menu choices into numbers 
if mode == "1":
    transport_factor = 0.17
elif mode == "2":
    transport_factor = 0.07
elif mode == "3":
    transport_factor = 0.09
elif mode == "4":
    transport_factor = 0.04    
else:
    transport_factor = 0.0     
 
if diet == "1":
    diet_per_day = 1.7
elif diet == "2":
    diet_per_day = 2.5
else:
    diet_per_day = 3.3
 
if recycle == "1":
    recycle_multiplier = 1.0
elif recycle == "2":
    recycle_multiplier = 0.8
else:
    recycle_multiplier = 0.6
 
#  STEP 4: Calculate yearly emissions (kg CO2) 
electricity = kwh * ELECTRICITY_FACTOR * 12 / people
cooking_gas = cylinders * LPG_FACTOR * 12 / people
commute = km_per_week * transport_factor * 52
flying = flights * FLIGHT_FACTOR
food = diet_per_day * 365
shopping = shopping_rs * SHOPPING_FACTOR * 12 * recycle_multiplier
 
total = electricity + cooking_gas + commute + flying + food + shopping
 
categories = {
    "Electricity": electricity,
    "Cooking gas": cooking_gas,
    "Commute": commute,
    "Flights": flying,
    "Food": food,
    "Shopping": shopping,
}
 
# STEP 5: Show results
print("\n=== YOUR RESULTS (kg CO2 per year) ===")
for name in categories:
    kg = categories[name]
    percent = kg / total * 100 if total > 0 else 0   # share of total
    print(f"{name:<12} {kg:8.0f} kg  ({percent:.0f}%)")
print("-----------------------------------")
print(f"TOTAL        {total:8.0f} kg = {total / 1000:.2f} tonnes")
 
print("\nIndia average is", INDIA_AVERAGE, "kg. You are at", round(total / INDIA_AVERAGE, 1), "times that.")
print("About", round(total / TREE_ABSORBS), "trees would be needed to absorb your yearly emissions.")
 
# STEP 6: Recommendations (the 'reduce it' part of the task) 

sorted_categories = sorted(categories, key=categories.get, reverse=True)
top3 = sorted_categories[:3]
 
print("\n=== HOW TO REDUCE YOUR FOOTPRINT (top 3 sources) ===")
for name in top3:
    if categories[name] > 0:
        print("-", name + ":", TIPS[name])
 
print("\nNote: factors are approximate averages. Use results as an estimate, not an exact value.")
