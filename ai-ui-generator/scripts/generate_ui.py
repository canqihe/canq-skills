#!/usr/bin/env python3
"""
AI UI Generator - Universal UI Component Generator

Supports multiple AI providers:
- Gemini (Google)
- OpenAI (GPT-4, GPT-4o)
- Anthropic (Claude)
- Local models (via OpenAI-compatible API)
"""

import argparse
import json
import os
import sys
from enum import Enum
from typing import Optional, AsyncGenerator


class Provider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class UIGenerator:
    """Universal AI UI Generator supporting multiple providers."""

    def __init__(self, provider: Provider, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key or os.getenv(f"{provider.value.upper()}_API_KEY")
        self.base_url = base_url

        if not self.api_key and provider != Provider.LOCAL:
            raise ValueError(f"API key required for {provider.value}")

        self._init_client()

    def _init_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == Provider.GEMINI:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except ImportError:
                raise ImportError("Install google-genai: pip install google-genai")

        elif self.provider == Provider.OPENAI:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                raise ImportError("Install openai: pip install openai")

        elif self.provider == Provider.ANTHROPIC:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                raise ImportError("Install anthropic: pip install anthropic")

        elif self.provider == Provider.LOCAL:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key="not-needed", base_url=self.base_url or "http://localhost:11434/v1")
            except ImportError:
                raise ImportError("Install openai: pip install openai")

    def generate(
        self,
        prompt: str,
        style: str = "modern",
        count: int = 1,
        temperature: float = 0.9,
        stream: bool = False,
    ) -> str | list[str] | AsyncGenerator[str, None]:
        """
        Generate UI components.

        Args:
            prompt: User's UI description
            style: Design style direction
            count: Number of variations to generate
            temperature: Sampling temperature
            stream: Enable streaming response

        Returns:
            Generated HTML code(s) or async generator for streaming
        """
        system_prompt = self._build_system_prompt(style)

        if self.provider == Provider.GEMINI:
            return self._generate_gemini(system_prompt, prompt, count, temperature, stream)
        elif self.provider in (Provider.OPENAI, Provider.LOCAL):
            return self._generate_openai_compat(system_prompt, prompt, count, temperature, stream)
        elif self.provider == Provider.ANTHROPIC:
            return self._generate_anthropic(system_prompt, prompt, count, temperature, stream)

    def _build_system_prompt(self, style: str) -> str:
        """Build the system prompt for UI generation."""
        return f"""You are an expert UI/UX designer and frontend engineer.

Generate high-fidelity, production-ready HTML/CSS UI components.

**Design Direction: {style}**

**Visual Execution Rules:**
1. **Materiality**: Use the style metaphor to drive every CSS choice
2. **Typography**: Use modern system fonts or Google Fonts
3. **Motion**: Include subtle CSS animations (hover, transitions)
4. **Layout**: Be bold with negative space and visual hierarchy
5. **Accessibility**: Ensure proper contrast ratios and semantic HTML

**Output Format:**
- Return ONLY raw HTML (no markdown code fences)
- Include embedded CSS in <style> tags
- Include JavaScript in <script> tags if needed for interactivity
- Make components self-contained and copy-paste ready

**IP Safeguard:**
- No specific artist names or trademarks
- Use physical and material metaphors instead"""

    def _generate_gemini(self, system_prompt: str, prompt: str, count: int, temperature: float, stream: bool):
        """Generate using Google Gemini API."""
        full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"

        if stream:
            response = self.client.models.generate_content_stream(
                model="gemini-2.0-flash-exp",
                contents=full_prompt,
                config={"temperature": temperature}
            )
            return response
        else:
            if count == 1:
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=full_prompt,
                    config={"temperature": temperature}
                )
                return self._clean_html(response.text)
            else:
                results = []
                for _ in range(count):
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash-exp",
                        contents=full_prompt,
                        config={"temperature": temperature}
                    )
                    results.append(self._clean_html(response.text))
                return results

    def _generate_openai_compat(self, system_prompt: str, prompt: str, count: int, temperature: float, stream: bool):
        """Generate using OpenAI-compatible API (OpenAI, local models, etc.)."""
        model = os.getenv("OPENAI_MODEL", "gpt-4o")

        if stream:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                stream=True
            )
            return self._stream_openai(response)
        else:
            if count == 1:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                return self._clean_html(response.choices[0].message.content)
            else:
                results = []
                for _ in range(count):
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=temperature
                    )
                    results.append(self._clean_html(response.choices[0].message.content))
                return results

    def _generate_anthropic(self, system_prompt: str, prompt: str, count: int, temperature: float, stream: bool):
        """Generate using Anthropic Claude API."""
        if stream:
            response = self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response
        else:
            if count == 1:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=8192,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return self._clean_html(response.content[0].text)
            else:
                results = []
                for _ in range(count):
                    response = self.client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=8192,
                        system=system_prompt,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature
                    )
                    results.append(self._clean_html(response.content[0].text))
                return results

    async def _stream_openai(self, response):
        """Helper to stream OpenAI responses."""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    @staticmethod
    def _clean_html(html: Optional[str]) -> str:
        """Clean markdown code fences from generated HTML."""
        if not html:
            return ""

        html = html.strip()
        if html.startswith("```html"):
            html = html[7:].lstrip()
        elif html.startswith("```"):
            html = html[3:].lstrip()

        if html.endswith("```"):
            html = html[:-3].rstrip()

        return html


def main():
    parser = argparse.ArgumentParser(description="AI UI Generator")
    parser.add_argument("prompt", help="UI description to generate")
    parser.add_argument("-p", "--provider", choices=["gemini", "openai", "anthropic", "local"],
                        default="gemini", help="AI provider")
    parser.add_argument("-s", "--style", default="Modern minimalist",
                        help="Design style direction")
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="Number of variations")
    parser.add_argument("-t", "--temperature", type=float, default=0.9,
                        help="Sampling temperature")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--stream", action="store_true",
                        help="Enable streaming output")

    args = parser.parse_args()

    try:
        generator = UIGenerator(Provider(args.provider))

        if args.stream:
            print("Streaming response...")
            for chunk in generator.generate(
                args.prompt,
                style=args.style,
                count=args.count,
                temperature=args.temperature,
                stream=True
            ):
                print(chunk, end="", flush=True)
            print()
        else:
            result = generator.generate(
                args.prompt,
                style=args.style,
                count=args.count,
                temperature=args.temperature
            )

            if isinstance(result, list):
                for i, html in enumerate(result):
                    output_path = args.output or f"output_{i}.html"
                    with open(output_path, "w") as f:
                        f.write(html)
                    print(f"Generated variation {i+1} -> {output_path}")
            else:
                output_path = args.output or "output.html"
                with open(output_path, "w") as f:
                    f.write(result)
                print(f"Generated UI -> {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
