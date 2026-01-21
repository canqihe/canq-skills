# Agent Implementation

This file provides Python implementation patterns for the movie production agents using the agno framework.

## Prerequisites

```bash
pip install agno anthropic google-generativeai serpapi
```

## Basic Implementation Pattern

### Using Claude (Recommended)

```python
from agno.agent import Agent
from agno.team import Team
from anthropic import Anthropic

# Initialize Claude client
client = Anthropic(api_key="your-anthropic-api-key")

# ScriptWriter Agent
script_writer = Agent(
    name="ScriptWriter",
    model=client,
    description="Expert screenplay writer. Given a movie idea and genre, develop a compelling script outline.",
    instructions=[
        "Write a script outline with 3-5 main characters and key plot points.",
        "Outline the three-act structure and suggest 2-3 twists.",
        "Ensure the script aligns with the specified genre and target audience.",
    ],
)

# CastingDirector Agent (with built-in search)
casting_director = Agent(
    name="CastingDirector",
    model=client,
    description="Talented casting director. Given a script outline and character descriptions, suggest suitable actors.",
    instructions=[
        "Suggest 2-3 actors for each main role.",
        "Use web search to verify actor availability.",
        "Provide a brief explanation for each casting suggestion.",
        "Consider diversity and representation in your casting choices.",
    ],
    # Claude has built-in web search capability
    tools=[WebSearchTool()],  # Hypothetical tool
)

# MovieProducer Team
movie_producer = Team(
    name="MovieProducer",
    model=client,
    members=[script_writer, casting_director],
    description="Experienced movie producer overseeing script and casting.",
    instructions=[
        "Ask ScriptWriter for a script outline based on the movie idea.",
        "Pass the outline to CastingDirector for casting suggestions.",
        "Summarize the script outline and casting suggestions.",
        "Provide a concise movie concept overview.",
    ],
    markdown=True,
)

# Usage
response = movie_producer.run(
    "Movie idea: A retired astronaut discovers aliens are invading Earth, "
    "but only his grandchildren believe him. Genre: Sci-Fi Thriller. "
    "Target audience: Adults. Runtime: 120 minutes"
)

print(response.content)
```

### Using Gemini with SerpAPI

```python
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.serpapi import SerpApiTools

# Configuration
google_api_key = "your-google-api-key"
serp_api_key = "your-serpapi-key"

# ScriptWriter Agent
script_writer = Agent(
    name="ScriptWriter",
    model=Gemini(id="gemini-2.5-flash", api_key=google_api_key),
    description="Expert screenplay writer. Given a movie idea and genre, develop a compelling script outline.",
    instructions=[
        "Write a script outline with 3-5 main characters and key plot points.",
        "Outline the three-act structure and suggest 2-3 twists.",
        "Ensure the script aligns with the specified genre and target audience.",
    ],
)

# CastingDirector Agent (with SerpAPI)
casting_director = Agent(
    name="CastingDirector",
    model=Gemini(id="gemini-2.5-flash", api_key=google_api_key),
    description="Talented casting director. Given a script outline and character descriptions, suggest suitable actors.",
    instructions=[
        "Suggest 2-3 actors for each main role.",
        "Check actors' current status using `search_google`.",
        "Provide a brief explanation for each casting suggestion.",
        "Consider diversity and representation in your casting choices.",
    ],
    tools=[SerpApiTools(api_key=serp_api_key)],
)

# MovieProducer Team
movie_producer = Team(
    name="MovieProducer",
    model=Gemini(id="gemini-2.5-flash", api_key=google_api_key),
    members=[script_writer, casting_director],
    description="Experienced movie producer overseeing script and casting.",
    instructions=[
        "Ask ScriptWriter for a script outline based on the movie idea.",
        "Pass the outline to CastingDirector for casting suggestions.",
        "Summarize the script outline and casting suggestions.",
        "Provide a concise movie concept overview.",
    ],
    markdown=True,
)

# Usage
response = movie_producer.run(
    "Movie idea: A retired astronaut discovers aliens are invading Earth, "
    "but only his grandchildren believe him. Genre: Sci-Fi Thriller. "
    "Target audience: Adults. Runtime: 120 minutes"
)

print(response.content)
```

## Streaming Implementation

For interactive development with real-time feedback:

```python
# Stream the response
response = movie_producer.run(
    "Movie idea: A heist during the Oscars ceremony",
    stream=True
)

for chunk in response:
    if hasattr(chunk, 'content'):
        print(chunk.content, end='', flush=True)
```

## Step-by-Step Implementation

For more granular control, run agents sequentially:

```python
# Step 1: Generate script outline
script_outline = script_writer.run(
    "Create a script outline for: A heist during the Oscars ceremony. "
    "Genre: Action-Comedy. Target audience: General. Runtime: 110 minutes."
)

print("=== SCRIPT OUTLINE ===")
print(script_outline.content)

# Step 2: Generate casting suggestions
casting_suggestions = casting_director.run(
    f"Based on this script outline:\n{script_outline.content}\n\n"
    "Suggest actors for all main roles."
)

print("\n=== CASTING SUGGESTIONS ===")
print(casting_suggestions.content)

# Step 3: Compile final concept
final_concept = f"""
# Movie Concept

## Script Outline
{script_outline.content}

## Casting Recommendations
{casting_suggestions.content}

## Production Notes
[Additional production insights would be added here]
"""

print(final_concept)
```

## Configuration Management

For production use, use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Model configuration
MODEL_CONFIG = {
    'claude': {
        'api_key': os.getenv('ANTHROPIC_API_KEY'),
        'model': 'claude-sonnet-4-5-20250929',
    },
    'gemini': {
        'api_key': os.getenv('GOOGLE_API_KEY'),
        'model': 'gemini-2.5-flash',
    }
}

