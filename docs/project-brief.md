# Mailchimp Marketing Trends Engine: Design & Development Prompt

## Project Overview

I need to design and build a working prototype of a Mailchimp Marketing Trends Engine that scans the web for real-time marketing trends, along with preparing a comprehensive 75-minute presentation that demonstrates both the system's capabilities and my technical expertise.

## Deliverables

1. **Working Prototype**
   - Real-time web crawler that identifies marketing trends across social media and forums
   - Data analysis engine that processes and categorizes trends
   - User-friendly dashboard with visualizations
   - API integration with Mailchimp services
   - Comprehensive documentation at each development stage

2. **75-Minute Presentation**
   - 5-minute personal introduction
   - 10-minute professional achievements showcase
   - 60-minute system design presentation with live demo

## Technical Requirements

### Data Collection System

- Design web crawlers for Twitter, Reddit, LinkedIn, Instagram, and marketing forums
- Implement rate limiting and respect robots.txt
- Create data extraction patterns for different content types
- Develop scheduling system for continuous crawling

### Data Processing Pipeline

- Design real-time data processing using stream processing
- Implement NLP for topic extraction and sentiment analysis
- Create trend identification algorithms based on:
  - Mention frequency
  - Growth rate
  - User engagement metrics
  - Cross-platform correlation

### Storage Architecture

- Design schema for raw data collection
- Create optimized data warehouse for trend analysis
- Implement caching layer for dashboard performance

### AI Components

- Topic modeling using transformer-based NLP
- Anomaly detection for emerging trends
- Predictive analytics for trend forecasting
- Content recommendation engine for Mailchimp users

### User Interface

- Interactive dashboard with filterable trend categories
- Time-series visualizations of trend evolution
- Integration points with Mailchimp campaign creation
- API documentation for third-party developers

## Non-Functional Requirements

- Near real-time updates (< 5 minute delay)
- Scalable architecture to handle traffic spikes
- High availability (99.9%)
- Data privacy compliance
- Cost-efficient cloud resource utilization

## Presentation Structure

1. **Introduction (5 min)**
   - Career journey highlighting relevant experience
   - Personal motivation for this project

2. **Professional Achievements (10 min)**
   - Previous work with data processing systems
   - Experience with AI/ML implementations
   - Relevant marketing technology projects

3. **System Design (60 min)**
   - Assumptions and constraints (2 min)
   - Functional and non-functional requirements (5 min)
   - Entity model and data flow (5 min)
   - System architecture with diagrams (5 min)
   - AI components deep-dive (10 min)
   - **Live Demo** (15 min)
     - Show real-time trend discovery
     - Demonstrate dashboard functionality
     - Showcase Mailchimp integration
   - Scalability and performance considerations (5 min)
   - Implementation challenges and solutions (5 min)
   - Future enhancements (3 min)
   - Q&A (5 min)

## Development Timeline

- Day 1: Architecture design, data source identification, initial crawler setup
- Day 2: Data processing pipeline, storage implementation, basic trend analysis
- Day 3: Dashboard development, AI model integration, Mailchimp API connection
- Day 4: Testing, documentation, presentation preparation

## Evaluation Criteria Alignment

- **Programming Fundamentals**: Demonstrate clean code, proper error handling, and efficient algorithms
- **Product Engineering + AI**: Showcase AI implementation details, data science approach, and user-centric design
- **Tech Adaptability**: Highlight cross-platform integration, technology tradeoffs, and scalability decisions

## Resources Needed

- Cloud platform (AWS/GCP/Azure)
- NLP libraries (spaCy, Hugging Face Transformers)
- Stream processing framework (Kafka/Kinesis)
- Visualization libraries (D3.js, Chart.js)
- Database solutions (PostgreSQL, Redis, Elasticsearch)
- API development framework (FastAPI/Flask)

Please help me refine this design and suggest implementation approaches that would be most impressive for the interview while remaining practical to build within 3-4 days.
