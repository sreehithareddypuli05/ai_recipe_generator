# import faiss
# import pandas as pd
# from sentence_transformers import SentenceTransformer

# # Load AI model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Load FAISS index
# index = faiss.read_index("recipe_project/datasets/cleaned/models/recipe_index.faiss")

# # Load recipes
# recipes = pd.read_pickle("recipe_project/datasets/cleaned/models/recipes.pkl")

# # User input
# query = "tomato onion cheese"

# # Convert query to embedding
# query_embedding = model.encode([query], convert_to_numpy=True)

# # Search
# distances, indices = index.search(query_embedding, k=5)

# print("Recommended Recipes:\n")

# for i in indices[0]:
#     recipe = recipes.iloc[i]

#     print("=" * 50)
#     print("Recipe:", recipe["name"])
#     print("Ingredients:", recipe["ingredients"])
#     print("Cooking Time:", recipe["minutes"], "minutes")


import pickle
with open("recipe_project/datasets/cleaned/models/recipes.pkl", "rb") as f:
    data = pickle.load(f)
print(type(data))
import pandas as pd
df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
print(df.columns.tolist())
print(df.iloc[0])