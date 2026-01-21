# AI Teaching Team - Complete Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Active internet connection

## Step 1: Install Dependencies

```bash
pip install streamlit==1.41.1
pip install openai==1.58.1
pip install duckduckgo-search==6.4.1
pip install typing-extensions>=4.5.0
pip install agno>=2.2.10
pip install composio-phidata==0.6.9
pip install composio_core
pip install composio==0.1.1
pip install google-search-results==2.4.2
```

Or install from requirements file:
```bash
pip install -r scripts/requirements.txt
```

## Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (format: sk-...)

## Step 3: Setup Composio and Google Docs

### 3a. Create Composio Account

1. Go to [Composio Platform](https://composio.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Copy your API key

### 3b. Authenticate Google Docs

**Method 1: Command Line (Recommended)**
```bash
# Install Composio CLI
pip install composio-core

# Add Google Docs integration
composio add googledocs

# Follow the authentication flow:
# - Select OAUTH2
# - Choose your Google account
# - Grant permissions
```

**Method 2: Web Dashboard**
1. Go to [Composio Apps](https://app.composio.dev/app/googledocs)
2. Click "Create Integration" (violet button)
3. Select your Google account
4. Complete OAuth authentication

## Step 4: Get SerpAPI Key

1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for an account
3. Navigate to API Keys section
4. Copy your API key

## Step 5: Run the Application

```bash
# Navigate to skill directory
cd /Users/colin/.claude/skills/ai-teaching-team

# Start Streamlit app
streamlit run scripts/run_teaching_team.py
```

The application will open in your browser at `http://localhost:8501`

## Step 6: Configure API Keys in App

1. Enter OpenAI API Key in sidebar
2. Enter Composio API Key in sidebar
3. Enter SerpAPI Key in sidebar
4. Enter a topic (e.g., "Machine Learning", "Python Programming")
5. Click "Start" to generate learning materials

## Troubleshooting

### Google Docs Connection Issues

**Error: "Error initializing ComposioToolSet"**
- Verify Composio API key is correct
- Ensure `composio add googledocs` was run successfully
- Check OAuth authentication is active

**Error: "Failed to create document"**
- Re-authenticate Google Docs: `composio add googledocs`
- Check Google account permissions
- Verify Composio connection is active in dashboard

### OpenAI API Issues

**Error: "Incorrect API key provided"**
- Verify API key format (should start with sk-)
- Check for extra spaces when pasting
- Ensure key has active credits

**Error: "Rate limit exceeded"**
- Check OpenAI account has available credits
- Wait a few minutes before retrying
- Consider upgrading to paid tier

### SerpAPI Issues

**Error: "Invalid API key"**
- Verify SerpAPI key is correct
- Check account has search credits remaining
- Ensure key is active (not expired)

### General Issues

**Application won't start**
- Verify all dependencies installed: `pip list | grep -E "streamlit|openai|agno|composio"`
- Check Python version: `python --version` (must be 3.8+)
- Try clearing Streamlit cache: `streamlit cache clear`

**Agents not responding**
- Check terminal for error messages
- Verify all API keys are entered
- Ensure stable internet connection
- Try a simpler topic first

## Environment Variables (Optional)

Instead of entering keys in the UI, set as environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export COMPOSIO_API_KEY="..."
export SERPAPI_API_KEY="..."
```

Then modify `scripts/run_teaching_team.py` to read from environment.
