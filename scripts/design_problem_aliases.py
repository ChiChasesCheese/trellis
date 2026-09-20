"""How the survey agents' names fold into one problem each, and what is out of scope.
Read by design_problem_survey.py. Every line here is a judgement; BUILD.md explains them."""

ALIASES = {
    "WhatsApp": "Chat / messaging",
    "Google Maps / mapping": "Google Maps",
    "Maps / navigation (Google Maps)": "Google Maps",
    "AI chat assistant (ChatGPT)": "ChatGPT-style LLM service",
    "LLM inference service": "ChatGPT-style LLM service",
    "Chatbot framework": "ChatGPT-style LLM service",
    "RAG system": "RAG (retrieval-augmented generation)",
    "Content aggregator (Reddit)": "Reddit / forum feed",
    "Nested comments system": "Reddit / forum feed",
    "Flash sale / high-contention inventory": "Flash sale system",
    "Distributed locking service": "Distributed lock service",
    "Coordination service (ZooKeeper)": "Distributed lock service",
    "Case study: Chubby": "Distributed lock service",
    "Identity/auth service": "Authentication system",
    "Graph search (social network)": "Social graph search",
    "Social graph (data structures)": "Social graph search",
    "E-commerce platform (Amazon/Shopify)": "E-commerce platform",
    "Inventory management system": "E-commerce platform",
    "Booking marketplace (Airbnb)": "Hotel reservation",
    "Airbnb / two-sided marketplace": "Hotel reservation",
    "Flight booking system": "Hotel reservation",
    "Stock trading (Robinhood)": "Stock exchange",
    "Online multiplayer game (Chess)": "Online multiplayer game",
    "Online chess service": "Online multiplayer game",
    "Video conferencing (Zoom)": "Video conferencing",
    "Short-form video (TikTok)": "Video streaming (YouTube/Netflix)",
    "Search engine (FB Post Search)": "Search engine",
    "Fitness activity feed (Strava)": "Fitness tracking (Strava)",
    "Fitness tracking app": "Fitness tracking (Strava)",
    "Nearby friends (real-time location)": "Proximity / nearby search (Yelp)",
    "Social network (Facebook)": "News feed / timeline",
    "Remote code execution service": "Online judge (LeetCode)",
    "Online code editor / collaborative IDE": "Google Docs / collaborative editing",
    "CI/CD deployment system": "CI/CD pipeline service",
    "Event/meetup scheduler": "Google Calendar",
    "Conference room booking": "Google Calendar",
    "Garbage collection system": "Garbage collector",
    "Trending topics": "Top-K / heavy hitters",
    "Product sales ranking (Amazon)": "Top-K / heavy hitters",
    "Distributed counter": "Ad click aggregation",
    "Large file distribution": "CDN",
}

# Prefixes. Another interview, or another domain of this vault.
OUT_OF_SCOPE = (
    "Case study:",                      # real systems read as papers: concept leaves and cases hold them
    "Recommendation system", "Ad click prediction", "Visual search", "Image ", "Machine translation",
    "Language translation", "Text ", "Generative image", "Video-generation", "Content moderation",
    "Social graph recommendation", "News feed / timeline (ML", "Search engine (video",   # ML model design
    "Parking lot", "Vending machine", "ATM machine", "Garbage collector", "Distributed linked list",
    "Pagination library",               # object-oriented / low-level design: the low-level-design domain
)
