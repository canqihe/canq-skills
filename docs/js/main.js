// Repository configuration
const REPO_OWNER = 'canqihe';
const REPO_NAME = 'canq-skills';
const BRANCH = 'master';
const CACHE_VERSION = '1737686400';

// Cache busting
const isGitHubPages = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';

// Get base path for skill files
function getBasePath(skillName, lang = 'en') {
    const fileName = lang === 'en' ? 'SKILL.md' : `SKILL.${lang}.md`;

    if (isGitHubPages) {
        return `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}/${skillName}/${fileName}?v=${CACHE_VERSION}`;
    } else {
        return `../${skillName}/${fileName}?v=${CACHE_VERSION}`;
    }
}

// Current state
let currentSkill = null;
let currentLang = 'en';

// All skills configuration
const SKILLS = {
    'ai-ui-generator': {
        name: 'ai-ui-generator',
        description: 'Universal AI-powered UI component generator',
        path: 'ai-ui-generator'
    },
    'algorithmic-art': {
        name: 'algorithmic-art',
        description: 'Creating algorithmic art using p5.js',
        path: 'algorithmic-art'
    },
    'art-master': {
        name: 'art-master',
        description: 'Art style prompt generator',
        path: 'art-master'
    },
    'baoyu-xhs-images': {
        name: 'baoyu-xhs-images',
        description: 'Xiaohongshu infographic series generator',
        path: 'baoyu-xhs-images'
    },
    'brand-guidelines': {
        name: 'brand-guidelines',
        description: 'Apply Anthropic\'s brand colors and typography',
        path: 'brand-guidelines'
    },
    'canvas-design': {
        name: 'canvas-design',
        description: 'Create visual art in .png and .pdf documents',
        path: 'canvas-design'
    },
    'design-master': {
        name: 'design-master',
        description: 'Graphic design prompt generator',
        path: 'design-master'
    },
    'doc-coauthoring': {
        name: 'doc-coauthoring',
        description: 'Guide for co-authoring documentation',
        path: 'doc-coauthoring'
    },
    'docx': {
        name: 'docx',
        description: 'Comprehensive document creation and editing',
        path: 'docx'
    },
    'data-analyst': {
        name: 'data-analyst',
        description: 'AI data analyst for CSV/Excel files',
        path: 'data-analyst'
    },
    'domain-classifier': {
        name: 'domain-classifier',
        description: 'AI domain classifier',
        path: 'domain-classifier'
    },
    'ec-view': {
        name: 'ec-view',
        description: 'E-commerce KV visual system prompt generator',
        path: 'ec-view'
    },
    'frontend-design': {
        name: 'frontend-design',
        description: 'Create production-grade frontend interfaces',
        path: 'frontend-design'
    },
    'infographic-creator': {
        name: 'infographic-creator',
        description: 'Create beautiful infographics',
        path: 'infographic-creator'
    },
    'intelligent-prompt-generator': {
        name: 'intelligent-prompt-generator',
        description: 'Intelligent prompt generator v2.0',
        path: 'intelligent-prompt-generator'
    },
    'internal-comms': {
        name: 'internal-comms',
        description: 'Write internal communications',
        path: 'internal-comms'
    },
    'mcp-builder': {
        name: 'mcp-builder',
        description: 'Guide for creating MCP servers',
        path: 'mcp-builder'
    },
    'notebooklm': {
        name: 'notebooklm',
        description: 'Query Google NotebookLM notebooks',
        path: 'notebooklm'
    },
    'pdf': {
        name: 'pdf',
        description: 'Comprehensive PDF manipulation toolkit',
        path: 'pdf'
    },
    'port-allocator': {
        name: 'port-allocator',
        description: 'Automatically allocate and manage development server ports',
        path: 'port-allocator'
    },
    'pptx': {
        name: 'pptx',
        description: 'Presentation creation and editing',
        path: 'pptx'
    },
    'product-master': {
        name: 'product-master',
        description: 'Product photography prompt generator',
        path: 'product-master'
    },
    'prompt-analyzer': {
        name: 'prompt-analyzer',
        description: 'Analyze and compare prompts',
        path: 'prompt-analyzer'
    },
    'prompt-extractor': {
        name: 'prompt-extractor',
        description: 'Extract modular structures from prompts',
        path: 'prompt-extractor'
    },
    'prompt-generator': {
        name: 'prompt-generator',
        description: 'Generate prompts from element database',
        path: 'prompt-generator'
    },
    'prompt-master': {
        name: 'prompt-master',
        description: 'Master prompt controller',
        path: 'prompt-master'
    },
    'prompt-xray': {
        name: 'prompt-xray',
        description: 'Reverse engineer knowledge from prompts',
        path: 'prompt-xray'
    },
    'remotion-best-practices': {
        name: 'remotion-best-practices',
        description: 'Best practices for Remotion video creation',
        path: 'remotion-best-practices'
    },
    'share-skill': {
        name: 'share-skill',
        description: 'Automatically share skills and migrate to code repositories',
        path: 'share-skill'
    },
    'skill-creator': {
        name: 'skill-creator',
        description: 'Guide for creating effective skills',
        path: 'skill-creator'
    },
    'skill-i18n': {
        name: 'skill-i18n',
        description: 'Translate skill documentation into multiple languages',
        path: 'skill-i18n'
    },
    'skill-permissions': {
        name: 'skill-permissions',
        description: 'Analyze skill permissions and batch authorization',
        path: 'skill-permissions'
    },
    'slack-gif-creator': {
        name: 'slack-gif-creator',
        description: 'Create animated GIFs for Slack',
        path: 'slack-gif-creator'
    },
    'theme-factory': {
        name: 'theme-factory',
        description: 'Toolkit for styling artifacts with themes',
        path: 'theme-factory'
    },
    'ui-check': {
        name: 'ui-check',
        description: 'Opinionated constraints for building interfaces',
        path: 'ui-check'
    },
    'ui-ux-pro-max': {
        name: 'ui-ux-pro-max',
        description: 'UI/UX design intelligence',
        path: 'ui-ux-pro-max'
    },
    'universal-learner': {
        name: 'universal-learner',
        description: 'Universal learner from prompts',
        path: 'universal-learner'
    },
    'video-master': {
        name: 'video-master',
        description: 'Video generation prompt controller',
        path: 'video-master'
    },
    'web-artifacts-builder': {
        name: 'web-artifacts-builder',
        description: 'Build elaborate HTML artifacts',
        path: 'web-artifacts-builder'
    },
    'web_style': {
        name: 'web_style',
        description: 'Website design style generator',
        path: 'web_style'
    },
    'webapp-testing': {
        name: 'webapp-testing',
        description: 'Test local web applications',
        path: 'webapp-testing'
    },
    'xlsx': {
        name: 'xlsx',
        description: 'Comprehensive spreadsheet toolkit',
        path: 'xlsx'
    },
    'youtube-clipper': {
        name: 'youtube-clipper',
        description: 'YouTube video intelligent editing tool',
        path: 'youtube-clipper'
    },
    'z-image': {
        name: 'z-image',
        description: 'Z-Image generation with ModelScope API',
        path: 'z-image'
    }
};

