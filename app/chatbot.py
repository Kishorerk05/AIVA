
# app/chatbot.py

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from app.config import llm
from app.email_service import is_valid_email, is_valid_mobile, send_otp, verify_otp
import re

# Create memory
memory = ConversationBufferMemory()

# Simple conversation state tracker
conversation_state = {
    "name_collected": False,
    "life_insurance_type_collected": False,
    "plan_for_collected": False,
    "age_collected": False,
    "gender_collected": False,
    "death_benefit_collected": False,
    "premium_flexibility_collected": False,
    "cash_value_goals_collected": False,
    "risk_tolerance_collected": False,
    "health_lifestyle_collected": False,
    "budget_collected": False,
    "coverage_duration_collected": False,
    "policy_goal_collected": False,
    "plans_confirmed": False,
    "plans_shown": False,
    "email_collected": False,
    "mobile_collected": False,
    "otp_sent": False,
    "email_verified": False
}

def reset_conversation_state():
    """Reset conversation state"""
    global conversation_state
    conversation_state = {
        "name_collected": False,
        "life_insurance_type_collected": False,
        "plan_for_collected": False,
        "age_collected": False,
        "gender_collected": False,
        "death_benefit_collected": False,
        "premium_flexibility_collected": False,
        "cash_value_goals_collected": False,
        "risk_tolerance_collected": False,
        "health_lifestyle_collected": False,
        "budget_collected": False,
        "coverage_duration_collected": False,
        "policy_goal_collected": False,
        "plans_confirmed": False,
        "plans_shown": False,
        "email_collected": False,
        "mobile_collected": False,
        "otp_sent": False,
        "email_verified": False
    }

