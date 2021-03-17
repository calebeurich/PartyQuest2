import numpy as np 
import random
from recipe_and_ingredient_classes import Recipe, Ingredient, KINDS

TOTAL_RECIPES_OUNCES = 0
NEW_RECIPES_TO_BE_GENERATED = 5



# def normalize_recipe(recipe):
#    denominator = 0 
#    for ingredient in recipe.ingredient_arr:
#       denominator += ingredient.quantity
#    factor = 100/denominator
#    for ingredient in recipe.ingredient_arr:
#       #renormalize values to 2 decimal points
#       ingredient.set_quantity(float("{:.2f}".format(ingredient.quantity * factor))) 

'''Function to find the Nth occurrence of a character  
    params:
        @string {str}: string that you are checking
        @ch {str}: the char you want to find the nth occurance of
        @N {int}: the number occurance you want to find
    return:
        int --> the nth occurance or -1 if not present
'''
def find_nth_occur(string, ch, N) : 
    occur = 0;  
    # loop to find the Nth occurence of the character  
    for i in range(len(string)) : 
        if (string[i] == ch) : 
            occur += 1;  
  
        if (occur == N) : 
            return i;  
      
    return -1; 

'''
This method reads the cleaned_recipes.txt file and creates the recipe and ingredient objects
from the inspiring set
params:
    NONE
return:
    @recipe_arr {arr[Recipe objs]}: this array contains all of the recipe objects from the inspiring set
    @all_ingredient_matrix {arr[arr[str]]}: this 2D matrix holds 11 arrays which each contain the ingredients 
    of one type. So the first array contains all types of sugar from the inspiring set, the next all types
    of flour, etc.
'''
def read_recipes():

    recipe_arr = []
    all_ingredient_matrix = [[],[],[],[],[],[],[],[],[],[],[]]

    open_file = open("cleaned_recipes.txt", 'r')
    lines = open_file.readlines()
    

    for i in range(len(lines)):
        # recipe starts after its url which all start with https
        if lines[i-1][0] == 'h': 
            j = i
            ingredients_arr = []
            # iterate through all ingredients
            while(lines[j] != '\n' and j < (len(lines) - 1)):
                line_split = lines[j][:-1].split()
                ingredient_amount = line_split[0]
                global TOTAL_RECIPES_OUNCES
                TOTAL_RECIPES_OUNCES += float(ingredient_amount)
                ingredient_name = " ".join(line_split[2:])
                ingredient = Ingredient(ingredient_name, float(ingredient_amount))
                if ingredient_name not in all_ingredient_matrix[KINDS.index(ingredient.kind)]:
                    all_ingredient_matrix[KINDS.index(ingredient.kind)].append(ingredient_name)
                ingredients_arr.append(ingredient)
                j+=1

            recipe_name = lines[i-1]
            name_begin_index = find_nth_occur(recipe_name, '/', 5)
            new_recipe_name = recipe_name[name_begin_index + 1 : -2]
            final_recipe_name = new_recipe_name.replace("-", " ")
            new_recipe = Recipe(final_recipe_name, ingredients_arr)
            recipe_arr.append(new_recipe)

    return [recipe_arr, all_ingredient_matrix]


'''
This method determines the ratios of the 11 different kinds of ingredients to each other from the recipes in the 
inspiring set
params:
    @all_recipes {arr[Recipe objs]}: all of the recipe objects from the inspiring set
return:
    @ingredient_kind_overall_ratio {arr[float]}: contains an array of the ratios of each type of ingredient to a whole
    recipe. The total of the ratios sum up to one.
'''
def determine_rations(all_recipes):

    recipe_kind_ratios_added = [0,0,0,0,0,0,0,0,0,0,0]

    for recipe in all_recipes:
        # this will be 11 indexes long, with the amounts of each type in the indexes respective to their position in KINDS
        ingredient_kind_amounts = [0,0,0,0,0,0,0,0,0,0,0] 
        for ingredient in recipe.ingredient_arr:
            ingredient_kind = ingredient.kind
            ingredient_quantity = ingredient.quantity
            # determines which kind of ingredient ratio to increment
            kind_index = KINDS.index(ingredient_kind)
            ingredient_kind_amounts[kind_index] += ingredient_quantity
        
        # normalizes the ratios for a singular recipe so that it sums up to 1 
        recipe_kind_ratio = np.divide(ingredient_kind_amounts, sum(ingredient_kind_amounts))
        # add all of the ratios together for all the recipes from the inspiring set
        recipe_kind_ratios_added += recipe_kind_ratio

    # divide every ratio within this array by the total number of recipes to make the total ratios also sum to 1
    ingredient_kind_overall_ratio = np.divide(recipe_kind_ratios_added, len(all_recipes))

    return ingredient_kind_overall_ratio


