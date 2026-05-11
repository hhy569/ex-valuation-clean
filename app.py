from flask import Flask, render_template, request, jsonify
import os
import base64
import requests
import time
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

BAIDU_API_KEY = os.getenv('BAIDU_API_KEY')
BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def get_baidu_access_token():
    auth_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        'grant_type': 'client_credentials',
        'client_id': BAIDU_API_KEY,
        'client_secret': BAIDU_SECRET_KEY
    }
    response = requests.get(auth_url, params=params)
    result = response.json()
    return result.get('access_token')

def get_deepseek_comfort_message(heartbreak_level, image_info="This photo is full of memories"):
    """Call DeepSeek LLM to generate philosophical comfort messages in English"""
    if not DEEPSEEK_API_KEY:
        return get_fallback_message(heartbreak_level)
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    unique_id = str(int(time.time() * 1000))[-6:]
    
    if heartbreak_level <= 2:
        mood = "Peaceful with mild sentimentality"
        depth = "gentle philosophical reflection"
        themes = random.choice([
            "cherishing small joys and gratitude",
            "finding peace in everyday moments",
            "appreciating life's gentle beauty",
            "the quiet wisdom in simple moments"
        ])
    elif heartbreak_level <= 5:
        mood = "Somewhat lost and melancholic"
        depth = "thoughtful philosophical comfort"
        themes = random.choice([
            "understanding impermanence and acceptance",
            "finding meaning in difficult times",
            "the wisdom in letting go",
            "navigating through uncertainty with grace"
        ])
    elif heartbreak_level <= 8:
        mood = "Deeply sorrowful"
        depth = "profound philosophical reflection and solace"
        themes = random.choice([
            "transformation through pain and rebirth",
            "the storm that clears the sky",
            "finding inner strength in darkness",
            "emerging stronger from the fire"
        ])
    else:
        mood = "Soul-deep pain"
        depth = "soul-touching philosophical dialogue"
        themes = random.choice([
            "the phoenix rising from ashes",
            "light existing within the darkest night",
            "the indestructible core of your being",
            "finding hope when hope seems impossible"
        ])
    
    time_phrases = random.choice([
        "Time, the great teacher",
        "In the passage of moments",
        "As the river of time flows endlessly",
        "Within the eternal now",
        "In the grand cycle of seasons",
        "Like the turning of the wheel"
    ])
    
    metaphors = random.choice([
        "leaves falling from ancient trees to nourish new growth",
        "waves meeting the shore, each one unique yet eternal",
        "seeds breaking through spring soil after long winter",
        "stars burning through the darkest night",
        "mountains standing firm through countless storms",
        "rivers carving canyons over millennia"
    ])
    
    opening_style = random.choice([
        "I sense the weight you carry",
        "I understand the ache you feel",
        "Your pain speaks to the depth of your capacity to love",
        "There is profound wisdom in your tears"
    ])
    
    prompt = f"""Please act as a wise philosopher and spiritual guide speaking to someone in genuine emotional pain.

User's situation:
- Heartbreak level: {heartbreak_level}/10 ({mood})
- Photo information: {image_info}
- Theme to explore: {themes}
- Unique session: #{unique_id}

Write a unique, heartfelt comfort message of 350-500 words. Requirements:

1. Begin with empathy: {opening_style}
2. Explore a philosophical angle related to: {themes}
3. Include natural metaphors about: {time_phrases} and {metaphors}
4. Discuss the paradox that our deepest pains often lead to our greatest growth
5. Reference wisdom from ONE of these traditions (choose randomly):
   - Buddhist: impermanence, detachment, compassion
   - Stoic: what we can control, virtue in adversity
   - Taoist: natural flow, yin and yang balance
   - Existentialist: creating meaning, authentic living
   - Native American: respect for all life, cycles of nature
6. Use beautiful, poetic language with SPECIFIC, UNIQUE imagery
7. NO emojis - keep it serious and genuine
8. End with a clear, powerful message of hope that feels earned
9. Write in first person as a caring elder who truly understands
10. This must feel COMPLETELY UNIQUE - like it was written just for this person

Make this feel like a personal letter, not a generic message."""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
    }
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'You are a wise philosopher and spiritual guide. You write deeply personal, unique comfort messages that feel like they come from someone who has personally experienced and overcome great suffering. Each message must be completely different from any other - avoid clichés and generic phrases.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.95,
        'max_tokens': 900,
        'top_p': 0.98
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return get_fallback_message(heartbreak_level)
    except Exception as e:
        print(f"DeepSeek AI call failed: {e}")
        return get_fallback_message(heartbreak_level)