# Tool configuration
TOOL_CONFIG = {
    'serpapi_key': os.getenv('SERPAPI_KEY'),
}

# Factory function
def create_movie_producer(model_choice='claude'):
    """Create a movie producer team with specified model."""
    config = MODEL_CONFIG[model_choice]

    script_writer = Agent(
        name="ScriptWriter",
        model=Gemini(id=config['model'], api_key=config['api_key']),
        description="Expert screenplay writer",
        instructions=[
            "Write script outlines with 3-5 main characters",
            "Use three-act structure with 2-3 plot twists",
            "Align with genre and target audience",
        ],
    )

    casting_director = Agent(
        name="CastingDirector",
        model=Gemini(id=config['model'], api_key=config['api_key']),
        description="Professional casting director",
        instructions=[
            "Suggest 2-3 actors per main role",
            "Use web search to verify availability",
            "Provide rationale for each suggestion",
            "Ensure diverse and inclusive casting",
        ],
        tools=[SerpApiTools(api_key=TOOL_CONFIG['serpapi_key'])],
    )

    return Team(
        name="MovieProducer",
        model=Gemini(id=config['model'], api_key=config['api_key']),
        members=[script_writer, casting_director],
        description="Experienced movie producer",
        instructions=[
            "Coordinate script and casting development",
            "Synthesize into cohesive concept document",
        ],
        markdown=True,
    )

# Usage
producer = create_movie_producer(model_choice='gemini')
response = producer.run("Movie idea: ...")
```

## Error Handling

```python
from agno.run.agent import RunOutput
import logging

logger = logging.getLogger(__name__)

def develop_movie_concept(movie_params, max_retries=3):
    """
    Develop a movie concept with retry logic.

    Args:
        movie_params: Dictionary with movie parameters
        max_retries: Maximum number of retry attempts

    Returns:
        RunOutput: The response from the movie producer
    """
    producer = create_movie_producer()

    for attempt in range(max_retries):
        try:
            response = producer.run(
                f"Movie idea: {movie_params['idea']}, "
                f"Genre: {movie_params['genre']}, "
                f"Target audience: {movie_params['audience']}, "
                f"Runtime: {movie_params['runtime']} minutes",
                stream=False
            )

            if response and response.content:
                return response
            else:
                logger.warning(f"Attempt {attempt + 1}: Empty response")

        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                raise

    raise RuntimeError("Failed to generate movie concept after maximum retries")
```

## Output File Management

Save concepts to organized directory structure:

```python
import json
from pathlib import Path
from datetime import datetime

def save_movie_concept(response: RunOutput, movie_params: dict):
    """Save movie concept to file with metadata."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in movie_params.get('title', 'untitled') if c.isalnum() or c in (' ', '-', '_')).strip()

    # Create output directory
    output_dir = Path("movie_concepts")
    output_dir.mkdir(exist_ok=True)

    # Save Markdown
    md_file = output_dir / f"{safe_title}_{timestamp}.md"
    md_file.write_text(response.content, encoding='utf-8')

    # Save metadata as JSON
    metadata = {
        'timestamp': timestamp,
        'params': movie_params,
        'file': str(md_file),
    }
    json_file = output_dir / f"{safe_title}_{timestamp}_metadata.json"
    json_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

    return md_file

# Usage
response = develop_movie_concept(movie_params)
saved_file = save_movie_concept(response, movie_params)
print(f"Concept saved to: {saved_file}")
```

## Testing

```python
import pytest

def test_script_writer():
    """Test ScriptWriter agent generates valid output."""
    script_writer = Agent(
        name="ScriptWriter",
        model=Gemini(id="gemini-2.5-flash", api_key=test_api_key),
        description="Test script writer",
        instructions=["Generate script outlines"],
    )

    response = script_writer.run(
        "Generate a script outline for a test movie. "
        "Genre: Comedy. Runtime: 90 minutes."
    )

    assert response.content is not None
    assert len(response.content) > 100
    assert "Act I" in response.content or "Act One" in response.content

def test_casting_director():
    """Test CastingDirector agent uses search."""
    casting_director = Agent(
        name="CastingDirector",
        model=Gemini(id="gemini-2.5-flash", api_key=test_api_key),
        description="Test casting director",
        instructions=["Suggest actors for roles"],
        tools=[SerpApiTools(api_key=test_serp_key)],
    )

    response = casting_director.run(
        "Suggest actors for a role: A 45-year-old retired astronaut. "
        "Character: Gritty, determined, haunted by past."
    )

    assert response.content is not None
    # Should have searched for actual actors
    assert len(response.content) > 50
```

## Performance Optimization

```python
# Cache actor information to reduce API calls
from functools import lru_cache

@lru_cache(maxsize=100)
def get_actor_info(actor_name: str) -> dict:
    """Cache actor information to reduce repeated searches."""
    # Implementation would search and cache results
    pass

# Use async for concurrent operations
import asyncio

async def develop_concept_async(movie_params: dict):
    """Develop concept with async operations."""
    # Implementation for async processing
    pass
```

## Notes

1. **Model Selection**: Claude generally produces better creative writing quality. Gemini is faster and more cost-effective for iterations.

2. **Search Capability**: Claude's built-in search is more convenient. Gemini requires SerpAPI setup.

3. **Cost Considerations**:
   - Script development is token-intensive (long outputs)
   - Casting requires search API calls
   - Consider caching for repeated queries

4. **Production Deployment**: For production use, consider:
   - Rate limiting
   - Request queuing
   - Response caching
   - Monitoring and logging
   - Cost tracking per request
