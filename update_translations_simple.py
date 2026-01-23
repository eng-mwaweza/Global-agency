"""
Simple translation updater that directly modifies .po files without Django setup
"""
import polib
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent

# Improved translations with better accuracy
NEW_STRINGS = {
    "Student Portal": {"sw": "Kituo cha Wanafunzi", "ar": "بوابة الطالب", "fr": "Portail Étudiant"},
    "Create Account Now": {"sw": "Fungua Akaunti Sasa", "ar": "إنشاء حساب الآن", "fr": "Créer un compte maintenant"},
    "Who We Are": {"sw": "Kuhusu Sisi", "ar": "من نحن", "fr": "Qui nous sommes"},
    "Leading the Way in International Education Counseling.": {
        "sw": "Tunaongoza katika Ushauri wa Elimu ya Kimataifa.",
        "ar": "رواد الاستشارات التعليمية الدولية.",
        "fr": "Leaders dans le conseil en éducation internationale."
    },
    "Founded in 2020 and launched in 2024, Africa Western Education Company Ltd is a professional educational consultancy empowering African students and professionals with reliable, transparent, and high-quality advisory services. We connect you to global learning opportunities while simplifying admissions, scholarship applications, and visa processes.": {
        "sw": "Kampuni yetu ilianzishwa mwaka 2020 na kuanza rasmi utendaji mwaka 2024. Africa Western Education Company Ltd ni kampuni ya ushauri wa elimu ya kitaalam inayowasaidia wanafunzi na wataalamu wa Kiafrika kupata fursa za masomo kimataifa kwa njia ya ushauri wa kuaminika, wenye uwazi na ubora wa hali ya juu. Tunakuunganisha na fursa za masomo ulimwenguni kote huku tukiwezesha mchakato wa maombi ya vyuo, ufadhili na visa.",
        "ar": "تأسست في عام 2020 وبدأت العمل في 2024، شركة Africa Western Education Company Ltd هي شركة استشارات تعليمية محترفة تمكّن الطلاب والمهنيين الأفارقة من خلال خدمات استشارية موثوقة وشفافة وعالية الجودة. نربطك بفرص التعلم العالمية مع تبسيط عمليات القبول الجامعي وطلبات المنح الدراسية وإجراءات التأشيرات.",
        "fr": "Fondée en 2020 et opérationnelle depuis 2024, Africa Western Education Company Ltd est une société de conseil éducatif professionnelle qui accompagne les étudiants et professionnels africains grâce à des services consultatifs fiables, transparents et de haute qualité. Nous vous connectons aux opportunités d'études internationales tout en simplifiant les admissions, les demandes de bourses et les procédures de visa."
    },
    "Our Mission": {"sw": "Dhamira Yetu", "ar": "مهمتنا", "fr": "Notre Mission"},
    "To empower African students and professionals by providing reliable, transparent, and high-quality educational consultancy services that connect them to global learning opportunities.": {
        "sw": "Kuwapa nguvu wanafunzi na wataalamu wa Kiafrika kwa kutoa huduma za ushauri wa elimu zinazotegemeka, zenye uwazi na ubora wa hali ya juu ambazo zinawaunganisha na fursa za masomo kimataifa.",
        "ar": "تمكين الطلاب والمهنيين الأفارقة من خلال توفير خدمات استشارية تعليمية موثوقة وشفافة وعالية الجودة تربطهم بفرص التعلم العالمية.",
        "fr": "Autonomiser les étudiants et professionnels africains en fournissant des services de conseil éducatif fiables, transparents et de haute qualité qui les connectent aux opportunités d'apprentissage mondiales."
    },
    "Our Vision": {"sw": "Dira Yetu", "ar": "رؤيتنا", "fr": "Notre Vision"},
    "To become Africa's leading and most trusted educational consultancy, shaping futures through global academic access and excellence.": {
        "sw": "Kuwa kampuni ya ushauri wa elimu inayoongoza na kuaminika zaidi Afrika, tukijenga mustakabali kupitia upatikanaji wa elimu ya kimataifa na ubora.",
        "ar": "أن نصبح الشركة الاستشارية التعليمية الرائدة والأكثر موثوقية في أفريقيا، نصنع المستقبل من خلال الوصول الأكاديمي العالمي والتميز.",
        "fr": "Devenir la société de conseil éducatif leader et la plus fiable d'Afrique, façonnant l'avenir grâce à l'accès académique mondial et l'excellence."
    },
    "The Pillars of Our Success": {"sw": "Misingi ya Mafanikio Yetu", "ar": "ركائز نجاحنا", "fr": "Les piliers de notre succès"},
    "Integrity": {"sw": "Uadilifu", "ar": "النزاهة", "fr": "Intégrité"},
    "We uphold honesty, transparency, and ethical standards in all our services and interactions.": {
        "sw": "Tunashikilia uaminifu, uwazi na viwango vya maadili katika huduma zetu zote na mwingiliano wetu.",
        "ar": "نحافظ على الصدق والشفافية والمعايير الأخلاقية في جميع خدماتنا وتعاملاتنا.",
        "fr": "Nous maintenons l'honnêteté, la transparence et les normes éthiques dans tous nos services et interactions."
    },
    "Innovation": {"sw": "Ubunifu", "ar": "الابتكار", "fr": "Innovation"},
    "We embrace creativity and continuously improve our services with new methods and technologies.": {
        "sw": "Tunakubali ubunifu na kuboresha huduma zetu mara kwa mara kwa mbinu na teknolojia mpya.",
        "ar": "نتبنى الإبداع ونحسّن خدماتنا باستمرار بأساليب وتقنيات جديدة.",
        "fr": "Nous adoptons la créativité et améliorons continuellement nos services avec de nouvelles méthodes et technologies."
    },
    "Excellence": {"sw": "Ubora", "ar": "التميز", "fr": "Excellence"},
    "We are committed to delivering the highest quality of service and achieving outstanding results for our clients.": {
        "sw": "Tumejitolea kutoa huduma bora zaidi na kufikia matokeo bora kwa wateja wetu.",
        "ar": "نحن ملتزمون بتقديم أعلى جودة من الخدمات وتحقيق نتائج متميزة لعملائنا.",
        "fr": "Nous nous engageons à fournir des services de la plus haute qualité et à obtenir des résultats exceptionnels pour nos clients."
    },
    "Customer Focus": {"sw": "Kuzingatia Wateja", "ar": "التركيز على العملاء", "fr": "Orientation client"},
    "Our clients are at the center of everything we do; we prioritize their needs and ensure satisfaction.": {
        "sw": "Wateja wetu ni kipaumbele chetu; tunaweka mahitaji yao mbele na kuhakikisha kuridhika kwao.",
        "ar": "عملاؤنا في صميم كل ما نقوم به؛ نعطي الأولوية لاحتياجاتهم ونضمن رضاهم.",
        "fr": "Nos clients sont au cœur de tout ce que nous faisons; nous priorisons leurs besoins et assurons leur satisfaction."
    },
    "Accountability": {"sw": "Uwajibikaji", "ar": "المساءلة", "fr": "Responsabilité"},
    "We take full responsibility for our actions and outcomes, ensuring reliability and trustworthiness.": {
        "sw": "Tunachukua jukumu kamili la vitendo vyetu na matokeo yake, tukihakikisha kutegemeka na kuaminika.",
        "ar": "نتحمل المسؤولية الكاملة عن أفعالنا ونتائجها، مما يضمن الموثوقية والجدارة بالثقة.",
        "fr": "Nous assumons l'entière responsabilité de nos actions et résultats, garantissant fiabilité et confiance."
    },
    "Teamwork": {"sw": "Ushirikiano", "ar": "العمل الجماعي", "fr": "Travail d'équipe"},
    "We foster collaboration and cooperation within our team and with partners to achieve common goals.": {
        "sw": "Tunaimarisha ushirikiano na kazi ya pamoja ndani ya timu yetu na na washirika wetu ili kufikia malengo yetu ya pamoja.",
        "ar": "نعزز التعاون والتنسيق داخل فريقنا ومع شركائنا لتحقيق أهداف مشتركة.",
        "fr": "Nous encourageons la collaboration et la coopération au sein de notre équipe et avec nos partenaires pour atteindre des objectifs communs."
    },
    "Our Comprehensive Services": {"sw": "Huduma Zetu Kamili", "ar": "خدماتنا الشاملة", "fr": "Nos services complets"},
    "End-to-End Study Abroad Support": {"sw": "Msaada Kamili wa Kusoma Nje ya Nchi", "ar": "دعم شامل للدراسة بالخارج", "fr": "Accompagnement complet pour études à l'étranger"},
    "From initial guidance to post-arrival support, we handle every aspect of your study abroad journey with expert care.": {
        "sw": "Kutoka mwongozo wa awali hadi msaada baada ya kuwasili, tunashughulikia kila kipengele cha safari yako ya masomo nje ya nchi kwa utaalamu na uzoefu.",
        "ar": "من التوجيه الأولي إلى الدعم بعد الوصول، نتعامل مع كل جانب من جوانب رحلة دراستك في الخارج بعناية خبراء.",
        "fr": "Du conseil initial au soutien post-arrivée, nous gérons chaque aspect de votre parcours d'études à l'étranger avec expertise."
    },
    "How We Help:": {"sw": "Jinsi Tunavyosaidia:", "ar": "كيف نساعدك:", "fr": "Comment nous aidons:"},
    "Personalized Profile Analysis:": {"sw": "Uchambuzi wa Wasifu wa Kibinafsi:", "ar": "تحليل الملف الشخصي:", "fr": "Analyse personnalisée du profil:"},
    "Comprehensive assessment of academic background, interests, and career goals": {
        "sw": "Tathmini kamili ya historia ya masomo, mapenzi na malengo ya kazi",
        "ar": "تقييم شامل للخلفية الأكاديمية والاهتمامات والأهداف المهنية",
        "fr": "Évaluation complète du parcours académique, des intérêts et des objectifs de carrière"
    },
    "University Shortlisting:": {"sw": "Uchaguzi wa Vyuo Vikuu:", "ar": "القائمة المختصرة للجامعات:", "fr": "Présélection universitaire:"},
    "Curated list of universities matching your profile and budget": {
        "sw": "Orodha iliyochaguliwa ya vyuo vikuu vinavyoendana na wasifu na bajeti yako",
        "ar": "قائمة مختارة من الجامعات التي تناسب ملفك وميزانيتك",
        "fr": "Liste sélectionnée d'universités correspondant à votre profil et budget"
    },
    "Course Selection:": {"sw": "Kuchagua Kozi:", "ar": "اختيار البرنامج:", "fr": "Sélection de programme:"},
    "Expert guidance on program choices with best career prospects": {
        "sw": "Ushauri wa kitaalamu juu ya uchaguzi wa programu zenye fursa bora za kazi",
        "ar": "إرشاد متخصص حول اختيارات البرامج ذات أفضل الآفاق المهنية",
        "fr": "Conseil d'experts sur les choix de programmes avec les meilleures perspectives professionnelles"
    },
    "Career Pathway Planning:": {"sw": "Kupanga Njia ya Kazi:", "ar": "تخطيط المسار المهني:", "fr": "Planification de parcours professionnel:"},
    "Long-term career strategy aligned with your chosen course": {
        "sw": "Mkakati wa muda mrefu wa kazi unaofanana na kozi uliyochagua",
        "ar": "استراتيجية مهنية طويلة المدى متوافقة مع البرنامج الذي اخترته",
        "fr": "Stratégie de carrière à long terme alignée sur votre programme choisi"
    },
    "AFRICA WESTERN EDUCATION COMPANY LTD": {"sw": "KAMPUNI YA ELIMU YA MAGHARIBI YA AFRIKA", "ar": "شركة أفريقيا ويسترن للتعليم المحدودة", "fr": "AFRICA WESTERN EDUCATION COMPANY LTD"},
    "Empowering African students and professionals through reliable, transparent, and high-quality educational consultancy services.": {
        "sw": "Tunawasaidia wanafunzi na wataalamu wa Kiafrika kupitia huduma za ushauri wa elimu zinazotegemeka, zenye uwazi na ubora wa hali ya juu.",
        "ar": "تمكين الطلاب والمهنيين الأفارقة من خلال خدمات استشارية تعليمية موثوقة وشفافة وعالية الجودة.",
        "fr": "Accompagner les étudiants et professionnels africains grâce à des services de conseil éducatif fiables, transparents et de haute qualité."
    },
    "Quick Links": {"sw": "Viungo vya Haraka", "ar": "روابط سريعة", "fr": "Liens rapides"},
    "Study Abroad": {"sw": "Soma Nje ya Nchi", "ar": "الدراسة في الخارج", "fr": "Études à l'étranger"},
    "Local Universities": {"sw": "Vyuo Vikuu vya Ndani", "ar": "الجامعات المحلية", "fr": "Universités locales"},
    "TCU Services": {"sw": "Huduma za TCU", "ar": "خدمات TCU", "fr": "Services TCU"},
    "Apply Now": {"sw": "Omba Sasa", "ar": "تقدم الآن", "fr": "Postulez maintenant"},
    "Our Services": {"sw": "Huduma Zetu", "ar": "خدماتنا", "fr": "Nos services"},
    "University Application Assistance": {"sw": "Msaada wa Maombi ya Chuo Kikuu", "ar": "مساعدة في طلبات الجامعة", "fr": "Assistance pour candidatures universitaires"},
    "Visa Processing Support": {"sw": "Msaada wa Kuchakata Visa", "ar": "دعم معالجة التأشيرات", "fr": "Aide au traitement des visas"},
    "TCU Application Services": {"sw": "Huduma za Maombi ya TCU", "ar": "خدمات طلبات TCU", "fr": "Services de candidature TCU"},
    "Pre-Departure Guidance": {"sw": "Mwongozo wa Kabla ya Kusafiri", "ar": "الإرشاد قبل المغادرة", "fr": "Orientation pré-départ"},
    "Scholarship Assistance": {"sw": "Msaada wa Kuzamia", "ar": "المساعدة في المنح الدراسية", "fr": "Assistance aux bourses d'études"},
    "Contact Us": {"sw": "Wasiliana Nasi", "ar": "اتصل بنا", "fr": "Contactez-nous"},
    "Dar es Salaam, Tanzania": {"sw": "Dar es Salaam, Tanzania", "ar": "دار السلام، تنزانيا", "fr": "Dar es Salaam, Tanzanie"},
    "Mon-Fri: 8:00 AM - 6:00 PM": {"sw": "Jumatatu-Ijumaa: Saa 8:00 Asubuhi - 6:00 Jioni", "ar": "الإثنين-الجمعة: 8:00 صباحاً - 6:00 مساءً", "fr": "Lun-Ven: 8h00 - 18h00"},
    "Sat: 9:00 AM - 2:00 PM": {"sw": "Jumamosi: Saa 9:00 Asubuhi - 2:00 Mchana", "ar": "السبت: 9:00 صباحاً - 2:00 مساءً", "fr": "Sam: 9h00 - 14h00"},
    "Privacy Policy": {"sw": "Sera ya Faragha", "ar": "سياسة الخصوصية", "fr": "Politique de confidentialité"},
    "Terms of Service": {"sw": "Masharti ya Huduma", "ar": "شروط الخدمة", "fr": "Conditions d'utilisation"},
    "Employee Login": {"sw": "Kuingia kwa Wafanyakazi", "ar": "تسجيل دخول الموظفين", "fr": "Connexion employés"},
}