def get_fallback_message(heartbreak_level):
    """Fallback messages when AI fails - now 15+ unique messages"""
    messages = [
        f"As leaves return to the earth, it is not an end, but another form of returning. Your heartbreak level is {heartbreak_level}/10, and this pain surges like a tide, but will also recede like one. Memory is like amber, freezing time, yet allowing us to see eternity within it. Pain is the soil of growth, letting us more deeply understand the true meaning of life. When you feel tired, remember to look up at the stars - those past moments have not truly disappeared; they have become stars, forever illuminating your path forward.",
        
        f"Life is like flowing water - sometimes rushing with joy, sometimes still with sorrow. Your heartbreak ({heartbreak_level}/10) is like a river meeting ancient rocks, creating beauty through the collision. But water always finds its way forward. The obstacle does not stop the river; it simply changes its path. You too will find your way. The very fact that you feel this deeply proves you are alive, that you love with your entire being.",
        
        f"In the garden of your soul, heartbreak is the rain that makes flowers possible. Your current pain at level {heartbreak_level}/10 is not a punishment but a transformation. Like the caterpillar that must dissolve completely before becoming a butterfly, you too are dissolving old versions of yourself to become who you are meant to be. This is not destruction; this is rebirth.",
        
        f"The ancient trees remember every storm they have weathered. Their strength was not built in calm weather but in the fury of wind and lightning. Your heart at {heartbreak_level}/10 is telling you something profound: you loved deeply, you connected truly, and that is never wasted. The storm will pass. You will stand taller than before.",
        
        f"Time is the great healer, but it does not heal by erasing. It heals by teaching. At your heartbreak level of {heartbreak_level}/10, time is asking you to look differently at your pain. What is this feeling trying to teach you? What boundary needs to be set? What part of yourself needs to be reclaimed? The answer is within the ache itself.",
        
        f"Mountains do not resist the river; they simply exist. The river shapes the mountain over thousands of years, not through force but through persistence. Your heartbreak ({heartbreak_level}/10) is like that river - it is carving new channels in your soul, creating depths you never knew existed. Trust the process of your own becoming.",
        
        f"There is a Japanese philosophy called 'mono no aware' - the pathos of things. It speaks to the bittersweet awareness of impermanence. Your pain at level {heartbreak_level}/10 is this awareness made acute. You grieve not because something was bad, but because it was beautiful. That beauty never disappears; it transforms.",
        
        f"The phoenix does not rise without burning. You at {heartbreak_level}/10 are in the fire right now, and it is terrifying. But the fire is not your enemy. It is burning away everything that was never really you - expectations, illusions, attachments that no longer serve your highest self. What remains will be pure gold.",
        
        f"In the darkest night, stars shine brightest. Your heartbreak of {heartbreak_level}/10 is that dark night, and you are the star. The very depth of your feeling proves the depth of your capacity to love, to connect, to be human. This is not weakness. This is extraordinary humanity. The dawn is coming.",
        
        f"Every great love story carries within it the seed of loss, because love that matters cannot be permanent. At {heartbreak_level}/10, you are feeling the full weight of having loved truly. That weight is not a burden - it is proof of your beautiful, loving heart. Carry it gently.",
        
        f"The ocean does not apologize for its waves. It simply continues, hour after hour, day after day, century after century. Your heartbreak ({heartbreak_level}/10) is a wave - massive, perhaps, but still just one wave in an infinite ocean of moments yet to come. The ocean continues. You will too.",
        
        f"Silence is not empty; it is full of answers waiting to be heard. At your current level {heartbreak_level}/10, perhaps the wisest thing is not to fill the void with distraction, but to sit with your pain, to listen to what it needs to tell you. You already know the way. You are finding it now.",
        
        f"Winter is not the opposite of spring; it is its necessary preparation. Your heartbreak of {heartbreak_level}/10 is winter, and you are in the quiet dormancy that precedes extraordinary growth. Rest now. The spring will come, and with it, flowers you cannot yet imagine.",
        
        f"The lotus blooms in muddy water, not because it ignores the mud, but because it transforms it. Your pain at {heartbreak_level}/10 is that muddy water, and you are becoming the lotus. This transformation requires the darkness as much as the light. Trust both.",
        
        f"Every ending is the hidden beginning of something else. At heartbreak level {heartbreak_level}/10, you are at a threshold - one door is closing, but that very act is revealing where the next door might be. Step forward with courage. The universe is guiding you even now."
    ]
    return random.choice(messages)