// Marketing content for skills (basic version - can be expanded)
const SKILL_MARKETING = {
    'port-allocator': {
        en: {
            headline: 'Never Fight Over Port 3000 Again',
            why: 'Running multiple Claude Code instances? Port 3000 already in use? Port Allocator automatically manages development server ports across all your projects, so you never have to manually kill processes or remember which port is free.',
            painPoints: [
                { icon: '🔥', title: 'Port Conflicts', desc: 'Error: EADDRINUSE: address already in use :::3000' },
                { icon: '🧠', title: 'Manual Tracking', desc: 'Which port was this project using again? Did I write it down?' },
                { icon: '💥', title: 'Process Hunting', desc: 'Running lsof and kill commands to free up ports' }
            ]
        },
        'zh-CN': {
            headline: '再也不用争抢3000端口',
            why: '运行多个Claude Code实例？3000端口已被占用？端口分配器自动管理所有项目的开发服务器端口，无需手动结束进程或记住哪个端口是空闲的。',
            painPoints: [
                { icon: '🔥', title: '端口冲突', desc: '错误：EADDRINUSE：地址已被使用 :::3000' },
                { icon: '🧠', title: '手动记录', desc: '这个项目用的是哪个端口？我记下来了吗？' },
                { icon: '💥', title: '进程查找', desc: '运行lsof和kill命令来释放端口' }
            ]
        },
        ja: {
            headline: 'ポート3000の争奪戦に終止符',
            why: '複数のClaude Codeインスタンスを実行していますか？ポート3000は既に使用中？ポートアロケーターは、すべてのプロジェクトの開発サーバーポートを自動的に管理するため、手動でプロセスを終了させたり、どのポートが空いているかを覚えたりする必要がありません。',
            painPoints: [
                { icon: '🔥', title: 'ポートの競合', desc: 'エラー：EADDRINUSE：アドレスは既に使用されています :::3000' },
                { icon: '🧠', title: '手動追跡', desc: 'このプロジェクトはどのポートを使用していましたか？メモしましたか？' },
                { icon: '💥', title: 'プロセス狩り', desc: 'lsofとkillコマンドを実行してポートを解放' }
            ]
        }
    },
    'share-skill': {
        en: {
            headline: 'Share Your Skills with the World',
            why: 'Created an amazing skill? Share it with the community! Share-Skill automates the entire process: migrate to GitHub, initialize Git, create documentation, and even generate a beautiful documentation website.',
            painPoints: [
                { icon: '🔥', title: 'Manual Migration', desc: 'Copy-pasting skill files, creating symlinks, initializing Git...' },
                { icon: '🧠', title: 'Documentation Hassle', desc: 'Writing README, creating docs site, maintaining multiple files' },
                { icon: '💥', title: 'Git Workflow', desc: 'Commit, push, handle remote URLs... it\'s tedious' }
            ]
        },
        'zh-CN': {
            headline: '与世界分享你的技能',
            why: '创建了一个惊人的skill？与社区分享吧！Share-Skill自动化整个过程：迁移到GitHub、初始化Git、创建文档，甚至生成精美的文档网站。',
            painPoints: [
                { icon: '🔥', title: '手动迁移', desc: '复制粘贴skill文件，创建符号链接，初始化Git...' },
                { icon: '🧠', title: '文档麻烦', desc: '编写README，创建文档站点，维护多个文件' },
                { icon: '💥', title: 'Git工作流', desc: '提交、推送、处理远程URL...太繁琐了' }
            ]
        },
        ja: {
            headline: 'あなたのスキルを世界と共有',
            why: '素晴らしいスキルを作成しましたか？コミュニティと共有しましょう！Share-Skillはプロセス全体を自動化します：GitHubへの移行、Gitの初期化、ドキュメントの作成、そして美しいドキュメントサイトの生成まで。',
            painPoints: [
                { icon: '🔥', title: '手動移行', desc: 'スキルファイルのコピペ、シンボリックリンクの作成、Gitの初期化...' },
                { icon: '🧠', title: 'ドキュメントの面倒', desc: 'READMEの記述、ドキュメントサイトの作成、複数ファイルの維持' },
                { icon: '💥', title: 'Gitワークフロー', desc: 'コミット、プッシュ、リモートURLの処理...面倒です' }
            ]
        }
    },
    'skill-i18n': {
        en: {
            headline: 'Make Your Skills Speak Every Language',
            why: 'Your skills are amazing—don\'t let language barriers limit their reach! Skill-i18n automatically translates your SKILL.md documentation into multiple languages, making your skills accessible to developers worldwide.',
            painPoints: [
                { icon: '🔥', title: 'Manual Translation', desc: 'Copy-pasting to Google Translate, formatting, fixing errors...' },
                { icon: '🧠', title: 'Maintenance Burden', desc: 'Update original file, then remember to update all translations' },
                { icon: '💥', title: 'Inconsistent Quality', desc: 'Some translations are great, others... not so much' }
            ]
        },
        'zh-CN': {
            headline: '让你的技能说所有语言',
            why: '你的技能很棒——不要让语言障碍限制它的传播！Skill-i18n自动将SKILL.md文档翻译成多种语言，使全球开发者都能访问你的技能。',
            painPoints: [
                { icon: '🔥', title: '手动翻译', desc: '复制粘贴到Google翻译，格式化，修复错误...' },
                { icon: '🧠', title: '维护负担', desc: '更新原文件后，记得更新所有翻译' },
                { icon: '💥', title: '质量不一致', desc: '有些翻译很好，其他的...就不太好了' }
            ]
        },
        ja: {
            headline: 'あなたのスキルを全言語で話せるように',
            why: 'あなたのスキルは素晴らしい—言語の壁でそのリーチを制限しないでください！Skill-i18nはSKILL.mdドキュメントを自動的に複数の言語に翻訳し、世界中の開発者があなたのスキルにアクセスできるようにします。',
            painPoints: [
                { icon: '🔥', title: '手動翻訳', desc: 'Google翻訳にコピペ、フォーマット、エラー修正...' },
                { icon: '🧠', title: '保守の負担', desc: '元のファイルを更新したら、すべての翻訳も更新することを覚えておく' },
                { icon: '💥', title: '品質のばらつき', desc: '一部の翻訳は素晴らしいが、他は...あまり良くない' }
            ]
        }
    },
    'skill-permissions': {
        en: {
            headline: 'Configure Permissions Once, Use Forever',
            why: 'Tired of confirming every Bash command? Skill Permissions analyzes what permissions each skill needs and authorizes them all in one go. Set it and forget it—focus on building, not approving prompts.',
            painPoints: [
                { icon: '🔥', title: 'Permission Fatigue', desc: 'Allow this command? Allow that command? Over and over' },
                { icon: '🧠', title: 'Unclear Requirements', desc: 'What permissions does this skill actually need?' },
                { icon: '💥', title: 'Manual Configuration', desc: 'Editing settings.json, guessing the right permission patterns' }
            ]
        },
        'zh-CN': {
            headline: '一次配置权限，永久使用',
            why: '厌倦了确认每个Bash命令？Skill Permissions分析每个skill需要什么权限，一次性全部授权。设置后忘掉它——专注于构建，而不是批准提示。',
            painPoints: [
                { icon: '🔥', title: '权限疲劳', desc: '允许这个命令？允许那个命令？一遍又一遍' },
                { icon: '🧠', title: '需求不明确', desc: '这个skill到底需要什么权限？' },
                { icon: '💥', title: '手动配置', desc: '编辑settings.json，猜测正确的权限模式' }
            ]
        },
        ja: {
            headline: '一度設定すれば永遠に使える',
            why: 'すべてのBashコマンドを確認するのはうんざり？Skill Permissionsは各スキルが必要とする権限を分析し、一度にすべてを承認します。設定して忘れてください—構築に集中し、プロンプトを承認するのではなく。',
            painPoints: [
                { icon: '🔥', title: '権限の疲労', desc: 'このコマンドを許可？あのコマンドを許可？何度も何度も' },
                { icon: '🧠', title: '要件が不明確', desc: 'このスキルは実際には何の権限が必要ですか？' },
                { icon: '💥', title: '手動設定', desc: 'settings.jsonを編集し、正しい権限パターンを推測' }
            ]
        }
    },
    'ai-ui-generator': {
        en: {
            headline: 'Generate Beautiful UI Components Instantly',
            why: 'Need a dashboard, form, or landing page? AI UI Generator creates production-ready HTML/CSS components in seconds. From glassmorphism to bento grid, get stunning interfaces without writing code from scratch.',
            painPoints: [
                { icon: '🔥', title: 'Blank Canvas', desc: 'Starting from zero? Which component library? Which design system?' },
                { icon: '🧠', title: 'Boilerplate Fatigue', desc: 'Writing the same HTML structure and CSS classes over and over' },
                { icon: '💥', title: 'Design Consistency', desc: 'Your components look different—no unified design language' }
            ]
        }
    },
    'algorithmic-art': {
        en: {
            headline: 'Create Generative Art with Code',
            why: 'Algorithmic Art skill turns p5.js into your creative canvas. Generate unique visuals, flow fields, and particle systems with seeded randomness—every piece is original and reproducible.',
            painPoints: [
                { icon: '🔥', title: 'Creative Block', desc: 'Staring at a blank canvas? Don\'t know where to start?' },
                { icon: '🧠', title: 'Manual Coding', desc: 'Writing complex p5.js sketches line by line takes time' },
                { icon: '💥', title: 'Reproducibility', desc: 'Found something cool but can\'t recreate it with different parameters' }
            ]
        }
    },
    'art-master': {
        en: {
            headline: 'Professional Art Style Prompts',
            why: 'Generate art in any style—watercolor, oil painting, surrealism, and more. Art Master creates expert-level prompts for AI art tools, capturing the essence of artistic techniques.',
            painPoints: [
                { icon: '🔥', title: 'Style Knowledge', desc: 'Don\'t know the difference between impasto and glazing techniques?' },
                { icon: '🧠', title: 'Prompt Crafting', desc: 'Your AI art looks generic—lacks professional artistic nuance' },
                { icon: '💥', title: 'Inconsistent Results', desc: 'Can\'t achieve the same style across multiple generations' }
            ]
        }
    },
    'brand-guidelines': {
        en: {
            headline: 'Apply Brand Guidelines Consistently',
            why: 'Keep your brand identity consistent across all artifacts. Brand Guidelines automatically applies Anthropic\'s official colors, typography, and design standards to any document or artifact.',
            painPoints: [
                { icon: '🔥', title: 'Brand Drift', desc: 'Each designer uses slightly different colors and fonts' },
                { icon: '🧠', title: 'Manual Enforcement', desc: 'Checking hex codes and font weights for every design' },
                { icon: '💥', title: 'Inconsistent Assets', desc: 'Your slides, docs, and UI don\'t look like they\'re from the same company' }
            ]
        }
    },
    'canvas-design': {
        en: {
            headline: 'Design Visual Art for Print and Web',
            why: 'Create stunning posters, art pieces, and visual designs as PNG or PDF. Canvas Design combines design philosophy with AI to produce original, professional artwork.',
            painPoints: [
                { icon: '🔥', title: 'Design Tools', desc: 'Don\'t know Figma? Photoshop feels overwhelming?' },
                { icon: '🧠', title: 'Creative Skills', desc: 'Have ideas but lack the technical design ability' },
                { icon: '💥', title: 'Format Issues', desc: 'Design looks great on screen but terrible when printed' }
            ]
        }
    },
    'design-master': {
        en: {
            headline: 'Expert Design Prompts for Any Need',
            why: 'Generate prompts for Bento Grid layouts, glassmorphism UI, minimalist interfaces, and more. Design Master knows design terminology and creates professional design instructions.',
            painPoints: [
                { icon: '🔥', title: 'Design Jargon', desc: 'Don\'t know the difference between skeuomorphism and neumorphism?' },
                { icon: '🧠', title: 'Vague Prompts', desc: '\'Make it look good\' doesn\'t give AI enough guidance' },
                { icon: '💥', title: 'Generic Results', desc: 'Your designs look like everyone else\'s AI-generated content' }
            ]
        }
    },
    'doc-coauthoring': {
        en: {
            headline: 'Write Better Docs, Together',
            why: 'Structured workflow for co-authoring documentation. Transfer context efficiently, refine content through iteration, and verify your docs work for readers.',
            painPoints: [
                { icon: '🔥', title: 'Context Loss', desc: 'Information gets lost in email threads and chat messages' },
                { icon: '🧠', title: 'Writer\'s Block', desc: 'Staring at a blank page, don\'t know how to structure the document' },
                { icon: '💥', title: 'Review Chaos', desc: 'Feedback is scattered, unorganized, and hard to track' }
            ]
        }
    },
    'docx': {
        en: {
            headline: 'Professional Document Automation',
            why: 'Create, edit, and analyze Word documents with tracked changes, comments, and perfect formatting. DocX handles professional documents at scale programmatically.',
            painPoints: [
                { icon: '🔥', title: 'Manual Editing', desc: 'Making the same changes to 50 documents one by one' },
                { icon: '🧠', title: 'Format Breaking', desc: 'Automated tools mess up your carefully crafted formatting' },
                { icon: '💥', title: 'Review Management', desc: 'Lost track of who changed what in the document' }
            ]
        }
    },
    'domain-classifier': {
        en: {
            headline: 'Intelligently Route to the Right Skill',
            why: 'Not sure which skill to use? Domain Classifier analyzes your request and automatically routes it to the appropriate expert skill for the best results.',
            painPoints: [
                { icon: '🔥', title: 'Skill Confusion', desc: '40 skills—how do you know which one to use?' },
                { icon: '🧠', title: 'Wrong Tool', desc: 'Using the wrong skill leads to poor results' },
                { icon: '💥', title: 'Manual Selection', desc: 'Have to read each skill\'s description to figure it out' }
            ]
        }
    },
    'ec-view': {
        en: {
            headline: 'E-commerce Visual Prompts Made Easy',
            why: 'Generate complete 10-poster series for product photography. EC View intelligently identifies product info and creates bilingual prompts in 9:16 vertical format.',
            painPoints: [
                { icon: '🔥', title: 'Product Photos', desc: 'Your product shots look amateur and inconsistent' },
                { icon: '🧠', title: 'Prompt Generation', desc: 'Writing prompts for every product variant is tedious' },
                { icon: '💥', title: 'Multi-format', desc: 'Need different aspect ratios for different platforms' }
            ]
        }
    },
    'frontend-design': {
        en: {
            headline: 'Production-Ready Frontend Interfaces',
            why: 'Build websites, landing pages, dashboards, and React components with high design quality. Avoids generic AI aesthetics—creates polished, creative code.',
            painPoints: [
                { icon: '🔥', title: 'Generic UI', desc: 'AI-generated interfaces all look the same—boring and template-y' },
                { icon: '🧠', title: 'Design Quality', desc: 'Your frontend lacks professional polish and attention to detail' },
                { icon: '💥', title: 'Code Structure', desc: 'Generated HTML/CSS is messy, unmaintainable, or hardcoded' }
            ]
        }
    },
    'infographic-creator': {
        en: {
            headline: 'Turn Data into Beautiful Infographics',
            why: 'Transform text content into stunning visual infographics. Make complex information digestible, memorable, and shareable.',
            painPoints: [
                { icon: '🔥', title: 'Data Visualization', desc: 'Your charts and graphs are boring and hard to understand' },
                { icon: '🧠', title: 'Design Skills', desc: 'Not a designer? Creating infographics feels overwhelming' },
                { icon: '💥', title: 'Information Overload', desc: 'Too much text—readers tune out' }
            ]
        }
    },
    'intelligent-prompt-generator': {
        en: {
            headline: 'Intelligent Prompts with Semantic Understanding',
            why: 'Advanced prompt generator v2.0 with semantic analysis, commonsense reasoning, and consistency checking. Generates perfect prompts for AI image generation.',
            painPoints: [
                { icon: '🔥', title: 'Prompt Quality', desc: 'Your AI generates weird results—prompts lack detail' },
                { icon: '🧠', title: 'Trial & Error', desc: 'Generating dozens of variations to find one that works' },
                { icon: '💥', title: 'Logical Errors', desc: 'Prompts contain impossible combinations or contradictions' }
            ]
        }
    },
    'internal-comms': {
        en: {
            headline: 'Professional Internal Communications',
            why: 'Write status reports, leadership updates, project announcements, and newsletters in your company\'s preferred format. Communicate clearly and professionally.',
            painPoints: [
                { icon: '🔥', title: 'Format Struggle', desc: 'Don\'t know your company\'s internal comms standards?' },
                { icon: '🧠', title: 'Tone Balance', desc: 'Too formal? Too casual? Hard to strike the right note' },
                { icon: '💥', title: 'Template Fatigue', desc: 'Writing the same types of updates over and over' }
            ]
        }
    },
    'mcp-builder': {
        en: {
            headline: 'Build MCP Servers with Ease',
            why: 'Create high-quality Model Context Protocol servers to connect Claude with external tools and APIs. Comprehensive guide for Python and TypeScript.',
            painPoints: [
                { icon: '🔥', title: 'MCP Learning Curve', desc: 'New to MCP? Documentation is scattered and overwhelming' },
                { icon: '🧠', title: 'Tool Design', desc: 'Not sure how to structure your MCP tools effectively' },
                { icon: '💥', title: 'Best Practices', desc: 'Worried about creating insecure or poorly designed servers' }
            ]
        }
    },
    'notebooklm': {
        en: {
            headline: 'Query Your Knowledge Base with AI',
            why: 'Search Google NotebookLM notebooks and get citation-backed answers from Gemini. Browser automation for library management and persistent auth.',
            painPoints: [
                { icon: '🔥', title: 'Information Silos', desc: 'Your notes are scattered across multiple notebooks' },
                { icon: '🧠', title: 'Manual Search', desc: 'Scrolling through hundreds of notebook pages to find information' },
                { icon: '💥', title: 'AI Hallucinations', desc: 'Chatbots make things up—notebook LM is source-grounded' }
            ]
        }
    },
    'pdf': {
        en: {
            headline: 'Complete PDF Manipulation Toolkit',
            why: 'Extract text and tables, create new PDFs, merge/split documents, fill forms programmatically. Process, generate, and analyze PDFs at scale.',
            painPoints: [
                { icon: '🔥', title: 'Manual Processing', desc: 'Filling out 100 PDF forms by hand? No thanks' },
                { icon: '🧠', title: 'Text Extraction', desc: 'Copying text from PDFs loses formatting and tables' },
                { icon: '💥', title: 'Document Assembly', desc: 'Merging PDFs while preserving bookmarks and formatting' }
            ]
        }
    },
    'pptx': {
        en: {
            headline: 'Presentation Creation and Editing',
            why: 'Create, edit, and analyze PowerPoint presentations. Modify content, adjust layouts, add speaker notes, and work with presentation files.',
            painPoints: [
                { icon: '🔥', title: 'Template Fatigue', desc: 'Starting from a blank slide deck every time' },
                { icon: '🧠', title: 'Layout Consistency', desc: 'Slides have different fonts, colors, and styles' },
                { icon: '💥', title: 'Bulk Editing', desc: 'Need to update the same content across 50 slides' }
            ]
        }
    },
    'product-master': {
        en: {
            headline: 'Professional Product Photography Prompts',
            why: 'Generate prompts for commercial product photography. From luxury watches to tech gadgets, create studio-quality product shots with expert lighting.',
            painPoints: [
                { icon: '🔥', title: 'Amateur Photos', desc: 'Your product shots look like they were taken with a phone' },
                { icon: '🧠', title: 'Lighting Knowledge', desc: 'Don\'t know softbox from rim light?' },
                { icon: '💥', title: 'Studio Setup', desc: 'Can\'t afford professional equipment and studio space' }
            ]
        }
    },
    'prompt-analyzer': {
        en: {
            headline: 'Deep Insights into Your Prompts',
            why: 'Analyze prompt details, compare variations, recommend similar prompts, and track element library statistics. Understand what makes prompts work.',
            painPoints: [
                { icon: '🔥', title: 'Prompt Mystery', desc: 'Some prompts work great, others fail—why?' },
                { icon: '🧠', title: 'A/B Testing', desc: 'No systematic way to compare prompt variations' },
                { icon: '💥', title: 'Knowledge Building', desc: 'Can\'t learn from your successful prompts' }
            ]
        }
    },
    'prompt-extractor': {
        en: {
            headline: 'Extract Reusable Patterns from Prompts',
            why: 'Analyze collections of prompts to extract modular structures. Build your own prompt library from successful examples and learn what makes them work.',
            painPoints: [
                { icon: '🔥', title: 'Prompt Chaos', desc: 'Thousands of prompts but no organization or insight' },
                { icon: '🧠', title: 'Pattern Discovery', desc: 'Manual analysis of prompt structures is time-consuming' },
                { icon: '💥', title: 'Reuse Difficulty', desc: 'Can\'t easily apply successful patterns to new prompts' }
            ]
        }
    },
    'prompt-generator': {
        en: {
            headline: 'Generate Prompts from Element Database',
            why: 'Create prompts using a curated database of elements. Access thousands of tested components for consistent, high-quality prompt generation.',
            painPoints: [
                { icon: '🔥', title: 'Vocabulary Limits', desc: 'Running out of new words and phrases for prompts' },
                { icon: '🧠', title: 'Inconsistent Quality', desc: 'Some prompts are great, others miss the mark' },
                { icon: '💥', title: 'Element Discovery', desc: 'Don\'t know which combinations work well together' }
            ]
        }
    },
    'prompt-master': {
        en: {
            headline: 'Master Controller for All Prompt Skills',
            why: 'Central controller that intelligently routes to the right prompt generation skill. Automatically selects the best tool based on your domain and requirements.',
            painPoints: [
                { icon: '🔥', title: 'Skill Overload', desc: 'Too many prompt skills—don\'t know which to use' },
                { icon: '🧠', title: 'Domain Confusion', desc: 'Portrait vs landscape vs product? Which skill handles this?' },
                { icon: '💥', title: 'Manual Routing', desc: 'Have to figure out the right skill yourself' }
            ]
        }
    },
    'prompt-xray': {
        en: {
            headline: 'Reverse Engineer Prompt Knowledge',
            why: 'Extract hidden knowledge from great prompts. Understand the "how-to" behind successful examples and make prompt techniques transparent.',
            painPoints: [
                { icon: '🔥', title: 'Black Box', desc: 'Great prompts work, but you don\'t know why' },
                { icon: '🧠', title: 'Technique Discovery', desc: 'Can\'t identify the patterns that make prompts successful' },
                { icon: '💥', title: 'Knowledge Transfer', desc: 'Hard to apply learnings from one prompt to another' }
            ]
        }
    },
    'skill-creator': {
        en: {
            headline: 'Create Effective Claude Code Skills',
            why: 'Comprehensive guide for building custom skills. Learn best practices, avoid common pitfalls, and create skills that integrate seamlessly with Claude Code.',
            painPoints: [
                { icon: '🔥', title: 'Getting Started', desc: 'Want to create a skill but don\'t know where to begin?' },
                { icon: '🧠', title: 'Documentation', desc: 'Unclear what makes a skill effective vs. broken' },
                { icon: '💥', title: 'Best Practices', desc: 'Reinventing the wheel—making avoidable mistakes' }
            ]
        }
    },
    'slack-gif-creator': {
        en: {
            headline: 'Create Animated GIFs for Slack',
            why: 'Design attention-grabbing GIFs optimized for Slack. Understand constraints, validation tools, and animation concepts for team communication.',
            painPoints: [
                { icon: '🔥', title: 'File Size Limits', desc: 'GIFs are too large to upload to Slack' },
                { icon: '🧠', title: 'Animation Ideas', desc: 'Don\'t know what kind of animations work well' },
                { icon: '💥', title: 'Loop Issues', desc: 'GIFs don\'t loop smoothly or have jarring transitions' }
            ]
        }
    },
    'theme-factory': {
        en: {
            headline: 'Style Artifacts with Beautiful Themes',
            why: 'Apply 10 pre-built themes to any artifact. Or create custom themes with complete color palettes and font pairings for consistent design.',
            painPoints: [
                { icon: '🔥', title: 'Design Inconsistency', desc: 'Each artifact has different colors and fonts' },
                { icon: '🧠', title: 'Color Theory', desc: 'Not sure which colors work well together?' },
                { icon: '💥', title: 'Theme Management', desc: 'Hard to maintain design consistency across multiple outputs' }
            ]
        }
    },
    'ui-check': {
        en: {
            headline: 'Opinionated Constraints for Better UI',
            why: 'Design principles and constraints for building interfaces. Avoid common pitfalls and create better user experiences with proven patterns.',
            painPoints: [
                { icon: '🔥', title: 'Design Decisions', desc: 'Too many choices—analysis paralysis' },
                { icon: '🧠', title: 'UX Mistakes', desc: 'Making the same usability errors over and over' },
                { icon: '💥', title: 'Inconsistency', desc: 'Different parts of your UI look and behave differently' }
            ]
        }
    },
    'ui-ux-pro-max': {
        en: {
            headline: 'Professional UI/UX Design Intelligence',
            why: '50 design styles, 21 color palettes, 20 font pairings, and expert guidance for building interfaces. Plan, build, and review web UI and applications.',
            painPoints: [
                { icon: '🔥', title: 'Design Overwhelm', desc: 'So many options—don\'t know where to start' },
                { icon: '🧠', title: 'Taste Gap', desc: 'Know what good design looks like but can\'t create it' },
                { icon: '💥', title: 'Inconsistent Results', desc: 'Some projects look great, others... not so much' }
            ]
        }
    },
    'universal-learner': {
        en: {
            headline: 'Learn from Any Prompt Collection',
            why: 'Universal learner extracts reusable elements from prompts in any domain. Continuously learn and build knowledge from any prompt collection.',
            painPoints: [
                { icon: '🔥', title: 'Domain Specificity', desc: 'Have prompts from different fields—can\'t find universal patterns' },
                { icon: '🧠', title: 'Knowledge Silos', desc: 'Learning is trapped in specific prompt collections' },
                { icon: '💥', title: 'Cross-Domain', desc: 'Can\'t apply learnings from one domain to another' }
            ]
        }
    },
    'video-master': {
        en: {
            headline: 'Video Generation Prompt Controller',
            why: 'Generate prompts for dynamic video scenes with camera movements, transitions, and effects. Create cinematic content with expert video terminology.',
            painPoints: [
                { icon: '🔥', title: 'Static Prompts', desc: 'Your video prompts describe images, not motion' },
                { icon: '🧠', title: 'Camera Language', desc: 'Don\'t know the difference between pan, tilt, and dolly?' },
                { icon: '💥', title: 'Cinematic Quality', desc: 'Generated videos feel amateur and lack production value' }
            ]
        }
    },
    'web-artifacts-builder': {
        en: {
            headline: 'Build Complex HTML Artifacts',
            why: 'Create elaborate multi-component Claude artifacts using modern web technologies. Supports React, Tailwind CSS, and shadcn/ui for complex interfaces.',
            painPoints: [
                { icon: '🔥', title: 'State Management', desc: 'Your artifacts are static and can\'t handle interaction' },
                { icon: '🧠', title: 'Component Libraries', desc: 'Not sure how to use shadcn/ui or Tailwind effectively?' },
                { icon: '💥', title: 'Complexity Limits', desc: 'Simple HTML isn\'t enough for your use case' }
            ]
        }
    },
    'web_style': {
        en: {
            headline: '21 Website Design Styles in One Place',
            why: 'Choose from 21 carefully designed front-end styles. Generate complete website code with selected design system instantly.',
            painPoints: [
                { icon: '🔥', title: 'Style Exploration', desc: 'Don\'t know what style fits your project?' },
                { icon: '🧠', title: 'Starting from Scratch', desc: 'Building design systems from zero is time-consuming' },
                { icon: '💥', title: 'Consistency', desc: 'Hard to maintain design consistency across pages' }
            ]
        }
    },
    'webapp-testing': {
        en: {
            headline: 'Test Local Web Applications with Playwright',
            why: 'Verify frontend functionality, debug UI behavior, capture browser screenshots, and view browser logs. Comprehensive testing toolkit for local development.',
            painPoints: [
                { icon: '🔥', title: 'Manual Testing', desc: 'Clicking through every feature before deployment is tedious' },
                { icon: '🧠', title: 'Visual Bugs', desc: 'UI breaks in certain browsers or screen sizes' },
                { icon: '💥', title: 'Debugging', desc: 'Can\'t see what\'s happening in the browser during tests' }
            ]
        }
    },
    'xlsx': {
        en: {
            headline: 'Complete Spreadsheet Toolkit',
            why: 'Create, edit, and analyze spreadsheets with formulas, formatting, and data analysis. Handle .xlsx, .xlsm, .csv files with full support.',
            painPoints: [
                { icon: '🔥', title: 'Manual Data Entry', desc: 'Typing data into spreadsheets cell by cell' },
                { icon: '🧠', title: 'Formula Errors', desc: 'Excel formulas break and are hard to debug' },
                { icon: '💥', title: 'Batch Processing', desc: 'Need to update 100 spreadsheets with the same change' }
            ]
        }
    },
    'z-image': {
        en: {
            headline: 'Generate Images with ModelScope API',
            why: 'Z-Image skill uses ModelScope API for AI image generation with async polling and automatic download. Reliable image generation workflow.',
            painPoints: [
                { icon: '🔥', title: 'API Complexity', desc: 'Handling async image generation is tricky' },
                { icon: '🧠', title: 'Polling Logic', desc: 'Don\'t know how to check if generation is complete?' },
                { icon: '💥', title: 'Error Handling', desc: 'Generation fails silently—no way to retry or debug' }
            ]
        }
    }
};

