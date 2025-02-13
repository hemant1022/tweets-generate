from flask import Flask, Response
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
import csv
from datetime import datetime, timedelta
import io
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


# Set padding token to be the same as EOS token
tokenizer.pad_token = tokenizer.eos_token

# Update the model config
model.config.pad_token_id = model.config.eos_token_id

# Function to generate a disaster tweet with varied prompts
def generate_random_disaster_tweet():
    disaster_events = [
    "Heavy flooding has affected the area surrounding",
    "A powerful hurricane made landfall near",
    "Severe wildfire is spreading across",
    "A tornado has been reported near",
    "A tsunami warning issued for the coast of",
    "Unusually strong winds are battering",
    "A dangerous storm system is developing near",
    "Flash floods are impacting communities around",
    "Wildfire containment efforts continue near",
    "Significant aftershocks detected around",
    "A landslide has occurred in the vicinity of",
    "Severe drought conditions are affecting",
    "Volcanic activity observed near",
    "Hailstorm warnings issued for",
    "Lightning strikes reported in",
    "Severe heatwave affecting",
    "Snowstorm expected to impact areas around",
    "Fog warnings in effect for",
    "Extreme weather causing disruptions near",
    "Government issues an immediate evacuation order in",
    "Electricity supply shut down as a precautionary measure in",
    "Power lines damaged, resulting in widespread outages across",
    "Emergency shelters set up to accommodate displaced residents in",
    "Energy infrastructure compromised, causing blackouts across",
    "Humanitarian aid organizations are providing relief supplies in",
    "Medical assistance is being dispatched to affected communities around",
    "Food and water distribution centers established for impacted areas near",
    "Rescue teams deployed to assist stranded individuals around",
    "Fuel supply disrupted, affecting emergency response in",
    "Local fuel stations running low due to supply disruptions near",
    "Road closures in effect as safety measure near",
    "Authorities implement curfews in affected regions of",
    "Power restoration efforts underway in affected areas of",
    "Volunteers mobilized to provide humanitarian support in",
    "Evacuation centers are operating at capacity in",
    "Power grid operators reporting delays in restoration near",
    "Casualties reported as rescue efforts intensify near",
    "Fatalities confirmed by first responders following the disaster in",
    "Hospitals report a surge in critical injuries near",
    "Ground effect complicating rescue operations in areas of severe flooding near",
    "Military support deployed for rescue operations near",
    "Local schools and community centers converted to emergency shelters in",
    "Damaged energy pipelines are affecting regional fuel supply near",
    "Severe energy shortages expected due to damaged infrastructure in",
    "Local power plants impacted by the disaster, affecting electricity supply near",
    "Essential services distributed for vulnerable populations impacted by",
    "Emergency crews work to restore power distribution channels in",
    "Energy crisis declared as supply remains limited in affected areas of",
    "Generators supplied to critical locations as power outages persist near",
    "Authorities confirm delays in energy restoration due to widespread damage near",
    "Local authorities report that full energy restoration could take weeks in",
    "Public advised to stay updated on rolling blackouts in affected areas near",
    "Local businesses pledge support and donations for disaster victims near",
    "Charitable organizations accept donations to assist with relief efforts near",
    "Long-term plans to rebuild energy infrastructure underway in disaster-hit areas of",
    "Temporary energy solutions, such as mobile generators, deployed in",
    "Severe heatwave exacerbating energy demand as recovery efforts continue in",
    "Residents asked to reduce non-essential power use as energy supply stabilizes near",
    "Cleanup efforts hindered by lack of power in rural areas near",
    "Rolling power outages reported as power is gradually restored near",
    "Energy shortages drive up demand for alternate energy sources in",
    "Reconstruction of essential infrastructure, including power grids, starts in",
    "Localized blackouts expected during energy restoration in",
    "Disaster response efforts hampered by fuel shortages in",
    "Emergency funds allocated for rehabilitation and rebuilding efforts in",
    "Transportation networks disrupted due to fallen debris and flooding in",
    "Major highways closed following severe damage in the region of",
    "Train services suspended across affected areas for safety inspections in",
    "Evacuations affecting transportation routes as authorities respond to the disaster in",
    "Buses rerouted due to road closures and damaged infrastructure near",
    "Emergency services struggle to reach remote areas due to washed-out roads in",
    "Shipping routes impacted as ports close due to severe weather conditions in",
    "Traffic accidents increase as visibility decreases from adverse weather conditions near",
    "Local authorities working to clear debris from roadways for safe transit in",
    "Federal aid requested to assist in restoring transportation systems post-disaster in",
    "Extensive building and structural damage reported as cleanup efforts begin near",
    "Bridges and tunnels rendered impassable due to structural damage in",
    "Floodwaters have submerged roads and highways, leaving neighborhoods isolated in",
    "Local businesses heavily impacted, facing structural damage and flooding near",
    "Schools and hospitals suffered major damage, requiring extensive repairs in",
    "Critical infrastructure such as water and sewage systems severely damaged near",
    "Local parks and green spaces destroyed or rendered unusable in",
    "Homes and apartments left uninhabitable, forcing residents to seek temporary housing in",
    "Roadway infrastructure, including signage and lighting, heavily damaged in",
    "Railway tracks and terminals report severe damage, suspending operations near",
    "Entire neighborhoods facing devastation, with thousands displaced in",
    "Retail and essential service facilities affected, leaving communities without supplies near",
    "Floodwaters damaged essential crop lands, leading to anticipated food shortages near",
    "Factories and manufacturing plants in the area face severe damage, disrupting production lines in",
    "Historic buildings and landmarks partially or completely destroyed by the disaster near",
    "Public health alert issued for contaminated water sources in",
    "Medical centers at full capacity, treating disaster-related injuries in",
    "Rescue helicopters deployed to evacuate stranded residents near",
    "Coast guard teams deployed for emergency assistance near",
    "Bridge collapses have isolated several communities near",
    "Officials urge the public to avoid non-essential travel near",
    "Elderly and vulnerable populations being evacuated from disaster zones near",
    "Animal shelters are overwhelmed with displaced pets near",
    "Shelter-in-place orders issued for areas affected by hazardous spills near",
    "Firefighters working round the clock to contain wildfires near",
    "Emergency phone lines experiencing high volumes near",
    "Local government provides emergency housing vouchers for displaced families near",
    "Military personnel assist with food distribution in affected areas near",
    "Temporary medical facilities set up in high-need areas near",
    "Utility companies distributing potable water to affected communities near",
    "Local airfields serving as staging areas for disaster relief teams near",
    "Railroad bridges out of service due to structural concerns near",
    "Traffic rerouted as landslides cover major roadways near",
    "Dam breach risk prompts immediate evacuations in",
    "Local government sets up child reunification centers near",
    "Emergency financial aid available for impacted small businesses near",
    "Authorities provide emergency flood cleanup kits to residents near",
    "Volunteers coordinating animal rescue and shelter operations near",
    "Reconstruction planning begins for critical transit infrastructure near",
    "Emergency response teams distributing portable heating units to affected areas near",
    "International humanitarian aid arrives to support disaster relief efforts near",
    "Temporary shelters overflowing as more residents are evacuated near",
    "Recovery efforts challenged by adverse weather conditions in",
    "Local sports facilities transformed into makeshift hospitals near",
    "Army engineers constructing temporary bridges to connect isolated areas near",
    "Damaged communication networks hinder rescue coordination near",
    "City water supply temporarily cut off due to contamination risk near",
    "Communities organize relief drives to support affected areas near",
    "Emergency hotline set up for family reunification inquiries near",
    "Police enforce curfew in disaster-hit regions to ensure public safety near",
    "Hospitals face shortages of critical medical supplies in",
    "Paramedics deployed to disaster sites to assist injured near",
    "Social media campaigns launched to coordinate volunteer efforts in",
    "Schools announce closures due to unsafe conditions near",
    "Families forced to leave pets behind due to lack of animal shelters near",
    "Community centers providing meals and temporary housing to evacuees near",
    "Air rescue teams mobilized for flood-affected areas near",
    "Firefighters battle blazes fueled by dry conditions near",
    "Flood defenses breached, causing water to inundate nearby homes in",
    "Hurricane response efforts underway as storm moves inland near",
    "Police urge residents to avoid driving in flooded areas near",
    "Local officials call for donations of food, water, and blankets near",
    "Volunteers gather supplies to distribute to impacted neighborhoods near",
    "Hospitals report increased cases of respiratory illness after fire near",
    "Federal disaster funds released to support local recovery efforts near",
    "Environmental groups express concern over pollution from oil spill near",
    "Governor declares state of emergency in disaster-affected areas near",
    "Local businesses organize donation drives to aid recovery near",
    "Fire suppression teams attempt to control spreading flames near",
    "National Guard dispatched to assist in flood evacuation efforts near",
    "Community volunteers assist with sandbagging efforts along rivers"
    ]


    
    locations = [
        "Notsuharu"
    ]

    event_prompt = random.choice(disaster_events)
    location = random.choice(locations)

    prompt = f"{event_prompt} {location}."
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones_like(inputs)
    
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,
        max_length=100,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.8,
        pad_token_id=tokenizer.eos_token_id
    )
    
    tweet = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return tweet



