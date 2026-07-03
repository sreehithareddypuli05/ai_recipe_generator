import pandas as pd

recipes = pd.read_csv("datasets/raw/RAW_recipes.csv")

# print(recipes.head())

# print(recipes.info())

# print(recipes.columns)
recipes = recipes[
    [
        "id",
        "name",
        "minutes",
        "tags",
        "nutrition",
        "steps",
        "ingredients",
        "n_ingredients"
    ]
]

# print(recipes.isnull().sum())

recipes = recipes.dropna()
recipes = recipes.drop_duplicates()

# print(recipes.shape)

# recipes.to_csv(
#     "datasets/cleaned/cleaned_recipes.csv",
#     index=False
# )

# print(recipes.columns)
# print(recipes.shape)


# print(recipes.iloc[0])

# print(recipes["ingredients"].iloc[0])
# print(type(recipes["ingredients"].iloc[0]))
# print(recipes["steps"].iloc[0])
# # print(type(recipes["steps"].iloc[0]))

# import ast

# recipes["ingredients"] = recipes["ingredients"].apply(ast.literal_eval)

# print(type(recipes["ingredients"].iloc[0]))
# print(recipes["ingredients"].iloc[0])

# print(repr(recipes["steps"].iloc[0]))


# import ast

# recipes["steps"] = recipes["steps"].apply(ast.literal_eval)

# print(type(recipes["steps"].iloc[0]))

# recipes.to_pickle("datasets/cleaned/cleaned_recipes.pkl")

recipes = pd.read_pickle("datasets/cleaned/cleaned_recipes.pkl")

print(type(recipes["ingredients"].iloc[0]))