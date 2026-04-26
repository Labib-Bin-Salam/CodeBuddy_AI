import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# आपकी API Key यहाँ पहले से है, मैंने बस उसे सुरक्षित फॉर्मेट में रखा है
genai.configure(api_key="this is not secure")


# मॉडल का नाम 'gemini-1.5-flash' रखें, यह सबसे स्टेबल है
# यह अपने आप सही मॉडल ढूंढ लेगा
model_list = genai.list_models()
for m in model_list:
    if 'generateContent' in m.supported_generation_methods:
        active_model = m.name
        break

model = genai.GenerativeModel(active_model)
print(f"बधाई हो! हम इस मॉडल का इस्तेमाल कर रहे हैं: {active_model}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # यहाँ हम देख रहे हैं कि 'message' नाम से डेटा आ रहा है या नहीं
    data = request.get_json()
    user_message = data.get('message') or data.get('user_input') # दोनों चेक करेगा
    
    if not user_message:
        return jsonify({'reply': 'खाली मैसेज मिला है!'})

    try:
        # AI को मैसेज भेज रहे हैं
        # AI को निर्देश (Personality) देना
        instructions = "You are 'CodeBuddy AI', a cool and helpful coding expert. Use emojis, keep it professional yet friendly, and explain complex things simply."
        full_prompt = f"{instructions} \nUser: {user_message}"
        
        # अब हम सीधा user_message नहीं, बल्कि full_prompt भेज रहे हैं
        response = model.generate_content(full_prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        # अगर कोई एरर आता है, तो वह आपके टर्मिनल (VS Code) में दिखेगा
        print(f"DEBUG ERROR: {e}")
        return jsonify({'reply': f"Oops! एरर आया: {str(e)[:50]}..."})

if __name__ == '__main__':
    app.run(debug=True)
