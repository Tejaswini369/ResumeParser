import streamlit as st
import os
import pickle
import re
import zipfile
from pdfminer.high_level import extract_text
import xgboost

# Function to unzip a file
def unzip_file(zip_path, extract_to):
    st.write(f"Unzipping {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        st.write(f"Unzipped to {extract_to}")
    except FileNotFoundError:
        st.error(f"File {zip_path} not found.")

# Function to load a model from a file
def load_model(file_path):
    st.write(f"Loading model from {file_path}")
    if not os.path.exists(file_path):
        st.error(f"File {file_path} does not exist.")
        return None
    try:
        with open(file_path, 'rb') as file:
            model = pickle.load(file)
            st.write(f"Successfully loaded {file_path}")
            return model
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

# Unzip the models
zip_file_path = 'models.zip'  # Ensure this file is in the root of your repository
unzip_dir = 'models'
if not os.path.exists(unzip_dir):
    unzip_file(zip_file_path, unzip_dir)

# Load all models
model_files = {
    'xgb_classifier_categorization': 'xgb_classifier_categorization.pkl',
    'tfidf_vectorizer_categorization': 'tfidf_vectorizer_categorization.pkl',
    'rf_classifier_job_recommendation': 'rf_classifier_job_recommendation.pkl',
    'tfidf_vectorizer_job_recommendation': 'tfidf_vectorizer_job_recommendation.pkl'
}

models = {}
for model_name, file_name in model_files.items():
    file_path = os.path.join(unzip_dir, file_name)
    models[model_name] = load_model(file_path)
    if models[model_name] is None:
        st.stop()

xgb_classifier_categorization = models['xgb_classifier_categorization']
tfidf_vectorizer_categorization = models['tfidf_vectorizer_categorization']
rf_classifier_job_recommendation = models['rf_classifier_job_recommendation']
tfidf_vectorizer_job_recommendation = models['tfidf_vectorizer_job_recommendation']

if xgb_classifier_categorization is None or tfidf_vectorizer_categorization is None or \
   rf_classifier_job_recommendation is None or tfidf_vectorizer_job_recommendation is None:
    st.error("One or more models could not be loaded. Please check the file paths and try again.")
    st.stop()

# Clean resume function
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

# Prediction and Category Name
def predict_category(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category = xgb_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category

# Prediction and Category Name
def job_recommendation(resume_text):
    resume_text= cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([resume_text])
    recommended_job = rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    return recommended_job

def pdf_to_text(file):
    reader = PdfReader(file)
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Extract information functions
def extract_contact_number_from_resume(text):
    contact_number = None
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number

def extract_email_from_resume(text):
    email = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

def extract_skills_from_resume(text):
    skills_list = [
        'Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL',
        'Tableau', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js',
        'Git', 'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization',
        'Matplotlib', 'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK',
        'Text Mining', 'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition',
        'Recommendation Systems', 'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning',
        'Neural Networks', 'Convolutional Neural Networks', 'Recurrent Neural Networks', 'Generative Adversarial Networks',
        'XGBoost', 'Random Forest', 'Decision Trees', 'Support Vector Machines', 'Linear Regression', 'Logistic Regression',
        'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN', 'Association Rule Learning', 'Apache Hadoop',
        'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL', 'Big Data Analytics',
        'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker',
        'Kubernetes', 'Linux', 'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls',
        'Encryption', 'Malware Analysis', 'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban',
        'Continuous Integration', 'Continuous Deployment', 'Software Development', 'Web Development', 'Mobile Development',
        'Backend Development', 'Frontend Development', 'Full-Stack Development', 'UI/UX Design', 'Responsive Design',
        'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite', 'Photoshop', 'Illustrator', 'InDesign', 'Figma',
        'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research', 'Customer Development', 'Lean Startup',
        'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing',
        'SEO', 'SEM', 'PPC', 'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)',
        'Salesforce', 'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting',
        'Ticketing Systems', 'ServiceNow', 'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium',
        'JUnit', 'Load Testing', 'Performance Testing', 'Regression Testing', 'Black Box Testing', 'White Box Testing',
        'API Testing', 'Mobile Testing', 'Usability Testing', 'Accessibility Testing', 'Cross-Browser Testing', 'Agile Testing',
        'User Acceptance Testing', 'Software Documentation', 'Technical Writing', 'Copywriting', 'Editing', 'Proofreading',
        'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento', 'Shopify', 'E-commerce', 'Payment Gateways',
        'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement', 'ERP Systems', 'SAP', 'Oracle', 'Microsoft Dynamics',
        'Tableau', 'Power BI', 'QlikView', 'Looker', 'Data Warehousing', 'ETL', 'Data Engineering', 'Data Governance',
        'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics', 'Descriptive Analytics',
        'Business Intelligence', 'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs',
        'GraphQL', 'SOAP', 'Microservices', 'Serverless Architecture', 'Lambda Functions', 'Event-Driven Architecture',
        'Message Queues', 'GraphQL', 'Socket.io', 'WebSockets', 'Ruby', 'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP',
        'Zend Framework', 'ASP.NET', 'C#', 'VB.NET', 'ASP.NET MVC', 'Entity Framework', 'Spring', 'Hibernate', 'Struts', 'Kotlin',
        'Swift', 'Objective-C', 'iOS Development', 'Android Development', 'Flutter', 'React Native', 'Ionic', 'Mobile UI/UX Design',
        'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI', 'Falcon', 'Tornado', 'WebSockets',
        'GraphQL', 'RESTful Web Services', 'SOAP', 'Microservices Architecture', 'Serverless Computing', 'AWS Lambda',
        'Google Cloud Functions', 'Azure Functions', 'Server Administration', 'System Administration', 'Network Administration',
        'Database Administration', 'MySQL', 'PostgreSQL', 'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'MongoDB',
        'Cassandra', 'Redis', 'Elasticsearch', 'Firebase', 'Google Analytics', 'Google Tag Manager', 'Adobe Analytics',
        'Marketing Automation', 'Customer Data Platforms', 'Segment', 'Salesforce Marketing Cloud', 'HubSpot CRM', 'Zapier',
        'IFTTT', 'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation', 'Natural Language Generation (NLG)',
        'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', '3D Modeling', 'Animation',
        'Motion Graphics', 'Game Design', 'Game Development', 'Level Design', 'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya',
        'Adobe After Effects', 'Adobe Premiere Pro', 'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production',
        'Digital Marketing', 'Content Strategy', 'Conversion Rate Optimization (CRO)', 'A/B Testing', 'Customer Experience (CX)',
        'User Experience (UX)', 'User Interface (UI)', 'Persona Development', 'User Journey Mapping', 'Information Architecture (IA)',
        'Wireframing', 'Prototyping', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)',
        'Localization (L10n)', 'Voice User Interface (VUI)', 'Chatbots', 'Natural Language Understanding (NLU)', 'Speech Synthesis',
        'Emotion Detection', 'Sentiment Analysis', 'Image Recognition', 'Object Detection', 'Facial Recognition', 'Gesture Recognition',
        'Document Recognition', 'Fraud Detection', 'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)',
        'Vulnerability Assessment', 'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)', 'Identity and Access Management (IAM)',
        'Single Sign-On (SSO)', 'Multi-Factor Authentication (MFA)', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)',
        'Smart Contracts', 'Web3', 'Non-Fungible Tokens (NFTs)', 'ROS', 'SLAM'
    ]
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