# === Updated Prompt Template for Life Insurance Focus ===
template = """
You are AIVA, an expert Life Insurance advisor chatbot specializing in all types of life insurance policies.

Your job is to collect detailed information about the user's life insurance needs and recommend the most suitable life insurance plan based on their selection.

IMPORTANT: You have conversation memory. Do NOT ask for information that has already been provided. Check the conversation history before asking questions.

Follow this EXACT structured flow for Life Insurance:

1. Ask for user's name: "What should I call you?"

2. Ask about type of life insurance: "What type of life insurance are you looking for? We have Term Life, Whole Life, Universal Life, Variable Life, and Indexed Universal Life (IUL)."

3. Ask who the plan is for: "Is this [selected type] plan for you or someone else?"

4. Ask for age: "What is the age of the person to be insured?"

5. Ask for gender: "What is their gender?"

### CONDITIONAL QUESTIONS BASED ON INSURANCE TYPE:

**For TERM LIFE INSURANCE:**
6. Ask for coverage amount: "How much coverage are you looking for? (e.g., $100,000, $500,000, $1M)"
7. Ask for term length: "How long do you want the coverage for? (10, 20, or 30 years are common)"
8. Ask about smoking/tobacco: "Do they smoke or use any tobacco products?"
9. Ask about medical conditions: "Do they have any serious or chronic medical conditions?"
10. Ask for occupation: "What is their occupation?"
11. Ask for budget: "What is your yearly budget for this insurance?"

**For UNIVERSAL LIFE INSURANCE:**
6. Ask for desired death benefit: "How much coverage do you want the policy to provide? (e.g., $250,000, $500,000, $1M)"
   ☑️ Mention: The higher the coverage, the higher the premium and cash value growth potential.
7. Ask about premium flexibility: "Do you want flexibility in how much and how often you pay your premiums?"
   ☑️ Mention: ULI allows variable premium amounts, so this matters.
8. Ask about cash value goals: "Are you interested in using this policy to build tax-deferred savings or investment?"
   ☑️ Mention: Key differentiator vs term plans.
9. Ask about investment risk tolerance: "Would you prefer a fixed interest rate, or are you open to market-linked returns?"
10. Ask about health & lifestyle: "Do you have any major health issues or lifestyle risks (e.g., smoking, alcohol, chronic illness)?"
11. Ask for budget: "How much are you willing to pay yearly for this policy?"
12. Ask about coverage duration: "Do you want this plan to cover you for your entire life or until a certain age?"
13. Ask about policy goal: "Is this for income replacement, legacy planning, estate tax shelter, or savings?"

**For WHOLE LIFE INSURANCE:**
6. Ask for coverage amount: "How much coverage are you looking for? (e.g., $100,000, $500,000, $1M)"
7. Ask about cash value goals: "Are you interested in building cash value over time?"
8. Ask about premium payment period: "Do you want to pay premiums for your entire life or for a limited period?"
9. Ask about health & lifestyle: "Do you have any major health issues or lifestyle risks?"
10. Ask for budget: "What is your yearly budget for this insurance?"
11. Ask about policy goal: "Is this for income replacement, legacy planning, or savings?"

**For VARIABLE LIFE INSURANCE:**
6. Ask for coverage amount: "How much coverage are you looking for?"
7. Ask about investment risk tolerance: "Are you comfortable with market-based returns and potential volatility?"
8. Ask about investment preferences: "What types of investments interest you (stocks, bonds, mutual funds)?"
9. Ask about health & lifestyle: "Do you have any major health issues or lifestyle risks?"
10. Ask for budget: "What is your yearly budget for this insurance?"
11. Ask about policy goal: "Is this for income replacement, legacy planning, or investment growth?"

**For INDEXED UNIVERSAL LIFE (IUL):**
6. Ask for coverage amount: "How much coverage are you looking for?"
7. Ask about index preferences: "Which market index interests you (S&P 500, NASDAQ, etc.)?"
8. Ask about participation rate: "Are you comfortable with caps on potential gains?"
9. Ask about health & lifestyle: "Do you have any major health issues or lifestyle risks?"
10. Ask for budget: "What is your yearly budget for this insurance?"
11. Ask about policy goal: "Is this for income replacement, legacy planning, or market-linked growth?"

CRITICAL CONVERSATION RULES:
- If user has already provided all required information AND confirmed to show plans, proceed directly to showing life insurance plans.
- If user says "okay" or "yes" after seeing their information summary, immediately show the life insurance plans.
- Do NOT ask for name or any other information if it has already been provided in the conversation.
- Check conversation history to avoid repeating questions.
- If the conversation shows that all information has been collected and user has confirmed, skip directly to showing plans.
- NEVER repeat "Nice to meet you" or similar greetings after the initial greeting.
- NEVER repeat the initial greeting "Hello! I'm AIVA, your insurance assistant."
- After collecting the name, move directly to the next question without any greeting repetition.
- Keep responses clean and avoid redundant pleasantries.
- Do NOT say "I'm here to help you with your insurance needs" repeatedly.
- After getting the name, ask the next question directly without any additional greetings.
- If the conversation shows that all information has been collected and user has confirmed, skip directly to showing plans.

When showing life insurance plans, you MUST output them EXACTLY in this format with line breaks and indentation:

Based on your inputs, here are your [INSURANCE TYPE] options:

1. [Plan Name]:
   Coverage Amount: $[amount based on user input]
   Term Length: [for term] / Premium Flexibility: [for others]
   Features: [key features]
   Risk Level: [Low/Medium/High]
   Annual Premium: $[calculated amount]
   Additional Benefits: [any extra benefits]

2. [Plan Name]:
   Coverage Amount: $[amount based on user input]
   Term Length: [for term] / Premium Flexibility: [for others]
   Features: [key features]
   Risk Level: [Low/Medium/High]
   Annual Premium: $[calculated amount]
   Additional Benefits: [any extra benefits]

3. [Plan Name]:
   Coverage Amount: $[amount based on user input]
   Term Length: [for term] / Premium Flexibility: [for others]
   Features: [key features]
   Risk Level: [Low/Medium/High]
   Annual Premium: $[calculated amount]
   Additional Benefits: [any extra benefits]

Always follow this format with line breaks exactly as shown.

After user selects a plan:
- Show a list of top life insurance companies offering that plan (3–4 options).
- If user says "more", show more companies.
- After user chooses a company, ask for email and mobile number for agent contact.

**EMAIL VERIFICATION PROCESS:**
After collecting email and mobile information:
1. If only email is provided, ask: "Please also provide your mobile number so our agent can contact you."
2. If both email and mobile are provided, send OTP to email and say: "I've sent a 6-digit OTP to your email address. Please enter the OTP to verify your email."
3. When user provides OTP, verify it and respond with "Email verified successfully!" if correct, or "Invalid OTP. Please try again." if incorrect.
4. Only proceed to final confirmation after email verification is complete.
- If user asks about a specific company not in the list, provide information about:
  * Whether that company supports their plan type
  * Similar plans they might offer
  * Contact information or website
  * Any special requirements or restrictions
- Once user selects a company, ask:
   "Please provide your email and mobile number so our agent can contact you."
- CRITICAL: You MUST collect BOTH email AND phone number separately.
- If user provides only email, respond with: "Thank you for the email. Please also provide your mobile number."
- If user provides only phone number, respond with: "Thank you for the phone number. Please also provide your email address."
- IMPORTANT: Validate email format (should contain @ and .com/.org/.net etc.)
- IMPORTANT: Validate mobile number (should be 10 digits minimum)
- ONLY when BOTH email AND phone number are provided, respond:
   "Thank you! Our team will contact you soon."
- NEVER say "Thank you" until both email and phone number are collected.

Important:
- Use a new line after each field (Coverage Amount, Term Length/Premium Flexibility, Features, Risk Level, Annual Premium, Additional Benefits).
- Do NOT put the plans on one single line.
- Keep the indentation exactly like shown above.
- NEVER repeat "I'll call you [name] for our conversation" - this is forbidden.

After collecting all the required fields, follow this exact sequence:

1. First, display the user's information in a simple list format:

Here is your Life Insurance profile:

Name: <value>
Life Insurance Type: <value>
Plan For: <value>
Age: <value>
Gender: <value>
[Additional fields based on insurance type]

2. Then ask for confirmation:
"Please confirm, should I show you the [INSURANCE TYPE] plans? You can also make any changes to your information if needed."

3. Only after user confirms, then show the life insurance plans.

Ensure:
- Ask for user's name first like "What should I call you?".
- Each message is clear and conversational.
- Never repeat already gathered data.
- If user tries to change an answer, update and continue smoothly.
- Keep the response very short and concise.
- Give the response in a properly organized format.
- After collecting ALL information, show the summary table FIRST.
- Only show life insurance plans AFTER user confirms the information is correct.
- Explain the plan in a neat, organized manner with bullet points and line breaks while giving the plans.
- After getting the user name, use it sparingly and don't repeat it continuously.
- When users ask about specific insurance companies:
  * Provide accurate information about plan compatibility
  * Mention if the company offers similar coverage options
  * Suggest alternatives if the company doesn't support their plan type
  * Be helpful and informative, even if the company isn't in your initial list
- CRITICAL: Never repeat "I'll call you [name] for our conversation" - this phrase is completely forbidden.
- CRITICAL: If user has confirmed to show plans, proceed immediately to showing plans without asking for any information again.
- CRITICAL: After getting the name, ask the next question directly without any greeting repetition.
- CRITICAL: Do NOT repeat "I'm here to help you with your insurance needs" after the initial greeting.
- CRITICAL: Keep responses clean and avoid redundant pleasantries.

Begin by asking:
"Hello! I'm AIVA, your Life Insurance specialist. How can I help you today?"
{history}
User: {input}
AIVA:
"""

