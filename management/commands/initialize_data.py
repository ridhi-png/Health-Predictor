from django.core.management.base import BaseCommand
from health_predictor.models import Symptom, Disease, Remedy

class Command(BaseCommand):
    help = 'Initialize database with symptoms, diseases, and remedies data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing health predictor data...')
        
        # Create symptoms
        self.create_symptoms()
        
        # Create diseases
        self.create_diseases()
        
        # Create remedies
        self.create_remedies()
        
        # Link diseases to symptoms
        self.link_diseases_to_symptoms()
        
        # Link remedies to diseases
        self.link_remedies_to_diseases()
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized health predictor data!'))
    
    def create_symptoms(self):
        self.stdout.write('Creating symptoms...')
        
        symptoms_data = [
            # Head symptoms
            {'name': 'Headache', 'body_part': 'Head', 'description': 'Pain in the head or upper neck'},
            {'name': 'Dizziness', 'body_part': 'Head', 'description': 'Feeling lightheaded or unsteady'},
            {'name': 'Blurred vision', 'body_part': 'Head', 'description': 'Lack of sharpness of vision resulting in the inability to see fine detail'},
            {'name': 'Migraine', 'body_part': 'Head', 'description': 'Recurring severe headache, often with nausea and visual disturbances'},
            {'name': 'Ear pain', 'body_part': 'Head', 'description': 'Pain in or around the ear'},
            
            # Chest symptoms
            {'name': 'Chest pain', 'body_part': 'Chest', 'description': 'Pain or discomfort in the chest area'},
            {'name': 'Shortness of breath', 'body_part': 'Chest', 'description': 'Difficulty breathing or feeling like you cannot get enough air'},
            {'name': 'Cough', 'body_part': 'Chest', 'description': 'Sudden expulsion of air from the lungs'},
            {'name': 'Wheezing', 'body_part': 'Chest', 'description': 'Breathing with a whistling or rattling sound in the chest'},
            {'name': 'Heart palpitations', 'body_part': 'Chest', 'description': 'Feelings of having a fast-beating, fluttering or pounding heart'},
            
            # Abdomen symptoms
            {'name': 'Abdominal pain', 'body_part': 'Abdomen', 'description': 'Pain felt between the chest and groin'},
            {'name': 'Nausea', 'body_part': 'Abdomen', 'description': 'Feeling of sickness with an inclination to vomit'},
            {'name': 'Vomiting', 'body_part': 'Abdomen', 'description': 'Forcible voluntary or involuntary emptying of stomach contents through the mouth'},
            {'name': 'Diarrhea', 'body_part': 'Abdomen', 'description': 'Loose, watery stools occurring more frequently than usual'},
            {'name': 'Constipation', 'body_part': 'Abdomen', 'description': 'Infrequent bowel movements that may be painful'},
            
            # Limbs symptoms
            {'name': 'Joint pain', 'body_part': 'Limbs', 'description': 'Discomfort, aches, or soreness in joints'},
            {'name': 'Muscle weakness', 'body_part': 'Limbs', 'description': 'Lack of muscle strength or muscle fatigue'},
            {'name': 'Swelling', 'body_part': 'Limbs', 'description': 'Enlargement of a body part due to fluid accumulation'},
            {'name': 'Numbness', 'body_part': 'Limbs', 'description': 'Lack of sensation in a body part'},
            {'name': 'Tingling', 'body_part': 'Limbs', 'description': 'Pins and needles sensation'},
            
            # General symptoms
            {'name': 'Fever', 'body_part': 'General', 'description': 'Elevated body temperature'},
            {'name': 'Fatigue', 'body_part': 'General', 'description': 'Extreme tiredness resulting from mental or physical exertion'},
            {'name': 'Chills', 'body_part': 'General', 'description': 'Feeling of coldness accompanied by shivering'},
            {'name': 'Night sweats', 'body_part': 'General', 'description': 'Excessive sweating during sleep'},
            {'name': 'Weight loss', 'body_part': 'General', 'description': 'Unintentional decrease in body weight'},
            {'name': 'Loss of appetite', 'body_part': 'General', 'description': 'Reduced desire to eat'},
            {'name': 'Insomnia', 'body_part': 'General', 'description': 'Difficulty falling or staying asleep'},
            {'name': 'Anxiety', 'body_part': 'General', 'description': 'Feeling of worry, nervousness, or unease'},
            {'name': 'Depression', 'body_part': 'General', 'description': 'Persistent feeling of sadness and loss of interest'},
            {'name': 'Rash', 'body_part': 'Skin', 'description': 'Area of irritated or swollen skin'},
        ]
        
        for symptom_data in symptoms_data:
            Symptom.objects.get_or_create(
                name=symptom_data['name'],
                defaults={
                    'body_part': symptom_data['body_part'],
                    'description': symptom_data['description']
                }
            )
        
        self.stdout.write(f'Created {len(symptoms_data)} symptoms')
    
    def create_diseases(self):
        self.stdout.write('Creating diseases...')
        
        diseases_data = [
            {
                'name': 'Common Cold',
                'description': 'A viral infectious disease of the upper respiratory tract that primarily affects the nose.',
                'severity': 'MILD'
            },
            {
                'name': 'Influenza',
                'description': 'A viral infection that attacks your respiratory system — your nose, throat and lungs.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Migraine',
                'description': 'A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Tension Headache',
                'description': 'A mild to moderate pain often described as feeling like a tight band around the head.',
                'severity': 'MILD'
            },
            {
                'name': 'Gastroenteritis',
                'description': 'Inflammation of the lining of the stomach and intestines, characterized by diarrhea, abdominal cramps, nausea, vomiting, and sometimes fever.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Irritable Bowel Syndrome',
                'description': 'A common disorder that affects the large intestine. Signs and symptoms include cramping, abdominal pain, bloating, gas, and diarrhea or constipation, or both.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Arthritis',
                'description': 'Inflammation of one or more joints, causing pain and stiffness that can worsen with age.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Anxiety Disorder',
                'description': 'A mental health disorder characterized by feelings of worry, anxiety, or fear that are strong enough to interfere with one\'s daily activities.',
                'severity': 'MODERATE'
            },
            {
                'name': 'Depression',
                'description': 'A mental health disorder characterized by persistently depressed mood or loss of interest in activities, causing significant impairment in daily life.',
                'severity': 'SEVERE'
            },
            {
                'name': 'Insomnia',
                'description': 'A sleep disorder that can make it hard to fall asleep, hard to stay asleep, or cause you to wake up too early and not be able to get back to sleep.',
                'severity': 'MODERATE'
            },
        ]
        
        for disease_data in diseases_data:
            Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults={
                    'description': disease_data['description'],
                    'severity_level': 5 if disease_data['severity'] == 'MODERATE' else (8 if disease_data['severity'] == 'SEVERE' else 2)
                }
            )
        
        self.stdout.write(f'Created {len(diseases_data)} diseases')
    
    def create_remedies(self):
        self.stdout.write('Creating remedies...')
        
        remedies_data = [
            # Herbal remedies
            {
                'name': 'Ginger Tea',
                'type': 'NATURAL',
                'description': 'A tea made from ginger root that helps with nausea, digestion, and inflammation.',
                'instructions': 'Steep 1-2 teaspoons of freshly grated ginger in hot water for 5-10 minutes. Strain and add honey if desired.'
            },
            {
                'name': 'Peppermint Tea',
                'type': 'NATURAL',
                'description': 'A tea made from peppermint leaves that helps with digestive issues and headaches.',
                'instructions': 'Steep 1-2 teaspoons of dried peppermint leaves in hot water for 5-10 minutes. Strain and drink.'
            },
            {
                'name': 'Chamomile Tea',
                'type': 'NATURAL',
                'description': 'A tea made from chamomile flowers that helps with sleep, anxiety, and digestive issues.',
                'instructions': 'Steep 1-2 teaspoons of dried chamomile flowers in hot water for 5-10 minutes. Strain and drink before bedtime.'
            },
            {
                'name': 'Turmeric Milk',
                'type': 'NATURAL',
                'description': 'A warm milk drink with turmeric that helps with inflammation and pain.',
                'instructions': 'Mix 1/2 teaspoon of turmeric powder in a cup of warm milk. Add honey to taste. Drink once daily.'
            },
            {
                'name': 'Echinacea Supplement',
                'type': 'NATURAL',
                'description': 'An herbal supplement that helps boost the immune system.',
                'instructions': 'Take as directed on the supplement packaging, typically 300-500mg three times daily during illness.'
            },
            
            # Yoga remedies
            {
                'name': 'Child\'s Pose (Balasana)',
                'type': 'YOGA',
                'description': 'A resting pose that gently stretches the hips, thighs, and ankles while calming the brain and helping relieve stress and fatigue.',
                'instructions': 'Kneel on the floor. Touch your big toes together and sit on your heels, then separate your knees about as wide as your hips. Exhale and lay your torso down between your thighs. Extend your arms forward. Hold for 30 seconds to a few minutes.'
            },
            {
                'name': 'Legs-Up-The-Wall Pose (Viparita Karani)',
                'type': 'YOGA',
                'description': 'A restorative yoga pose that helps relieve tired legs, gently stretches the back of the neck, front torso, and back of the legs.',
                'instructions': 'Sit with one side of your body against a wall. Swing your legs up onto the wall as you lie back. Your buttocks should be as close to the wall as comfortable. Relax your arms at your sides. Close your eyes and breathe deeply. Hold for 5-15 minutes.'
            },
            {
                'name': 'Corpse Pose (Savasana)',
                'type': 'YOGA',
                'description': 'A pose of total relaxation, making it one of the most challenging asanas.',
                'instructions': 'Lie on your back with your legs straight and arms at your sides, palms facing up. Close your eyes and breathe naturally. Relax your entire body. Stay in this pose for 5-15 minutes.'
            },
            {
                'name': 'Cat-Cow Stretch (Marjaryasana-Bitilasana)',
                'type': 'YOGA',
                'description': 'A gentle flow between two poses that warms the body and brings flexibility to the spine.',
                'instructions': 'Start on your hands and knees. Inhale, arch your back and lift your head (Cow). Exhale, round your spine and tuck your chin (Cat). Repeat 5-10 times, moving with your breath.'
            },
            {
                'name': 'Seated Forward Bend (Paschimottanasana)',
                'type': 'YOGA',
                'description': 'A seated forward fold that stretches the spine, shoulders, and hamstrings.',
                'instructions': 'Sit with your legs extended in front of you. Inhale and lengthen your spine. Exhale and hinge at your hips to fold forward, reaching for your feet. Hold for 30 seconds to 1 minute.'
            },
            
            # Diet remedies
            {
                'name': 'BRAT Diet',
                'type': 'DIET',
                'description': 'A diet consisting of bananas, rice, applesauce, and toast that helps with digestive issues.',
                'instructions': 'Eat only bananas, rice, applesauce, and toast for 24-48 hours during acute digestive issues. Gradually reintroduce other foods as symptoms improve.'
            },
            {
                'name': 'Anti-Inflammatory Diet',
                'type': 'DIET',
                'description': 'A diet rich in fruits, vegetables, whole grains, and omega-3 fatty acids that helps reduce inflammation.',
                'instructions': 'Increase intake of fruits, vegetables, whole grains, fatty fish, nuts, and olive oil. Reduce intake of processed foods, red meat, and added sugars.'
            },
            {
                'name': 'Hydration Therapy',
                'type': 'DIET',
                'description': 'Increased fluid intake to help with various conditions including headaches, fatigue, and constipation.',
                'instructions': 'Drink at least 8-10 glasses of water daily. Include herbal teas and clear broths. Avoid caffeine and alcohol.'
            },
            {
                'name': 'Elimination Diet',
                'type': 'DIET',
                'description': 'A short-term eating plan that eliminates certain foods that may be causing allergies or other digestive reactions.',
                'instructions': 'Remove common allergens (dairy, gluten, eggs, soy, nuts) from your diet for 2-3 weeks. Reintroduce one food at a time, noting any reactions.'
            },
            {
                'name': 'Probiotic-Rich Diet',
                'type': 'DIET',
                'description': 'A diet rich in probiotic foods that help maintain gut health.',
                'instructions': 'Include yogurt, kefir, sauerkraut, kimchi, and other fermented foods in your daily diet. Start with small amounts and gradually increase.'
            },
            
            # Other remedies
            {
                'name': 'Hot Compress',
                'type': 'LIFESTYLE',
                'description': 'Application of heat to relieve pain and stiffness.',
                'instructions': 'Soak a clean cloth in hot water, wring out excess water, and apply to the affected area for 15-20 minutes. Repeat 3-4 times daily.'
            },
            {
                'name': 'Cold Compress',
                'type': 'LIFESTYLE',
                'description': 'Application of cold to reduce inflammation and numb pain.',
                'instructions': 'Wrap ice in a thin towel and apply to the affected area for 15-20 minutes. Repeat every 2-3 hours as needed.'
            },
            {
                'name': 'Epsom Salt Bath',
                'type': 'LIFESTYLE',
                'description': 'A warm bath with Epsom salts to relieve muscle pain and reduce inflammation.',
                'instructions': 'Add 2 cups of Epsom salt to a warm bath. Soak for 15-20 minutes. Pat dry afterward and drink water to stay hydrated.'
            },
            {
                'name': 'Deep Breathing Exercises',
                'type': 'LIFESTYLE',
                'description': 'Controlled breathing techniques to reduce stress and anxiety.',
                'instructions': 'Sit or lie in a comfortable position. Inhale slowly through your nose for a count of 4, hold for 2, then exhale through your mouth for a count of 6. Repeat for 5-10 minutes.'
            },
            {
                'name': 'Progressive Muscle Relaxation',
                'type': 'LIFESTYLE',
                'description': 'A technique that involves tensing and then relaxing muscle groups to reduce stress and anxiety.',
                'instructions': 'Starting with your toes, tense each muscle group for 5 seconds, then relax for 30 seconds. Work your way up through your body to your head.'
            },
        ]
        
        for remedy_data in remedies_data:
            Remedy.objects.get_or_create(
                name=remedy_data['name'],
                defaults={
                    'remedy_type': remedy_data['type'],
                    'description': remedy_data['description'],
                    'instructions': remedy_data['instructions']
                }
            )
        
        self.stdout.write(f'Created {len(remedies_data)} remedies')
    
    def link_diseases_to_symptoms(self):
        self.stdout.write('Linking diseases to symptoms...')
        
        disease_symptom_map = {
            'Common Cold': ['Cough', 'Fever', 'Headache', 'Fatigue', 'Sore Throat'],
            'Influenza': ['Fever', 'Cough', 'Fatigue', 'Chills', 'Headache', 'Muscle weakness'],
            'Migraine': ['Headache', 'Nausea', 'Blurred vision', 'Dizziness'],
            'Tension Headache': ['Headache', 'Fatigue', 'Muscle weakness'],
            'Gastroenteritis': ['Nausea', 'Vomiting', 'Diarrhea', 'Abdominal pain', 'Fever'],
            'Irritable Bowel Syndrome': ['Abdominal pain', 'Diarrhea', 'Constipation', 'Nausea'],
            'Arthritis': ['Joint pain', 'Swelling', 'Fatigue', 'Stiffness'],
            'Anxiety Disorder': ['Anxiety', 'Heart palpitations', 'Shortness of breath', 'Insomnia'],
            'Depression': ['Depression', 'Fatigue', 'Insomnia', 'Loss of appetite', 'Weight loss'],
            'Insomnia': ['Insomnia', 'Fatigue', 'Anxiety', 'Headache'],
        }
        
        for disease_name, symptom_names in disease_symptom_map.items():
            try:
                disease = Disease.objects.get(name=disease_name)
                for symptom_name in symptom_names:
                    try:
                        symptom = Symptom.objects.get(name__icontains=symptom_name)
                        disease.symptoms.add(symptom)
                    except Symptom.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Symptom {symptom_name} not found'))
            except Disease.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Disease {disease_name} not found'))
        
        self.stdout.write('Linked diseases to symptoms')
    
    def link_remedies_to_diseases(self):
        self.stdout.write('Linking remedies to diseases...')
        
        disease_remedy_map = {
            'Common Cold': ['Ginger Tea', 'Hydration Therapy', 'Echinacea Supplement', 'Hot Compress'],
            'Influenza': ['Hydration Therapy', 'Ginger Tea', 'Echinacea Supplement', 'Rest'],
            'Migraine': ['Cold Compress', 'Peppermint Tea', 'Deep Breathing Exercises', 'Legs-Up-The-Wall Pose'],
            'Tension Headache': ['Hot Compress', 'Progressive Muscle Relaxation', 'Peppermint Tea', 'Seated Forward Bend'],
            'Gastroenteritis': ['BRAT Diet', 'Hydration Therapy', 'Ginger Tea', 'Rest'],
            'Irritable Bowel Syndrome': ['Peppermint Tea', 'Probiotic-Rich Diet', 'Elimination Diet', 'Cat-Cow Stretch'],
            'Arthritis': ['Turmeric Milk', 'Anti-Inflammatory Diet', 'Epsom Salt Bath', 'Child\'s Pose'],
            'Anxiety Disorder': ['Chamomile Tea', 'Deep Breathing Exercises', 'Progressive Muscle Relaxation', 'Legs-Up-The-Wall Pose'],
            'Depression': ['Anti-Inflammatory Diet', 'Deep Breathing Exercises', 'Corpse Pose', 'Hydration Therapy'],
            'Insomnia': ['Chamomile Tea', 'Progressive Muscle Relaxation', 'Corpse Pose', 'Legs-Up-The-Wall Pose'],
        }
        
        for disease_name, remedy_names in disease_remedy_map.items():
            try:
                disease = Disease.objects.get(name=disease_name)
                for remedy_name in remedy_names:
                    try:
                        remedy = Remedy.objects.get(name__icontains=remedy_name)
                        disease.remedies.add(remedy)
                    except Remedy.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Remedy {remedy_name} not found'))
            except Disease.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Disease {disease_name} not found'))
        
        self.stdout.write('Linked remedies to diseases')