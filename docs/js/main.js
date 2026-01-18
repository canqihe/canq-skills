// Repository configuration
const REPO_OWNER = 'canqihe';
const REPO_NAME = 'canq-skills';
const BRANCH = 'master';
const CACHE_VERSION = '1737283200';

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
    'ui-skills': {
        name: 'ui-skills',
        description: 'Opinionated constraints for building interfaces',
        path: 'ui-skills'
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
        content.innerHTML = `
            <div class="error-message">
                <h2>Unable to Load Skill</h2>
                <p>Could not load documentation for <strong>${skillName}</strong>. This might be because:</p>
                <ul>
                    <li>The skill doesn't have a SKILL.md file</li>
                    <li>The file path is incorrect</li>
                    <li>Network error accessing GitHub</li>
                </ul>
                <p><a href="https://github.com/${REPO_OWNER}/${REPO_NAME}" target="_blank">View on GitHub</a></p>
            </div>
        `;
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