prompt = PromptTemplate(input_variables=["history", "input"], template=template)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False
)

def format_plans(text):
    # Convert plan formatting to proper markdown
    # Ensure each plan starts on a new line with markdown headers
    text = re.sub(r"(\d\.\s[A-Za-z\s]+Universal Life:?)", r"\n### \1", text)
    
    # Convert plan details to the format you want (each field on separate line)
    # Handle different spacing patterns and convert to your desired format
    text = re.sub(r"(\s+)(Death Benefit:)\s+(.+)", r"\n\2\n\3", text)
    text = re.sub(r"(\s+)(Premium Flexibility:)\s+(.+)", r"\n\2\n\3", text)
    text = re.sub(r"(\s+)(Cash Value Growth:)\s+(.+)", r"\n\2\n\3", text)
    text = re.sub(r"(\s+)(Risk Level:)\s+(.+)", r"\n\2\n\3", text)
    text = re.sub(r"(\s+)(Annual Premium:)\s+(.+)", r"\n\2\n\3", text)
    text = re.sub(r"(\s+)(Features:)\s+(.+)", r"\n\2\n\3", text)
    
    # Also handle cases where there might be different spacing
    text = re.sub(r"Death Benefit:\s+(.+)", r"Death Benefit:\n\1", text)
    text = re.sub(r"Premium Flexibility:\s+(.+)", r"Premium Flexibility:\n\1", text)
    text = re.sub(r"Cash Value Growth:\s+(.+)", r"Cash Value Growth:\n\1", text)
    text = re.sub(r"Risk Level:\s+(.+)", r"Risk Level:\n\1", text)
    text = re.sub(r"Annual Premium:\s+(.+)", r"Annual Premium:\n\1", text)
    text = re.sub(r"Features:\s+(.+)", r"Features:\n\1", text)
    
    # Handle the specific case from your example - convert bullet points to separate lines
    text = re.sub(r"Traditional Universal Life:\s*- \*\*Death Benefit:\*\*", r"### 1. Traditional Universal Life:\nDeath Benefit:", text)
    text = re.sub(r"Indexed Universal Life \(IUL\):\s*- \*\*Death Benefit:\*\*", r"\n### 2. Indexed Universal Life (IUL):\nDeath Benefit:", text)
    text = re.sub(r"Variable Universal Life \(VUL\):\s*- \*\*Death Benefit:\*\*", r"\n### 3. Variable Universal Life (VUL):\nDeath Benefit:", text)
    
    # Remove any remaining bullet points and bold formatting
    text = re.sub(r"- \*\*(.+?):\*\*", r"\1:", text)
    text = re.sub(r"- (.+?):", r"\1:", text)
    
    # Clean up extra spaces and enforce correct structure
    return text.strip()

