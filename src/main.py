import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes - important for Vercel frontend connection
CORS(app, origins=["*"])

# Predefined responses for the chatbot
CHATBOT_RESPONSES = {
    "services": [
        "We offer three main services: Automated Workflows using Zapier, Make, n8n, and Python; Conversational AI Agents including WhatsApp bots and GPT-powered chatbots; and AGI Research & Innovation with custom agents and AI stack optimization.",
        "Our services include workflow automation, AI chatbot development, and cutting-edge AGI research. We help businesses automate repetitive tasks and create intelligent conversational experiences.",
        "At ACH'x Automation, we specialize in automated workflows, conversational AI agents, and AGI research. We've helped 500+ businesses save 95% of their time through intelligent automation."
    ],
    "pricing": [
        "Our pricing varies based on project complexity and requirements. I'd recommend booking a free consultation to discuss your specific needs and get a customized quote.",
        "We offer flexible pricing options tailored to your business needs. For detailed pricing information, please book a free strategy call with our team.",
        "Pricing depends on the scope and complexity of your automation needs. Let's schedule a free consultation to provide you with an accurate quote."
    ],
    "automation": [
        "We automate everything from email marketing campaigns to customer support workflows. Our tools include Zapier, Make, n8n, and custom Python scripts to streamline your business processes.",
        "Our automation solutions can handle repetitive tasks, data processing, customer communications, and complex business workflows. We've automated over 500 workflows for businesses like yours.",
        "We create intelligent automation that saves time and reduces errors. From simple task automation to complex AI-powered workflows, we've got you covered."
    ],
    "contact": [
        "You can reach us through our website contact form, book a free strategy call, or connect with us on social media. We're here to help with all your automation needs!",
        "Feel free to book a free consultation using the 'Book a Call' button on our website. We'd love to discuss how we can help automate your business processes.",
        "The best way to get started is to book a free strategy call. Click the 'Book a Free Strategy Call' button and let's discuss your automation needs!"
    ],
    "default": [
        "That's a great question! At ACH'x Automation, we specialize in creating intelligent automation solutions. Would you like to know more about our services, pricing, or how we can help your business?",
        "I'm here to help you learn about our AI automation services! We offer workflow automation, conversational AI agents, and AGI research. What specific area interests you most?",
        "Thanks for your interest in ACH'x Automation! We help businesses save time through intelligent automation. Feel free to ask about our services, pricing, or book a free consultation.",
        "Hello! I'm here to assist you with information about our automation services. We've helped 500+ businesses automate their workflows and save 95% of their time. How can I help you today?"
    ]
}

def get_chatbot_response(message):
    """Generate a response based on the user's message"""
    message_lower = message.lower()
    
    # Check for keywords and return appropriate responses
    if any(word in message_lower for word in ['service', 'what do you', 'offer', 'do you do']):
        return random.choice(CHATBOT_RESPONSES['services'])
    elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'how much', 'payment']):
        return random.choice(CHATBOT_RESPONSES['pricing'])
    elif any(word in message_lower for word in ['automat', 'workflow', 'zapier', 'make', 'n8n']):
        return random.choice(CHATBOT_RESPONSES['automation'])
    elif any(word in message_lower for word in ['contact', 'reach', 'call', 'phone', 'email']):
        return random.choice(CHATBOT_RESPONSES['contact'])
    else:
        return random.choice(CHATBOT_RESPONSES['default'])

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate response based on keywords
        ai_response = get_chatbot_response(user_message)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'ACH\'x Automation Chatbot API',
        'environment': os.environ.get('RENDER_SERVICE_NAME', 'development')
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'ACH\'x Automation Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'chat': '/api/chat',
            'health': '/api/health'
        }
    })

if __name__ == '__main__':
    # Use PORT environment variable for Render deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