def analyze_image_with_baidu(image_path):
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    access_token = get_baidu_access_token()
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_detect?access_token={access_token}"

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'image': img_base64}

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def calculate_soul_value(analysis_result, heartbreak_level):
    base_value = heartbreak_level * 100

    try:
        if 'result' in analysis_result and analysis_result['result']:
            person_num = analysis_result['result'].get('person_num', 0)
            face_num = analysis_result['result'].get('face_num', 0)
            base_value += person_num * 200
            base_value += face_num * 150
        else:
            base_value += 50
    except:
        base_value += 50

    timestamp = int(time.time())
    random.seed(timestamp + heartbreak_level + hash(str(analysis_result)))
    random_factor = random.randint(100, 800)
    sentiment_factor = random.randint(heartbreak_level * 20, heartbreak_level * 50)
    
    final_value = base_value + random_factor + sentiment_factor
    return final_value

def parse_image_info(analysis_result):
    """Parse image analysis result to generate image description"""
    try:
        if 'result' in analysis_result and analysis_result['result']:
            person_num = analysis_result['result'].get('person_num', 0)
            face_num = analysis_result['result'].get('face_num', 0)
            if person_num > 0:
                return f"There are {person_num} people in the photo"
            else:
                return "This is a special photo"
    except:
        pass
    return "This photo is full of memories"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    heartbreak_level = request.form.get('heartbreak_level', type=int, default=5)

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = f"soul_{int(time.time())}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            analysis_result = analyze_image_with_baidu(filepath)
            soul_value = calculate_soul_value(analysis_result, heartbreak_level)
            image_info = parse_image_info(analysis_result)
            ai_comfort_message = get_deepseek_comfort_message(heartbreak_level, image_info)
        except Exception as e:
            print(f"Processing failed: {e}")
            soul_value = heartbreak_level * 100 + int(time.time() % 300)
            ai_comfort_message = get_fallback_message(heartbreak_level)

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'soul_value': soul_value,
            'message': f'🔮 Soul Value: ${soul_value}',
            'emotional_message': ai_comfort_message
        })


@app.route('/burn-message', methods=['POST'])
def burn_message():
    heartbreak_level = request.json.get('heartbreak_level', 5)
    
    try:
        ai_message = get_deepseek_comfort_message(heartbreak_level, "The memory has been burned - a new chapter begins")
    except Exception as e:
        print(f"AI call failed: {e}")
        ai_message = get_fallback_message(heartbreak_level)
    
    return jsonify({
        'message': ai_message
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000, debug=True)