# === Formatter for user info ===
def format_user_info(text):
    if "Here is your Life Insurance profile:" in text:
        # Convert to simple list format without table headers
        text = re.sub(r"Here is your Life Insurance profile:", r"Here is your Life Insurance profile:", text)
        
        # Convert table format to simple list format
        text = re.sub(r"\| \*\*Name:\*\* \| (.+) \|", r"Name: \1", text)
        text = re.sub(r"\| \*\*Life Insurance Type:\*\* \| (.+) \|", r"Life Insurance Type: \1", text)
        text = re.sub(r"\| \*\*Plan For:\*\* \| (.+) \|", r"Plan For: \1", text)
        text = re.sub(r"\| \*\*Age:\*\* \| (.+) \|", r"Age: \1", text)
        text = re.sub(r"\| \*\*Gender:\*\* \| (.+) \|", r"Gender: \1", text)
        text = re.sub(r"\| \*\*Desired Death Benefit:\*\* \| (.+) \|", r"Desired Death Benefit: \1", text)
        text = re.sub(r"\| \*\*Premium Flexibility:\*\* \| (.+) \|", r"Premium Flexibility: \1", text)
        text = re.sub(r"\| \*\*Cash Value Goals:\*\* \| (.+) \|", r"Cash Value Goals: \1", text)
        text = re.sub(r"\| \*\*Risk Tolerance:\*\* \| (.+) \|", r"Risk Tolerance: \1", text)
        text = re.sub(r"\| \*\*Health & Lifestyle:\*\* \| (.+) \|", r"Health & Lifestyle: \1", text)
        text = re.sub(r"\| \*\*Annual Budget:\*\* \| (.+) \|", r"Annual Budget: \1", text)
        text = re.sub(r"\| \*\*Coverage Duration:\*\* \| (.+) \|", r"Coverage Duration: \1", text)
        text = re.sub(r"\| \*\*Policy Goal:\*\* \| (.+) \|", r"Policy Goal: \1", text)
        
        # Remove table header and separator
        text = re.sub(r"\| Field \| Value \|\n\|-------\|-------\|", r"", text)
        
        # Add line breaks between each field for better readability
        text = re.sub(r"Name: (.+)\nLife Insurance Type:", r"Name: \1\n\nLife Insurance Type:", text)
        text = re.sub(r"Life Insurance Type: (.+)\nPlan For:", r"Life Insurance Type: \1\n\nPlan For:", text)
        text = re.sub(r"Plan For: (.+)\nAge:", r"Plan For: \1\n\nAge:", text)
        text = re.sub(r"Age: (.+)\nGender:", r"Age: \1\n\nGender:", text)
        text = re.sub(r"Gender: (.+)\nDesired Death Benefit:", r"Gender: \1\n\nDesired Death Benefit:", text)
        text = re.sub(r"Desired Death Benefit: (.+)\nPremium Flexibility:", r"Desired Death Benefit: \1\n\nPremium Flexibility:", text)
        text = re.sub(r"Premium Flexibility: (.+)\nCash Value Goals:", r"Premium Flexibility: \1\n\nCash Value Goals:", text)
        text = re.sub(r"Cash Value Goals: (.+)\nRisk Tolerance:", r"Cash Value Goals: \1\n\nRisk Tolerance:", text)
        text = re.sub(r"Risk Tolerance: (.+)\nHealth & Lifestyle:", r"Risk Tolerance: \1\n\nHealth & Lifestyle:", text)
        text = re.sub(r"Health & Lifestyle: (.+)\nAnnual Budget:", r"Health & Lifestyle: \1\n\nAnnual Budget:", text)
        text = re.sub(r"Annual Budget: (.+)\nCoverage Duration:", r"Annual Budget: \1\n\nCoverage Duration:", text)
        text = re.sub(r"Coverage Duration: (.+)\nPolicy Goal:", r"Coverage Duration: \1\n\nPolicy Goal:", text)
        
    return text.strip()

