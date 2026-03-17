<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a>
</p>

# Canqihe's Skills

My collection of custom Claude Code skills for productivity and automation.

## Skills

| Skill | Description |
|-------|-------------|
| [ai-ui-generator](./ai-ui-generator/) | Universal AI-powered UI component generator |
| [algorithmic-art](./algorithmic-art/) | Creating algorithmic art using p5.js |
| [art-master](./art-master/) | Art style prompt generator |
| [baoyu-article-illustrator](./baoyu-article-illustrator/) | Analyze articles and generate illustrations |
| [baoyu-comic](./baoyu-comic/) | Knowledge comic creator |
| [baoyu-compress-image](./baoyu-compress-image/) | Compress images to WebP or PNG |
| [baoyu-cover-image](./baoyu-cover-image/) | Generate article cover images |
| [baoyu-danger-gemini-web](./baoyu-danger-gemini-web/) | Generate images and text via Gemini Web API |
| [baoyu-danger-x-to-markdown](./baoyu-danger-x-to-markdown/) | Convert X (Twitter) tweets to markdown |
| [baoyu-format-markdown](./baoyu-format-markdown/) | Format plain text or markdown files |
| [baoyu-image-gen](./baoyu-image-gen/) | AI image generation with multiple APIs |
| [baoyu-infographic](./baoyu-infographic/) | Generate professional infographics |
| [baoyu-markdown-to-html](./baoyu-markdown-to-html/) | Convert Markdown to styled HTML |
| [baoyu-post-to-wechat](./baoyu-post-to-wechat/) | Post content to WeChat Official Account |
| [baoyu-post-to-x](./baoyu-post-to-x/) | Post content to X (Twitter) |
| [baoyu-slide-deck](./baoyu-slide-deck/) | Generate professional slide deck images |
| [baoyu-translate-local](./baoyu-translate-local/) | Translate articles between languages |
| [baoyu-url-to-markdown](./baoyu-url-to-markdown/) | Convert any URL to markdown |
| [baoyu-xhs-images](./baoyu-xhs-images/) | Xiaohongshu infographic series generator |
| [brand-guidelines](./brand-guidelines/) | Apply Anthropic's brand colors and typography |
| [canvas-design](./canvas-design/) | Create visual art in .png and .pdf documents |
| [design-master](./design-master/) | Graphic design prompt generator |
| [doc-coauthoring](./doc-coauthoring/) | Guide for co-authoring documentation |
| [docx](./docx/) | Comprehensive document creation and editing |
| [data-analyst](./data-analyst/) | AI data analyst for CSV/Excel files |
| [domain-classifier](./domain-classifier/) | AI domain classifier |
| [ec-view](./ec-view/) | E-commerce KV visual system prompt generator |
| [edge-tts-local](./edge-tts-local/) | Text-to-speech conversion using Edge TTS |
| [find-skills](./find-skills/) | Discover and install skills |
| [frontend-design](./frontend-design/) | Create production-grade frontend interfaces |
| [gemini-watermark-remover](./gemini-watermark-remover/) | Remove Gemini AI watermark from images |
| [infographic-creator](./infographic-creator/) | Create beautiful infographics |
| [intelligent-prompt-generator](./intelligent-prompt-generator/) | Intelligent prompt generator v2.0 |
| [internal-comms](./internal-comms/) | Write internal communications |
| [ljg-explain-concept](./ljg-explain-concept/) | Deep concept anatomist |
| [manim-composer](./manim-composer/) | Create educational videos with Manim |
| [manimce-best-practices](./manimce-best-practices/) | Best practices for Manim Community Edition |
| [manimgl-best-practices](./manimgl-best-practices/) | Best practices for ManimGL |
| [mcp-builder](./mcp-builder/) | Guide for creating MCP servers |
| [morning-report](./morning-report/) | Generate daily morning reports |
| [notebooklm](./notebooklm/) | Query Google NotebookLM notebooks |
| [podcast-article-generator](./podcast-article-generator/) | Podcast article generator |
| [pokieticker](./pokieticker/) | Analyze stock price changes and query SQLite database |
| [pdf](./pdf/) | Comprehensive PDF manipulation toolkit |
| [pptx](./pptx/) | Presentation creation and editing |
| [port-allocator](./port-allocator/) | Automatically allocate and manage development server ports |
| [product-master](./product-master/) | Product photography prompt generator |
| [prompt-analyzer](./prompt-analyzer/) | Analyze and compare prompts |
| [prompt-extractor](./prompt-extractor/) | Extract modular structures from prompts |
| [prompt-generator](./prompt-generator/) | Generate prompts from element database |
| [prompt-master](./prompt-master/) | Master prompt controller |
| [prompt-xray](./prompt-xray/) | Reverse engineer knowledge from prompts |
| [release-skills](./release-skills/) | Universal release workflow for skills |
| [remotion-best-practices](./remotion-best-practices/) | Best practices for Remotion video creation |
| [seedance](./seedance/) | Generate video prompts for Seedance |
| [share-skill](./share-skill/) | Automatically share skills and migrate to code repositories |
| [skill-creator](./skill-creator/) | Guide for creating effective skills |
| [skill-i18n](./skill-i18n/) | Translate skill documentation into multiple languages |
| [skill-permissions](./skill-permissions/) | Analyze skill permissions and batch authorization |
| [slack-gif-creator](./slack-gif-creator/) | Create animated GIFs for Slack |
| [social-content](./social-content/) | Social media content creation and optimization |
| [storyboard-generator](./storyboard-generator/) | Generate multi-shot storyboards for videos |
| [theme-factory](./theme-factory/) | Toolkit for styling artifacts with themes |
| [ui-check](./ui-check/) | Opinionated constraints for building interfaces |
| [ui-ux-pro-max](./ui-ux-pro-max/) | UI/UX design intelligence |
| [universal-learner](./universal-learner/) | Universal learner from prompts |
| [video-master](./video-master/) | Video generation prompt controller |
| [video-storyboarding](./video-storyboarding/) | Pre-production planning for tech demo videos |
| [web-artifacts-builder](./web-artifacts-builder/) | Build elaborate HTML artifacts |
| [web-reader-summary](./web-reader-summary/) | Web reader and summary |
| [web_style](./web_style/) | Website design style generator |
| [webapp-testing](./webapp-testing/) | Test local web applications |
| [xhs-images](./xhs-images/) | Xiaohongshu image generator |
| [xlsx](./xlsx/) | Comprehensive spreadsheet toolkit |
| [youtube-clipper](./youtube-clipper/) | YouTube video intelligent editing tool |
| [z-image](./z-image/) | Z-Image generation with ModelScope API |

## Documentation

This skill set has an online documentation site generated by [share-skill](./share-skill/).

**GitHub Pages:**
```
https://canqihe.github.io/canq-skills/
```

### Setup GitHub Pages

1. Go to repository **Settings** -> **Pages**
2. Under "Source", select **Deploy from a branch**
3. Choose branch: `master` (or `main`), folder: `/docs`
4. (Optional) Add custom domain

## Installation

```bash
# Add the marketplace
/plugin marketplace add canqihe/skills

# Install individual skills
/plugin install <skill-name>@canqihe-skills
```

## License

MIT

---

Made with ♥ by [Canqihe's skills](https://github.com/canqihe)