def extract_education_from_resume(text):
    education = []
    education_keywords = [
        'Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering', 'Mechanical Engineering',
        'Civil Engineering', 'Chemical Engineering', 'Biomedical Engineering', 'Aerospace Engineering', 'Nuclear Engineering',
        'Industrial Engineering', 'Systems Engineering', 'Environmental Engineering', 'Petroleum Engineering',
        'Geological Engineering', 'Marine Engineering', 'Robotics Engineering', 'Biotechnology', 'Biochemistry', 'Microbiology',
        'Genetics', 'Molecular Biology', 'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology',
        'Physiology', 'Anatomy', 'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration',
        'Nursing', 'Medicine', 'Dentistry', 'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography',
        'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Nutrition', 'Sports Science', 'Kinesiology',
        'Exercise Physiology', 'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work',
        'Sociology', 'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics',
        'Finance', 'Accounting', 'Business Administration', 'Management', 'Marketing', 'Entrepreneurship',
        'Hospitality Management', 'Tourism Management', 'Supply Chain Management', 'Logistics Management',
        'Operations Management', 'Human Resource Management', 'Organizational Behavior', 'Project Management',
        'Quality Management', 'Risk Management', 'Strategic Management', 'Public Administration', 'Urban Planning',
        'Architecture', 'Interior Design', 'Landscape Architecture', 'Fine Arts', 'Visual Arts', 'Graphic Design',
        'Fashion Design', 'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies',
        'Communication Studies', 'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics',
        'Translation Studies', 'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology',
        'Philosophy', 'Theology', 'Religious Studies', 'Ethics', 'Early Childhood Education', 'Elementary Education',
        'Secondary Education', 'Special Education', 'Higher Education', 'Adult Education', 'Distance Education',
        'Online Education', 'Instructional Design', 'Curriculum Development', 'Electronics and Communication Engineering',
        'Library Science', 'Information Science', 'Computer Engineering', 'Software Development', 'Cybersecurity',
        'Information Security', 'Network Engineering', 'Data Science', 'Data Analytics', 'Business Analytics',
        'Operations Research', 'Decision Sciences', 'Human-Computer Interaction', 'User Experience Design',
        'User Interface Design', 'Content Strategy', 'Brand Management', 'Public Relations',
        'Corporate Communications', 'Media Production', 'Digital Media', 'Web Development', 'Mobile App Development',
        'Game Development', 'Digital Forensics', 'Forensic Science', 'Criminalistics', 'Crime Scene Investigation', 'Emergency Management',
        'Fire Science', 'Environmental Science', 'Climate Science', 'Meteorology', 'Geography', 'Geomatics',
        'Remote Sensing', 'Geoinformatics', 'Cartography', 'GIS (Geographic Information Systems)',
        'Environmental Management', 'Sustainability Studies', 'Renewable Energy', 'Green Technology', 'Ecology',
        'Conservation Biology', 'Wildlife Biology', 'Zoology', 'Electronics and Communications Engineering'
    ]
    for keyword in education_keywords:
        pattern = r"\b{}\b".format(re.escape(keyword))
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            education.extend(matches)
    return education

