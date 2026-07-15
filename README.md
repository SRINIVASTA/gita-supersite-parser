# 🕉️ IIT Kanpur Git Supersite Data Pipeline & Analytics Studio

An enterprise-grade, serverless data extraction pipeline and research dashboard designed for parsing unstructured layout dumps from the IIT Kanpur Gita Supersite. This system transforms raw multilingual text layouts into schema-validated, indexable JSON documents and provides advanced NLP token splitting, interactive analytics, and server-side synchronized audio screen reading.

🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://gita-supersite-parser-fv3cznbz4rxhva9zuabmc2.streamlit.app/))

---

## 📂 Repository Architecture
The workspace uses a strictly organized, decoupled structure separating the processing engine from the web interface layer:

```text
├── app.py                # Main Streamlit web application dashboard (UI, Charts, TTS)
├── pipeline.py           # Backend core parsing engine & data validation layer
├── requirements.txt      # Cloud environment container dependencies
├── sample_dump.txt       # Embedded test dataset containing raw verse layouts
└── README.md             # Project documentation and manual guide
```

---

## 📊 How to Use the Embedded Test Dataset
The project includes an embedded `sample_dump.txt` file directly inside the repository tree for quick platform validation.

1. Locate the `sample_dump.txt` file in the file explorer list up above.
2. Click on the file name to open its content window.
3. Click the **"Raw"** button in the upper-right corner of the code frame to view the plain text.
4. Download the file to your computer or copy the text segments.
5. Launch your active Streamlit dashboard, pass the security portal, and drop the text into **📁 Local File Drag & Drop** to trigger the parsing algorithms instantly.
```

---

## ✨ Key Platform Features

1. **Serverless Data Ingestion (Option B)**: Supports local workspace `.txt` drag-and-drop file ingestion, running immediate regex compilers to bind multilingual scripts deterministically.
2. **Linguistic Morphological NLP Layer**: Includes a rule-based Sanskrit *Sandhi* compound splitting matrix engine that automatically identifies and decomposes heavy compound words into their base components.
3. **Advanced Interactive Studio Charts**: Replaces static layout renders with dynamic, hardware-accelerated **Plotly** data visualizers mapping absolute word metrics and text weight distribution metrics on the fly.
4. **CORS-Proof Backend Audio Synthesizer**: Utilizes a server-side **Google Text-to-Speech (gTTS)** streaming engine. This completely bypasses standard browser iframe sandbox mutes, ensuring 100% reliable audio playbacks for **Sanskrit (hi), Telugu (te), and English (en)** on all systems.
5. **Deterministic Visual Highlighting**: Syncs with user selection inputs to immediately highlight text layers on screen using professional design tints while triggering instant audio auto-play, completely bypassing asynchronous client lag conditions.
6. **Cross-Script Multi-Word Search Engine**: Supports global, case-insensitive keyword searches matching text across Sanskrit, Telugu, and English layouts simultaneously.
7. **Scholarly Security Authentication Gateway**: Restricts core data assets behind an entry passkey wall to establish protected editing environments.

---

## 🛠️ Step-by-Step Deployment Manual

### 1. Configure Repository Dependencies
Ensure your `requirements.txt` file is committed to your repository root containing exactly these lines:
```text
streamlit>=1.30.0
pandas
plotly
gTTS
```

### 2. Connect to Streamlit Cloud
1. Navigate directly to the **[Streamlit Community Cloud Dashboard](https://streamlit.io)**.
2. Authenticate securely using your **GitHub account link**.
3. Click the blue **"New App"** button at the top-right corner.
4. Select your specific repository name (`iitk-indic-data-pipeline`) and set the main file path to exactly `app.py`.
5. Click **"Deploy!"**. The container compilation process will configure and launch your app live within 1–2 minutes.

---

## 🔐 Secure Access Credentials
The core analytical dashboards and export interfaces remain locked behind a cryptographic gate. Use these credentials to sign in past the landing panel:

* **Username Identification ID**: `scholar`
* **Access Passkey Key**: `iitk2026`

---

## 📊 Sample Dump Format for Testing
To test the pipeline out of the box, create a local plain text file (e.g., `sample_dump.txt`), paste this raw block layout, and feed it into the ingestion zone:

```text
[CHAPTER: 01, VERSE: 01]
SANSKRIT: धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः। मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय॥
TELUGU: ధర్మక్షేత్రే కురుక్షేత్రే సమవేతా యుయుత్సవః। మామకాః పాండవాశ్చైవ కిమకుర్వత సంజయ॥
ENGLISH: O Sanjaya, what did my sons and the sons of Pandu do, when they gathered together at the holy field of Kurukshetra, eager for battle?

[CHAPTER: 02, VERSE: 47]
SANSKRIT: कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥
TELUGU: కర్మణ్యేవాధికారస్తే మా ఫలేషు కదాచన। మా కర్మఫలహేతుర్భూర్మా తే సంగోఽస్త్వకర్మణి॥
ENGLISH: You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions.
```

---

## 📜 Metadata License & Processing Framework
* **Data Processor & Maintainer**: Appala Srinivas Tanakala
* **Output Format Schema**: Schema-validated JSON Arrays & UTF-8-SIG Editable Spreadsheet CSV Layouts
## ✒️ Author and Credits

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### Connect with Me
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