// Internationalization
const I18N = {
    en: {
        skills: 'Skills',
        onThisPage: 'On This Page',
        installation: 'Installation',
        installDesc: 'The easiest way to install:',
        addMarketplace: 'Add marketplace',
        installSkills: 'Install skills',
        moreOptions: 'More installation options',
        loading: 'Loading skill documentation...',
        selectSkill: 'Select a skill to view its documentation'
    },
    'zh-CN': {
        skills: '技能',
        onThisPage: '本页目录',
        installation: '安装方法',
        installDesc: '最简单的安装方式：',
        addMarketplace: '添加市场',
        installSkills: '安装技能',
        moreOptions: '更多安装选项',
        loading: '正在加载技能文档...',
        selectSkill: '选择一个技能查看其文档'
    },
    ja: {
        skills: 'スキル',
        onThisPage: '目次',
        installation: 'インストール',
        installDesc: '最も簡単なインストール方法：',
        addMarketplace: 'マーケットプレイスを追加',
        installSkills: 'スキルをインストール',
        moreOptions: 'その他のインストールオプション',
        loading: 'スキルドキュメントを読み込んでいます...',
        selectSkill: 'ドキュメントを表示するスキルを選択してください'
    }
};

// Get docs URL for footer
function getDocsUrl() {
    const customDomain = null; // Can be configured in share-skill config
    if (customDomain) {
        return `https://${customDomain}/`;
    }
    return `https://${REPO_OWNER}.github.io/${REPO_NAME}/`;
}

