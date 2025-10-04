## Language Converter (CN/EN → JP + Romaji)
**Status:** 🚧 **In progress** (actively building; APIs and UI are evolving)

**Overview**
A lightweight web application that converts Chinese/English text (with special handling for Chinese names) into Japanese and provides Romaji pronunciation. Built with a focus on simplicity, speed, and reliable name conversion.

**Motivation**
For non-native speakers, converting personal names or specific terms into natural Japanese pronunciation can be challenging. This tool simplifies that process with one-click conversion, particularly focusing on Chinese name romanization and Japanese pronunciation.

**Key Features**
- Special Chinese name handling using custom pronunciation mapping
- Japanese text output with corresponding Romaji pronunciation
- Clean, responsive UI with dark mode support
- Dockerized for easy local development and deployment

**Tech Stack**
- **Frontend:** Next.js (TypeScript), React, Tailwind CSS
- **Backend:** FastAPI (Python)
- **Libraries:** romkan (Japanese text to Romaji conversion), deep_translator (general text translation)
- **DevOps:** Docker, docker-compose

**Project Structure**
```
language-converter/
├── frontend/             # Next.js frontend application
├── backend-fastapi/      # FastAPI backend service
│   └── app/
│       ├── main.py       # Main API routes and logic
│       └── name_mapping.py # Custom Chinese name to Japanese pronunciation mapping
└── docker-compose.yml    # Docker configuration for local development
```

**Implementation Details**
The application uses two main approaches for text conversion:

1. **Custom Mapping for Chinese Names:**
   - For 2-4 character Chinese names, it uses predefined mappings in `name_mapping.py` to convert directly to Japanese pronunciation
   - The mapping includes common Chinese surnames (`chinese_surname_map`) and given names (`chinese_given_name_map`)
   - After obtaining the Japanese pronunciation, it uses the romkan library to convert to Romaji

2. **General Text Translation:**
   - For other text inputs, it leverages `deep_translator` with Google Translator API
   - Latin-dominant text is passed through directly to preserve formatting

**How to Run the Project**

### Prerequisites
- Docker and docker-compose installed on your machine

### Starting the Application
1. Clone the repository (replace with your actual repo URL)
```bash
# Using HTTP
git clone https://github.com/your-username/language-converter.git
# Using SSH
git clone git@github.com:your-username/language-converter.git
cd language-converter
```

2. Start the application using docker-compose
```bash
docker-compose up --build
```

3. Access the application
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

### Stopping the Application
```bash
docker-compose down
```

**Current Implementation Approach**
The current system relies on a manually curated mapping file (`name_mapping.py`) for Chinese name translation. This approach provides deterministic and fast results for common Chinese names but has limitations in coverage for rare or less common names and characters.

**Future Enhancement: LLM Integration**
While the custom mapping works well for many cases, a potential future enhancement would be to integrate a Large Language Model (LLM) to handle the translation process. This would:
- Provide more comprehensive coverage of names and terms
- Handle contextual translations more effectively
- Adapt to different pronunciation styles and preferences
- Automatically learn and improve from user interactions
- Reduce the need for manual maintenance of mapping files

**Current Limitations and Future Improvements**

1. **Enhanced Mapping System:**
   - The current system relies on a manually curated mapping file, which has limitations in coverage
   - Future versions could integrate a large language model (LLM) to provide more comprehensive and contextually accurate translations

2. **Additional Features:**
   - Support for different Romaji styles (Hepburn, Kunrei-shiki, Nihon-shiki)
   - Batch processing and export functionality
   - User-customizable dictionaries and preferences
   - Expanded language support beyond Chinese and English

3. **Performance Optimizations:**
   - Caching of frequently requested translations
   - Integration with translation APIs for better coverage of non-name text

**Contributing**
Contributions are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.

