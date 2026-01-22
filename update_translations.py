#!/usr/bin/env python
"""
Update translations in .po files with new strings extracted from templates
"""

import os
import re
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
django.setup()

# Import polib for working with .po files
try:
    import polib
except ImportError:
    print("Installing polib...")
    import subprocess
    subprocess.run(['pip', 'install', 'polib'], check=True)
    import polib

# New strings that need to be added to translations
NEW_STRINGS = {
    "Student Portal": {"sw": "Kituo cha Wanafunzi", "ar": "بوابة الطالب", "fr": "Portail Étudiant"},
    "Create Account Now": {"sw": "Tengeneza Akaunti Sasa", "ar": "إنشاء حساب الآن", "fr": "Créer un compte maintenant"},
    "Who We Are": {"sw": "Nani Tunavyo Kuwa", "ar": "من نحن", "fr": "Qui sommes-nous"},
    "Leading the Way in International Education Counseling.": {
        "sw": "Kuongoza Njia katika Ushauri wa Elimu ya Kimataifa.",
        "ar": "الرائدة في مجال الاستشارات التعليمية الدولية.",
        "fr": "Leader en matière de conseil en éducation internationale."
    },
    "Founded in 2020 and launched in 2024, Africa Western Education Company Ltd is a professional educational consultancy empowering African students and professionals with reliable, transparent, and high-quality advisory services. We connect you to global learning opportunities while simplifying admissions, scholarship applications, and visa processes.": {
        "sw": "Iliyoanzishwa mwaka 2020 na kuanzishwa rasmi 2024, Africa Western Education Company Ltd ni mshauri wa elimu wa kitaaluma anayehamisha wanafunzi wa Kiafrika na wataalamu na huduma inayoweza kutegemea, zenye uwazi na za ubora wa juu. Tunakuunganisha na fursa za kujifunza duniani ilhali tunarahisisha ombi la kujiandikisha, maombi ya kuzamia na michakato ya visa.",
        "ar": "تأسست عام 2020 وأطلقت في عام 2024، شركة Africa Western Education Company Ltd هي شركة استشارات تعليمية احترافية تمكن الطلاب والمحترفين الأفارقة من خلال خدمات استشارية موثوقة وشفافة وعالية الجودة. نحن نربطك بفرص التعلم العالمية مع تبسيط عمليات القبول وطلبات المنح الدراسية ومعالجات التأشيرات.",
        "fr": "Fondée en 2020 et lancée en 2024, Africa Western Education Company Ltd est une entreprise de conseil en éducation professionnelle qui autonomise les étudiants et les professionnels africains grâce à des services consultatifs fiables, transparents et de haute qualité. Nous vous connectons à des opportunités d'apprentissage mondiales tout en simplifiant les processus d'admission, les demandes de bourses et les procédures de visa."
    },
    "Our Mission": {"sw": "Lengo Letu", "ar": "مهمتنا", "fr": "Notre Mission"},
    "To empower African students and professionals by providing reliable, transparent, and high-quality educational consultancy services that connect them to global learning opportunities.": {
        "sw": "Kuhamisha wanafunzi wa Kiafrika na wataalamu kwa kutoa huduma za ushauri wa elimu inayoweza kutegemea, zenye uwazi na za ubora wa juu zinazowaunganisha na fursa za kujifunza duniani.",
        "ar": "تمكين الطلاب والمحترفين الأفارقة من خلال تقديم خدمات استشارية تعليمية موثوقة وشفافة وعالية الجودة تربطهم بفرص التعلم العالمية.",
        "fr": "Autonomiser les étudiants et les professionnels africains en fournissant des services de conseil en éducation fiables, transparents et de haute qualité qui les relient à des opportunités d'apprentissage mondiales."
    },
    "Our Vision": {"sw": "Macho Yetu", "ar": "رؤيتنا", "fr": "Notre Vision"},
    "To become Africa's leading and most trusted educational consultancy, shaping futures through global academic access and excellence.": {
        "sw": "Kuwa kampuni ya ushauri wa elimu inayoongoza na kuaminika zaidi Afrika, inayounda siku za kesho kwa njia ya upatikanaji wa elimu ya kimataifa na kusitifikika.",
        "ar": "أن تصبح شركة الاستشارات التعليمية الرائدة والأكثر ثقة في أفريقيا، تشكل المستقبل من خلال الوصول الأكاديمي العالمي والتميز.",
        "fr": "Devenir la première et la plus fiable entreprise de conseil en éducation en Afrique, façonnant l'avenir grâce à l'accès académique mondial et l'excellence."
    },
    "The Pillars of Our Success": {"sw": "Nguzo za Mafanikio Yetu", "ar": "أعمدة نجاحنا", "fr": "Les piliers de notre succès"},
    "Integrity": {"sw": "Uadilifu", "ar": "النزاهة", "fr": "Intégrité"},
    "We uphold honesty, transparency, and ethical standards in all our services and interactions.": {
        "sw": "Tunashikilia uaminifu, uwazi, na kaida za maadili katika huduma zetu zote na mwingiliano.",
        "ar": "نحن نتمسك بالصدق والشفافية والمعايير الأخلاقية في جميع خدماتنا والتفاعلات.",
        "fr": "Nous défendons l'honnêteté, la transparence et les normes éthiques dans tous nos services et nos interactions."
    },
    "Innovation": {"sw": "Ubunifu", "ar": "الابتكار", "fr": "Innovation"},
    "We embrace creativity and continuously improve our services with new methods and technologies.": {
        "sw": "Tunakubali ubunifu na kuendelea kuboresha huduma zetu kwa njia mpya na teknolohia.",
        "ar": "نحن نتبنى الإبداع ونحسن خدماتنا باستمرار بطرق وتقنيات جديدة.",
        "fr": "Nous embrassons la créativité et améliorons continuellement nos services avec de nouvelles méthodes et technologies."
    },
    "Excellence": {"sw": "Ubora", "ar": "التميز", "fr": "Excellence"},
    "We are committed to delivering the highest quality of service and achieving outstanding results for our clients.": {
        "sw": "Tumejitolea kutoa huduma ya ubora wa juu zaidi na kufikia matokeo yanayoibangua kwa wateja wetu.",
        "ar": "نحن ملتزمون بتقديم أعلى جودة من الخدمة وتحقيق نتائج استثنائية لعملائنا.",
        "fr": "Nous nous engageons à fournir la plus haute qualité de service et à obtenir des résultats exceptionnels pour nos clients."
    },
    "Customer Focus": {"sw": "Mkazo wa Mteja", "ar": "التركيز على العميل", "fr": "Orientation client"},
    "Our clients are at the center of everything we do; we prioritize their needs and ensure satisfaction.": {
        "sw": "Wateja wetu wako katikati ya kila kitu tunachokifanya; tunaprioritize mahitaji yao na kuhakikisha kuridhika.",
        "ar": "عملاؤنا في مركز كل ما نفعله؛ نعطي الأولوية لاحتياجاتهم ونضمن الرضا.",
        "fr": "Nos clients sont au centre de tout ce que nous faisons; nous prioritorisons leurs besoins et assurons la satisfaction."
    },
    "Accountability": {"sw": "Wajibu", "ar": "المساءلة", "fr": "Responsabilité"},
    "We take full responsibility for our actions and outcomes, ensuring reliability and trustworthiness.": {
        "sw": "Tunachukua jukumu kamili kwa vitendo vyetu na matokeo, kuhakikisha kutegemewa na kuaminika.",
        "ar": "نحن نتحمل المسؤولية الكاملة عن أفعالنا ونتائجنا، مما يضمن الموثوقية والجدارة بالثقة.",
        "fr": "Nous assumons la responsabilité complète de nos actions et de nos résultats, assurant la fiabilité et la confiance."
    },
    "Teamwork": {"sw": "Kazi ya Timu", "ar": "العمل الجماعي", "fr": "Travail d'équipe"},
    "We foster collaboration and cooperation within our team and with partners to achieve common goals.": {
        "sw": "Tunawakamatia ushirikiano na kazi ya pamoja ndani ya timu yetu na na washirika kupata lengo la pamoja.",
        "ar": "نحن نعزز التعاون والعمل الجماعي داخل فريقنا وشركائنا لتحقيق أهداف مشتركة.",
        "fr": "Nous favorisons la collaboration et la coopération au sein de notre équipe et avec nos partenaires pour atteindre des objectifs communs."
    },
    "Our Comprehensive Services": {"sw": "Huduma Zetu Kamili", "ar": "خدماتنا الشاملة", "fr": "Nos services complets"},
    "End-to-End Study Abroad Support": {"sw": "Msaada wa Kujifunza Nje Kamili", "ar": "دعم الدراسة بالخارج من النهاية إلى النهاية", "fr": "Soutien complet pour étudier à l'étranger"},
    "From initial guidance to post-arrival support, we handle every aspect of your study abroad journey with expert care.": {
        "sw": "Kutoka kwa mwongozo wa mwanzo hadi msaada baada ya kuwasili, tunakabili kila jibu la safari yako ya kujifunza nje kwa huduma ya kumbukumbu.",
        "ar": "من التوجيه الأولي إلى الدعم بعد الوصول، نتعامل مع كل جوانب رحلة الدراسة بالخارج بعناية متخصصة.",
        "fr": "Du guidage initial au soutien post-arrivée, nous gérons chaque aspect de votre parcours d'études à l'étranger avec un soin expert."
    },
    "How We Help:": {"sw": "Jinsi Tunavyosaidia:", "ar": "كيف نساعد:", "fr": "Comment nous aidons:"},
    "Personalized Profile Analysis:": {"sw": "Uchambuzi wa Wasifu wa Kibinafsi:", "ar": "تحليل الملف الشخصي المخصص:", "fr": "Analyse du profil personnalisé:"},
    "Comprehensive assessment of academic background, interests, and career goals": {
        "sw": "Tathmini kamili ya asili ya elimu, maslahi, na lengo la kazi",
        "ar": "تقييم شامل للخلفية الأكاديمية والاهتمامات والأهداف الوظيفية",
        "fr": "Évaluation complète des antécédents scolaires, des intérêts et des objectifs professionnels"
    },
    "University Shortlisting:": {"sw": "Orodha Fupi ya Chuo cha Juu:", "ar": "قائمة جامعات مختصرة:", "fr": "Liste raccourcie des universités:"},
    "Curated list of universities matching your profile and budget": {
        "sw": "Orodha inayokaguliwa kwa haraka ya chuo cha juu zinazofanana na wasifu wako na bajeti",
        "ar": "قائمة منسقة من الجامعات التي تطابق ملفك الشخصي وميزانيتك",
        "fr": "Liste sélectionnée d'universités correspondant à votre profil et à votre budget"
    },
    "Course Selection:": {"sw": "Kuchagua Kozi:", "ar": "اختيار الدورة:", "fr": "Sélection des cours:"},
    "Expert guidance on program choices with best career prospects": {
        "sw": "Mwongozo wa kumbukumbu juu ya kuchagua programu na prospekti nzuri za kazi",
        "ar": "التوجيه الخبير بشأن اختيار البرنامج مع أفضل آفاق مهنية",
        "fr": "Orientation d'experts sur les choix de programmes avec les meilleures perspectives de carrière"
    },
    "Career Pathway Planning:": {"sw": "Kupanga Njia ya Kazi:", "ar": "تخطيط المسار الوظيفي:", "fr": "Planification du parcours professionnel:"},
    "Long-term career strategy aligned with your chosen course": {
        "sw": "Mkakati wa kazi wa muda mrefu inayofanana na kozi uliyochagua",
        "ar": "استراتيجية وظيفية طويلة الأجل متوافقة مع الدورة التي اخترتها",
        "fr": "Stratégie de carrière à long terme alignée avec le cours que vous avez choisi"
    },
    "AFRICA WESTERN EDUCATION COMPANY LTD": {"sw": "KAMPUNI YA ELIMU YA MAGHARIBI YA AFRICA", "ar": "شركة التعليم الغربية الأفريقية المحدودة", "fr": "SOCIÉTÉ DE L'ÉDUCATION OCCIDENTALE AFRICAINE LTÉE"},
    "Empowering African students and professionals through reliable, transparent, and high-quality educational consultancy services.": {
        "sw": "Kuhamisha wanafunzi wa Kiafrika na wataalamu kwa njia ya huduma za ushauri wa elimu inayoweza kutegemea, zenye uwazi na za ubora.",
        "ar": "تمكين الطلاب والمحترفين الأفارقة من خلال خدمات الاستشارات التعليمية الموثوقة والشفافة والعالية الجودة.",
        "fr": "Autonomiser les étudiants et les professionnels africains grâce à des services de conseil en éducation fiables, transparents et de haute qualité."
    },
    "Quick Links": {"sw": "Kiungo cha Haraka", "ar": "روابط سريعة", "fr": "Liens rapides"},
    "Study Abroad": {"sw": "Kujifunza Nje", "ar": "الدراسة بالخارج", "fr": "Étudier à l'étranger"},
    "Local Universities": {"sw": "Chuo cha Juu cha Ndani", "ar": "الجامعات المحلية", "fr": "Universités locales"},
    "TCU Services": {"sw": "Huduma za TCU", "ar": "خدمات TCU", "fr": "Services TCU"},
    "Apply Now": {"sw": "Jiandikishe Sasa", "ar": "تقدم الآن", "fr": "Postulez maintenant"},
    "Our Services": {"sw": "Huduma Zetu", "ar": "خدماتنا", "fr": "Nos services"},
    "University Application Assistance": {"sw": "Msaada wa Ombi la Chuo cha Juu", "ar": "مساعدة في تطبيق الجامعة", "fr": "Assistance de demande universitaire"},
    "Visa Processing Support": {"sw": "Msaada wa Usindikaji wa Visa", "ar": "دعم معالجة التأشيرة", "fr": "Soutien au traitement des visas"},
    "TCU Application Services": {"sw": "Huduma za Ombi la TCU", "ar": "خدمات تطبيق TCU", "fr": "Services de demande TCU"},
    "Pre-Departure Guidance": {"sw": "Mwongozo Kabla ya Kuondoka", "ar": "التوجيه قبل المغادرة", "fr": "Orientation avant le départ"},
    "Scholarship Assistance": {"sw": "Msaada wa Kuzamia", "ar": "مساعدة المنح الدراسية", "fr": "Aide aux bourses d'études"},
    "Contact Us": {"sw": "Wasiliana Nasi", "ar": "اتصل بنا", "fr": "Nous contacter"},
    "Dar es Salaam, Tanzania": {"sw": "Dar es Salaam, Tanzania", "ar": "دار السلام، تنزانيا", "fr": "Dar es Salaam, Tanzanie"},
    "Mon-Fri: 8:00 AM - 6:00 PM": {"sw": "Jumatatu-Ijumaa: 8:00 AM - 6:00 PM", "ar": "الاثنين-الجمعة: 8:00 صباحًا - 6:00 مساءً", "fr": "Lun-Ven: 8:00 AM - 6:00 PM"},
    "Sat: 9:00 AM - 2:00 PM": {"sw": "Jumamosi: 9:00 AM - 2:00 PM", "ar": "السبت: 9:00 صباحًا - 2:00 مساءً", "fr": "Sam: 9:00 AM - 2:00 PM"},
    "Privacy Policy": {"sw": "Sera ya Faragha", "ar": "سياسة الخصوصية", "fr": "Politique de confidentialité"},
    "Terms of Service": {"sw": "Sheria za Huduma", "ar": "شروط الخدمة", "fr": "Conditions de service"},
    "Employee Login": {"sw": "Kuingia kama Mfanyakazi", "ar": "دخول الموظف", "fr": "Connexion employé"},
}

