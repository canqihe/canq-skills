---
name: ai-teaching-team
description: "Educational system that uses 4 specialized AI agents (Professor, Academic Advisor, Research Librarian, Teaching Assistant) to generate comprehensive learning materials for any topic. Use when users request creating learning plans, generating educational content and exercises, designing learning roadmaps, building structured educational experiences, or developing complete course materials with knowledge bases and resources."
---

# AI Teaching Agent Team

## Overview

Transform any topic into a comprehensive learning experience using a team of 4 specialized AI agents that collaborate to create professional-grade educational materials. Each agent creates detailed Google Docs covering different aspects of learning: knowledge foundation, structured roadmap, curated resources, and practice exercises.

## When to Use This Skill

Use this skill when users ask for:
- "Create a learning plan for [topic]"
- "Teach me about [subject]"
- "Generate course materials for [topic]"
- "I want to learn [programming language/technology/concept]"
- "Design a curriculum for [subject]"
- "Make educational resources about [topic]"

## Setup Requirements

Before running, users must configure:

1. **OpenAI API Key** - Required for GPT-4o-mini model access
2. **Composio API Key** - Required for Google Docs integration
   - Users must also run: `composio add googledocs` and authenticate via OAuth
3. **SerpAPI Key** - Required for web search functionality

## The Teaching Agents

### 🧠 Professor Agent (Knowledge Builder)
- Creates comprehensive knowledge base documents
- Explains topics from first principles
- Covers fundamental concepts, advanced topics, and current developments
- Output: Detailed Google Doc with proper formatting, headings, and examples

### 🗺️ Academic Advisor Agent (Roadmap Architect)
- Designs structured learning paths
- Breaks topics into logical subtopics with progression order
- Includes time estimates and prerequisites
- Output: Visual roadmap document with clear milestone markers

### 📚 Research Librarian Agent (Resource Curator)
- Searches for high-quality learning materials using SerpAPI
- Compiles technical blogs, GitHub repos, documentation, tutorials, courses
- Provides descriptions and quality assessments
- Output: Categorized resource list with difficulty ratings

### ✍️ Teaching Assistant Agent (Practice Designer)
- Creates progressive exercises, quizzes, and hands-on projects
- Develops real-world application scenarios
- Provides detailed solutions and explanations
- Output: Complete practice workbook with answer keys

## Usage

### Quick Start

```bash
# Navigate to the skill directory
cd /Users/colin/.claude/skills/ai-teaching-team

# Run the teaching team application
streamlit run scripts/run_teaching_team.py
```

### Workflow

1. Launch the Streamlit application
2. Enter API keys in the sidebar (or set as environment variables)
3. Input the topic to learn about
4. Click "Start" to generate learning materials
5. Wait for all 4 agents to complete their tasks
6. Access the 4 Google Docs created for each agent's output
7. View agent responses in the Streamlit interface

### Agent Execution Order

Agents run sequentially in this order:
1. Professor (knowledge base)
2. Academic Advisor (learning roadmap)
3. Research Librarian (resource curation)
4. Teaching Assistant (practice materials)

Each agent creates its own Google Doc with formatted content.

## Technical Architecture

**Dependencies:**
- `streamlit==1.41.1` - Web UI
- `openai==1.58.1` - OpenAI API client
- `agno>=2.2.10` - Agent framework
- `composio-phidata==0.6.9` - Google Docs integration
- `google-search-results==2.4.2` - SerpAPI client

**Agent Configuration:**
- Model: GPT-4o-mini (cost-effective, fast)
- Tools: Google Docs (create/update), SerpApi (web search)
- Format: Markdown output with structured documents
- Debug Mode: Enabled for detailed logging

## Output Structure

Each agent generates:
1. **Streamlit Response** - Markdown content displayed in the UI
2. **Google Doc Link** - Direct link to the created document
3. **Debug Logs** - Terminal output with execution details

Google Docs are created with:
- Professional formatting
- Clear headings and sections
- Structured content organization
- Table of contents (for longer documents)

## Customization

To modify agent behavior, edit the agent configurations in `scripts/run_teaching_team.py`:

- Change `instructions` to adjust agent tasks
- Modify `tools` to add/remove integrations
- Update `model` parameter to use different OpenAI models
- Adjust agent `role` and `name` as needed

## Troubleshooting

**Google Docs Integration Issues:**
- Ensure `composio add googledocs` has been run
- Verify OAuth authentication completed successfully
- Check Composio connection ID is properly configured

**API Key Errors:**
- Verify all three API keys are entered correctly
- Check API keys have necessary permissions
- Ensure API accounts have active credits/quotas

**Agent Response Issues:**
- Enable debug mode to see detailed logs
- Check terminal output for error messages
- Verify topic input is clear and specific
