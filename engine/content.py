"""AI phrase generation with permanent no-repeat history."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime

import requests

import config
from config import CATEGORIES, CATEGORIES_NATIVE, HISTORY_DIR, MAX_RECENT_CATEGORIES

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"

PHRASE_KEY = config.LANGUAGE["history_key"]
LANGUAGE_NAME = config.LANGUAGE["name"]
NATIVE_NAME = config.LANGUAGE["native_name"]

# ==== FALLBACK PHRASES START ====
FALLBACK_PHRASES = [
    {"english": "Hello, nice to meet you.", "native": "నమస్కారం, మీతో పరిచయం సంతోషం.", "transliteration": "Namaskaram, meeto parichayam santosham."},
    {"english": "Good morning!", "native": "శుభోదయం!", "transliteration": "Shubhodayam!"},
    {"english": "Good evening, how are you?", "native": "శుభ సాయంత్రం, ఎలా ఉన్నారు?", "transliteration": "Shubha sayantram, elaa unnaru?"},
    {"english": "See you tomorrow!", "native": "రేపు కలవాల!", "transliteration": "Repu kalavaala!"},
    {"english": "Goodbye, take care.", "native": "వీడ్కోలు, జాగ్రత్తగా ఉండండి.", "transliteration": "Veedkolu, jaagrattaga undandi."},
    {"english": "Thank you very much.", "native": "చాలా ధన్యవాదాలు.", "transliteration": "Chala dhanyavaadaalu."},
    {"english": "You're welcome.", "native": "పర్వాలేదు.", "transliteration": "Parvaaledu."},
    {"english": "I'm sorry, excuse me.", "native": "క్షమించండి.", "transliteration": "Kshaminchandi."},
    {"english": "Yes, that's correct.", "native": "అవును, అది సరే.", "transliteration": "Avunu, adi sare."},
    {"english": "No, I don't think so.", "native": "లేదు, నా అభిప్రాయం లేదు.", "transliteration": "Ledu, na abhipraayam ledu."},
    {"english": "How are you doing today?", "native": "ఈరోజు ఎలా ఉన్నారు?", "transliteration": "Eeroju elaa unnaru?"},
    {"english": "I'm fine, thank you.", "native": "నేను బాగున్నాను, ధన్యవాదాలు.", "transliteration": "Nenu baagunnanu, dhanyavaadaalu."},
    {"english": "What's your name?", "native": "మీ పేరు ఏమిటి?", "transliteration": "Mee peru emit?"},
    {"english": "My name is...", "native": "నా పేరు...", "transliteration": "Naa peru..."},
    {"english": "Nice to meet you too.", "native": "మీతో పరిచయం ఆనందం.", "transliteration": "Meeto parichayam aanandam."},
    {"english": "Where is the bathroom?", "native": "బాత్రూమ్ ఎక్కడ ఉంది?", "transliteration": "Bathroom ekkada undi?"},
    {"english": "How do I get there?", "native": "అక్కడికి ఎలా వెళ్ళాలి?", "transliteration": "Akkadiki elaa vellaali?"},
    {"english": "I need a taxi, please.", "native": "నాకు టాక్సీ కావాలి, దయచేసి.", "transliteration": "Naaku taxi kaavaali, dayachesi."},
    {"english": "Take me to the hotel.", "native": "హోటల్‌కి తీసుకెళ్ళండి.", "transliteration": "Hotel ki teesukellandi."},
    {"english": "How much does it cost?", "native": "ఎంత ఖర్చవుతుంది?", "transliteration": "Entha karchavuthund?"},
    {"english": "Can I see the menu?", "native": "మెనూ చూపించగలరా?", "transliteration": "Menu choopinchagalara?"},
    {"english": "This looks delicious!", "native": "ఇది రుచిగా కనిపిస్తోంది!", "transliteration": "Idi ruchigaa kanipistondi!"},
    {"english": "Water, please.", "native": "నీళ్లు, దయచేసి.", "transliteration": "Neellu, dayachesi."},
    {"english": "Check, please.", "native": "బిల్లు, దయచేసి.", "transliteration": "Billu, dayachesi."},
    {"english": "It was delicious!", "native": "చాలా రుచిగా ఉంది!", "transliteration": "Chala ruchigaa undi!"},
    {"english": "How much is this?", "native": "ఇది ఎంత?", "transliteration": "Idi entha?"},
    {"english": "Can I try this on?", "native": "దీన్ని ట్రై చేయవచ్చా?", "transliteration": "Deenni try cheyyavachaa?"},
    {"english": "Do you have a smaller size?", "native": "చిన్న సైజు ఉందా?", "transliteration": "Chinna size undaa?"},
    {"english": "I'll take this one.", "native": "ఇది తీసుకుంటాను.", "transliteration": "Idi teesukuntaanu."},
    {"english": "Can I pay by card?", "native": "కార్డుతో చెల్లించవచ్చా?", "transliteration": "Cardutho chellinchavachaa?"},
    {"english": "Help me, please!", "native": "సహాయం చేయండి!", "transliteration": "Sahayam cheyandi!"},
    {"english": "Call the police!", "native": "పోలీసుకి ఫోన్ చేయండి!", "transliteration": "Police ki phone cheyandi!"},
    {"english": "I need a doctor.", "native": "నాకు డాక్టర్ కావాలి.", "transliteration": "Naaku doctor kaavaali."},
    {"english": "Where is the hospital?", "native": "ఆసుపత్రి ఎక్కడ ఉంది?", "transliteration": "Aasupatri ekkada undi?"},
    {"english": "I'm lost, can you help?", "native": "నేను దారి తప్పాను, సహాయం చేయగలరా?", "transliteration": "Nenu daari tappanu, sahayam cheyagalaraa?"},
    {"english": "This is my mother.", "native": "ఇది నా అమ్మ.", "transliteration": "Idi naa amma."},
    {"english": "This is my father.", "native": "ఇది నా నాన్న.", "transliteration": "Idi naa nanna."},
    {"english": "I have an older brother.", "native": "నాకు అన్నయ్య ఉన్నారు.", "transliteration": "Naaku annayya unnaaru."},
    {"english": "I have a younger sister.", "native": "నాకు చెల్లి ఉంది.", "transliteration": "Naaku chelli undi."},
    {"english": "These are my parents.", "native": "వీరు నా తల్లిదండ్రులు.", "transliteration": "Veera naa tallidandhrulu."},
    {"english": "One, two, three.", "native": "ఒకటి, రెండు, మూడు.", "transliteration": "Okati, rendu, moodu."},
    {"english": "Four, five, six.", "native": "నాలుగు, ఐదు, ఆరు.", "transliteration": "Naalugu, aidu, aaru."},
    {"english": "Seven, eight, nine, ten.", "native": "ఏడు, ఎనిమిది, తొమ్మిది, పది.", "transliteration": "Eedu, enimidi, thomidi, padi."},
    {"english": "What number is this?", "native": "ఇది ఏ సంఖ్య?", "transliteration": "Idi ee sankhya?"},
    {"english": "Give me two, please.", "native": "రెండు ఇవ్వండి, దయచేసి.", "transliteration": "Rendu ivvandi, dayachesi."},
    {"english": "What time is it?", "native": "ఇప్పుడు ఎంత సేపు?", "transliteration": "Ippudu entha sepu?"},
    {"english": "It's three o'clock.", "native": "మూడు గంటలు అయింది.", "transliteration": "Moodu gantalu aindi."},
    {"english": "See you at noon.", "native": "మధ్యాహ్నం కలవాల.", "transliteration": "Madhyaahnham kalavaala."},
    {"english": "I'll be there in five minutes.", "native": "ఐదు నిమిషాల్లో వస్తాను.", "transliteration": "Aidu nimishaallo vastaana."},
    {"english": "What day is today?", "native": "ఈరోజు ఏమి రోజు?", "transliteration": "Eeroju emi roju?"},
    {"english": "Believe in yourself.", "native": "మీపై నమ్మకం ఉంచుకోండి.", "transliteration": "Meepai nammakam unchukondi."},
    {"english": "You are capable of amazing things.", "native": "మీరు అద్భుతమైన పనులు చేయగలరు.", "transliteration": "Meeru-adbhuthamaina panulu cheyagalaru."},
    {"english": "Dream big, start small.", "native": "పెద్ద కల కనండి, చిన్నదానితో మొదలుపెట్టండి.", "transliteration": "Pedda kala kanandi, chinnadaani tho modalupettandi."},
    {"english": "Your future is created by your actions.", "native": "మీ భవిష్యత్తు మీ చర్యలతో నిర్మించబడుతుంది.", "transliteration": "Mee bhavishthattu mee charyalatho nirminchabaduthundi."},
    {"english": "Never give up on your dreams.", "native": "మీ కలలను ఎప్పుడూ వదులుకోకండి.", "transliteration": "Mee kalalanu eppuduu vadulukokandi."},
    {"english": "Love yourself first.", "native": "ముందు మిమ్మల్ని ప్రేమించుకోండి.", "transliteration": "Mundu mimmlanni premichukondi."},
    {"english": "Love makes everything possible.", "native": "ప్రేమ అన్నీ సాధ్యం చేస్తుంది.", "transliteration": "Prema annii saadhyam chesthundi."},
    {"english": "You are loved more than you know.", "native": "మీరు ఊహించిన దానికన్నా ఎక్కువ ప్రేమించబడుతున్నారు.", "transliteration": "Meeru ohinchina daanikanna ekkuva preminchabaduthunnaaru."},
    {"english": "Love is the greatest power.", "native": "ప్రేమే అతిపెద్ద శక్తి.", "transliteration": "Preme athipedda shakthi."},
    {"english": "Spread love everywhere you go.", "native": "ఎక్కడికి వెళ్ళినా ప్రేమ పంచండి.", "transliteration": "Ekkadiki vellina prema panchandi."},
    {"english": "Success comes from hard work.", "native": "విజయం కష్టం నుండి వస్తుంది.", "transliteration": "Vijayam kashtam nundi vasthundi."},
    {"english": "Keep going, you're getting there.", "native": "కొనసాగించండి, మీరు చేరుకుంటున్నారు.", "transliteration": "Konasaaginchandi, meeru cherukuthunnaaru."},
    {"english": "Every step counts toward success.", "native": "ప్రతి అడుగూ విజయానికి దోహదపడుతుంది.", "transliteration": "Prathi-adugoo vijayaaniki dohadapaduthundi."},
    {"english": "Your effort will pay off.", "native": "మీ కృషి ఫలిస్తుంది.", "transliteration": "Mee krushi phalisthundi."},
    {"english": "Success is a journey, not a destination.", "native": "విజయం ఒక ప్రయాణం, గమ్యం కాదు.", "transliteration": "Vijayam oka prayaanam, gamyam kaadu."},
    {"english": "Knowledge is power.", "native": "జ్ఞానమే శక్తి.", "transliteration": "Jnāaname shakthi."},
    {"english": "Learn from yesterday, live for today.", "native": "నిన్నటి నుండి నేర్చుకోండి, ఈరోజు బ్రతకండి.", "transliteration": "Ninnati nundi nearchukondi, eeroju brathakandi."},
    {"english": "The wise learn from others' mistakes.", "native": "వివేకులు ఇతరుల తప్పుల నుండి నేర్చుకుంటారు.", "transliteration": "Vivekulu itharula thappula nundi nearchukuntaaru."},
    {"english": "Experience is the best teacher.", "native": "అనుభవమే ఉత్తమ గురువు.", "transliteration": "Anubhavame-uthama guruvu."},
    {"english": "Wisdom comes with age.", "native": "వయస్సుతో జ్ఞానం వస్తుంది.", "transliteration": "Vayassutho jnaanam vasthundi."},
    {"english": "Happiness is a choice.", "native": "సంతోషం ఒక ఎంపిక.", "transliteration": "Santhosham oka empika."},
    {"english": "Find joy in the little things.", "native": "చిన్న చిన్న విషయాల్లో ఆనందం కనుగొనండి.", "transliteration": "Chinna chinna vishayaallo aanandam kanugonandi."},
    {"english": "Your happiness matters most.", "native": "మీ సంతోషమే అత్యంత ముఖ్యం.", "transliteration": "Mee santhoshame-athyantam mukhyam."},
    {"english": "Smile, it makes others happy.", "native": "చిన్నగా నవ్వండి, ఇది ఇతరులను సంతోషపరుస్తుంది.", "transliteration": "Chinnagaa navvandi, idi itharulana santhosha-parusthundi."},
    {"english": "Happiness is contagious, spread it.", "native": "సంతోషం అంటువ్వుతుంది, పంచండి.", "transliteration": "Santhosham antuvuventhundi, panchandi."},
    {"english": "Better today than yesterday.", "native": "నిన్నటి కన్నా ఈరోజు మెరుగ్గా ఉంది.", "transliteration": "Ninnat kanna eerou meruggaa undi."},
    {"english": "Small steps lead to big changes.", "native": "చిన్న అడుగులు పెద్ద మార్పులకు దారితీస్తాయి.", "transliteration": "Chinna adugulu pedda maarpulaku daaritheesthaayi."},
    {"english": "Invest in yourself daily.", "native": "ప్రతిరోజు మీలో పెట్టుబడి చేయండి.", "transliteration": "Prathi-roju meelo pettu-badi cheyandi."},
    {"english": "Growth requires discomfort.", "native": "వృద్ధికి అసౌకర్యం అవసరం.", "transliteration": "Vrudhdhiki asoukaryam avasaram."},
    {"english": "Be your own competition.", "native": "మీ స్వంత పోటీదారుడిగా ఉండండి.", "transliteration": "Mee swantha pootidaarudigaa undandi."},
    {"english": "I am grateful for today.", "native": "ఈరోజుకి నేను కృతజ్ఞుడిని.", "transliteration": "Eerojuki nenu kruthagnudini."},
    {"english": "Thank you for everything.", "native": "అంతా ధన్యవాదాలు.", "transliteration": "Anthaa dhanyavaadaalu."},
    {"english": "Gratitude turns what we have into enough.", "native": "కృతజ్ఞత మనకు ఉన్నదానిని సరిపోనట్లు చేస్తుంది.", "transliteration": "Kruthagnatha manaku unnadaanini sariponaTlu chesthundi."},
    {"english": "Count your blessings daily.", "native": "ప్రతిరోజు మీ వరాలను లెక్కించండి.", "transliteration": "Prathiroju mee varaalana lekkinchandi."},
    {"english": "A grateful heart is a happy heart.", "native": "కృతజ్ఞతాపూరిత హృదయం సంతోషపూరిత హృదయం.", "transliteration": "Kruthagnatha-pooritha hridayam santhosha-pooritha hridayam."},
    {"english": "Friends make life better.", "native": "స్నేహితులు జీవితాన్ని మెరుగుపరుస్తారు.", "transliteration": "Snehithulu jeevithaanni merugu-parustaaru."},
    {"english": "A true friend is always there.", "native": "నిజమైన స్నేహితుడు ఎప్పుడూ ఉంటాడు.", "transliteration": "Nijamaina snehithudu eppudoo untaadu."},
    {"english": "Friendship is a precious gift.", "native": "స్నేహం విలువైన బహుమతి.", "transliteration": "Snehatham viluvaina bahumathi."},
    {"english": "Good friends are like stars.", "native": "మంచి స్నేహితులు నక్షత్రాల లాంటివి.", "transliteration": "Manchi snehithulu nakshathrala laantivi."},
    {"english": "Cherish your true friends.", "native": "మీ నిజమైన స్నేహితులను విలువచేయండి.", "transliteration": "Mee nijamaina snehithulana viluva-cheyandi."},
    {"english": "Hope never dies.", "native": "ఆశ ఎప్పుడూ చనిపోదు.", "transliteration": "Aasha eppudoo chanipoodu."},
    {"english": "Tomorrow is a new beginning.", "native": "రేపు ఒక కొత్త ప్రారంభం.", "transliteration": "Repu oka koththa praarambham."},
    {"english": "Keep hope alive in your heart.", "native": "మీ హృదయంలో ఆశను సజీవంగా ఉంచుకోండి.", "transliteration": "Mee hridayamlo aashana sajaeeavagaa unchukondi."},
    {"english": "Hope is the light in darkness.", "native": "ఆశ చీకటిలో వెలుగు.", "transliteration": "Aasha cheekatilo velugu."},
    {"english": "Where there's hope, there's life.", "native": "ఆశ ఉన్నచోట జీవితం ఉంది.", "transliteration": "Aasha unnachota jeevitham undi."},
    {"english": "Create something beautiful today.", "native": "ఈరోజు ఏదైనా అందమైనది సృష్టించండి.", "transliteration": "Eeroju edaina-andamainadi srushtimchandi."},
    {"english": "Your creativity is unique.", "native": "మీ సృజనాత్మకత అద్వితీయం.", "transliteration": "Mee srujanaathmakatha-advitheeyam."},
    {"english": "Let your imagination run wild.", "native": "మీ ఊహలను స్వేచ్ఛగా వదులుకోండి.", "transliteration": "Mee oohalana swechchagaa vadulukondi."},
    {"english": "Art comes from the heart.", "native": "కళ హృదయం నుండి వస్తుంది.", "transliteration": "Kala hridayam nundi vasthundi."},
    {"english": "Every day is a canvas.", "native": "ప్రతిరోజు ఒక కాన్వాస్.", "transliteration": "Prathiroju oka canvas."},
    {"english": "Find peace within yourself.", "native": "మీలో శాంతిని కనుగొనండి.", "transliteration": "Meelo shanthini kanugonandi."},
    {"english": "Calm mind, happy heart.", "native": "ప్రశాంత మనస్సు, సంతోషపూరిత హృదయం.", "transliteration": "Prashaantha manassu, santhosha-pooritha hridayam."},
    {"english": "Peace begins with a smile.", "native": "శాంతి ఒక చిన్నగుడుపుతో మొదలవుతుంది.", "transliteration": "Shanth oka chinnagudiputho modalavuthundi."},
    {"english": "Breathe deeply, let go.", "native": "లోతుగా ఊపిరి తీసుకోండి, వదులుకోండి.", "transliteration": "Lothugaa oopiri theesukondi, vadulukondi."},
    {"english": "Your inner peace is precious.", "native": "మీ అంతర్ శాంతి విలువైనది.", "transliteration": "Mee anthar shanthi viluvainadhi."},
    {"english": "Believe you can, you're right.", "native": "మీరు చేయగలరని నమ్మండి, మీరు సరే.", "transliteration": "Meeru cheyagalarani nammnadi, meeru sare."},
    {"english": "You are stronger than you think.", "native": "మీరు అనుకున్న దానికన్నా బలంగా ఉన్నారు.", "transliteration": "Meeru anukunna daanikanna balangaa unnaru."},
    {"english": "Confidence comes from within.", "native": "విశ్వాసం లోపలి నుండి వస్తుంది.", "transliteration": "Vishwaasam lopali nundi vasthundi."},
    {"english": "Stand tall, be proud.", "native": "నిటారుగా నిలబడండి, గర్వంగా ఉండండి.", "transliteration": "Nitaarugaa nilabidandi, garvamgaa undandi."},
    {"english": "You have what it takes.", "native": "మీకు అవసరమైనది మీలో ఉంది.", "transliteration": "Meeku avasaramainadhi meelo undi."},
    {"english": "Never give up, keep going.", "native": "ఎప్పుడూ వదులుకోకండి, కొనసాగండి.", "transliteration": "Eppudoo vadulukokandi, konasaagandi."},
    {"english": "Persistence beats talent.", "native": "పట్టుదల ప్రతిభని ఓడిస్తుంది.", "transliteration": "Pattudala prathibhani oadisthundi."},
    {"english": "Fall seven times, rise eight.", "native": "ఏడుసార్లు కూలితే ఎనిమిది సార్లు లెగెదులుకోండి.", "transliteration": "Edusaarlu koolithe enimidi saarlu legedulukondi."},
    {"english": "Hard work pays off eventually.", "native": "కష్టం చివరకు ఫలిస్తుంది.", "transliteration": "Kashtam chivaraku phalisthundi."},
    {"english": "Stay the course, don't quit.", "native": "మార్గంలో ఉండండి, వదులుకోకండి.", "transliteration": "Maargamlo undandi, vadulukokandi."},
    {"english": "Let inspiration guide you.", "native": "స్ఫూర్తి మిమ్మల్ని మార్గనిర్దేశం చేయనివ్వండి.", "transliteration": "Sphoorthi mimmlanni maarga-nirdesham cheyanivvandi."},
    {"english": "Be the inspiration others need.", "native": "ఇతరులకు అవసరమైన స్ఫూర్తిగా ఉండండి.", "transliteration": "Itharulaku avasaramaina sphoorthigaa undandi."},
    {"english": "Inspire by example, not words.", "native": "మాటలతో కాదు, ఆదర్శంతో స్ఫూర్తినివ్వండి.", "transliteration": "Maatalatho kaadu, aadarshamtho sphoorthi-nivvandi."},
    {"english": "Your story inspires others.", "native": "మీ కథ ఇతరులను స్ఫూర్తివంతం చేస్తుంది.", "transliteration": "Mee katha itharulana sphoorthi-vantham chesthundi."},
    {"english": "Find inspiration in nature.", "native": "ప్రకృతిలో స్ఫూర్తిని కనుగొనండి.", "transliteration": "Prakruthilo sphoorthini kanugonandi."},
    {"english": "Choose positivity every day.", "native": "ప్రతిరోజు సానుకూలతను ఎంచుకోండి.", "transliteration": "Prathiroju saanukoolathana enchukondi."},
    {"english": "Positive thoughts create positive life.", "native": "సానుకూల ఆలోచనలు సానుకూల జీవితాన్ని సృష్టిస్తాయి.", "transliteration": "Saanukoola aalochanalu saanukoola jeevithaanni srushtistaayi."},
    {"english": "Surround yourself with positivity.", "native": "మిమ్మల్ని సానుకూలతతో చుట్టుముట్టండి.", "transliteration": "Mimmlanni saanukoolathatho chuttumuttandi."},
    {"english": "Every day is a fresh start.", "native": "ప్రతిరోజు ఒక కొత్త ప్రారంభం.", "transliteration": "Prathiroju oka koththa praarambham."},
    {"english": "Live life with a positive heart.", "native": "సానుకూల హృదయంతో జీవించండి.", "transliteration": "Saanukoola hridayamtho jeevinchandi."},
    {"english": "Be brave, take the leap.", "native": "ధైర్యంగా ఉండండి, ముందుకు వెళ్ళండి.", "transliteration": "Dhairyangaa undandi, mundhuku vellandi."},
    {"english": "Courage is not absence of fear.", "native": "ధైర్యం అనేది భయం లేకపోవడం కాదు.", "transliteration": "Dhairyam anedhi bhayam lekapovadam kaadhu."},
    {"english": "Face your fears with courage.", "native": "ధైర్యంతో మీ భయాలను ఎదుర్కోండి.", "transliteration": "Dhiryantho mee bhayaalana edhurukondi."},
    {"english": "Brave hearts change the world.", "native": "ధైర్యవంతుల హృదయాలు ప్రపంచాన్ని మారుస్తాయి.", "transliteration": "Dhairya-vanthula hridayaalu prapanchaanni maaruthaayi."},
    {"english": "Courage grows with use.", "native": "ధైర్యం వాడుకోగా పెరుగుతుంది.", "transliteration": "Dhairyam vaadukogaa peruguthundi."},
    {"english": "Be kind to everyone you meet.", "native": "మీరు కలుసుకునే ప్రతి ఒక్కరితో దయగా ఉండండి.", "transliteration": "Meeru kalusukuney prathi okkaritho dhayagaa undandi."},
    {"english": "Kindness costs nothing, means everything.", "native": "దయకు ఖర్చు లేదు, అది అంతా అర్థం చేస్తుంది.", "transliteration": "Dayaku kharchu ledu, adi anthaa artham chesthundi."},
    {"english": "A kind word warms the heart.", "native": "దయగల మాట హృదయాన్ని వెచ్చగా చేస్తుంది.", "transliteration": "Dayagala maata hridayaanni vechchagaa chesthundi."},
    {"english": "Spread kindness wherever you go.", "native": "ఎక్కడికి వెళ్ళినా దయను పంచండి.", "transliteration": "Ekkadiki vellina dayana panchandi."},
    {"english": "Kindness makes the world better.", "native": "దయ ప్రపంచాన్ని మెరుగుపరుస్తుంది.", "transliteration": "Daya prapanchaanni merugu-parusthundi."},
    {"english": "Good things come to those who wait.", "native": "ఎదురుచూసేవారికి మంచి విషయాలు వస్తాయి.", "transliteration": "Edhuruchosevaariki manchi vishayaalu vasthaayi."},
    {"english": "Patience is a virtue.", "native": "ఓపిక ఒక సుగుణం.", "transliteration": "Opika oka sugunam."},
    {"english": "Take your time, don't rush.", "native": "మీ సమయం తీసుకోండి, త్వరపడకండి.", "transliteration": "Mee samayam theesukondi, thvarapada-kandi."},
    {"english": "Patience brings peace of mind.", "native": "ఓపిక మనసుకు శాంతినిస్తుంది.", "transliteration": "Opika manasuku shanthim-isthundi."},
    {"english": "Wait patiently, trust the process.", "native": "ఓపికగా ఎదురుచూడండి, ప్రక్రియను నమ్మండి.", "transliteration": "Opikagaa edhuruchoodandi, prakriyana nammnadi."},
    {"english": "Forgive and set yourself free.", "native": "క్షమించండి, మిమ్మల్ని విముక్తం చేసుకోండి.", "transliteration": "Kshaminchandi, mimmlanni vimuktham chesukondi."},
    {"english": "Forgiveness is a gift to yourself.", "native": "క్షమాపణ మీకు మీరే ఇచ్చుకున్న బహుమతి.", "transliteration": "Kshamaapanam meeku meeray ichhukunna bahumathi."},
    {"english": "Let go of grudges, find peace.", "native": "పగలను వదులుకోండి, శాంతిని కనుగొనండి.", "transliteration": "Pagalana vadulukondi, shaanthini kanugonandi."},
    {"english": "To err is human, to forgive divine.", "native": "తప్పు చేయడం మానవ సహజం, క్షమించడం దైవికం.", "transliteration": "Thappu cheyadam maanava sahajam, kshaminchadam daivikam."},
    {"english": "Forgiveness heals all wounds.", "native": "క్షమాపణ అన్ని గాయాలను నయం చేస్తుంది.", "transliteration": "Kshamaapanam anni gaayaalana nayam chesthundi."},
    {"english": "You are stronger than you know.", "native": "మీరు తెలుసుకున్న దానికన్నా బలంగా ఉన్నారు.", "transliteration": "Meeru thelusukunna daanikanna balangaa-unnaru."},
    {"english": "Strength comes from within.", "native": "బలం లోపలి నుండి వస్తుంది.", "transliteration": "Balam lopali nundi vasthundi."},
    {"english": "Your struggles develop your strength.", "native": "మీ పోరాటాలు మీ బలాన్ని పెంచుతాయి.", "transliteration": "Mee pooraatallu mee balanni penchuthaayi."},
    {"english": "Be strong, stay steady.", "native": "బలంగా ఉండండి, స్థిరంగా ఉండండి.", "transliteration": "Balamgaa undandi, sthiramgaa undandi."},
    {"english": "Inner strength conquers all.", "native": "అంతర్బలం అన్నింటినీ జయిస్తుంది.", "transliteration": "Anthar-balam annintini jayisthundi."},
    {"english": "Find joy in every moment.", "native": "ప్రతి క్షణంలో ఆనందాన్ని కనుగొనండి.", "transliteration": "Prathi kshanamlo aanandhaanni kanugonandi."},
    {"english": "Joy is contagious, spread it.", "native": "ఆనందం అంటువ్వుతుంది, పంచండి.", "transliteration": "Aanandham antuvuventhundi, panchandi."},
    {"english": "Let joy fill your heart today.", "native": "ఈరోజు ఆనందం మీ హృదయాన్ని నింపనివ్వండి.", "transliteration": "Eeroju aanandam mee hridayaanni ninpaa-nivvandi."},
    {"english": "Choose joy over worry.", "native": "బెంగ కంటే ఆనందాన్ని ఎంచుకోండి.", "transliteration": "Benga kantey aanandhaanni enchukondi."},
    {"english": "Joy is the simplest form of gratitude.", "native": "ఆనందం అనేది కృతజ్ఞత యొక్క సరళమైన రూపం.", "transliteration": "Aanandham anedhi kruthagnatha yokka sarala-maina roopam."},
    {"english": "Find balance in your life.", "native": "మీ జీవితంలో సమతుల్యతను కనుగొనండి.", "transliteration": "Mee jeevithamlo samathul yathana kanugonandi."},
    {"english": "Balance is the key to happiness.", "native": "సమతుల్యతే సంతోషానికి మార్గం.", "transliteration": "Samathulyathe santhoshaaniki maargam."},
    {"english": "Work hard, rest well.", "native": "గట్టిగా పని చేయండి, బాగా విశ్రాంతి తీసుకోండి.", "transliteration": "Gattigaa pani cheyandi, baagaa vishraanthi theesukondi."},
    {"english": "A balanced life is a peaceful life.", "native": "సమతుల్య జీవితమే శాంతిమయ జీవితం.", "transliteration": "Samathuly jeevithame shaanthimaya jeevitham."},
    {"english": "Prioritize what matters most.", "native": "అత్యంత ముఖ్యమైనదానికి ప్రాధాన్యత ఇవ్వండి.", "transliteration": "Athyantam mukhyamainadaaniki praadhaanyatha ivvandi."},
    {"english": "Growth happens outside your comfort zone.", "native": "వృద్ధి మీ సౌకర్య మండలం వెలుపల జరుగుతుంది.", "transliteration": "Vrudhdhi mee soukarthya mandalam velupala Jaruguthundi."},
    {"english": "Embrace change, grow stronger.", "native": "మార్పును ఆహ్వానించండి, బలపడండి.", "transliteration": "Maarupuna aahvaaninchandi, balapadandi."},
    {"english": "Every challenge is a growth opportunity.", "native": "ప్రతి సవాలూ వృద్ధికి ఒక అవకాశం.", "transliteration": "Prathi-savaaloo vrudhdhiki oka avakaasham."},
    {"english": "Grow through what you go through.", "native": "మీ అనుభవాల ద్వారా పెరగండి.", "transliteration": "Mee anubhavaala dhwaaraa peragandi."},
    {"english": "Personal growth is a lifelong journey.", "native": "వ్యక్తిగత వృద్ధి జీవితాంతపు ప్రయాణం.", "transliteration": "Vyakthigatha vrudhdhi jeevithaanthapu prayaanam."},
    {"english": "Find your purpose, live it.", "native": "మీ ప్రయోజనాన్ని కనుగొనండి, దానిని జీవించండి.", "transliteration": "Mee prayojanaanni kanugonandi, daanini jeevinchandi."},
    {"english": "Purpose gives life meaning.", "native": "ప్రయోజనం జీవితానికి అర్థాన్ని ఇస్తుంది.", "transliteration": "Prayojanam jeevithaaniki arthaanni isthundi."},
    {"english": "Live with purpose and passion.", "native": "ప్రయోజనంతో మరియు ఉత్సాహంతో జీవించండి.", "transliteration": "Prayojanamtho mariyu uthsaahamtho jeevinchandi."},
    {"english": "Your purpose is your calling.", "native": "మీ ప్రయోజనమే మీ పిలుపు.", "transliteration": "Mee prayojaname-mee pilupu."},
    {"english": "Discover purpose in everyday moments.", "native": "రోజువారీ క్షణాల్లో ప్రయోజనాన్ని కనుగొనండి.", "transliteration": "Rojuvaaree kshanaallo prayojanaanni kanugonandi."},
    {"english": "Be present in this moment.", "native": "ఈ క్షణంలో ఉండండి.", "transliteration": "Ee kshanamlo undandi."},
    {"english": "Mindfulness brings inner peace.", "native": "సంపూర్ణ అవగాహన అంతర్ శాంతినిస్తుంది.", "transliteration": "Sampoorna avagaahana anthar shaanthini-sthundi."},
    {"english": "Breathe deeply, stay mindful.", "native": "లోతుగా ఊపిరి తీసుకోండి, జాగ్రత్తగా ఉండండి.", "transliteration": "Lothugaa oopiri theesukondi, jaagrattagaa undandi."},
    {"english": "The present moment is all we have.", "native": "ప్రస్తుత క్షణమే మనకు ఉన్నదంతా.", "transliteration": "Prasthutha kshaname manaku unna-danthaa."},
    {"english": "Practice mindfulness daily.", "native": "ప్రతిరోజు సంపూర్ణ అవగాహనను అభ్యాసం చేయండి.", "transliteration": "Prathiroju sampoorna avagaahanana abhyaasam cheyandi."},
]
# ==== FALLBACK PHRASES END ====


def _load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_phrase_history():
    data = _load_json(PHRASE_HISTORY_FILE, {"phrases": [], "last_updated": None})
    data.setdefault("phrases", [])
    return data


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    _save_json(PHRASE_HISTORY_FILE, data)


def is_phrase_used(english):
    english_lower = english.lower().strip()
    for p in load_phrase_history()["phrases"]:
        if p.get("english", "").lower().strip() == english_lower:
            return True
    return False


def _history_native(p):
    for key in (PHRASE_KEY, "vietnamese", "native", "translation", "target"):
        value = p.get(key)
        if value:
            return str(value)
    return ""


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    for phrase in phrases:
        history["phrases"].append({
            "english": phrase["english"],
            PHRASE_KEY: phrase["native"],
            "transliteration": phrase.get("transliteration", ""),
            "category": category,
            "generated_at": datetime.now().isoformat(),
        })
    save_phrase_history(history)
    print(f"[content] Saved {len(phrases)} phrases (history total: {len(history['phrases'])})")


def get_available_category():
    data = _load_json(RECENT_CATEGORIES_FILE, {"recent_categories": [], "last_updated": None})
    recent = data.get("recent_categories", [])
    available = [c for c in CATEGORIES if c not in recent]
    if not available:
        recent = recent[-5:]
        available = [c for c in CATEGORIES if c not in recent]
        print("[rotation] Reset recent categories")
    selected = random.choice(available)
    recent.append(selected)
    data["recent_categories"] = recent[-MAX_RECENT_CATEGORIES:]
    data["last_updated"] = datetime.now().isoformat()
    _save_json(RECENT_CATEGORIES_FILE, data)
    print(f"[rotation] Category: {selected} ({len(available)} available)")
    return selected


def _normalize_phrase(item):
    if not isinstance(item, dict):
        return None
    english = str(item.get("english", "")).strip()
    native = str(
        item.get(PHRASE_KEY)
        or item.get("native")
        or item.get("vietnamese")
        or item.get("translation")
        or ""
    ).strip()
    translit = str(item.get("transliteration") or item.get("romanization") or item.get("romaji") or "").strip()
    if not english or not native:
        return None
    if len(english.split()) > 16:
        return None
    if "/" in native or "|" in native:
        native = native.split("/")[0].split("|")[0].strip()
    return {
        "english": english.replace("  ", " ").strip(),
        "native": native.strip(),
        "transliteration": translit.strip().strip("[]"),
    }


def _history_keys(history):
    used_en = set()
    used_nat = set()
    for p in history.get("phrases", []):
        en = str(p.get("english", "")).lower().strip()
        nat = _history_native(p).lower().strip()
        if en:
            used_en.add(en)
        if nat:
            used_nat.add(nat)
    return used_en, used_nat


def generate_phrases(category_english: str, num_phrases: int = 5) -> list:
    category_native = CATEGORIES_NATIVE[category_english]
    history = load_phrase_history()
    used_en, used_nat = _history_keys(history)
    recent_english = [
        p["english"] for p in history["phrases"] if p.get("category") == category_english
    ][-30:]

    models = [config.AI_MODEL]
    if "gemini-fast" not in models:
        models.append("gemini-fast")

    if config.POLLINATIONS_API_KEY:
        for attempt in range(5):
            model = models[0] if attempt < 3 else models[-1]
            try:
                phrases = _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model)
                unique = []
                for item in phrases:
                    p = _normalize_phrase(item)
                    if not p:
                        continue
                    key_en = p["english"].lower().strip()
                    key_nat = p["native"].lower().strip()
                    if key_en in used_en or key_nat in used_nat:
                        continue
                    if any(key_en == u["english"].lower().strip() for u in unique):
                        continue
                    used_en.add(key_en)
                    used_nat.add(key_nat)
                    unique.append(p)
                    if len(unique) >= num_phrases:
                        break
                if len(unique) >= num_phrases:
                    add_phrases_to_history(unique[:num_phrases], category_english)
                    return unique[:num_phrases]
                print(f"[content] Attempt {attempt + 1}: only {len(unique)} fresh phrases (need {num_phrases})")
            except Exception as exc:  # noqa: BLE001 - network boundary
                print(f"[content] Attempt {attempt + 1} failed ({model}): {exc}")
            time.sleep(1.5 * (attempt + 1))
    else:
        print("[content] No POLLINATIONS_API_KEY, using fallback phrases")

    fresh_fallback = []
    for p in FALLBACK_PHRASES:
        if p["english"].lower().strip() in used_en or p["native"].lower().strip() in used_nat:
            continue
        fresh_fallback.append(p)
    if not fresh_fallback:
        raise RuntimeError("Phrase API unavailable and no unused fallback phrases left; refusing to reuse phrases")
    chosen = fresh_fallback[:num_phrases]
    if len(chosen) < num_phrases:
        print(f"[content] Only {len(chosen)} fresh fallback phrases; building a shorter lesson")
    add_phrases_to_history(chosen, category_english)
    return chosen


def _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model=None):
    avoid = ""
    if recent_english:
        avoid = "\nDo NOT reuse any of these phrases:\n" + "\n".join(f"- {p}" for p in recent_english)

    prompt = f"""Create {num_phrases * 6} unique {category_english} phrases for English speakers learning {LANGUAGE_NAME}.
{avoid}

Rules:
1. Keep every phrase short and natural (4-11 words in English).
2. Use natural commas for TTS breathing pauses.
3. Each phrase must be speakable in 2-4 seconds.
4. Write clean {LANGUAGE_NAME} in {NATIVE_NAME} with correct accents and orthography. One translation only, no slashes.
5. Transliteration is a friendly Roman-script pronunciation guide for English speakers (not IPA).
6. Vary the sentence patterns and emotions. No duplicates.
7. Phrases must feel like real everyday language, not textbook filler.

Return ONLY a JSON array:
[{{"english": "...", "native": "...", "transliteration": "..."}}]"""

    response = requests.post(
        "https://gen.pollinations.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.POLLINATIONS_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or config.AI_MODEL,
            "messages": [
                {"role": "system", "content": f"You are a {LANGUAGE_NAME} teacher creating short, natural, varied bilingual phrases. Reply with JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": min(0.95 + attempt * 0.02, 1.0),
        },
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    if "```json" in content:
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in content:
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    start = content.find("[")
    end = content.rfind("]")
    if start >= 0 and end > start:
        content = content[start:end + 1]

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("AI did not return a JSON array")
    return data