# Function to generate a random username
def generate_username():
    adjectives = [
        "Swift", "Rapid", "Quick", "Fast", "Speedy", "Prompt", "Immediate", "Urgent", "Dynamic", "Resilient", 
        "Courageous", "Heroic", "Bold", "Alert", "Vigilant", "Watchful", "Steady", "Dependable", "Trusty", 
        "Valiant", "Gallant", "Reliable", "Safe", "Active", "Vital", "Forceful", "Firm", "Sturdy", "Stable", 
        "Resilient", "Enduring", "Solid", "Mighty", "Steadfast", "Loyal", "Alerted", "Aware", "Cautious", 
        "Clear", "Clever", "Prepared", "Ready", "Quick", "Brisk", "Resolute", "Tenacious", "Determined", 
        "Steady", "Purposeful", "Brave", "True", "Secure", "Protected", "Healthy", "Resistant", "Robust", 
        "Strong", "Shielded", "Assured", "Encouraging", "Faithful", "Guardian", "Protector", "Sentry", 
        "Lifeline", "Defense", "Foresight", "Safeguard", "Sanctuary", "Fortress", "Bastion", "Haven", "Shelter",
        "Lookout", "Refuge", "Sanctum", "Stronghold", "Reliance", "Assurance", "Bulwark", "Foundation", "Ally", 
        "Help", "Assist", "Service", "Aid", "Provision", "Backer", "Comfort", "Support", "Empathy", "Patience", 
        "Courage", "Strength", "Safety", "Warning", "Alertness", "Observation", "Protection", "Shelter",
        "Fortify", "Reinforce", "Guardian", "Secured", "Brace", "Defensive", "Safehold", "Clearance", 
        "Approval", "Solidify", "Fortified", "Barrier", "Vanguard", "Bulwark", "Barrier", "Defense"
    ]

    nouns = [
        "Response", "Alert", "Warning", "Update", "Info", "Report", "Call", "Signal", "Beacon", "Rescue", 
        "Guide", "Direction", "Path", "Aide", "Assistance", "Backer", "Healer", "Rebuilder", "Savior", 
        "Watch", "Guardian", "Sentinel", "Sentry", "Fort", "Stronghold", "Watchdog", "Warrior", "Outpost", 
        "Barrier", "Haven", "Lifeline", "Line", "Lineage", "Lineup", "Tribe", "Network", "Alliance", "Chain", 
        "Family", "Forum", "Link", "Band", "Crew", "Support", "Strength", "Firm", "Brave", "Safe", "Sound", 
        "Backup", "Assurance", "Safety", "Fortification", "Pledge", "Promise", "Reliance", "Help", "Shelter",
        "Safeguard", "Cover", "Companion", "Foundation", "Trust", "Hope", "Beacon", "Bolt", "Gate", "Corner", 
        "Steeple", "Lookout", "Observer", "Gatherer", "Source", "Supply", "Provider", "Protection", 
        "Protector", "Healer", "Defender", "Fighter", "Watcher", "Bodyguard", "Aid", "Guardian", "Foreman", 
        "Leader", "Security", "Patrol", "Bracer", "Knower", "Rescuer", "Shelterer", "Networker", "Signal", 
        "Inform", "Informer", "Announcer", "Reassure", "Confirm", "Loyal", "Steadfast", "Stable", "Safe", 
        "Dependable", "Sustainable", "Resource", "Benefactor", "Defender", "Savior", "Helper", "Protector", 
        "Preserver", "Guardian"
    ]

    return f"{random.choice(adjectives)}{random.choice(nouns)}"

# Function to generate a set of tweets
def generate_tweets():
    tweets = []
    now = datetime.now()
    for i in range(5):  # Generate 10 unique tweets
        print(f"Generating tweet {i+1}")
        username = generate_username()
        handle = f"@{username.lower()}"
        tweet_text = generate_random_disaster_tweet()
        timestamp = now + timedelta(minutes=i * 6)

        tweets.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "handle": handle,
            "tweet": tweet_text
        })
    return tweets

# API endpoint to provide tweets in CSV format
@app.route('/api/tweets', methods=['GET'])
def get_tweets_csv():
    tweets = generate_tweets()
    
    # Convert to CSV format
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp", "username", "handle", "tweet"])
    writer.writeheader()
    for tweet in tweets:
        writer.writerow(tweet)
    
    csv_data = output.getvalue()
    output.close()

    # Return CSV data as a response
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=tweets.csv"
        }
    )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
