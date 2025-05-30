import streamlit as st
import os
from autogen import AssistantAgent, UserProxyAgent
from autogen.llm import OpenAI

# Load OpenAI API key securely
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

# Create the LLM specifying the faster model (GPT-3.5-turbo)
llm = OpenAI(model="gpt-3.5-turbo")

# Define the assistant agent (disable Docker)
assistant = AssistantAgent(
    name="analyzer_agent",
    llm=llm,
    system_message="""
You are an assistant that:
1. Extracts all mentioned people and companies from the article.
2. Selects 3–5 of the most relevant hashtags from the given list based on the article category.
Return the result as JSON with the keys: people, companies, hashtags.
""",
    code_execution_config={"use_docker": False}
)

# Define the user proxy agent (disable Docker)
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)

# Streamlit UI
st.title("📰 Article Analyzer")

article = st.text_area("Paste the article text here")
category = st.selectbox("Select the article category", ["PCI", "NI", "PI", "FIF"])

if st.button("Analyze") and article.strip():
    tag_list = hashtags.get(category, [])
    user_message = f"""
Category: {category}
Available hashtags: {', '.join(tag_list)}

Article:
\"\"\"{article}\"\"\"
"""
    with st.spinner("Analyzing article, please wait..."):
        try:
            result = user_proxy.initiate_chat(
                recipient=assistant,
                messages=[{"role": "user", "content": user_message}]
            )
            st.subheader("🔍 Extracted Information")
            st.json(result)
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