def update_po_file(po_file_path, language):
    """Update a .po file with new translations"""
    print(f"\nUpdating {language} .po file: {po_file_path}")
    
    # Check if file exists
    if not os.path.exists(po_file_path):
        print(f"File not found: {po_file_path}")
        return
    
    # Load the .po file
    po = polib.pofile(po_file_path)
    
    # Add new entries
    added = 0
    for english, translations_dict in NEW_STRINGS.items():
        if language not in translations_dict:
            continue
        
        # Check if entry already exists
        existing_entry = po.find(english)
        
        if existing_entry:
            # Update existing entry
            existing_entry.msgstr = translations_dict[language]
            print(f"  Updated: {english[:50]}...")
        else:
            # Add new entry
            entry = polib.POEntry(
                msgid=english,
                msgstr=translations_dict[language],
            )
            po.append(entry)
            added += 1
            print(f"  Added: {english[:50]}...")
    
    # Save the updated .po file
    po.save(po_file_path)
    print(f"\nSaved {po_file_path} with {added} new entries")
    
    # Compile to .mo file
    mo_file_path = po_file_path.replace('.po', '.mo')
    po.save_as_mofile(mo_file_path)
    print(f"Compiled to: {mo_file_path}")

# Update .po files for all languages
locale_dir = 'locale'
for language in ['sw', 'ar', 'fr']:
    po_file = os.path.join(locale_dir, language, 'LC_MESSAGES', 'django.po')
    update_po_file(po_file, language)

print("\n=== Translation update completed ===")