// Render marketing section
function renderMarketingSection(skillName) {
    const marketing = SKILL_MARKETING[skillName];
    if (!marketing) return '';

    const content = marketing[currentLang] || marketing['en'];
    if (!content) return '';

    return `
        <div class="marketing-section">
            <h2 class="marketing-title">${content.headline}</h2>
            <p class="marketing-why">${content.why}</p>
            <div class="pain-points-grid">
                ${content.painPoints.map(point => `
                    <div class="pain-point-card glass">
                        <div class="pain-point-icon">${point.icon}</div>
                        <h3 class="pain-point-title">${point.title}</h3>
                        <p class="pain-point-desc">${point.desc}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Load skill content
async function loadSkill(skillName) {
    const content = document.getElementById('content');
    content.innerHTML = `<div class="loading">${I18N[currentLang].loading}</div>`;

    try {
        const response = await fetch(getBasePath(skillName, currentLang));
        if (!response.ok) {
            throw new Error('Failed to load skill documentation');
        }

        const markdown = await response.text();

        // Render marketing section first
        const marketing = renderMarketingSection(skillName);

        // Parse markdown
        const html = marked.parse(markdown);

        content.innerHTML = marketing + html;

        // Apply syntax highlighting
        document.querySelectorAll('#content pre code').forEach((block) => {
            hljs.highlightElement(block);
        });

        // Reinitialize Tocbot
        tocbot.init({
            tocSelector: '.js-toc',
            contentSelector: '.js-toc-content',
            headingSelector: 'h1, h2, h3',
            scrollSmooth: true,
            scrollSmoothDuration: 300,
            headingsOffset: 100,
            scrollSmoothOffset: -100
        });

        currentSkill = skillName;

        // Update active state in sidebar
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-skill') === skillName) {
                link.classList.add('active');
            }
        });

        // Update URL hash
        window.location.hash = skillName;

    } catch (error) {
        console.error('Error loading skill:', error);

        // Check if skill exists in SKILLS object
        const skill = SKILLS[skillName];
        if (skill && skill.description) {
            // Show description as fallback
            const marketing = renderMarketingSection(skillName);
            const fallbackContent = `
                <div class="skill-description">
                    <h2>${skill.name}</h2>
                    <p class="lead">${skill.description}</p>
                    <p><em>Note: Full documentation (SKILL.md) is not available for this skill yet. You can still install and use it - see the installation instructions on the right.</em></p>
                </div>
            `;
            content.innerHTML = marketing + fallbackContent;
        } else {
            // Show error message
            content.innerHTML = `
                <div class="error-message">
                    <h2>Unable to Load Skill</h2>
                    <p>Could not load documentation for <strong>${skillName}</strong>.</p>
                    <p><a href="https://github.com/${REPO_OWNER}/${REPO_NAME}" target="_blank">View on GitHub</a></p>
                </div>
            `;
        }
    }
}

