"""
Management command to seed the database with 50 popular Indian recipes.

Usage:
    python manage.py seed_indian_recipes

Safe to re-run: existing recipes (matched by name) are skipped, not duplicated.

Note: youtube_link is left blank for every recipe by default (it's an
optional field per the Recipe model). Add real video links later via the
Django admin, or wire up a "submit a video for this recipe" feature on the
frontend — the field is ready to accept it.
"""
from django.core.management.base import BaseCommand
from recipes.models import Recipe


RECIPES = [
    # ---------------- BREAKFAST ----------------
    dict(
        recipe_name="Masala Dosa",
        ingredients="2 cups dosa batter (rice + urad dal, fermented)\n4 medium potatoes, boiled\n1 onion, sliced\n1 tsp mustard seeds\n1 tsp urad dal\n2 green chillies, chopped\n1/2 tsp turmeric powder\nCurry leaves\nOil as needed\nSalt to taste",
        preparation_steps="Heat oil in a pan, add mustard seeds and let them splutter.\nAdd urad dal, curry leaves, green chillies and onions; saute until soft.\nAdd turmeric and mashed boiled potatoes, mix well to make the potato masala filling.\nHeat a flat tawa, pour a ladle of dosa batter and spread thin in a circular motion.\nDrizzle oil around edges, cook until golden and crisp.\nPlace potato masala in the center, fold the dosa and serve hot with coconut chutney and sambar.",
        cooking_time=30, servings=4, difficulty="medium", category="breakfast",
    ),
    dict(
        recipe_name="Soft Idli with Coconut Chutney",
        ingredients="2 cups idli batter (fermented rice + urad dal)\n1 cup grated coconut\n2 green chillies\n1 inch ginger\nRoasted chana dal (1 tbsp)\nMustard seeds, curry leaves for tempering\nSalt to taste",
        preparation_steps="Grease idli moulds and pour fermented batter into each cavity.\nSteam in an idli steamer for 10-12 minutes until a toothpick comes out clean.\nFor chutney, grind coconut, green chillies, ginger, roasted chana dal, salt with a little water.\nTemper with mustard seeds and curry leaves in hot oil, pour over chutney.\nServe warm idlis with the coconut chutney and sambar.",
        cooking_time=20, servings=4, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Poha (Flattened Rice)",
        ingredients="2 cups thick poha (flattened rice)\n1 onion, chopped\n1 potato, diced small\n1 tsp mustard seeds\nCurry leaves\n2 green chillies, chopped\n1/2 tsp turmeric powder\nPeanuts, a handful\nLemon juice\nCoriander leaves, chopped\nSalt to taste",
        preparation_steps="Rinse poha in a colander under water until soft, then drain well.\nHeat oil, add mustard seeds, peanuts, curry leaves and green chillies.\nAdd onion and diced potato, cook until potato is tender.\nAdd turmeric and salt, then fold in the rinsed poha gently.\nCook for 2-3 minutes on low heat, finish with lemon juice and coriander.",
        cooking_time=20, servings=3, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Vegetable Upma",
        ingredients="1 cup semolina (rava/sooji)\n1 onion, chopped\n1/2 cup mixed vegetables (carrot, peas, beans)\n1 tsp mustard seeds\n1 tsp urad dal\nCurry leaves\n2.5 cups water\nGhee or oil\nSalt to taste",
        preparation_steps="Dry roast semolina in a pan until lightly golden and aromatic; set aside.\nHeat ghee, add mustard seeds, urad dal and curry leaves.\nAdd onion and vegetables, saute until softened.\nAdd water and salt, bring to a boil.\nLower heat and slowly stir in roasted semolina, stirring continuously to avoid lumps.\nCover and cook for 2-3 minutes until water is absorbed and upma is fluffy.",
        cooking_time=20, servings=3, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Aloo Paratha",
        ingredients="2 cups wheat flour\n3 medium potatoes, boiled and mashed\n1 green chilli, finely chopped\n1/2 tsp cumin seeds\n1/2 tsp garam masala\nCoriander leaves, chopped\nGhee/butter for cooking\nSalt to taste",
        preparation_steps="Knead wheat flour with water and a pinch of salt into a soft dough; rest 15 minutes.\nMix mashed potatoes with chillies, cumin, garam masala, coriander and salt for the filling.\nRoll a dough ball into a small disc, place filling in the center and seal edges.\nRoll out gently into a flat paratha, dusting with flour as needed.\nCook on a hot tawa with ghee on both sides until golden brown spots appear.\nServe hot with curd and pickle.",
        cooking_time=35, servings=4, difficulty="medium", category="breakfast",
    ),
    dict(
        recipe_name="Besan Chilla",
        ingredients="1 cup gram flour (besan)\n1 onion, finely chopped\n1 tomato, finely chopped\n1 green chilli, chopped\n1/4 tsp turmeric powder\nCoriander leaves, chopped\nWater as needed\nOil for cooking\nSalt to taste",
        preparation_steps="Whisk besan with water, turmeric and salt into a smooth, lump-free batter.\nStir in onion, tomato, chilli and coriander leaves.\nHeat a non-stick tawa, pour a ladle of batter and spread into a thin circle.\nDrizzle oil around the edges, cook until golden on both sides.\nServe hot with mint chutney or ketchup.",
        cooking_time=15, servings=2, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Medu Vada",
        ingredients="1 cup urad dal, soaked 4 hours\n1 onion, finely chopped\n1 green chilli, chopped\nCurry leaves, chopped\n1/2 tsp black pepper, crushed\nOil for deep frying\nSalt to taste",
        preparation_steps="Drain and grind urad dal with very little water into a thick, fluffy batter.\nMix in onion, chilli, curry leaves, pepper and salt; whisk well to aerate the batter.\nWet your hands, shape small balls with a hole in the center (classic vada shape).\nDeep fry in hot oil until golden brown and crisp on the outside.\nServe hot with sambar and coconut chutney.",
        cooking_time=30, servings=4, difficulty="medium", category="breakfast",
    ),
    dict(
        recipe_name="Uttapam",
        ingredients="2 cups dosa/idli batter\n1 onion, finely chopped\n1 tomato, finely chopped\n1 green chilli, chopped\nCoriander leaves, chopped\nOil as needed\nSalt to taste",
        preparation_steps="Mix chopped onion, tomato, chilli and coriander into the batter, or keep separate to sprinkle on top.\nHeat a tawa, pour a ladle of batter and spread slightly thicker than a dosa.\nSprinkle the vegetable mix on top and press gently.\nDrizzle oil around edges, cook covered on low-medium heat until base is golden.\nFlip and cook briefly on the other side, then serve hot with chutney.",
        cooking_time=20, servings=3, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Ven Pongal",
        ingredients="1/2 cup rice\n1/2 cup moong dal (split yellow lentils)\n1 inch ginger, chopped\n1 tsp cumin seeds\n1/2 tsp black pepper, crushed\nCashews, a handful\nGhee\nCurry leaves\nSalt to taste\n4 cups water",
        preparation_steps="Dry roast moong dal lightly, then pressure cook with rice and water until very soft and mushy.\nHeat ghee, fry cashews until golden, add cumin, pepper, ginger and curry leaves.\nPour the tempering over the cooked rice-dal mixture and mix well, adding salt.\nAdjust consistency with hot water if needed and simmer for 2-3 minutes.\nServe hot with coconut chutney and sambar.",
        cooking_time=25, servings=3, difficulty="easy", category="breakfast",
    ),
    dict(
        recipe_name="Sabudana Khichdi",
        ingredients="1 cup sabudana (tapioca pearls), soaked overnight\n2 medium potatoes, diced\n1/2 cup roasted peanuts, crushed\n1 tsp cumin seeds\n2 green chillies, chopped\nLemon juice\nCoriander leaves, chopped\nGhee/oil\nSalt to taste",
        preparation_steps="Drain soaked sabudana well and fluff with a fork so the pearls are separate.\nHeat ghee, add cumin seeds and green chillies, then diced potatoes; cook until tender.\nAdd crushed peanuts and the sabudana, mix gently on low heat.\nCook for 5-7 minutes, stirring occasionally, until pearls turn translucent.\nFinish with lemon juice, salt and coriander leaves; serve hot.",
        cooking_time=20, servings=3, difficulty="easy", category="breakfast",
    ),

    # ---------------- LUNCH / DINNER MAINS ----------------
    dict(
        recipe_name="Paneer Butter Masala",
        ingredients="250g paneer, cubed\n3 tomatoes\n1 onion\n10 cashews\n1 inch ginger\n3 garlic cloves\n1 tsp red chilli powder\n1/2 tsp garam masala\n2 tbsp butter\n2 tbsp cream\nKasuri methi (dried fenugreek leaves)\nSalt to taste",
        preparation_steps="Boil tomatoes, onion, cashews, ginger and garlic together until soft, then blend into a smooth paste.\nHeat butter in a pan, add the blended paste and cook until it thickens and oil separates.\nAdd chilli powder, garam masala and salt; cook for 2-3 minutes.\nAdd paneer cubes and a splash of water, simmer for 5 minutes.\nStir in cream and crushed kasuri methi, simmer 2 more minutes.\nServe hot with naan or rice.",
        cooking_time=35, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Butter Chicken (Murgh Makhani)",
        ingredients="500g chicken, boneless\n1 cup yogurt\n1 tbsp ginger-garlic paste\n1 tsp red chilli powder\n4 tomatoes\n10 cashews\n2 tbsp butter\n1 tsp garam masala\n2 tbsp cream\nKasuri methi\nSalt to taste",
        preparation_steps="Marinate chicken in yogurt, ginger-garlic paste, chilli powder and salt for at least 1 hour.\nGrill or pan-sear the marinated chicken until cooked through and slightly charred; set aside.\nBoil tomatoes and cashews until soft, blend into a smooth paste.\nHeat butter, cook the tomato-cashew paste until it thickens, add garam masala and salt.\nAdd the cooked chicken and simmer for 8-10 minutes.\nFinish with cream and crushed kasuri methi; serve hot with naan or rice.",
        cooking_time=50, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Chicken Biryani",
        ingredients="500g chicken, curry cut\n2 cups basmati rice, soaked\n2 onions, sliced\n1 cup yogurt\n2 tomatoes\n1 tbsp ginger-garlic paste\n2 tsp biryani masala\nMint and coriander leaves\nWhole spices (bay leaf, cardamom, cinnamon, cloves)\nSaffron soaked in warm milk\nGhee/oil\nSalt to taste",
        preparation_steps="Marinate chicken with yogurt, ginger-garlic paste, biryani masala and salt for 1 hour.\nDeep fry sliced onions until golden brown and crisp (birista); set aside.\nIn the same oil, cook marinated chicken with tomatoes until chicken is nearly done; layer mint and coriander on top.\nParboil soaked rice with whole spices and salt until 70% cooked, then drain.\nLayer the parboiled rice over the chicken, top with fried onions, saffron milk and a drizzle of ghee.\nCover tightly and cook on low heat (dum) for 20-25 minutes, then gently mix and serve hot.",
        cooking_time=75, servings=5, difficulty="hard", category="dinner",
    ),
    dict(
        recipe_name="Vegetable Biryani",
        ingredients="2 cups basmati rice, soaked\n2 cups mixed vegetables (carrot, beans, peas, potato)\n1 onion, sliced\n1 cup yogurt\n2 tsp biryani masala\nMint and coriander leaves\nWhole spices (bay leaf, cardamom, cinnamon)\nGhee/oil\nSalt to taste",
        preparation_steps="Fry sliced onions until golden and crisp; set aside half for garnish.\nIn the same pan, saute mixed vegetables with biryani masala, yogurt and salt until half-cooked.\nParboil soaked rice with whole spices until 70% done, then drain.\nLayer rice over the vegetable masala, top with fried onions, mint and coriander.\nCover and cook on low heat (dum) for 20 minutes.\nGently fluff and mix before serving hot with raita.",
        cooking_time=55, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Rajma Chawal (Kidney Bean Curry with Rice)",
        ingredients="1 cup rajma (kidney beans), soaked overnight\n2 onions, chopped\n2 tomatoes, pureed\n1 tbsp ginger-garlic paste\n1 tsp cumin seeds\n1 tsp red chilli powder\n1 tsp garam masala\nCoriander leaves\nSteamed rice for serving\nSalt to taste",
        preparation_steps="Pressure cook soaked rajma with salt and water until soft, about 5-6 whistles.\nHeat oil, add cumin seeds, then onions; saute until golden brown.\nAdd ginger-garlic paste and cook until raw smell disappears.\nAdd tomato puree, chilli powder and garam masala; cook until oil separates.\nAdd cooked rajma along with its water, simmer for 15-20 minutes until thickened.\nGarnish with coriander and serve hot over steamed rice.",
        cooking_time=50, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Chole (Chana Masala)",
        ingredients="2 cups chickpeas, soaked overnight\n2 onions, chopped\n2 tomatoes, pureed\n1 tbsp ginger-garlic paste\n2 tsp chole masala\n1 tsp red chilli powder\nCoriander leaves\nSalt to taste",
        preparation_steps="Pressure cook soaked chickpeas with salt until soft, about 6-7 whistles.\nHeat oil, saute onions until golden brown.\nAdd ginger-garlic paste, cook until fragrant, then add tomato puree.\nAdd chole masala and chilli powder, cook until oil separates.\nAdd cooked chickpeas with some cooking liquid, simmer for 15 minutes until thick.\nGarnish with coriander, serve with bhature or rice.",
        cooking_time=50, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Dal Tadka",
        ingredients="1 cup toor dal (split pigeon peas)\n1 onion, chopped\n1 tomato, chopped\n1 tsp cumin seeds\n2 dried red chillies\n3 garlic cloves, sliced\n1/2 tsp turmeric powder\nGhee\nCoriander leaves\nSalt to taste",
        preparation_steps="Pressure cook toor dal with turmeric and salt until soft and mushy.\nWhisk the cooked dal smooth and adjust consistency with water.\nHeat ghee in a small pan, add cumin seeds, garlic and dried red chillies; let them sizzle.\nAdd onion and tomato, saute until soft.\nPour this tempering over the dal and simmer for 5 minutes.\nGarnish with coriander and serve hot with rice or roti.",
        cooking_time=30, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Dal Makhani",
        ingredients="1 cup whole black urad dal, soaked overnight\n1/4 cup rajma, soaked overnight\n2 tomatoes, pureed\n1 tbsp ginger-garlic paste\n2 tbsp butter\n2 tbsp cream\n1 tsp garam masala\nSalt to taste",
        preparation_steps="Pressure cook soaked urad dal and rajma together with salt until very soft, about 8-10 whistles.\nHeat butter, add ginger-garlic paste and cook briefly, then add tomato puree.\nCook until the puree thickens, add garam masala.\nAdd the cooked dal mixture, mash slightly, and simmer on low heat for 25-30 minutes, stirring occasionally.\nStir in cream towards the end and simmer 5 more minutes.\nServe hot with naan or rice.",
        cooking_time=60, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Palak Paneer",
        ingredients="250g paneer, cubed\n4 cups spinach leaves\n1 onion, chopped\n2 tomatoes, chopped\n1 tbsp ginger-garlic paste\n1 green chilli\n1/2 tsp garam masala\nCream (optional)\nSalt to taste",
        preparation_steps="Blanch spinach leaves in boiling water for 2 minutes, then plunge into cold water and blend into a smooth puree.\nHeat oil, saute onions until golden, add ginger-garlic paste and green chilli.\nAdd tomatoes and cook until soft and mushy.\nAdd the spinach puree, garam masala and salt; simmer for 5-7 minutes.\nAdd paneer cubes and simmer for another 5 minutes.\nFinish with a swirl of cream if desired and serve hot with roti.",
        cooking_time=30, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Baingan Bharta",
        ingredients="2 large eggplants (baingan)\n1 onion, finely chopped\n2 tomatoes, finely chopped\n1 tbsp ginger-garlic paste\n2 green chillies, chopped\n1/2 tsp turmeric powder\nCoriander leaves\nSalt to taste",
        preparation_steps="Roast the whole eggplants directly over a flame or in an oven until the skin is charred and flesh is soft.\nLet cool, then peel off the charred skin and mash the flesh.\nHeat oil, saute onions until golden, add ginger-garlic paste and green chillies.\nAdd tomatoes and turmeric, cook until tomatoes break down.\nAdd the mashed eggplant and salt, cook for 8-10 minutes until well combined.\nGarnish with coriander and serve with roti.",
        cooking_time=40, servings=3, difficulty="medium", category="lunch",
    ),
    dict(
        recipe_name="Aloo Gobi",
        ingredients="2 potatoes, cubed\n1 small cauliflower, cut into florets\n1 onion, chopped\n1 tomato, chopped\n1 tsp cumin seeds\n1/2 tsp turmeric powder\n1 tsp coriander powder\nCoriander leaves\nSalt to taste",
        preparation_steps="Heat oil, add cumin seeds, then onions; saute until translucent.\nAdd potatoes and cauliflower, stir-fry for a few minutes.\nAdd turmeric, coriander powder and salt; mix well.\nCover and cook on low-medium heat, stirring occasionally, until vegetables are tender, about 15-20 minutes.\nAdd chopped tomato towards the end and cook until soft.\nGarnish with coriander leaves and serve hot with roti.",
        cooking_time=30, servings=3, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Bhindi Masala",
        ingredients="300g okra (bhindi), sliced\n1 onion, sliced\n1 tomato, chopped\n1/2 tsp turmeric powder\n1 tsp coriander powder\n1/2 tsp amchur (dry mango powder)\nSalt to taste",
        preparation_steps="Heat oil in a wide pan, add sliced okra and stir-fry on medium-high heat until no longer slimy, about 8-10 minutes; set aside.\nIn the same pan, saute onions until golden.\nAdd tomato, turmeric and coriander powder, cook until soft.\nReturn the cooked okra to the pan, add amchur and salt, mix gently.\nCook for another 3-4 minutes and serve hot with roti.",
        cooking_time=25, servings=3, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Kadai Paneer",
        ingredients="250g paneer, cubed\n1 onion, cubed\n1 capsicum, cubed\n2 tomatoes, pureed\n1 tbsp kadai masala (coriander seeds, red chillies, roasted and ground)\n1 tbsp ginger-garlic paste\nCoriander leaves\nSalt to taste",
        preparation_steps="Heat oil, add ginger-garlic paste and saute briefly.\nAdd tomato puree and kadai masala, cook until oil separates.\nAdd onion and capsicum cubes, stir-fry for 3-4 minutes keeping them slightly crunchy.\nAdd paneer cubes and salt, toss gently to coat in the masala.\nCook for 3-4 minutes more, garnish with coriander and serve hot.",
        cooking_time=30, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Shahi Paneer",
        ingredients="250g paneer, cubed\n2 onions\n2 tomatoes\n10 cashews\n1 tbsp ginger-garlic paste\n1/2 tsp garam masala\n2 tbsp cream\nSalt to taste",
        preparation_steps="Boil onions, tomatoes and cashews until soft, then blend into a smooth paste.\nHeat oil/butter, add ginger-garlic paste, then the blended paste; cook until it thickens.\nAdd garam masala and salt, cook for a few minutes.\nAdd paneer cubes and a little water, simmer for 5-7 minutes.\nStir in cream and simmer 2 more minutes; serve hot with naan.",
        cooking_time=35, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Malai Kofta",
        ingredients="2 potatoes, boiled and mashed\n100g paneer, grated\n2 tbsp cornflour\n2 onions\n2 tomatoes\n10 cashews\nCream\n1/2 tsp garam masala\nOil for frying\nSalt to taste",
        preparation_steps="Mix mashed potato, grated paneer, cornflour and salt; shape into small balls (koftas).\nDeep fry the koftas until golden brown and crisp; drain on paper towels.\nBoil onions, tomatoes and cashews until soft, blend into a smooth paste.\nCook the paste in oil until it thickens, add garam masala and salt.\nStir in cream and simmer for a few minutes.\nJust before serving, add the koftas to the gravy so they stay crisp.",
        cooking_time=45, servings=4, difficulty="hard", category="dinner",
    ),
    dict(
        recipe_name="Chicken Tikka Masala",
        ingredients="500g chicken, boneless, cubed\n1 cup yogurt\n1 tbsp ginger-garlic paste\n2 tsp tikka masala spice mix\n2 tomatoes, pureed\n1 onion, chopped\nCream\nCoriander leaves\nSalt to taste",
        preparation_steps="Marinate chicken cubes in yogurt, ginger-garlic paste, half the spice mix and salt for at least 1 hour.\nSkewer and grill or pan-sear the chicken until charred and cooked through; set aside.\nHeat oil, saute onions until golden, add remaining spice mix and tomato puree, cook until thickened.\nAdd the grilled chicken pieces and simmer in the gravy for 8-10 minutes.\nStir in cream, garnish with coriander, and serve hot with naan or rice.",
        cooking_time=50, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Egg Curry",
        ingredients="6 eggs, boiled\n2 onions, chopped\n2 tomatoes, pureed\n1 tbsp ginger-garlic paste\n1 tsp red chilli powder\n1/2 tsp turmeric powder\n1 tsp garam masala\nCoriander leaves\nSalt to taste",
        preparation_steps="Peel boiled eggs and lightly score or pierce the surface so they soak up flavor.\nHeat oil, saute onions until golden brown.\nAdd ginger-garlic paste, then tomato puree, chilli powder and turmeric; cook until oil separates.\nAdd water to reach desired gravy consistency, simmer for 10 minutes.\nAdd boiled eggs and garam masala, simmer for 5 more minutes.\nGarnish with coriander and serve with rice or roti.",
        cooking_time=30, servings=4, difficulty="easy", category="dinner",
    ),
    dict(
        recipe_name="Goan Fish Curry",
        ingredients="500g fish fillets (kingfish or pomfret)\n1 cup grated coconut\n4 dried red chillies\n1 tsp coriander seeds\n1/2 tsp turmeric powder\n1 small ball tamarind\n1 onion, chopped\nCurry leaves\nSalt to taste",
        preparation_steps="Grind coconut, dried red chillies, coriander seeds and turmeric with a little water into a smooth paste.\nHeat oil, saute onion and curry leaves until softened.\nAdd the ground coconut paste and cook for a few minutes.\nAdd tamarind pulp and water to reach a curry consistency, bring to a simmer.\nGently slide in fish pieces and salt, simmer for 8-10 minutes without stirring too much.\nServe hot with steamed rice.",
        cooking_time=35, servings=4, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Mutton Rogan Josh",
        ingredients="500g mutton, curry cut\n1 cup yogurt\n2 onions, sliced\n1 tbsp ginger-garlic paste\n2 tsp Kashmiri red chilli powder\n1 tsp fennel powder\nWhole spices (bay leaf, cardamom, cinnamon, cloves)\nSalt to taste",
        preparation_steps="Heat oil, fry sliced onions until deep golden brown; set aside half for garnish, blend the rest into a paste.\nIn the same oil, add whole spices and ginger-garlic paste, saute briefly.\nAdd mutton pieces and sear on high heat until browned.\nAdd yogurt, chilli powder, fennel powder and the onion paste; mix well.\nAdd water, cover and simmer on low heat for 45-60 minutes until mutton is tender.\nGarnish with reserved fried onions and serve hot with rice.",
        cooking_time=90, servings=4, difficulty="hard", category="dinner",
    ),
    dict(
        recipe_name="Sambar",
        ingredients="1 cup toor dal\n1 cup mixed vegetables (drumstick, brinjal, pumpkin)\n2 tbsp sambar powder\n1 small ball tamarind\n1 tsp mustard seeds\nCurry leaves\n2 dried red chillies\nSalt to taste",
        preparation_steps="Pressure cook toor dal with turmeric until soft and mash well.\nCook mixed vegetables in water until tender.\nAdd tamarind pulp, sambar powder and salt to the vegetables, simmer for 10 minutes.\nAdd the mashed dal and mix well, simmering for another 10 minutes; adjust consistency with water.\nHeat oil, add mustard seeds, dried red chillies and curry leaves; pour this tempering over the sambar.\nServe hot with idli, dosa or rice.",
        cooking_time=40, servings=4, difficulty="medium", category="lunch",
    ),
    dict(
        recipe_name="Rasam",
        ingredients="1/4 cup toor dal\n2 tomatoes, chopped\n1 small ball tamarind\n2 tsp rasam powder\n1 tsp mustard seeds\nCurry leaves\nA pinch of asafoetida\nCoriander leaves\nSalt to taste",
        preparation_steps="Pressure cook toor dal until soft; mash and set aside.\nBoil tomatoes, tamarind pulp, rasam powder and salt in water for 10 minutes.\nAdd the mashed dal and simmer for 5-7 minutes, adjusting consistency with water.\nHeat oil, add mustard seeds, curry leaves and asafoetida; pour over the rasam.\nGarnish with coriander leaves and serve hot with rice.",
        cooking_time=25, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Methi Malai Matar (Fenugreek Peas in Creamy Gravy)",
        ingredients="2 cups fresh fenugreek leaves (methi), chopped\n1 cup green peas\n1 onion, chopped\n10 cashews, soaked\n1/2 tsp garam masala\nCream\nSalt to taste",
        preparation_steps="Blanch fenugreek leaves briefly to reduce bitterness, then drain.\nBlend soaked cashews into a smooth paste with a little water.\nHeat oil, saute onions until golden, add the cashew paste and cook for 2-3 minutes.\nAdd peas and fenugreek leaves, cook for 5-7 minutes until peas are tender.\nAdd garam masala and salt, stir in cream and simmer for 2 minutes.\nServe hot with roti or rice.",
        cooking_time=25, servings=3, difficulty="medium", category="dinner",
    ),
    dict(
        recipe_name="Aloo Matar (Potato Peas Curry)",
        ingredients="3 potatoes, cubed\n1 cup green peas\n1 onion, chopped\n2 tomatoes, pureed\n1 tsp cumin seeds\n1/2 tsp turmeric powder\n1 tsp coriander powder\nCoriander leaves\nSalt to taste",
        preparation_steps="Heat oil, add cumin seeds, then onions; saute until golden.\nAdd tomato puree, turmeric and coriander powder; cook until oil separates.\nAdd potatoes and peas, mix well to coat in the masala.\nAdd water, cover and simmer until potatoes and peas are tender, about 15-20 minutes.\nGarnish with coriander and serve hot with roti or rice.",
        cooking_time=30, servings=3, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Kadhi Pakora",
        ingredients="1 cup gram flour (besan)\n1.5 cups yogurt\n1 onion, sliced (for pakoras)\n1 tsp mustard seeds\n1 tsp cumin seeds\nCurry leaves\n1/2 tsp turmeric powder\nOil for frying\nSalt to taste",
        preparation_steps="Mix half the besan with sliced onion and water into a thick batter; deep fry small pakoras until golden, set aside.\nWhisk remaining besan with yogurt, turmeric, salt and water until smooth.\nHeat oil, add mustard seeds, cumin seeds and curry leaves; pour in the yogurt-besan mixture.\nBring to a gentle boil, stirring continuously to prevent curdling, then simmer for 15-20 minutes until thickened.\nAdd the fried pakoras just before serving and simmer 2-3 minutes.\nServe hot with steamed rice.",
        cooking_time=40, servings=4, difficulty="medium", category="lunch",
    ),
    dict(
        recipe_name="Lemon Rice",
        ingredients="2 cups cooked rice, cooled\n2 tbsp lemon juice\n1 tsp mustard seeds\n1 tsp urad dal\n1 tsp chana dal\n2 dried red chillies\nCurry leaves\nPeanuts, a handful\n1/2 tsp turmeric powder\nSalt to taste",
        preparation_steps="Heat oil, add mustard seeds, urad dal, chana dal and peanuts; fry until golden.\nAdd dried red chillies and curry leaves, fry briefly.\nAdd turmeric powder and the cooked rice, mix gently to coat evenly.\nTurn off heat, add lemon juice and salt, mix well.\nServe warm or at room temperature.",
        cooking_time=15, servings=3, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Jeera Rice",
        ingredients="2 cups basmati rice, soaked\n2 tsp cumin seeds\n1 bay leaf\n1 inch cinnamon stick\nGhee\nSalt to taste\n4 cups water",
        preparation_steps="Heat ghee in a pot, add cumin seeds, bay leaf and cinnamon; let them sizzle.\nAdd soaked and drained rice, gently saute for 2 minutes.\nAdd water and salt, bring to a boil.\nCover and simmer on low heat until rice is cooked and water is absorbed, about 15 minutes.\nFluff with a fork and serve hot alongside dal or curry.",
        cooking_time=25, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Vegetable Pulao",
        ingredients="2 cups basmati rice, soaked\n1 cup mixed vegetables (carrot, beans, peas)\n1 onion, sliced\nWhole spices (bay leaf, cardamom, cinnamon, cloves)\n1 tsp ginger-garlic paste\nGhee\nSalt to taste\n4 cups water",
        preparation_steps="Heat ghee, add whole spices and sliced onion; saute until onion is golden.\nAdd ginger-garlic paste and mixed vegetables, stir-fry for 2-3 minutes.\nAdd soaked and drained rice, gently mix to coat with the masala.\nAdd water and salt, bring to a boil.\nCover and simmer on low heat for 15-18 minutes until rice is cooked.\nFluff gently and serve hot with raita.",
        cooking_time=35, servings=4, difficulty="easy", category="lunch",
    ),
    dict(
        recipe_name="Hyderabadi Vegetable Dum Biryani",
        ingredients="2 cups basmati rice, soaked\n2 cups mixed vegetables and paneer\n1 cup yogurt\n2 onions, sliced and fried\n2 tsp biryani masala\nMint and coriander leaves\nSaffron soaked in milk\nGhee\nSalt to taste",
        preparation_steps="Marinate vegetables and paneer in yogurt, biryani masala and salt for 30 minutes.\nCook the marinated mixture in a heavy-bottomed pot until vegetables are half-cooked.\nParboil soaked rice with whole spices until 70% cooked, then drain.\nLayer rice over the vegetable masala, topping with fried onions, mint, coriander and saffron milk.\nCover tightly with a lid (seal with dough if needed) and cook on low heat (dum) for 20-25 minutes.\nGently mix and serve hot with raita.",
        cooking_time=60, servings=4, difficulty="hard", category="dinner",
    ),

    # ---------------- SNACKS / STREET FOOD ----------------
    dict(
        recipe_name="Samosa",
        ingredients="2 cups all-purpose flour\n3 potatoes, boiled and mashed\n1/2 cup green peas\n1 tsp cumin seeds\n1 tsp coriander powder\n1/2 tsp garam masala\nOil for frying\nSalt to taste",
        preparation_steps="Knead flour with a little oil, water and salt into a stiff dough; rest 20 minutes.\nHeat oil, add cumin seeds, then peas and mashed potatoes; season with coriander powder, garam masala and salt to make the filling.\nRoll dough into small ovals, cut in half, and shape each half into a cone.\nFill the cone with potato filling and seal the edges firmly.\nDeep fry samosas on medium heat until golden brown and crisp.\nServe hot with mint or tamarind chutney.",
        cooking_time=50, servings=6, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Onion Pakora",
        ingredients="2 onions, thinly sliced\n1 cup gram flour (besan)\n2 tbsp rice flour\n1/2 tsp red chilli powder\n1/4 tsp turmeric powder\nCoriander leaves, chopped\nOil for frying\nSalt to taste",
        preparation_steps="Mix sliced onions with salt and let sit for 10 minutes to release moisture.\nAdd besan, rice flour, chilli powder, turmeric and coriander leaves; mix into a thick coating batter using minimal water.\nHeat oil for deep frying.\nDrop small portions of the mixture into hot oil and fry until golden brown and crisp.\nDrain on paper towels and serve hot with chutney or ketchup.",
        cooking_time=25, servings=4, difficulty="easy", category="snack",
    ),
    dict(
        recipe_name="Vada Pav",
        ingredients="4 pav (soft bread rolls)\n3 potatoes, boiled and mashed\n1 tsp mustard seeds\nCurry leaves\n1 tbsp ginger-garlic-green chilli paste\n1/2 tsp turmeric powder\n1 cup gram flour (besan) for batter\nGarlic chutney\nOil for frying\nSalt to taste",
        preparation_steps="Heat oil, add mustard seeds and curry leaves, then ginger-garlic-chilli paste; saute briefly.\nAdd turmeric and mashed potatoes, mix well and season with salt to make the vada filling.\nShape the potato mixture into small round balls.\nDip each ball in a besan batter and deep fry until golden brown and crisp.\nSlit the pav, spread garlic chutney inside, and sandwich a hot vada in each.\nServe immediately with fried green chillies.",
        cooking_time=35, servings=4, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Pav Bhaji",
        ingredients="4 pav (bread rolls)\n3 potatoes, boiled\n1 cup cauliflower, boiled\n1/2 cup green peas, boiled\n2 onions, finely chopped\n2 tomatoes, finely chopped\n2 tbsp pav bhaji masala\nButter\nLemon juice\nCoriander leaves\nSalt to taste",
        preparation_steps="Heat butter, saute half the chopped onions until soft.\nAdd tomatoes and pav bhaji masala, cook until tomatoes break down.\nAdd boiled potatoes, cauliflower and peas, mash everything together with a potato masher while cooking.\nAdd water as needed and simmer for 10-15 minutes until thick and well combined, adjusting salt.\nToast pav halves on a griddle with butter until golden.\nServe the bhaji hot, topped with butter, raw onion, coriander and a lemon wedge, alongside the toasted pav.",
        cooking_time=40, servings=4, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Pani Puri",
        ingredients="30 puris (crisp hollow semolina/wheat shells)\n2 potatoes, boiled and mashed\n1/2 cup boiled chickpeas\n1 cup mint leaves\n1/2 cup coriander leaves\n2 green chillies\n1 tsp tamarind pulp\nChaat masala\nBlack salt\nCold water",
        preparation_steps="Blend mint, coriander, green chillies, tamarind, chaat masala and black salt with cold water to make the spicy-tangy pani; strain and chill.\nMix mashed potatoes and chickpeas with a little chaat masala and salt for the filling.\nGently crack a small hole in the top of each puri.\nFill each puri with a little potato-chickpea filling.\nDip or fill with the chilled pani just before eating, and serve immediately to keep the puris crisp.",
        cooking_time=30, servings=4, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Bhel Puri",
        ingredients="3 cups puffed rice (murmura)\n1/2 cup sev (crispy gram flour noodles)\n1 potato, boiled and diced\n1 onion, finely chopped\n1 tomato, finely chopped\nGreen chutney (mint-coriander)\nTamarind chutney\nChaat masala\nCoriander leaves",
        preparation_steps="In a large bowl, combine puffed rice, diced potato, onion and tomato.\nAdd green chutney and tamarind chutney to taste, and a sprinkle of chaat masala.\nToss everything together quickly and lightly so the puffed rice stays crisp.\nTop with sev and chopped coriander leaves.\nServe immediately, as bhel puri turns soggy if left to sit.",
        cooking_time=15, servings=3, difficulty="easy", category="snack",
    ),
    dict(
        recipe_name="Dhokla",
        ingredients="1.5 cups gram flour (besan)\n1 tbsp semolina\n1 tbsp yogurt\n1 tsp ginger-green chilli paste\n1 tsp fruit salt (ENO) or baking soda\n1 tsp mustard seeds\nCurry leaves\n2 green chillies, slit\nSugar, a pinch\nSalt to taste",
        preparation_steps="Whisk besan, semolina, yogurt, ginger-chilli paste, sugar, salt and water into a smooth, thick batter.\nJust before steaming, add fruit salt/baking soda and a splash of water; mix gently as it froths up.\nPour into a greased steaming tin and steam for 15-20 minutes until a toothpick comes out clean.\nLet cool slightly, then cut into squares.\nFor tempering, heat oil, add mustard seeds, curry leaves and slit green chillies; pour over the dhokla along with a little water.\nGarnish with coriander and serve.",
        cooking_time=35, servings=4, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Misal Pav",
        ingredients="1 cup mixed sprouted lentils (moth beans)\n4 pav (bread rolls)\n1 onion, chopped\n2 tomatoes, chopped\n2 tbsp misal/goda masala\nFarsan (crispy snack mix) for topping\nCoriander leaves\nLemon juice\nSalt to taste",
        preparation_steps="Pressure cook sprouted lentils with salt until tender.\nHeat oil, saute onions until golden, add misal masala and tomatoes, cook until soft.\nAdd the cooked sprouts along with their water, simmer for 15-20 minutes until flavors meld.\nAdjust consistency with water to make a thin, spicy curry (usal).\nLadle the usal into bowls, top generously with farsan, chopped onion and coriander.\nServe hot with pav and a wedge of lemon.",
        cooking_time=40, servings=4, difficulty="medium", category="snack",
    ),
    dict(
        recipe_name="Paneer Tikka",
        ingredients="250g paneer, cubed\n1 capsicum, cubed\n1 onion, cubed\n1 cup yogurt\n1 tbsp ginger-garlic paste\n1 tsp tandoori masala\n1/2 tsp red chilli powder\nLemon juice\nSalt to taste",
        preparation_steps="Whisk yogurt with ginger-garlic paste, tandoori masala, chilli powder, lemon juice and salt to make the marinade.\nAdd paneer, capsicum and onion to the marinade, coat well and rest for 30 minutes.\nThread the marinated pieces onto skewers.\nGrill or pan-sear on high heat, turning occasionally, until edges are charred and paneer is lightly golden.\nServe hot with mint chutney and lemon wedges.",
        cooking_time=40, servings=3, difficulty="easy", category="appetizer",
    ),
    dict(
        recipe_name="Dahi Vada",
        ingredients="1 cup urad dal, soaked 4 hours\n2 cups thick yogurt, whisked\nTamarind chutney\nMint chutney\nRoasted cumin powder\nRed chilli powder\nOil for frying\nSalt to taste",
        preparation_steps="Grind soaked urad dal with minimal water into a thick, fluffy batter.\nShape into small balls and deep fry until golden brown; drain.\nSoak the fried vadas in warm water for 10-15 minutes until soft, then gently squeeze out excess water.\nArrange vadas on a plate and pour whisked yogurt generously over them.\nDrizzle with tamarind and mint chutneys, and sprinkle cumin powder, chilli powder and salt.\nChill briefly and serve cold.",
        cooking_time=40, servings=4, difficulty="medium", category="snack",
    ),

    # ---------------- DESSERTS ----------------
    dict(
        recipe_name="Gulab Jamun",
        ingredients="1 cup milk powder\n3 tbsp all-purpose flour\n1/4 tsp baking soda\n2 tbsp ghee\nMilk as needed\n2 cups sugar\n2 cups water\nA few cardamom pods\nOil/ghee for frying",
        preparation_steps="Mix milk powder, flour and baking soda; rub in ghee, then bring together with a little milk into a soft dough.\nShape the dough into small smooth balls, ensuring no cracks on the surface.\nMake a sugar syrup by boiling sugar, water and cardamom until slightly sticky; keep warm.\nHeat oil/ghee on low-medium heat and fry the balls slowly, stirring gently, until evenly golden brown all over.\nDrain and immediately drop the warm jamuns into the warm sugar syrup.\nLet them soak for at least 30 minutes before serving.",
        cooking_time=45, servings=6, difficulty="medium", category="dessert",
    ),
    dict(
        recipe_name="Gajar Halwa (Carrot Halwa)",
        ingredients="1 kg carrots, grated\n1 liter full-fat milk\n1/2 cup sugar\n3 tbsp ghee\nCashews and raisins, a handful\n1/2 tsp cardamom powder",
        preparation_steps="Heat ghee in a heavy-bottomed pan, add grated carrots and saute for 5-7 minutes.\nAdd milk and bring to a boil, then simmer, stirring often, until the milk is mostly absorbed and carrots are soft (30-40 minutes).\nAdd sugar and continue cooking, stirring frequently, until the mixture thickens and turns glossy.\nIn a separate small pan, fry cashews and raisins in a little ghee until golden.\nStir in the cardamom powder and fried nuts.\nServe warm, optionally with a scoop of vanilla ice cream.",
        cooking_time=60, servings=6, difficulty="medium", category="dessert",
    ),
]


class Command(BaseCommand):
    help = "Seeds the database with 50 popular Indian recipes (youtube_link left blank, optional)."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for recipe_data in RECIPES:
            recipe_data = dict(recipe_data)
            recipe_data.setdefault('youtube_link', '')
            recipe_data.setdefault('is_ai_generated', False)

            obj, created = Recipe.objects.get_or_create(
                recipe_name=recipe_data['recipe_name'],
                defaults=recipe_data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {obj.recipe_name}"))
            else:
                skipped_count += 1
                self.stdout.write(f"Skipped (already exists): {obj.recipe_name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created_count} recipes added, {skipped_count} already existed."
        ))
        self.stdout.write(
            f"Total recipes defined in this command: {len(RECIPES)}"
        )