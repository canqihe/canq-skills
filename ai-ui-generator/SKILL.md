---
name: ai-ui-generator
description: Universal AI-powered UI component generator that uses the current conversation model (GLM, Claude, GPT, etc.) to generate production-ready HTML/CSS code. Use when user requests generating UI components, creating web interfaces or mockups, building HTML/CSS layouts, designing cards forms dashboards or other frontend elements. Supports various design styles like glassmorphism, bento grid, brutalist, minimalist and outputs complete self-contained HTML files.
---

# AI UI Generator

Generate production-ready UI components using the current AI model in the conversation.

## Quick Start

When user requests UI generation:

1. Ask for clarification if needed (component type, style, features)
2. Generate complete HTML file with embedded CSS/JavaScript
3. Save to user's Desktop or specified location
4. Open in browser for preview

## Design Style Library

See [prompts.md](references/prompts.md) for comprehensive style and component library.

Common styles:
- **Glassmorphism** - Frosted glass, transparency, blur effects
- **Bento Grid** - Asymmetric grid layout, rounded corners
- **Brutalist** - Raw typography, high contrast, bold borders
- **Neumorphic** - Soft shadows, subtle depth, extruded shapes
- **Minimalist** - Whitespace, clean lines, subtle colors
- **Cyberpunk** - Neon colors, glitch effects, dark backgrounds
- **Retro** - Pixel art, vintage colors, nostalgic UI

## Component Types

**Cards**: Weather, profile, product, statistics
**Forms**: Login, signup, contact, search
**Navigation**: Header, sidebar, tabs, breadcrumbs
**Data Display**: Dashboard, table, chart, calendar
**Media**: Player, gallery, carousel, card stack

## Generation Guidelines

### Output Format

Always generate **complete, self-contained HTML** files with:
- `<!DOCTYPE html>` and proper `<head>` section
- Embedded CSS in `<style>` tags
- JavaScript in `<script>` tags if interactivity needed
- Responsive design with viewport meta tag
- No external dependencies (use system fonts or CSS-only solutions)

### Quality Standards

1. **Visual Polish** - Proper spacing, shadows, gradients, hover effects
2. **Accessibility** - Semantic HTML, proper contrast, focus states
3. **Responsiveness** - Mobile-friendly, flexible layouts
4. **Interactivity** - Working buttons, hover states, smooth transitions
5. **Modern CSS** - Flexbox, Grid, CSS variables, animations

### IP Safeguard

- No specific artist names or brand references
- Use physical/material metaphors for styles
- Avoid trademarked elements

## Examples

**Prompt**: "Generate a glassmorphic music player"

**Response**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Player</title>
    <style>
        /* Complete CSS here */
    </style>
</head>
<body>
    <!-- Complete HTML structure -->
    <script>
        /* Interactive JavaScript if needed */
    </script>
</body>
</html>
```

Then save to `/Users/colin/Desktop/music_player.html` and open with `open` command.

## Workflow

1. **Understand Request** - Clarify component type, style, features
2. **Generate Code** - Create complete HTML with CSS/JS
3. **Save File** - Write to Desktop or user-specified path
4. **Preview** - Open in browser automatically
5. **Iterate** - Refine based on feedback if needed

## Resources

- **references/prompts.md** - Style library, component types, and prompting techniques
- **scripts/generate_ui.py** - External API version (use only if user specifically requests external provider)