'''
This method generates a set of new recipes equal to the global variable NEW_RECIPES_TO_BE_GENERATED. It does this by taking
the 'ideal' ratio of kinds of ingredients from the @overall_ingredient_kind_ratio, and then slightly altering it. It alters it by
either adding a randomly generated number between its negative value and its positive value.  So the two edge cases are that the ingredient
kind can have 0oz, or 2 times the 'ideal' ratio in it.  Then the total amount of ounces in the recipe will be similary randomly generated. The average
ounces of a recipe is found in this method, and it is multiplied by 0.75-1.5 to determine the total amount of ounces for the newly generated recipe. 
It will also (currently) select one ingredient from each type to be added to the recipe in the amount of ounces of its slightly altered ratio.
params:
    @overall_ingredient_kind_ratio {arr[float]}: contains an array of the ratios of each type of ingredient to a whole
    recipe. THe total of the ratios sum up to one.
    @ingredient_kinds_array {arr[arr[str]]}: this 2D matrix holds 11 arrays which each contain the ingredients 
    of one type. So the first array contains all types of sugar from the inspiring set, the next all types
    of flour, etc.
    @num_recipes {int}: the number of recipes from our inspiring set
return:
    generated_recipes {arr[Recipe objs]}: this contains the newly generated recipes
'''      
def generate_recipes(overall_ingredient_kind_ratio, ingredient_kinds_array, num_recipes):

    generated_recipes = []

    new_ratios = []
    for i in range(NEW_RECIPES_TO_BE_GENERATED):
        cloned_ratios = overall_ingredient_kind_ratio.copy()
        for j in range(len(cloned_ratios)):
            value_to_add = np.random.uniform(-1 * cloned_ratios[j], cloned_ratios[j])
            cloned_ratios[j] = cloned_ratios[j] + value_to_add
        new_ratios.append(cloned_ratios)

    for ratio_arr in new_ratios:
        ingredient_arr = []
        for i in range(len(ingredient_kinds_array)): 
            # special case for 'other' kind of ingredients where we want multiple of them instead of just 1
            if i == (len(ingredient_kinds_array) - 1):
                other_ingredients_to_add = []
                print(len(ingredient_kinds_array[i]))
                num_other_ingredients = random.randint(1, 5)
                print('num other ingredients: ' + str(num_other_ingredients))
                for j in range(num_other_ingredients):
                    other_ingredient_name_to_add = ingredient_kinds_array[i][random.randint(0, len(ingredient_kinds_array[i]) - 1)]
                    # check to make sure ingredient not already selected
                    while(other_ingredient_name_to_add in other_ingredients_to_add):
                        other_ingredient_name_to_add = ingredient_kinds_array[i][random.randint(0, len(ingredient_kinds_array[i]) - 1)]
                    other_ingredients_to_add.append(other_ingredient_name_to_add)
                for ingredient in other_ingredients_to_add:
                    factor_to_mult_by = (TOTAL_RECIPES_OUNCES / num_recipes) * np.random.uniform(0.75, 1.5)
                    new_ingredient_quantity = float("{:.2f}".format((ratio_arr[i] / len(other_ingredients_to_add)) * factor_to_mult_by))
                    ingredient_to_add = Ingredient(ingredient, new_ingredient_quantity)
                    ingredient_arr.append(ingredient_to_add)
            else:
                new_ingredient_name = np.random.choice(ingredient_kinds_array[i])
                # average amount of ounces in a recipe from inspiring set times a random number for variability
                factor_to_mult_by = (TOTAL_RECIPES_OUNCES / num_recipes) * np.random.uniform(0.75, 1.5)
                new_ingredient_quantity = float("{:.2f}".format(ratio_arr[i] * factor_to_mult_by))
                ingredient_to_add = Ingredient(new_ingredient_name, new_ingredient_quantity)
                ingredient_arr.append(ingredient_to_add)
        recipe_name = ingredient_arr[-1].name + ' cookie #' + str(random.randint(0,100))
        new_recipe = Recipe(recipe_name, ingredient_arr)
        generated_recipes.append(new_recipe)

    return generated_recipes




if __name__ == "__main__":
    read_recipes_return = read_recipes()

    # list of all recipes from inspiring set
    all_recipes = read_recipes_return[0]

    # list of all ingredients sorted by their kind
    ingredient_kinds_array = read_recipes_return[1]

    # ratio (adding up to 1) or our kinds from the recipes in the inspiring set
    overall_ingredient_kind_ratio = determine_rations(all_recipes)

    # our new recipes!
    new_crazy_recipes = generate_recipes(overall_ingredient_kind_ratio, ingredient_kinds_array, len(all_recipes))

    print("\n")

    # this will print the recipes out for you once you run this file!
    for recipe in new_crazy_recipes:
        print(recipe)


    



