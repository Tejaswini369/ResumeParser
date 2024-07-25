# ResumeParser
Resume Parser and Job Recommendation System
1.	Developed a resume parser with a Flask-based API, enabling users to upload resumes and automatically extract key skills, provide job recommendations, and categorize job industries (finance, healthcare, IT) using a random forest model.
2. Developed a resume parser with a Streamlit based API, enabling users to upload resumes and automatically extract key skills, provide job recommendations, and categorize job industries (finance, healthcare, IT) using a XG Boost model.
3. Trained the system on a dataset of 25,000 resumes, achieving high accuracy of about 90% in skill extraction and job classification, enhancing job search efficiency for users.

This model can be improved by training on larger dataset. Currently trying to combine the power of LLMs to handle larger datasets and improve accuracy.


**Instructions to run **
1. Download the models (.pkl) files.
2. Run the app.py file from your python environment either with Flask
   or Run the streamlit_app.py to run the streamlit API.
3. You will get a link to your local host in case of Flask and will directly open in case of Streamlit.
4. Click on the link and upload any resume.



Go through the Skills Extraction file and add more skills to improve the accuracy as there is word matching between the input skills and the keywords in the resume.