def update_po_file(lang_code, translations):
    """Update a single language's .po file"""
    po_file_path = BASE_DIR / 'locale' / lang_code / 'LC_MESSAGES' / 'django.po'
    
    if not po_file_path.exists():
        print(f"Warning: {po_file_path} does not exist!")
        return
    
    # Load the .po file
    po = polib.pofile(str(po_file_path))
    
    added_count = 0
    updated_count = 0
    
    # Process each string
    for english_text, translated_text in translations.items():
        # Check if entry already exists
        existing_entry = po.find(english_text)
        
        if existing_entry:
            # Update existing entry
            if existing_entry.msgstr != translated_text:
                existing_entry.msgstr = translated_text
                updated_count += 1
        else:
            # Add new entry
            entry = polib.POEntry(
                msgid=english_text,
                msgstr=translated_text,
            )
            po.append(entry)
            added_count += 1
    
    # Save the .po file
    po.save()
    
    # Compile to .mo file
    mo_file_path = po_file_path.parent / 'django.mo'
    po.save_as_mofile(str(mo_file_path))
    
    print(f"{lang_code.upper()}: Added {added_count} new entries, Updated {updated_count} existing entries")
    return added_count, updated_count

def main():
    """Main function to update all translation files"""
    print("=" * 60)
    print("UPDATING TRANSLATIONS WITH IMPROVED ACCURACY")
    print("=" * 60)
    
    # Process each language
    for lang_code in ['sw', 'ar', 'fr']:
        print(f"\nProcessing {lang_code.upper()} translations...")
        
        # Extract translations for this language
        lang_translations = {}
        for english_text, translations in NEW_STRINGS.items():
            if lang_code in translations:
                lang_translations[english_text] = translations[lang_code]
        
        # Update the .po file
        update_po_file(lang_code, lang_translations)
    
    print("\n" + "=" * 60)
    print("ALL TRANSLATIONS UPDATED AND COMPILED SUCCESSFULLY!")
    print("=" * 60)
    print("\nPlease restart your Django server for changes to take effect:")
    print("  python manage.py runserver")

if __name__ == "__main__":
    main()