def extract_name_from_resume(text):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name

# Extract text from PDF
def extract_text_from_pdf(file):
    return extract_text(file)

# Streamlit app




# Streamlit app
st.title("Resume Analysis App")

uploaded_file = st.file_uploader("Upload a resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        text = uploaded_file.read().decode('utf-8')
    else:
        st.error("Invalid file format. Please upload a PDF or TXT file.")
    
    text = clean_text(text)
    text_vectorized = tfidf_vectorizer_categorization.transform([text])
    
    predicted_category = xgb_classifier_categorization.predict(text_vectorized)[0]
    
    st.subheader("Predicted Category")
    st.write(predicted_category)
    
    st.subheader("Recommended Job")
    recommended_job = job_recommendation(text)
    st.write(recommended_job)

    st.subheader("Contact Information")
    phone = extract_contact_number_from_resume(text)
    email = extract_email_from_resume(text)
    st.write(f"Phone: {phone}")
    st.write(f"Email: {email}")

    st.subheader("Extracted Skills")
    extracted_skills = extract_skills_from_resume(text)
    st.write(", ".join(extracted_skills))

    st.subheader("Extracted Name")
    name = extract_name_from_resume(text)
    st.write(name)

    st.subheader("Extracted Education")
    extracted_education = extract_education_from_resume(text)
    st.write(", ".join(extracted_education))
