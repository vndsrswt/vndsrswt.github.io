const toolData = [
    {
        category: "Development",
        links: [
            { name: "GitHub", url: "https://github.com", description: "Source code hosting and collaboration." },
            { name: "MDN Web Docs", url: "https://developer.mozilla.org", description: "Resources for developers by developers." },
            { name: "Stack Overflow", url: "https://stackoverflow.com", description: "Q&A for professional and enthusiast programmers." },
            { name: "Can I Use", url: "https://caniuse.com", description: "Browser support tables for modern web technologies." }
        ]
    },
    {
        category: "Design",
        links: [
            { name: "Figma", url: "https://figma.com", description: "Collaborative interface design tool." },
            { name: "Coolors", url: "https://coolors.co", description: "The super fast color palettes generator." },
            { name: "Unsplash", url: "https://unsplash.com", description: "Beautiful, free images and photos." },
            { name: "Lucide Icons", url: "https://lucide.dev", description: "Beautiful & consistent icon toolkit." }
        ]
    },
    {
        category: "AI",
        links: [
            { name: "ChatGPT", url: "https://chat.openai.com", description: "Conversational AI by OpenAI." },
            { name: "Claude", url: "https://claude.ai", description: "Anthropic's helpful, harmless AI." },
            { name: "Perplexity", url: "https://perplexity.ai", description: "AI-powered search engine." }
        ]
    },
    {
        category: "Office",
        links: [
            { name: "Google Drive", url: "https://drive.google.com", description: "Cloud storage and file synchronization." },
            { name: "Notion", url: "https://notion.so", description: "The all-in-one workspace." },
            { name: "Outlook", url: "https://outlook.live.com", description: "Personal email and calendar." }
        ]
    },
    {
        category: "Personal",
        links: [
            { name: "YouTube", url: "https://youtube.com", description: "Video sharing platform." },
            { name: "Reddit", url: "https://reddit.com", description: "Network of communities based on interests." },
            { name: "Pocket", url: "https://getpocket.com", description: "Save articles and videos for later." }
        ]
    }
];

const projectData = [
    {
        title: "E-Commerce Platform",
        description: "A full-featured online store built with React and Node.js. Features include product management, shopping cart, and secure checkout.",
        tech: ["React", "Node.js", "MongoDB", "Stripe"],
        link: "#"
    },
    {
        title: "Task Management App",
        description: "A productivity tool to help teams collaborate on projects. Includes real-time updates and intuitive task tracking.",
        tech: ["Vue.js", "Firebase", "Tailwind CSS"],
        link: "#"
    },
    {
        title: "Weather Dashboard",
        description: "A sleek weather application providing real-time forecasts and historical weather data using open-source APIs.",
        tech: ["JavaScript", "OpenWeatherMap API", "CSS Grid"],
        link: "#"
    }
];

const dashboard = document.getElementById('dashboard');
const projectsGrid = document.getElementById('projects-grid');
const searchInput = document.getElementById('searchInput');

function renderProjects() {
    projectsGrid.innerHTML = '';
    
    projectData.forEach(project => {
        const card = document.createElement('div');
        card.className = 'project-card';
        
        card.innerHTML = `
            <div class="project-img-placeholder"></div>
            <div class="project-info">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="tech-stack">
                    ${project.tech.map(t => `<span class="tech-tag">${t}</span>`).join('')}
                </div>
                <a href="${project.link}" class="project-link">View Project →</a>
            </div>
        `;
        
        projectsGrid.appendChild(card);
    });
}

function renderDashboard(data) {
    dashboard.innerHTML = '';
    
    if (data.length === 0) {
        dashboard.innerHTML = '<div class="loading">No tools found matching your search.</div>';
        return;
    }

    data.forEach(categoryObj => {
        const card = document.createElement('div');
        card.className = 'card';
        
        const title = document.createElement('h2');
        title.className = 'card-title';
        title.textContent = categoryObj.category;
        card.appendChild(title);
        
        const list = document.createElement('ul');
        list.className = 'link-list';
        
        categoryObj.links.forEach(link => {
            const item = document.createElement('li');
            item.className = 'link-item';
            
            const anchor = document.createElement('a');
            anchor.href = link.url;
            anchor.target = "_blank";
            anchor.rel = "noopener noreferrer";
            anchor.textContent = link.name;
            
            const desc = document.createElement('div');
            desc.className = 'link-description';
            desc.textContent = link.description;
            
            item.appendChild(anchor);
            item.appendChild(desc);
            list.appendChild(item);
        });
        
        card.appendChild(list);
        dashboard.appendChild(card);
    });
}

function filterTools(query) {
    const lowerQuery = query.toLowerCase();
    
    const filteredData = toolData.map(categoryObj => {
        if (categoryObj.category.toLowerCase().includes(lowerQuery)) {
            return categoryObj;
        }
        
        const matchedLinks = categoryObj.links.filter(link => 
            link.name.toLowerCase().includes(lowerQuery) || 
            link.description.toLowerCase().includes(lowerQuery)
        );
        
        if (matchedLinks.length > 0) {
            return {
                ...categoryObj,
                links: matchedLinks
            };
        }
        
        return null;
    }).filter(item => item !== null);
    
    renderDashboard(filteredData);
}

// Event Listeners
searchInput.addEventListener('input', (e) => {
    filterTools(e.target.value);
});

// Sidebar Logic
const sidebarToggle = document.getElementById('sidebarToggle');
const collapseBtn = document.getElementById('collapseBtn');
const sidebar = document.getElementById('sidebar');
const submenuToggles = document.querySelectorAll('.submenu-toggle');
const navLinks = document.querySelectorAll('.sidebar-nav a:not(.submenu-toggle)');

// Mobile Toggle
sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    sidebarToggle.classList.toggle('active');
});

// Desktop Collapse
collapseBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    
    // Close all submenus when collapsing
    if (sidebar.classList.contains('collapsed')) {
        document.querySelectorAll('.has-submenu').forEach(el => el.classList.remove('open'));
    }
});

// Multilevel Submenu Toggle
submenuToggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent bubbling to parent menus
        
        if (sidebar.classList.contains('collapsed')) {
            sidebar.classList.remove('collapsed');
        }
        
        const parent = toggle.closest('.has-submenu');
        const isOpen = parent.classList.contains('open');
        
        // Close siblings at the same level
        const siblingSubmenus = parent.parentElement.querySelectorAll(':scope > .has-submenu');
        siblingSubmenus.forEach(el => {
            if (el !== parent) el.classList.remove('open');
        });
        
        // Toggle current
        parent.classList.toggle('open');
    });
});

// Close mobile sidebar and handle active states
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarToggle.classList.remove('active');
        
        // Update active link
        document.querySelectorAll('.sidebar-nav a').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Initial Render
document.addEventListener('DOMContentLoaded', () => {
    renderProjects();
    renderDashboard(toolData);
});
