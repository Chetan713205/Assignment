# **Multilingual Property Data Extraction Report**

---

## **📌 Introduction**
This report outlines the process of converting a multilingual property dataset into a structured format by extracting key attributes from property descriptions. The goal was to extract the **Project Name** (mandatory) and various area details (if available) from property descriptions written in multiple languages (including Marathi and Kannada). The entire process was implemented using **open-source tools and libraries**, ensuring cost-effectiveness and reproducibility.

---

## **🛠 Tools & Technologies Used**
- **Python** (Primary programming language)
- **Pandas** (Data manipulation)
- **LangChain-Groq** (LLM API for translation & extraction)
- **Llama3-8b-8192** (Open-source LLM for text processing)
- **Regex & JSON** (Data parsing)
- **Caching & Retry Mechanisms** (Handling rate limits)
- **CSV/Excel/JSON** (Data storage formats)

🔹 **All tools used were open-source, with no paid subscriptions or proprietary software.**

---

## **📂 Input Data**
The dataset provided was an Excel file (`Multilingual_Analyst_Assignment.xlsx`) containing property descriptions in multiple languages (Marathi, Kannada, etc.). The key column was:
- **Column A: "Property Description"** (Textual descriptions of properties in different languages).

---

## **🚀 Step-by-Step Process**

### **1️⃣ Step 1: Translation of Multilingual Text to English**
Since the property descriptions were in multiple languages, the first task was to **translate them into English** for consistent processing.

#### **🔧 Implementation (`app2.py`)**  
- Used **LangChain-Groq** with **Llama3-8b-8192** for translation.
- Implemented **caching** to avoid reprocessing the same text.
- Applied **exponential backoff** to handle API rate limits.
- Output: **`Multilingual_Analyst_Assignment_translated.xlsx`** (All text translated to English).

---

### **2️⃣ Step 2: Extracting Structured Data from Property Descriptions**
After translation, the next step was to **extract structured attributes** (Project Name, Carpet Area, etc.) from the descriptions.

#### **🔧 Implementation (`app3.py`)**  
- Used **LangChain-Groq** with **Llama3-8b-8192** for structured extraction.
- Designed a **custom prompt** to enforce JSON output format.
- Implemented **retry logic** (exponential backoff) to handle API failures.
- Processed data in **batches** to avoid rate limits.
- Output: **`extracted_properties.json`** (Structured JSON with extracted fields).

---

### **3️⃣ Step 3: Converting JSON to Structured CSV**
The final step was to convert the extracted JSON into a clean, structured CSV file.

#### **🔧 Implementation (`json_to_csv.py`)**  
- Loaded JSON data and filtered out invalid/error entries.
- Used **Pandas’ `json_normalize`** to flatten nested JSON.
- Saved the structured output as: **`final_df.csv`**.

---

## **📊 Output Data Structure**
The final CSV (`final_df.csv`) contains the output data. 

---

## **🔍 Challenges & Solutions**
| **Challenge** | **Solution** |
|--------------|-------------|
| **Multilingual Text** | Used LLM-based translation to English. |
| **API Rate Limits** | Implemented exponential backoff & batch processing. |
| **Inconsistent Data Format** | Used strict JSON parsing with regex fallback. |
| **Error Handling** | Logged errors & skipped invalid entries. |

---

## **🚀 Future Enhancements**
To improve accuracy and efficiency, we can explore:
1. **Fine-tuning Open-Source LLMs**  
   - Use **LoRA (Low-Rank Adaptation)** or **QLoRA (Quantized LoRA)** to fine-tune models on **Marathi & Kannada** property data.
   - Benefits: Better extraction accuracy, reduced API dependency.
2. **Rule-Based Post-Processing**  
   - Add regex-based validation for area units (sq ft, sq m).
3. **Deployment as a Web Service**  
   - Use **FastAPI** to create an automated extraction pipeline.

---

## **🎯 Conclusion**
This project successfully transformed **multilingual, unstructured property descriptions** into a **structured CSV** with key attributes extracted. The entire workflow was built using **open-source tools**, ensuring accessibility and scalability. Future improvements could involve **fine-tuning models** for better multilingual support and deploying the solution as an automated service.

### **✨ Key Takeaways**
✔ **100% Open-Source** (No paid tools used)  
✔ **Scalable Batch Processing** (Handles large datasets efficiently)  
✔ **Flexible for Future Improvements** (Supports fine-tuning & rule-based enhancements)  

---

### **📌 Final Output Files**
1. **`Multilingual_Analyst_Assignment_translated.xlsx`** (Translated descriptions)  
2. **`extracted_properties.json`** (Raw extracted JSON)  
3. **`final_df.csv`** (Final structured output)  

---

**🔹 End of Report 🔹**  
*Thank you for reviewing! Let me know if further enhancements are needed.* 🚀
