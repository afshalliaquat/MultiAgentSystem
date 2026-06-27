# MultiAgent Research Pipeline

## 📋 Project Overview

The **MultiAgent Research Pipeline** is an intelligent, multi-stage system that automates professional research report generation. It combines multiple AI agents with LLM capabilities to search the web, extract relevant content, synthesize findings into comprehensive reports, and provide critical feedback—all orchestrated through a clean, modern web interface.

The system leverages **LangChain**, **Mistral AI**, and specialized web tools to deliver structured, fact-checked research outputs on any given topic.

---

## 🎯 Key Features

### 1. **Multi-Agent Architecture**
- **Search Agent**: Conducts web searches using Tavily API to gather recent, reliable information
- **Reader Agent**: Scrapes and extracts relevant content from URLs using BeautifulSoup
- **Writer Chain**: Generates detailed, professionally structured research reports with citations
- **Critic Chain**: Evaluates reports with scores (0-10) and constructive feedback

### 2. **Intelligent Processing Pipeline**
- Modular design with clear separation of concerns
- Sequential workflow: Search → Scrape → Write → Review
- Context-aware chaining of LLM calls for coherent output

### 3. **Web-Based User Interface**
- Clean, modern HTML/CSS frontend
- Real-time display of:
  - Search summaries
  - Extracted URLs with source links
  - Scraped content previews
  - Generated research reports
  - Critic feedback and scores
- Form-based topic input with error handling

### 4. **Robust Error Handling**
- Request timeout management
- Network error handling
- Graceful fallbacks for missing data
- User-friendly error messages

---

## 🏗️ Project Structure

```
MultiAgentSystem/
│
├── agents.py              # LangChain agent definitions and LLM chains
├── pipeline.py            # Core research execution pipeline
├── tools.py               # Web search and web scraper tools
├── ui_server.py           # HTTP server and web interface handler
├── requirement.txt        # Python package dependencies
│
├── templates/
│   └── index.html         # HTML template for web UI
│
└── static/
    └── style.css          # CSS styling for the web interface
```

---

## 🔧 Technical Architecture

### **Core Components**

#### **agents.py**
Defines the AI agents and chains:
- **Search Agent**: Uses `create_agent()` with web_search tool
- **Reader Agent**: Uses `create_agent()` with web_scraper tool
- **Writer Chain**: Prompts the LLM to structure research findings into:
  - Introduction
  - Key Findings (minimum 3 points)
  - Conclusion
  - Sources list
- **Critic Chain**: Evaluates reports with:
  - Numerical score (0-10)
  - Strengths analysis
  - Areas for improvement
  - One-line verdict

**LLM Used**: Mistral Small 2506 (via LangChain integration)

#### **tools.py**
Custom tools for agent interaction:
- **`web_search(query)`**: Searches using Tavily API, returns top 5 results with titles, URLs, and snippets
- **`web_scraper(url)`**: Fetches webpage content, cleans HTML (removes scripts, styles, nav, footer), returns up to 3000 characters of text

#### **pipeline.py**
Orchestrates the complete workflow:
1. **Step 1 - Search**: Initializes search agent with topic query
2. **Step 2 - Read**: Passes top 3 extracted URLs to reader agent
3. **Step 3 - Write**: Combines search results and scraped content into a research report
4. **Step 4 - Review**: Critic chain evaluates the generated report

Helper functions:
- `extract_urls_from_messages()`: Extracts URLs from agent message history using regex
- `content_to_string()`: Converts various content types to plain strings
- `research_pipeline(topic)`: Main orchestration function that returns a state dictionary

#### **ui_server.py**
HTTP server providing web interface:
- **GET `/`**: Renders main page with form
- **GET `/style.css`**: Serves CSS stylesheet
- **POST `/`**: Processes research topic submission and displays results
- `render_page()`: Builds HTML with dynamic content insertion
- `ResearchUIHandler`: HTTP request handler managing requests

---

## 📦 Dependencies

### Core LLM & Framework
- `langchain` (≥0.2.0)
- `langchain-core` (≥0.2.0)
- `langchain-community` (≥0.2.0)
- `langchain-mistralai`: Mistral AI integration
- `langchain-huggingface`: Hugging Face model support

### Web Search & Scraping
- `tavily-python` (≥0.3.0): Web search API
- `beautifulsoup4` (≥4.12.0): HTML parsing
- `requests` (≥2.31.0): HTTP requests
- `lxml` (≥5.0.0): XML/HTML processing

### Utilities & Infrastructure
- `python-dotenv` (≥1.0.0): Environment variable management
- `transformers` & `sentence-transformers`: NLP processing
- `aiohttp` (≥3.9.0): Async HTTP support
- `pandas` (≥2.0.0): Data manipulation
- `tiktoken` (≥0.6.0): Token counting
- `rich` (≥13.7.0): Pretty console output
- `tenacity` (≥8.2.0): Retry logic
- `pydantic` (≥2.5.0): Data validation
- `orjson` (≥3.9.0): JSON serialization
- `html5lib` (≥1.1): HTML parsing

