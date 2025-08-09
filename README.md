# 🤖 MIRA Chatbot Persona Tester

This project implements an AI chatbot solution designed to reduce the burden on caregivers supporting people with mild cognitive dementia (PWD), while also enhancing the lifestyle of those living with dementia. The core of this application is an A/B test to evaluate the impact of the chatbot's tone on user trust and engagement.

The application allows users to interact with two distinct chatbot personas:
* **Warm & Empathetic**: A supportive assistant that provides emotional recognition and reassuring advice.
* **Clinical & Direct**: An objective assistant that focuses on factual information and clear, concise instructions.

By running this application, we can gather data on which tone is more effective for building user trust and encouraging continued usage, ultimately aiming to provide a more effective tool for caregivers.

---

## Getting Started

This guide will walk you through setting up and running the Streamlit application for local testing.

### **Prerequisites**
1.  Python 3.10 or higher
2.  Git

### **Setup and Run**

1.  **Clone the Repository:**
    * Open a terminal and clone this repository to your local machine.
        ```bash
        git clone [https://github.com/felix21g/mira-webtesting.git](https://github.com/felix21g/mira-webtesting.git)
        ```
    * Navigate into the project directory.
        ```bash
        cd mira-webtesting
        ```

2.  **Set up the Virtual Environment and Install Dependencies:**
    * Create and activate a virtual environment.
        ```bash
        python -m venv venv
        # On Windows: .\venv\Scripts\activate
        # On macOS/Linux: source venv/bin/activate
        ```
    * Install all necessary dependencies from the `requirements.txt` file.
        ```bash
        pip install -r requirements.txt
        ```

3.  **Configure API Keys:**
    * Create a folder named `.streamlit` in your project's root directory.
    * Inside the `.streamlit` folder, create a file named `secrets.toml`.
    * Add your OpenAI API key to the `secrets.toml` file.
        ```toml
        # .streamlit/secrets.toml
        OPENAI_API_KEY="your-secret-api-key-here"
        ```

4.  **Run the Streamlit App:**
    * With your virtual environment activated, run the following command from the project root:
        ```bash
        streamlit run streamlit_app.py
        ```
    * This will open the web application in your browser, allowing you to begin testing the two chatbot personas.

---

## Key Components and Technologies

* **Framework**: The application is built using **Streamlit** for rapid development of the web-based user interface.
* **Chatbot Logic**: The core chatbot functionality is powered by the **OpenAI API (GPT-3.5 Turbo)**.
* **Chatbot Personas**: The chatbot's behavior is guided by two distinct system prompts, creating a **Warm & Empathetic** persona and a **Clinical & Direct** persona for A/B testing.
* **Database**: Chat history and other user data are stored in **Firebase Firestore**.
* **LLM Model Reference**: The project is inspired by the capabilities of fine-tuned models like `rohitashva/dementia-chatbot-llm-model` for dementia-specific conversations.

---

## Further Reading

* **Streamlit Documentation**: For a comprehensive guide on building and deploying Streamlit applications.
* **OpenAI API Documentation**: For details on using the Chat Completions API and managing API keys.
* **Firebase Firestore Documentation**: For information on how the database is structured and accessed in the project.
* **Dementia Singapore**: A key local resource for caregivers in Singapore, providing support and information.
* **Agency for Integrated Care (AIC)**: A source for information on government schemes and support for caregivers in Singapore.
* **Caregivers Alliance Limited (CAL)**: An organization offering training and support groups for caregivers of people with dementia in Singapore.