// Populate skills list
function populateSkillsList() {
    const sidebarSkills = document.getElementById('sidebarSkills');
    const mobileMenuSkills = document.getElementById('mobileMenuSkills');

    const skillsHtml = Object.values(SKILLS).map(skill => `
        <a class="sidebar-link" href="#${skill.name}" data-skill="${skill.name}">
            ${skill.name}
        </a>
    `).join('');

    if (sidebarSkills) {
        sidebarSkills.innerHTML = skillsHtml;
    }

    if (mobileMenuSkills) {
        mobileMenuSkills.innerHTML = skillsHtml;
    }

    // Add click handlers
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const skillName = link.getAttribute('data-skill');
            loadSkill(skillName);

            // Close mobile menu if open
            document.getElementById('mobileMenu').classList.remove('active');
        });
    });
}

// Update UI language
function updateLanguage(lang) {
    currentLang = lang;

    // Update lang label
    document.querySelector('.lang-label').textContent = lang.toUpperCase();

    // Update i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (I18N[lang] && I18N[lang][key]) {
            el.textContent = I18N[lang][key];
        }
    });

    // Reload current skill if any
    if (currentSkill) {
        loadSkill(currentSkill);
    }
}

// Initialize GitHub user info
async function initGitHubUserInfo() {
    const repoLink = document.getElementById('repoLink');
    const userAvatar = document.getElementById('userAvatar');
    const favicon = document.getElementById('favicon');
    const footerLink = document.getElementById('footerLink');

    if (repoLink) {
        repoLink.href = `https://github.com/${REPO_OWNER}/${REPO_NAME}`;
    }

    if (footerLink) {
        footerLink.href = getDocsUrl();
        footerLink.textContent = `${REPO_OWNER}'s skills`;
    }

    try {
        const response = await fetch(`https://api.github.com/users/${REPO_OWNER}`);
        if (response.ok) {
            const user = await response.json();

            if (userAvatar && user.avatar_url) {
                userAvatar.src = user.avatar_url;
            }

            if (favicon && user.avatar_url) {
                favicon.href = user.avatar_url;
            }
        }
    } catch (error) {
        console.error('Error fetching GitHub user info:', error);
    }
}

// Initialize mobile menu
function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuClose = document.getElementById('mobileMenuClose');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('active');
        });
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
    }

    // Close menu when clicking outside
    mobileMenu.addEventListener('click', (e) => {
        if (e.target === mobileMenu) {
            mobileMenu.classList.remove('active');
        }
    });
}

// Initialize language toggle
function initLanguageToggle() {
    const langToggle = document.getElementById('langToggle');
    const langs = ['en', 'zh-CN', 'ja'];
    let currentIndex = 0;

    if (langToggle) {
        langToggle.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % langs.length;
            updateLanguage(langs[currentIndex]);
        });
    }
}

// Handle URL hash on load
function handleInitialHash() {
    const hash = window.location.hash.slice(1); // Remove #
    if (hash && SKILLS[hash]) {
        loadSkill(hash);
    } else {
        // Load first skill by default
        const firstSkill = Object.keys(SKILLS)[0];
        loadSkill(firstSkill);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initGitHubUserInfo();
    populateSkillsList();
    initMobileMenu();
    initLanguageToggle();
    handleInitialHash();
});