def handle_email_verification(user_input):
    """Handle email verification and OTP process"""
    global conversation_state
    
    # Parse input to extract email and mobile if both are provided
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Updated mobile pattern to handle spaces and various formats
    mobile_pattern = r'(\+91\s*)?[6-9]\d{9}|\d{10}'
    
    found_emails = re.findall(email_pattern, user_input)
    # Clean mobile numbers by removing spaces and extract valid ones
    potential_mobiles = re.findall(r'[\+\d\s]+', user_input)
    found_mobiles = []
    for mob in potential_mobiles:
        clean_mob = re.sub(r'[\s\-\(\)]', '', mob)
        if re.match(r'^(\+91)?[6-9]\d{9}$', clean_mob):
            found_mobiles.append(clean_mob)
    
    # Check if user is providing OTP (6 digits)
    if (user_input.strip().isdigit() and len(user_input.strip()) == 6 and 
        conversation_state["otp_sent"] and not conversation_state["email_verified"]):
        user_email = conversation_state.get("user_email")
        if user_email:
            verified, message = verify_otp(user_email, user_input.strip())
            if verified:
                conversation_state["email_verified"] = True
                return "Email verified successfully! Our agent will contact you soon at the provided email and mobile number. Thank you for choosing our insurance services!"
            else:
                return message
        else:
            return "Please provide your email address first."
    
    # Handle email and mobile collection
    if not conversation_state["email_collected"] or not conversation_state["mobile_collected"]:
        
        # Check if both email and mobile are provided in single input
        if found_emails and found_mobiles and not conversation_state["email_collected"]:
            email = found_emails[0]
            mobile = found_mobiles[0]
            
            if is_valid_email(email) and is_valid_mobile(mobile):
                conversation_state["email_collected"] = True
                conversation_state["mobile_collected"] = True
                conversation_state["user_email"] = email
                conversation_state["user_mobile"] = mobile
                
                # Send OTP immediately
                otp_sent, message = send_otp(email)
                if otp_sent:
                    conversation_state["otp_sent"] = True
                    return "I've sent a 6-digit OTP to your email address. Please enter the OTP to verify your email."
                else:
                    return f"Sorry, there was an issue sending the OTP: {message}. Please try again."
            else:
                if not is_valid_email(email):
                    return "Please provide a valid email address."
                else:
                    return "Please provide a valid mobile number (10 digits or with +91 country code)."
        
        # Handle email only
        elif found_emails and not conversation_state["email_collected"]:
            email = found_emails[0]
            if is_valid_email(email):
                conversation_state["email_collected"] = True
                conversation_state["user_email"] = email
                
                if conversation_state["mobile_collected"]:
                    # Send OTP if mobile already collected
                    otp_sent, message = send_otp(email)
                    if otp_sent:
                        conversation_state["otp_sent"] = True
                        return "I've sent a 6-digit OTP to your email address. Please enter the OTP to verify your email."
                    else:
                        return f"Sorry, there was an issue sending the OTP: {message}. Please try again."
                else:
                    return "Thank you for providing your email. Please also provide your mobile number so our agent can contact you."
            else:
                return "Please provide a valid email address."
        
        # Handle mobile only
        elif found_mobiles and not conversation_state["mobile_collected"]:
            mobile = found_mobiles[0]
            if is_valid_mobile(mobile):
                conversation_state["mobile_collected"] = True
                conversation_state["user_mobile"] = mobile
                
                if conversation_state["email_collected"]:
                    # Send OTP if email already collected
                    user_email = conversation_state.get("user_email")
                    if user_email:
                        otp_sent, message = send_otp(user_email)
                        if otp_sent:
                            conversation_state["otp_sent"] = True
                            return "I've sent a 6-digit OTP to your email address. Please enter the OTP to verify your email."
                        else:
                            return f"Sorry, there was an issue sending the OTP: {message}. Please try again."
                else:
                    return "Thank you for providing your mobile number. Please also provide your email address."
            else:
                return "Please provide a valid mobile number (10 digits or with +91 country code)."
        
        # If no valid email or mobile found in input
        elif '@' in user_input or any(char.isdigit() for char in user_input):
            if '@' in user_input:
                return "Please provide a valid email address."
            else:
                return "Please provide a valid mobile number (10 digits or with +91 country code)."
    
    return None  # No email verification handling needed

def get_response(user_input):
    # Check if this is a new conversation (first message)
    if not memory.chat_memory.messages:
        reset_conversation_state()
    
    # Handle email verification process if we're in that stage
    # Check if we're waiting for email/mobile/OTP after company selection
    conversation_history = str(memory.chat_memory.messages)
    
    # Check if we're in email verification phase (after company selection)
    if ("Please provide your email and mobile number" in conversation_history or 
        conversation_state["email_collected"] or conversation_state["mobile_collected"] or 
        conversation_state["otp_sent"]):
        
        email_verification_response = handle_email_verification(user_input)
        if email_verification_response:
            # Add to memory manually to maintain conversation flow
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(email_verification_response)
            return email_verification_response
    
    # Normal chatbot flow
    raw = conversation.invoke(user_input)["response"]
    formatted = format_plans(raw)
    formatted = format_user_info(formatted)
    return formatted
