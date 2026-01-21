---
name: movie-production
description: "Interactive AI-powered movie production assistant that helps develop movie concepts through multi-step dialogue. Use when user wants to: Develop movie ideas into full concepts, Generate script outlines with character development and plot structure, Get casting suggestions for main roles, Create professional movie concept documents with script and casting details. Supports multiple AI models (Claude/Gemini) with configurable search capabilities for actor research."
---

# Movie Production

## Overview

Transform movie ideas into professional production concepts through interactive dialogue. This skill orchestrates three specialized AI agents—ScriptWriter, CastingDirector, and MovieProducer—to develop compelling script outlines and casting recommendations tailored to your creative vision.

## Core Capabilities

### 1. Script Development
- Generate detailed script outlines with character descriptions
- Structure plot using three-act narrative framework
- Suggest 2-3 plot twists aligned with genre and audience
- Develop 3-5 main characters with distinct personalities

### 2. Casting Recommendations
- Suggest 2-3 actors for each main role
- Research actor availability and recent work using web search
- Provide rationale for casting choices based on performance history
- Consider diversity and representation in casting decisions

### 3. Concept Synthesis
- Combine script and casting into cohesive movie concept
- Format output as professional Markdown document
- Provide concise overview suitable for pitch meetings

## Workflow

### Phase 1: Gather Requirements

Ask user for:

1. **Movie Idea** - Brief description (1-3 sentences)
2. **Genre** - Action, Comedy, Drama, Sci-Fi, Horror, Romance, Thriller
3. **Target Audience** - General, Children, Teenagers, Adults, Mature
4. **Runtime** - Estimated duration in minutes (60-180)
5. **Language** - Primary language for script

Example interaction:
```
User: "I want to make a movie about a retired astronaut who discovers
      Earth is being invaded by aliens, but only his grandchildren believe him."

Claude: "Great concept! A few questions:
        - What genre appeals to you? (Sci-Fi thriller, Family adventure, etc.)
        - Who's your target audience?
        - What runtime are you aiming for?
        - Any specific tone preferences? (Serious, humorous, dark, etc.)"
```

### Phase 2: Script Development (ScriptWriter Agent)

Execute ScriptWriter agent with gathered parameters:

**Agent Instructions:**
- Write script outline with 3-5 main characters
- Develop three-act structure (Setup, Confrontation, Resolution)
- Suggest 2-3 plot twists consistent with genre
- Ensure alignment with specified genre and target audience
- Include key dialogue snippets and scene descriptions

**Output Format:**
```markdown
# Script Outline: [Movie Title]

## Characters
1. **[Character Name]** - Age, role, brief personality
2. **[Character Name]** - Age, role, brief personality
...

## Act Structure

### Act I: The Setup
- Inciting incident
- Character introductions
- Story setup

### Act II: The Confrontation
- Rising action
- Plot Twist 1: [Description]
- Plot Twist 2: [Description]

### Act III: The Resolution
- Climax
- Resolution
- Theme payoff

## Key Scenes
- Scene 1: [Brief description]
- Scene 2: [Brief description]
...
```

### Phase 3: Casting Research (CastingDirector Agent)

Pass script outline to CastingDirector agent:

**Agent Instructions:**
- Suggest 2-3 actors for each main role
- Use web search to verify actor availability and recent work
- Consider age appropriateness, acting style, and box office appeal
- Provide brief justification for each recommendation
- Ensure diverse and inclusive casting choices

**Required Tool:** Web search (SerpAPI or Claude's built-in search)

**Output Format:**
```markdown
# Casting Recommendations

## [Character Name]
- **Option 1:** [Actor Name] - Rationale (recent work, acting style)
- **Option 2:** [Actor Name] - Rationale
- **Option 3:** [Actor Name] - Rationale

## [Character Name]
...
```

### Phase 4: Concept Synthesis (MovieProducer Agent)

Compile and format final movie concept:

**Output Format:**
```markdown
# Movie Concept: [Title]

## Overview
[2-3 sentence pitch]

## Details
- **Genre:** [Genre]
- **Target Audience:** [Audience]
- **Runtime:** [X] minutes
- **Language:** [Language]

[Include full Script Outline and Casting Recommendations from above]

## Production Notes
- Key production considerations
- Budget level (Low/Medium/Blockbuster)
- Special effects requirements
- Target release window suggestions
```

## Model Configuration

This skill supports multiple AI models. Choose based on user preference:

### Option 1: Claude (Recommended)
- **Model:** claude-sonnet-4-5-20250929 or claude-opus-4-5-20251101
- **Strengths:** Superior creative writing, character development
- **Search:** Built-in web search capability (no external API needed)
- **Use when:** User wants best quality output, has Anthropic API access

### Option 2: Gemini
- **Model:** gemini-2.5-flash
- **Strengths:** Fast generation, cost-effective
- **Search:** Requires SerpAPI key
- **Use when:** User prefers Google, has Gemini API access

### Option 3: User's Choice
Let user specify model. Ask:
- "Which AI model would you like to use? (Claude/Gemini/Other)"
- Obtain required API keys accordingly

## Implementation

### Direct Implementation (No Scripts)

For most use cases, implement agents directly in conversation using Claude's native capabilities:

1. **ScriptWriter** - Use Claude directly with system prompt from [references/agents.md](references/agents.md)
2. **CastingDirector** - Use Claude with web search (built-in or SerpAPI)
3. **MovieProducer** - Use Claude to compile and format output

This is the recommended approach as it's most flexible and leverages Claude's full capabilities.

### Scripted Implementation (Advanced)

If deterministic reliability is needed for production use, see [references/agent_implementation.md](references/agent_implementation.md) for Python implementation patterns using agno framework.

## References

- [references/agents.md](references/agents.md) - Detailed agent configurations and prompts
- [references/agent_implementation.md](references/agent_implementation.md) - Python implementation examples
- [references/workflow_examples.md](references/workflow_examples.md) - Complete workflow examples

## Interactive Development Pattern

Unlike the original Streamlit app which generates everything at once, this skill emphasizes **interactive refinement**:

1. **Start with basics** - Get initial concept from user
2. **Iterate on script** - Refine outline based on feedback
3. **Refine casting** - Adjust actor suggestions based on user preferences
4. **Finalize concept** - Compile polished document

Example dialogue flow:
```
User: "I want a sci-fi movie about Mars colonization"

Claude: [Generates initial script outline]

User: "Make it darker, add more conflict between colony leaders"

Claude: [Refines script with requested changes]

User: "Who should play the main character?"

Claude: [Provides casting suggestions with web search]

User: "I love Option 1, but who else could play the antagonist?"

Claude: [Provides additional casting options]

Claude: [Compiles final concept document]
```

## Quality Standards

- **Script outlines** should include clear character motivations and story arc
- **Casting suggestions** should be realistic and match character descriptions
- **Final document** should be pitch-ready and professionally formatted
- **All content** should align with specified genre and target audience
