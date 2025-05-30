import streamlit as st
import os
from autogen import AssistantAgent, UserProxyAgent

# Load OpenAI API key securely from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]

# Hashtag options per category
hashtags = {
    "PCI": [
        "#BusinessNews", "#naturalskincare", "#Partnership", "#naturalcosmetics", "#personalcare",
        "#dermatology", "#personalcareproducts", "#collagen", "#beautynews", "#acne",
        "#beautyindustry", "#planetaryhealth", "#beautybusiness", "#sustainability", "#beautyproducts",
        "#organicbeauty", "#beautycare", "#cleanbeauty", "#beautytrends", "#greenbeauty",
        "#beautytech", "#animaltesting", "#artificialintelligence", "#crueltyfree", "#makeup",
        "#veganbeauty", "#cosmetics", "#naturalingredients", "#cosmeticsindustry", "#cosmeticingredients",
        "#cosmeticindustry", "#productsafety", "#skin", "#regulations", "#skincare",
        "#ingredients", "#skincareproducts", "#perfume", "#skinhealth", "#fragrance",
        "#healthyskin", "#fragrances", "#sensitiveskin", "#cosmeticpackaging", "#sunscreen",
        "#aroma", "#suncare", "#aromatheraphy", "#beauty", "#antibiotics",
        "#crueltyfreebeauty", "#mensgrooming", "#botanical", "#oralcare", "#dentalhealth",
        "#dentalhygiene"
    ],
    "NI": [
        "#health", "#wellness", "#nutrition", "#organic", "#organicproducts",
        "#ingredients", "#microbiome", "#probiotics", "#prebiotics", "#holistichealth",
        "#protein", "#supplements", "#vitamins", "#infantnutrition", "#immunity",
        "#immunehealth", "#hearthealth", "#bloodpressure", "#obesity", "#diabetes",
        "#guthealth", "#pharmaceuticals", "#nutraceuticals", "#functionalfoods", "#plantbased",
        "#foodsecurity", "#foodinsecurity", "#foodsystems", "#botanicalextracts", "#healthissues",
        "#healthproducts", "#healthcare", "#junkfood", "#childnutrition", "#weightmanagement",
        "#capsules", "#metabolism", "#cardiovascularhealth", "#regulation", "#policy",
        "#innovation", "#mentalhealth", "#government", "#womenshealth", "#healthbenefits",
        "#foodindustry", "#environment", "#climatechange", "#chemicals", "#healthy",
        "#diet", "#sustainable", "#nutritional", "#wellbeing"
    ],
    "PI": [
        "#beveragepackaging", "#packagingtechnology", "#packagingsolutions", "#bioplastic", "#paperindustry",
        "#pharmapackaging", "#bioplastics", "#paperpackaging", "#smartpackaging", "#caps",
        "#plastic", "#biodegradable", "#chemicalrecycling", "#plasticbottles", "#circularpackaging",
        "#chemicals", "#plasticfree", "#ppwr", "#circulareconomy", "#plasticpackaging",
        "#biobasedmaterials", "#climatechange", "#plasticpollution", "#singleuseplastic", "#compostable",
        "#plastics", "#packagingmachinery", "#ecofriendly", "#plasticsindustry", "#plantbased",
        "#ecommerce", "#recycling", "#compostablepackaging", "#environmental", "#renewables",
        "#foodservice", "#environmentallyfriendly", "#reusablepackaging", "#biobased", "#environmentalsustainability",
        "#singleuseplastics", "#foodandbeverage", "#foodpackaging", "#sustainability", "#flexiblepackaging",
        "#foodwaste", "#sustainablepackaging", "#recyclablepackaging", "#globalwarming", "#wastemanagement",
        "#recycled", "#greenenergy", "#zeroplastic", "#greenhousegas", "#reuse",
        "#greenwashing", "#packagingindustry", "#labels", "#paper", "#packaging",
        "#bio", "#packagingdesign", "#packaginginnovation", "#packagingnews"
    ],
    "FIF": [
        "#agriculture", "#agrifood", "#alternativeproteins", "#bakery", "#beverages",
        "#bioscience", "#cleanlabel", "#climatechange", "#confectionery", "#consumertrends",
        "#dairy", "#desserts", "#farming", "#flavors", "#food",
        "#foodandbeverage", "#foodandbeverageindustry", "#foodindustry", "#foodingredients", "#foodinnovation",
        "#foodnews", "#foodsafety", "#foodscience", "#foodsecurity", "#foodtechnology",
        "#foodtrends", "#foodwaste", "#gmo", "#healthyfood", "#marketresearch",
        "#meatalternatives", "#plantbased", "#protein", "#shelflife", "#supplychain",
        "#sustainability", "#sustainablefood", "#sweets", "#taste", "#texture",
        "#vegan"
    ]
}

# Streamlit UI
st.title("📰 Article Analyzer with AutoGen")

article = st.text_area("Paste your article here:")
category = st.selectbox("Select the article category:", list(hashtags.keys()))

# Analyze button logic
if st.button("Analyze"):
    if not article.strip():
        st.warning("Please paste an article first.")
    else:
        selected_hashtags = ", ".join(hashtags[category])

        # Build the prompt
        user_message = f"""
        Analyze the following news article. Extract and list all people and companies mentioned.
        Then, from the following hashtag options for the {category} category, suggest the most suitable 3–5 hashtags.

        Hashtag options: {selected_hashtags}

        Article:
        \"\"\"{article}\"\"\"
        """

        # Set up AutoGen agents
        user_proxy = UserProxyAgent(name="user_proxy", human_input_mode="NEVER")
        assistant = AssistantAgent(name="assistant")

        # Run the analysis
        with st.spinner("Analyzing..."):
            result = user_proxy.initiate_chat(
                recipient=assistant,
                messages=[{"role": "user", "content": user_message}]
            )

        # Display results
        st.subheader("🔍 Extracted Information")
        st.json(result)