---

## 🚀 Usage Guide

### **Prerequisites**
1. Python 3.8+ installed
2. Virtual environment set up
3. API keys configured:
   - `MISTRAL_API_KEY`: Mistral AI API key
   - `TAVILY_API_KEY`: Tavily search API key

### **Installation**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirement.txt

# Create .env file with API keys
echo MISTRAL_API_KEY=your_key >> .env
echo TAVILY_API_KEY=your_key >> .env
```

### **Running the Application**

#### **Option 1: CLI (Terminal)**
```bash
python pipeline.py
# Enter a research topic when prompted
```

#### **Option 2: Web UI**
```bash
python ui_server.py
# Browser opens automatically at http://127.0.0.1:8000
```

### **Example Workflow**

**Input Topic**: "Artificial Intelligence in Healthcare 2024"

**Output Generated**:
1. **Search Summary**: Latest web sources on AI in healthcare
2. **URLs**: List of authoritative sources (with clickable links)
3. **Scraped Content**: Extracted key information from top sources
4. **Research Report**: Professionally formatted report with:
   - Introduction to AI in healthcare
   - 3+ key findings with detailed explanations
   - Conclusion synthesizing the research
   - Complete source citations
5. **Critic Feedback**: 
   - Score (e.g., "8.5/10")
   - Strengths identified
   - Improvement areas
   - Final verdict

---

## 🔄 Data Flow

```
User Input (Topic)
    ↓
[Search Agent] → Web Search API (Tavily) → Search Results + URLs
    ↓
[Reader Agent] → Web Scraper (BeautifulSoup) → Extracted Content
    ↓
[Writer Chain] → LLM (Mistral) → Structured Research Report
    ↓
[Critic Chain] → LLM (Mistral) → Evaluation + Feedback
    ↓
Web UI / Console Output
```

---

## 🎨 User Interface

The web interface features:

- **Hero Section**: 
  - Project title and tagline
  - Current topic metadata
  - Form input for research topic submission

- **Results Section** (displayed after submission):
  - **Critic Score Card**: Displays review score prominently
  - **Search Summary**: Raw findings from web search
  - **Extracted URLs**: Clickable links to sources
  - **Scraped Content**: Cleaned webpage text
  - **Full Report**: Complete research document
  - **Critic Feedback**: Detailed review with strengths/improvements

- **Styling**:
  - Modern CSS with glassmorphism effects
  - Responsive grid layout
  - Professional color scheme (teal/green accents)
  - Clean typography with "Segoe UI" font stack

---

## ⚙️ Configuration

### **Environment Variables** (.env file)
```
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### **LLM Settings** (agents.py)
- Model: `mistral-small-2506`
- Temperature: `0` (deterministic, factual responses)

### **Server Settings** (ui_server.py)
- Default Host: `127.0.0.1` (localhost)
- Default Port: `8000`
- Auto-browser opening: Enabled

### **Tool Settings** (tools.py)
- Web Search: Top 5 results
- Web Scraper: 
  - Request timeout: 8 seconds
  - Character limit: 3000 characters
  - Removes: scripts, styles, nav, footer tags

---

## 🔒 Error Handling

The system includes robust error handling:

- **Network Errors**: Caught and reported with descriptive messages
- **Missing Data**: Graceful fallbacks ("No data available")
- **Timeout**: 8-second timeout on web requests
- **Invalid Input**: Form validation and user feedback
- **API Failures**: Exception handling with user notification

---

## 🎓 Use Cases

1. **Market Research**: Analyze industry trends and competitive landscape
2. **Academic Writing**: Gather citations and structure research findings
3. **News Aggregation**: Summarize recent news on specific topics
4. **Competitive Analysis**: Research competitor products and strategies
5. **Content Creation**: Generate research-backed articles or blog posts
6. **Due Diligence**: Investigate topics before investment decisions

---

## 🚧 Future Enhancements

- [ ] Multi-language support for research topics
- [ ] Custom report templates
- [ ] Export to PDF/DOCX formats
- [ ] Research history and saved reports
- [ ] Advanced filtering of search results
- [ ] Integration with more LLM providers
- [ ] Citation format options (APA, MLA, Chicago)
- [ ] Collaborative editing and review workflows
- [ ] Database storage for reports
- [ ] API endpoint for programmatic access

---

## 📝 Notes

- The pipeline executes sequentially, with each step dependent on previous results
- Mistral AI's zero-temperature setting ensures consistent, factual output
- Tavily API is preferred for search quality and recent information
- The web UI automatically extracts and displays URLs for easy reference
- All external content is sanitized and escaped for security

---

## 🤝 Contributing

This project demonstrates:
- Multi-agent LLM orchestration patterns
- LangChain integration with custom tools
- Web scraping and content extraction
- HTTP server implementation in Python
- Modern UI/UX design principles
- Robust error handling in distributed systems
