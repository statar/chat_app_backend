import json
from ibm_watson import ToneAnalyzerV3

emotion_text = {1:" :)", 2:" :(", 3:" :/"}
happy_emoji_ids = ['joy']
sad_emoji_ids = ['anger', 'fear', 'sadness']

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='Xwq-iMNrvN7mYajfgaACxkChGUR9gUdX5K8Lv1X9e83k',
    url='https://gateway-fra.watsonplatform.net/tone-analyzer/api'
)
def desideEmoji(tones):
    selected_motion = 3
    highest_score = 0
    for tone in tones:
        if (tone['score'] > highest_score):
            if (tone['tone_id'] in happy_emoji_ids):
                selected_motion = 1
            elif (tone['tone_id'] in sad_emoji_ids):
                selected_motion = 2
            else:
                selected_motion = 3
    return emotion_text[selected_motion]
    
def getEmotionDetection(text_content):

    tone_analysis = tone_analyzer.tone(
        {'text': text_content},
        content_type='application/json'
    ).get_result()
    return desideEmoji(tone_analysis['document_tone']['tones'])
    