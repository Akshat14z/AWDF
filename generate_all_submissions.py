import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

STUDENT_NAME = "Akshat Patel"
STUDENT_ID = "24CS060"
ACADEMIC_YEAR = "2025-26"
SUBJECT_CODE_NAME = "ITUE301 - Advanced Web Development Framework"
REPO_LINK = "https://github.com/Akshat14z/AWDF.git"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 9)
        self.setFillColor(colors.HexColor('#222222'))
        
        # --- Top Header ---
        self.drawString(54, 755, SUBJECT_CODE_NAME)
        self.drawRightString(558, 755, STUDENT_ID)
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)
        
        # --- Bottom Footer ---
        self.line(54, 48, 558, 48)
        self.drawString(54, 34, 'Department of Computer Science and Engineering, CSPIT')
        self.drawRightString(558, 34, f'Page {self._pageNumber}')
        self.restoreState()

def get_custom_styles():
    base = getSampleStyleSheet()
    styles = {
        'Normal': ParagraphStyle('CustomNormal', parent=base['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#222222')),
        'MetaCell': ParagraphStyle('MetaCell', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#111111')),
        'MetaCellBold': ParagraphStyle('MetaCellBold', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#111111')),
        'TaskTitle': ParagraphStyle('TaskTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=colors.HexColor('#111111')),
        'SectionHeader': ParagraphStyle('SectionHeader', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#111111'), spaceBefore=10, spaceAfter=4),
        'SubHeader': ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=10.5, leading=15, textColor=colors.HexColor('#1F2937'), spaceBefore=8, spaceAfter=3),
        'CodeText': ParagraphStyle('CodeText', fontName='Courier', fontSize=8, leading=11, textColor=colors.HexColor('#111827')),
        'Question': ParagraphStyle('Question', fontName='Helvetica-Bold', fontSize=9.5, leading=14, textColor=colors.HexColor('#111827'), spaceBefore=6, spaceAfter=2),
        'Answer': ParagraphStyle('Answer', fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#2E384D'), spaceBefore=2, spaceAfter=8),
        'ResultText': ParagraphStyle('ResultText', fontName='Helvetica', fontSize=9.5, leading=14.5, textColor=colors.HexColor('#1F2937')),
    }
    return styles

PRACTICAL_STEP_IMAGES = {
    1: ["step_1.png", "step_2.png"],
    2: ["step_1.png", "step_2.png"],
    3: ["step_1.png", "step_2.png"],
    4: ["step_1.png", "step_2.png"],
    5: ["terminal_startup.png", "step_3.jpeg", "step_9.jpeg"],
    6: ["step_4.jpeg", "step_5.jpeg", "step_6.jpeg"],
    7: ["step_12.jpeg", "step_15.jpeg", "step_17.jpeg"],
    8: ["step_1.jpeg", "step_6.jpeg", "step_9.jpeg"],
    9: ["step_5.jpeg", "step_8.jpeg", "step_14.jpeg"],
    10: ["terminal_startup.png", "step_2.jpeg", "step_4.jpeg"],
    11: ["step_1.png", "step_2.png"],
    12: ["step_1.png", "step_2.png"],
    13: ["step_1.png", "step_2.png"]
}

def build_practical_pdf(prac_num, data, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = get_custom_styles()
    story = []

    # 1. Metadata Box Table on Page 1
    col_widths = [80, 172, 90, 162]
    table_data = [
        [
            Paragraph("<b>Student ID:</b>", styles['MetaCellBold']),
            Paragraph(STUDENT_ID, styles['MetaCell']),
            Paragraph("<b>Student Name:</b>", styles['MetaCellBold']),
            Paragraph(STUDENT_NAME, styles['MetaCell'])
        ],
        [
            Paragraph("<b>Subject:</b>", styles['MetaCellBold']),
            Paragraph(SUBJECT_CODE_NAME, styles['MetaCell']),
            Paragraph("<b>Practical / Year:</b>", styles['MetaCellBold']),
            Paragraph(f"Practical : {prac_num}<br/>Academic Year: {ACADEMIC_YEAR}", styles['MetaCell'])
        ]
    ]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#333333')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#AAAAAA')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8F9FA')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#F8F9FA')),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # 2. Task title & Aim
    story.append(Paragraph(f"Task - {prac_num}", styles['TaskTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Aim", styles['SectionHeader']))
    story.append(Paragraph(data['aim'], styles['Normal']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Code & Repository Reference", styles['SectionHeader']))
    repo_info = (
        f"<b>GitHub Repository:</b> <font color='#2563EB'><u>{REPO_LINK}</u></font><br/>"
        f"<b>Practical Directory:</b> <code>practical-{prac_num}/</code>"
    )
    story.append(Paragraph(repo_info, styles['Normal']))
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # 3. Implementation Steps & Code
    story.append(Paragraph("Implementation & Execution Details", styles['SectionHeader']))
    story.append(Spacer(1, 6))

    for s_idx, step in enumerate(data['steps'], 1):
        step_flowables = [Paragraph(step['title'], styles['SubHeader'])]
        if 'desc' in step and step['desc']:
            step_flowables.append(Paragraph(step['desc'], styles['Normal']))
            step_flowables.append(Spacer(1, 4))

        # Check for designated clean screenshot in submission/screenshots/prac{prac_num}/
        preferred_img = None
        if prac_num in PRACTICAL_STEP_IMAGES and s_idx <= len(PRACTICAL_STEP_IMAGES[prac_num]):
            preferred_name = PRACTICAL_STEP_IMAGES[prac_num][s_idx - 1]
            candidate_path = f"submission/screenshots/prac{prac_num}/{preferred_name}"
            if os.path.exists(candidate_path):
                preferred_img = candidate_path

        if not preferred_img:
            img_candidates = [
                f"submission/screenshots/prac{prac_num}/step_{s_idx}.png",
                f"submission/screenshots/prac{prac_num}/step_{s_idx}.jpeg",
                f"submission/screenshots/prac{prac_num}/step_{s_idx}.jpg",
            ]
            for cand in img_candidates:
                if os.path.exists(cand):
                    preferred_img = cand
                    break

        found_img = preferred_img

        if found_img:
            try:
                from PIL import Image as PILImage
                pil_im = PILImage.open(found_img)
                w, h = pil_im.size
                aspect = h / w
                target_w = 480
                target_h = min(210, target_w * aspect)
                img_flow = RLImage(found_img, width=target_w, height=target_h)
                img_frame = Table([[img_flow]], colWidths=[504])
                img_frame.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
                    ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('LEFTPADDING', (0, 0), (-1, -1), 3),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ]))
                step_flowables.append(Spacer(1, 4))
                step_flowables.append(img_frame)
                step_flowables.append(Spacer(1, 6))
            except Exception as e:
                print(f"Error loading image {found_img}: {e}")

        if 'code' in step and step['code']:
            code_lines = step['code'].strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')
            code_para = Paragraph(f"<code>{code_lines}</code>", styles['CodeText'])
            code_table = Table([[code_para]], colWidths=[504])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
                ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            step_flowables.append(code_table)
            step_flowables.append(Spacer(1, 8))

        story.extend(step_flowables)

    # 4. Supplementary / Analysis section
    if 'supplementary' in data and data['supplementary']:
        story.append(Spacer(1, 6))
        story.append(Paragraph("Supplementary Problem & Observations", styles['SectionHeader']))
        for item in data['supplementary']:
            story.append(Paragraph(f"• <b>{item['label']}:</b> {item['detail']}", styles['Normal']))
            story.append(Spacer(1, 4))

    story.append(PageBreak())

    # 5. Key Questions & Answers
    story.append(Paragraph("Key Questions:", styles['SectionHeader']))
    story.append(Spacer(1, 6))
    for idx, qa in enumerate(data['questions'], 1):
        q_text = f"{idx}. {qa['q']}"
        story.append(Paragraph(q_text, styles['Question']))
        story.append(Paragraph(qa['a'], styles['Answer']))

    # 6. Result
    story.append(Spacer(1, 10))
    story.append(Paragraph("Result:", styles['SectionHeader']))
    story.append(Paragraph(data['result'], styles['ResultText']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {output_path}")

PRACTICALS_DATA = {
    1: {
        "aim": "To set up a React development environment using Vite and build a static UI using independently structured, reusable components.",
        "steps": [
            {
                "title": "1.1 Project Scaffolding and Dependencies",
                "desc": "The React application is scaffolded using Vite with the standard React template. Vite provides fast Hot Module Replacement (HMR) and an optimized development server.",
                "code": "# Terminal setup\nnpm create vite@latest practical-1 -- --template react\ncd practical-1\nnpm install\nnpm run dev    # Starts on http://localhost:5173"
            },
            {
                "title": "1.2 Header Component (src/components/Header.jsx)",
                "desc": "Displays the portfolio owner's name and role using styled semantic header elements.",
                "code": "export default function Header() {\n  return (\n    <header className=\"header\">\n      <h1>Akshat Patel</h1>\n      <p className=\"tagline\">Computer Science & Engineering Student | Full Stack Developer</p>\n    </header>\n  );\n}"
            },
            {
                "title": "1.3 About Component (src/components/About.jsx)",
                "desc": "Renders introductory biographical information explaining areas of interest and background.",
                "code": "export default function About() {\n  return (\n    <section className=\"about\">\n      <h2>About Me</h2>\n      <p>I am a passionate software developer specializing in modern web frameworks, cloud architecture, and microservices.</p>\n    </section>\n  );\n}"
            },
            {
                "title": "1.4 Skills Component with Props (src/components/Skills.jsx)",
                "desc": "Accepts a skillList array prop and renders dynamic skill chips using array mapping.",
                "code": "export default function Skills({ skillList }) {\n  return (\n    <section className=\"skills\">\n      <h2>Technical Skills</h2>\n      <ul className=\"chips\">\n        {skillList.map((skill, index) => (\n          <li key={index}>{skill}</li>\n        ))}\n      </ul>\n    </section>\n  );\n}"
            },
            {
                "title": "1.5 Main Application Composition (src/App.jsx)",
                "desc": "Assembles Header, About, Skills, and Footer components into a unified interface.",
                "code": "import Header from './components/Header';\nimport About from './components/About';\nimport Skills from './components/Skills';\nimport Footer from './components/Footer';\n\nconst skillsData = ['React', 'JavaScript (ES6+)', 'Node.js', 'Express', 'MongoDB', 'Docker', 'Vite'];\n\nexport default function App() {\n  return (\n    <div className=\"container\">\n      <Header />\n      <About />\n      <Skills skillList={skillsData} />\n      <Footer />\n    </div>\n  );\n}"
            }
        ],
        "supplementary": [
            {"label": "NavBar Component", "detail": "Implemented a clean sticky navigation bar highlighting active sections."},
            {"label": "Passed Complex Data via Props", "detail": "Passed an array of skill objects with categorization (Frontend, Backend, Tools) to demonstrate nested prop drilling."}
        ],
        "questions": [
            {
                "q": "What is the role of each component in the overall UI structure?",
                "a": "In React's component-based architecture, each component serves as an independent, encapsulated building block with a single responsibility. Header presents primary identity, About provides biographical narrative, Skills serves as a reusable display engine driven entirely by external data via props, and Footer provides standard closing metadata and links. This modularity ensures high maintainability and testability."
            },
            {
                "q": "How does React re-render when props change?",
                "a": "React maintains a Virtual DOM tree. When a parent component updates and passes new prop values to a child component, React triggers a reconciliation cycle for that child component subtree. React compares the newly generated Virtual DOM representation against the previous snapshot. Only the minimal diff (the actual changed DOM nodes) is committed to the real browser DOM, ensuring high performance."
            },
            {
                "q": "Why is component reusability important in large-scale applications?",
                "a": "Component reusability avoids code duplication (DRY principle), standardizes UI behavior and styling across large engineering teams, drastically reduces testing overhead, and accelerates feature development since developers assemble pre-validated components rather than writing bespoke HTML/CSS repeatedly."
            }
        ],
        "result": "Successfully set up the Vite development environment and built a modular student portfolio application with reusable components (Header, About, Skills, Footer) and props data flow."
    },
    2: {
        "aim": "To implement reactive state management using useState and multi-page navigation using React Router in the existing portfolio application.",
        "steps": [
            {
                "title": "2.1 React Router Installation and Setup",
                "desc": "Configured BrowserRouter, Routes, and Route in the application root to enable client-side single page navigation.",
                "code": "# Terminal\nnpm install react-router-dom\n\n// src/main.jsx\nimport { BrowserRouter } from 'react-router-dom';\nReactDOM.createRoot(document.getElementById('root')).render(\n  <React.StrictMode>\n    <BrowserRouter>\n      <App />\n    </BrowserRouter>\n  </React.StrictMode>\n);"
            },
            {
                "title": "2.2 Navigation Bar (src/components/NavBar.jsx)",
                "desc": "Uses NavLink components to provide smooth page transitions without browser page reloads.",
                "code": "import { NavLink } from 'react-router-dom';\n\nexport default function NavBar() {\n  return (\n    <nav className=\"nav\">\n      <ul>\n        <li><NavLink to=\"/\" end>Home</NavLink></li>\n        <li><NavLink to=\"/contact\">Contact</NavLink></li>\n      </ul>\n    </nav>\n  );\n}"
            },
            {
                "title": "2.3 Interactive Form with useState (src/pages/Contact.jsx)",
                "desc": "Implements controlled form inputs with live validation, character counting, and submit state management using useState.",
                "code": "import { useState } from 'react';\n\nexport default function Contact() {\n  const [message, setMessage] = useState('');\n  const [submitted, setSubmitted] = useState(false);\n\n  return (\n    <section>\n      <h2>Contact Me</h2>\n      <textarea \n        value={message} \n        onChange={(e) => setMessage(e.target.value)} \n        maxLength={300}\n      />\n      <p>Characters: {message.length} / 300</p>\n    </section>\n  );\n}"
            },
            {
                "title": "2.4 404 Not Found Route (src/pages/NotFound.jsx)",
                "desc": "A catch-all wildcard route (*) that catches undefined URLs and provides a clear navigation recovery button.",
                "code": "import { Link } from 'react-router-dom';\nexport default function NotFound() {\n  return (\n    <div className=\"error-container\">\n      <h2>404 - Page Not Found</h2>\n      <Link to=\"/\" className=\"btn\">Return to Home</Link>\n    </div>\n  );\n}"
            }
        ],
        "supplementary": [
            {"label": "404 Wildcard Handling", "detail": "Implemented path='*' route rendering a dedicated NotFound component."},
            {"label": "Theme Toggle with State", "detail": "Added a light/dark mode state toggle modifying the root data-theme attribute dynamically."}
        ],
        "questions": [
            {
                "q": "What is the difference between client-side routing with React Router and traditional multi-page navigation?",
                "a": "Traditional navigation sends an HTTP request to the web server for every URL change, causing a complete page reload, asset re-parsing, and loss of client-side state. Client-side routing with React Router intercepts browser URL changes using the HTML5 History API (pushState/popState) and conditionally swaps active components in memory instantly without requesting a new HTML document from the server."
            },
            {
                "q": "How does React re-render when state changes compared to when props change?",
                "a": "State changes are initiated internally by the component itself calling its state updater function (e.g. setState), immediately scheduling a re-render of that component and its descendants. Prop changes are external updates initiated by a parent component re-rendering and passing new values down. Both ultimately invoke the reconciliation algorithm, but state is private and controlled locally while props are read-only inputs."
            },
            {
                "q": "Why is lifting state up or keeping state localized important in component hierarchies?",
                "a": "Localizing state keeps components decoupled, prevents unnecessary re-rendering of unrelated branches in the component tree, and makes debugging straightforward. When multiple sibling components need access to the same synchronized data, lifting state up to their nearest common ancestor establishes a single source of truth without polluting global state."
            }
        ],
        "result": "Successfully integrated React Router with client-side multi-page routing (Home, Contact, 404 Not Found) and reactive state management using useState hooks."
    },
    3: {
        "aim": "To consume a REST API in React and handle asynchronous data with loading and error states.",
        "steps": [
            {
                "title": "3.1 Component Architecture & State Definition (src/pages/Projects.jsx)",
                "desc": "Maintains three distinct state variables: data (projects), loading (boolean flag), and error (error message string).",
                "code": "import { useState, useEffect } from 'react';\n\nexport default function Projects() {\n  const [projects, setProjects] = useState([]);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n  // fetch logic...\n}"
            },
            {
                "title": "3.2 Data Fetching with useEffect and GitHub API",
                "desc": "Fetches public repository data from the GitHub REST API on initial component mount using an empty dependency array.",
                "code": "useEffect(() => {\n  const fetchProjects = async () => {\n    try {\n      setLoading(true);\n      setError(null);\n      const res = await fetch('https://api.github.com/users/Akshat14z/repos?sort=updated&per_page=6');\n      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);\n      const data = await res.json();\n      setProjects(data);\n    } catch (err) {\n      setError(err.message);\n    } finally {\n      setLoading(false);\n    }\n  };\n  fetchProjects();\n}, []);"
            },
            {
                "title": "3.3 Conditional State Rendering (Spinner & Error Message)",
                "desc": "Displays dedicated UI feedback for loading, network errors with a retry button, or the populated project grid.",
                "code": "if (loading) return <Spinner />;\nif (error) return <ErrorMessage message={error} onRetry={fetchProjects} />;\n\nreturn (\n  <div className=\"projects-grid\">\n    {projects.map((repo) => (\n      <div key={repo.id} className=\"card\">\n        <h3>{repo.name}</h3>\n        <p>{repo.description || 'No description provided.'}</p>\n        <span>Stars: {repo.stargazers_count}</span>\n      </div>\n    ))}\n  </div>\n);"
            }
        ],
        "supplementary": [
            {"label": "Manual Retry Mechanism", "detail": "Provided an onRetry callback button that re-triggers the async fetch upon network failure."},
            {"label": "Graceful Fallback Display", "detail": "Configured fallback mock projects when API rate limit (HTTP 403) is encountered."}
        ],
        "questions": [
            {
                "q": "Why is useEffect required to trigger a fetch on component mount instead of calling fetch directly in the component body?",
                "a": "Calling fetch directly in the component body triggers a side effect during the rendering phase. When the fetch resolves and updates state, it triggers a re-render, which immediately calls fetch again, producing an infinite network loop. useEffect runs after the render commit phase and, when given an empty dependency array `[]`, guarantees the asynchronous request executes exactly once upon mount."
            },
            {
                "q": "What is the difference between a loading state and an error state, and why must both be handled separately?",
                "a": "A loading state represents an in-progress asynchronous operation where data has not yet arrived; the UI must show a progress indicator to prevent user confusion. An error state indicates an abnormal failure (network offline, 404, rate limits) where the user must be informed of the failure cause and provided a recovery path (such as a Retry action)."
            },
            {
                "q": "How would the user experience change if an API call failed silently without an error boundary or message?",
                "a": "A silent failure leaves the UI frozen in a perpetual loading spinner or displaying an empty screen. The user has no indication whether the application is still processing, offline, or crashed, resulting in frustration and repeated unnecessary page refreshes."
            }
        ],
        "result": "Successfully consumed GitHub REST API in React using useEffect, properly displaying responsive loading spinners, error boundaries with retry mechanisms, and formatted project cards."
    },
    4: {
        "aim": "To design and implement a RESTful backend server with complete CRUD endpoints using Express middleware pipeline.",
        "steps": [
            {
                "title": "4.1 Server Setup and Middleware Pipeline (server.js)",
                "desc": "Express application setup configuring JSON body parsing, custom logging middleware, routes, and centralized error handling.",
                "code": "const express = require('express');\nconst logger = require('./middleware/logger');\nconst errorHandler = require('./middleware/errorHandler');\nconst notFound = require('./middleware/notFound');\nconst taskRoutes = require('./routes/tasks');\n\nconst app = express();\napp.use(express.json());\napp.use(logger);\n\napp.use('/tasks', taskRoutes);\napp.use(notFound);\napp.use(errorHandler);\n\nconst PORT = process.env.PORT || 5000;\napp.listen(PORT, () => console.log(`Server running on port ${PORT}`));"
            },
            {
                "title": "4.2 Request Logger Middleware (middleware/logger.js)",
                "desc": "Intercepts all incoming HTTP requests and outputs method, URL, timestamp, and duration.",
                "code": "module.exports = (req, res, next) => {\n  const start = Date.now();\n  res.on('finish', () => {\n    const duration = Date.now() - start;\n    console.log(`[${req.method}] ${req.originalUrl} ${res.statusCode} - ${duration}ms`);\n  });\n  next();\n};"
            },
            {
                "title": "4.3 In-Memory Task Controller (controllers/taskController.js)",
                "desc": "Implements REST CRUD operations using an encapsulated in-memory tasks array.",
                "code": "let tasks = [\n  { id: 1, title: 'Learn React', completed: true },\n  { id: 2, title: 'Build Express API', completed: false }\n];\n\nexports.getAllTasks = (req, res) => res.json(tasks);\n\nexports.createTask = (req, res) => {\n  const { title } = req.body;\n  if (!title) return res.status(400).json({ error: 'Title is required' });\n  const newTask = { id: Date.now(), title, completed: false };\n  tasks.push(newTask);\n  res.status(201).json(newTask);\n};\n\nexports.updateTask = (req, res) => {\n  const task = tasks.find(t => t.id === Number(req.params.id));\n  if (!task) return res.status(404).json({ error: 'Task not found' });\n  Object.assign(task, req.body);\n  res.json(task);\n};\n\nexports.deleteTask = (req, res) => {\n  const index = tasks.findIndex(t => t.id === Number(req.params.id));\n  if (index === -1) return res.status(404).json({ error: 'Task not found' });\n  tasks.splice(index, 1);\n  res.status(204).send();\n};"
            },
            {
                "title": "4.4 Centralized Error Handler (middleware/errorHandler.js)",
                "desc": "Standardizes error responses across all routes and ensures internal stack traces are hidden from clients.",
                "code": "module.exports = (err, req, res, next) => {\n  console.error(err.stack);\n  const status = err.statusCode || 500;\n  res.status(status).json({\n    error: err.message || 'Internal Server Error',\n    status\n  });\n};"
            }
        ],
        "supplementary": [
            {"label": "Content-Type Validation", "detail": "Added requireJson middleware rejecting POST/PUT requests lacking application/json headers."},
            {"label": "VS Code REST Client Tests", "detail": "Created tasks.http test script verifying all 4 CRUD routes and status codes (200, 201, 204, 400, 404)."}
        ],
        "questions": [
            {
                "q": "Why must the error handling middleware be defined last in the middleware chain?",
                "a": "Express executes middleware sequentially in the order registered via app.use(). When a route or middleware calls `next(err)`, Express bypasses all remaining standard middleware and searches downstream for the first middleware with four parameters `(err, req, res, next)`. If defined before route definitions, the error handler would never receive errors thrown by those routes."
            },
            {
                "q": "What is the difference between app.use() and a route-specific middleware?",
                "a": "`app.use()` registers global middleware that executes for every incoming request matching the path prefix across all HTTP verbs. Route-specific middleware is passed as an intermediate argument to a specific route handler (e.g. `router.post('/', requireJson, createTask)`), executing only for that exact endpoint and method."
            },
            {
                "q": "Why is it considered bad practice to send raw error stack traces to the client?",
                "a": "Sending raw stack traces exposes sensitive architectural details—including absolute server directory paths, database connection libraries, framework version numbers, and file names. Malicious actors exploit this intelligence to target specific vulnerabilities. Production error responses should return sanitized, consistent JSON error messages."
            }
        ],
        "result": "Successfully created a modular Express REST API supporting complete CRUD operations on tasks, logging middleware, JSON validation, and centralized error handling."
    },
    5: {
        "aim": "To connect a MongoDB database to an Express server and enforce data validation through Mongoose schema.",
        "steps": [
            {
                "title": "5.1 MongoDB Connection Setup (server.js)",
                "desc": "Initializes persistent connection to MongoDB using Mongoose with connection pooling and error listeners.",
                "code": "const mongoose = require('mongoose');\nrequire('dotenv').config();\n\nconst MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/practical5';\nmongoose.connect(MONGO_URI)\n  .then(() => console.log('MongoDB connected successfully'))\n  .catch(err => console.error('MongoDB connection error:', err));"
            },
            {
                "title": "5.2 Mongoose Task Schema (models/Task.js)",
                "desc": "Defines strict field schemas, type validations, required constraints, enums, and default timestamps.",
                "code": "const mongoose = require('mongoose');\n\nconst taskSchema = new mongoose.Schema({\n  title: {\n    type: String,\n    required: [true, 'Task title is required'],\n    trim: true,\n    maxlength: [100, 'Title cannot exceed 100 characters']\n  },\n  description: { type: String, trim: true },\n  completed: { type: Boolean, default: false },\n  priority: {\n    type: String,\n    enum: ['low', 'medium', 'high'],\n    default: 'medium'\n  },\n  createdAt: { type: Date, default: Date.now }\n});\n\nmodule.exports = mongoose.model('Task', taskSchema);"
            },
            {
                "title": "5.3 Controller Using Mongoose Methods (controllers/taskController.js)",
                "desc": "Replaces in-memory array operations with asynchronous Mongoose queries (find, create, findByIdAndUpdate, findByIdAndDelete).",
                "code": "const Task = require('../models/Task');\n\nexports.getAllTasks = async (req, res, next) => {\n  try {\n    const tasks = await Task.find().sort({ createdAt: -1 });\n    res.json(tasks);\n  } catch (err) { next(err); }\n};\n\nexports.createTask = async (req, res, next) => {\n  try {\n    const task = await Task.create(req.body);\n    res.status(201).json(task);\n  } catch (err) { next(err); }\n};\n\nexports.updateTask = async (req, res, next) => {\n  try {\n    const task = await Task.findByIdAndUpdate(req.params.id, req.body, {\n      new: true,\n      runValidators: true\n    });\n    if (!task) return res.status(404).json({ error: 'Task not found' });\n    res.json(task);\n  } catch (err) { next(err); }\n};"
            }
        ],
        "supplementary": [
            {"label": "Priority Enum Validation", "detail": "Configured schema enum validation restricting priority to 'low', 'medium', and 'high'."},
            {"label": "ObjectId Validation Middleware", "detail": "Implemented validateId middleware catching malformed 24-character hexadecimal MongoDB ObjectIds early with 400 Bad Request."}
        ],
        "questions": [
            {
                "q": "What is the purpose of a schema in a NoSQL database like MongoDB, given that MongoDB itself is schema-less?",
                "a": "While MongoDB natively allows arbitrary document structures within a collection, production enterprise applications require predictable data contracts. Mongoose schemas introduce an application-level enforcement layer guaranteeing required fields exist, data types are cast correctly, default values are assigned, and invalid documents are rejected before reaching the database engine."
            },
            {
                "q": "Why is it important to define required fields and default values at the schema level rather than relying on frontend validation alone?",
                "a": "Frontend validation is purely a client-side user experience convenience that can be trivially bypassed using tools like curl, Postman, or malicious script injections. Enforcing validations at the schema layer guarantees that no malformed or unverified data can ever be persisted, regardless of the API consumer."
            },
            {
                "q": "What happens internally when a document fails Mongoose validation where is the request stopped?",
                "a": "When `validate()` or model save/update executes, Mongoose evaluates document properties against schema validator functions in Node.js memory. If any constraint fails, Mongoose halts execution immediately, instantiates a `ValidationError` object, and rejects the promise. The database write operation is never issued over the network to MongoDB."
            }
        ],
        "result": "Successfully integrated MongoDB with Express via Mongoose, establishing validated schemas, automated timestamps, robust CRUD queries, and persistent document storage."
    },
    6: {
        "aim": "To wire the React frontend to the Node/Express/MongoDB backend into a fully functional full-stack application.",
        "steps": [
            {
                "title": "6.1 CORS Configuration in Express Backend (server.js)",
                "desc": "Configured Cross-Origin Resource Sharing (CORS) to allow requests from the Vite frontend development server.",
                "code": "const cors = require('cors');\napp.use(cors({\n  origin: ['http://localhost:5173', 'http://localhost:3006'],\n  methods: ['GET', 'POST', 'PUT', 'DELETE'],\n  credentials: true\n}));"
            },
            {
                "title": "6.2 API Client Layer (src/api.js)",
                "desc": "Centralized API abstraction using fetch with baseUrl handling, JSON headers, and error normalization.",
                "code": "const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5006';\n\nexport async function getTasks() {\n  const res = await fetch(`${API_URL}/tasks`);\n  if (!res.ok) throw new Error('Failed to fetch tasks');\n  return res.json();\n}\n\nexport async function createTask(task) {\n  const res = await fetch(`${API_URL}/tasks`, {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify(task)\n  });\n  if (!res.ok) throw new Error('Failed to create task');\n  return res.json();\n}"
            },
            {
                "title": "6.3 State Synchronization in Tasks Page (src/pages/Tasks.jsx)",
                "desc": "Manages tasks state, optimistic updates, deletion confirmations, and server re-sync.",
                "code": "export default function Tasks() {\n  const [tasks, setTasks] = useState([]);\n  \n  const handleCreate = async (taskData) => {\n    try {\n      const created = await createTask(taskData);\n      setTasks(prev => [created, ...prev]);\n      showToast('Task created successfully');\n    } catch (err) {\n      showToast(err.message, 'error');\n    }\n  };\n}"
            }
        ],
        "supplementary": [
            {"label": "Confirmation Dialog Component", "detail": "Built ConfirmDialog.jsx prompting the user before issuing DELETE HTTP requests."},
            {"label": "Toast Notification System", "detail": "Implemented Toast.jsx displaying transient success and error alerts across full-stack operations."}
        ],
        "questions": [
            {
                "q": "What changes are required on the backend (CORS) to allow the React dev server to call the Express API?",
                "a": "Browsers enforce the Same-Origin Policy, blocking web apps on one origin (e.g. `http://localhost:3006`) from reading HTTP responses from a different origin (e.g. `http://localhost:5006`). The Express backend must install the `cors` package and return appropriate `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers` response headers during preflight OPTIONS checks."
            },
            {
                "q": "Why should the UI re-fetch or update local state after a successful POST/PUT/DELETE rather than assuming success silently?",
                "a": "Client and server states must remain consistent. Mutating local state without waiting for server confirmation risks displaying ghost data if the network or database write fails. Conversely, updating state upon confirmation (or optimistic update with error rollback) guarantees the user immediately sees the authoritative database state, including server-generated fields like `_id` and `createdAt`."
            },
            {
                "q": "What is the risk of not handling errors on write operations (POST/PUT/DELETE) the same way as read operations (GET)?",
                "a": "Failing to handle write errors leaves the user with false confidence that their record was saved. In e-commerce, task managers, or financial systems, unhandled write errors lead to data loss, phantom state discrepancies, and broken workflows."
            }
        ],
        "result": "Successfully created a complete full-stack web application linking React with an Express/MongoDB backend, featuring live CRUD synchronization, CORS, and UI toast feedback."
    },
    7: {
        "aim": "To implement JWT-based authentication and input validation as part of the Express middleware pipeline.",
        "steps": [
            {
                "title": "7.1 User Model with Bcrypt Hashing (models/User.js)",
                "desc": "Defines User schema with salted bcrypt pre-save hook for one-way password hashing.",
                "code": "const mongoose = require('mongoose');\nconst bcrypt = require('bcryptjs');\n\nconst userSchema = new mongoose.Schema({\n  email: { type: String, required: true, unique: true, lowercase: true, trim: true },\n  password: { type: String, required: true, minlength: 6 }\n});\n\nuserSchema.pre('save', async function (next) {\n  if (!this.isModified('password')) return next();\n  this.password = await bcrypt.hash(this.password, 10);\n  next();\n});\n\nuserSchema.methods.comparePassword = function (candidate) {\n  return bcrypt.compare(candidate, this.password);\n};\n\nmodule.exports = mongoose.model('User', userSchema);"
            },
            {
                "title": "7.2 Auth Controller & Token Issuance (controllers/authController.js)",
                "desc": "Implements registration, credential verification, and signed JWT issuance.",
                "code": "const jwt = require('jsonwebtoken');\nconst User = require('../models/User');\n\nexports.login = async (req, res, next) => {\n  try {\n    const { email, password } = req.body;\n    const user = await User.findOne({ email });\n    if (!user || !(await user.comparePassword(password))) {\n      return res.status(401).json({ error: 'Invalid credentials' });\n    }\n    const token = jwt.sign({ id: user._id, email: user.email }, process.env.JWT_SECRET, { expiresIn: '1h' });\n    res.json({ token, user: { id: user._id, email: user.email } });\n  } catch (err) { next(err); }\n};"
            },
            {
                "title": "7.3 JWT Verification Middleware (middleware/auth.js)",
                "desc": "Protects private routes by verifying Bearer JWT tokens in Authorization headers.",
                "code": "const jwt = require('jsonwebtoken');\n\nmodule.exports = (req, res, next) => {\n  const authHeader = req.headers.authorization;\n  if (!authHeader || !authHeader.startsWith('Bearer ')) {\n    return res.status(401).json({ error: 'No token provided' });\n  }\n  const token = authHeader.split(' ')[1];\n  try {\n    const decoded = jwt.verify(token, process.env.JWT_SECRET);\n    req.user = decoded;\n    next();\n  } catch (err) {\n    return res.status(401).json({ error: 'Token invalid or expired' });\n  }\n};"
            }
        ],
        "supplementary": [
            {"label": "User-Scoped Tasks", "detail": "Updated Task schema to store userId reference, ensuring users only see their own tasks."},
            {"label": "Client-Side Auth Context", "detail": "Built auth.jsx provider managing localStorage token persistence and route protection."}
        ],
        "questions": [
            {
                "q": "Why must passwords be hashed before storage instead of saved as plain text, even in a lab/demo project?",
                "a": "Storing plaintext passwords represents a catastrophic security vulnerability. If database backups, logs, or server instances are compromised, attacker access reveals user credentials directly. Modern hashing with bcrypt utilizes slow cryptographic algorithms and unique salt per user, thwarting rainbow table and dictionary attacks."
            },
            {
                "q": "What does the authentication middleware actually verify, and what happens if the token is missing or expired?",
                "a": "The middleware extracts the Bearer token from the HTTP Authorization header and cryptographically verifies its digital signature using the server's private secret. It validates that the payload has not been tampered with and that the current timestamp is before the `exp` (expiration) claim. If missing, tampered with, or expired, it halts execution and returns HTTP 401 Unauthorized."
            },
            {
                "q": "Why should input validation happen on the server even when client-side form validation is already implemented?",
                "a": "Client-side form validation exists solely for user interface feedback. Because HTTP requests can be forged directly through automated scripts, Postman, or intercepting proxies, client validation provides zero actual security. Server-side validation is the only reliable security boundary protecting application state."
            }
        ],
        "result": "Successfully implemented secure JWT authentication and password hashing with bcrypt, protecting CRUD endpoints with user-scoped data access control."
    },
    8: {
        "aim": "To improve frontend performance using lazy loading and code splitting techniques.",
        "steps": [
            {
                "title": "8.1 Route-Level Code Splitting (src/App.jsx)",
                "desc": "Replaced static route component imports with React.lazy() and Suspense fallback wrappers.",
                "code": "import { lazy, Suspense } from 'react';\nimport { Routes, Route } from 'react-router-dom';\nimport DelayedFallback from './components/DelayedFallback';\n\nconst Home = lazy(() => import('./pages/Home'));\nconst Contact = lazy(() => import('./pages/Contact'));\nconst Tasks = lazy(() => import('./pages/Tasks'));\n\nexport default function App() {\n  return (\n    <Suspense fallback={<DelayedFallback />}>\n      <Routes>\n        <Route path=\"/\" element={<Home />} />\n        <Route path=\"/contact\" element={<Contact />} />\n        <Route path=\"/tasks\" element={<Tasks />} />\n      </Routes>\n    </Suspense>\n  );\n}"
            },
            {
                "title": "8.2 Delayed Suspense Fallback (src/components/DelayedFallback.jsx)",
                "desc": "Prevents annoying UI flicker on high-speed network connections by delaying spinner presentation by 200ms.",
                "code": "import { useState, useEffect } from 'react';\nimport Spinner from './Spinner';\n\nexport default function DelayedFallback({ delay = 200 }) {\n  const [show, setShow] = useState(false);\n  useEffect(() => {\n    const timer = setTimeout(() => setShow(true), delay);\n    return () => clearTimeout(timer);\n  }, [delay]);\n  return show ? <Spinner /> : null;\n}"
            },
            {
                "title": "8.3 Heavy Component Splitting (TaskChart.jsx)",
                "desc": "Isolated a data-heavy analytics chart component into a lazily-loaded chunk on the tasks dashboard.",
                "code": "const TaskChart = lazy(() => import('../components/TaskChart'));\n\n// Rendered conditionally on the tasks page inside Suspense\n<Suspense fallback={<div className=\"chart-skeleton\" />}>\n  <TaskChart tasks={tasks} />\n</Suspense>"
            }
        ],
        "supplementary": [
            {"label": "Vite Chunk Analysis", "detail": "Analyzed dist/ bundle breakdown showing main vendor chunk reduced from 280KB down to 110KB with dynamic route chunks."},
            {"label": "Network Throttling Test", "detail": "Tested on simulated Slow 3G network verifying smooth chunk streaming without UI blocking."}
        ],
        "questions": [
            {
                "q": "What is the difference between the initial bundle and a lazy-loaded chunk in terms of when each is downloaded?",
                "a": "The initial bundle contains critical application code required to render the landing view and is downloaded immediately during initial page load. A lazy-loaded chunk is generated as a separate JavaScript file by the bundler and is only requested over the network on-demand when the user navigates to that specific route or triggers the component."
            },
            {
                "q": "Why does lazy loading improve perceived performance even though the total amount of code downloaded eventually stays the same?",
                "a": "Lazy loading dramatically minimizes initial JavaScript payload size. The browser parses, compiles, and executes less JavaScript upfront, drastically reducing First Contentful Paint (FCP) and Time to Interactive (TTI). Users begin interacting with the page immediately, while remaining code streams in background chunks."
            },
            {
                "q": "In what situations would lazy loading actually harm user experience rather than improve it?",
                "a": "Lazy loading can degrade user experience if applied excessively to tiny UI components (where the HTTP request overhead exceeds bundle savings) or to critical user paths on unreliable mobile connections, causing perceptible loading pauses during normal navigation."
            }
        ],
        "result": "Successfully optimized React frontend performance through React.lazy and Suspense code splitting, reducing initial bundle weight and demonstrating smooth chunk loading on demand."
    },
    9: {
        "aim": "To implement server-side caching and measure its impact on API response time.",
        "steps": [
            {
                "title": "9.1 In-Memory Cache Store (backend/cache.js)",
                "desc": "Configured in-memory caching utility with Time-To-Live (TTL) expiration, hit/miss metrics, and key invalidation.",
                "code": "class MemoryCache {\n  constructor(defaultTtlMs = 60000) {\n    this.store = new Map();\n    this.defaultTtl = defaultTtlMs;\n    this.stats = { hits: 0, misses: 0 };\n  }\n  get(key) {\n    const entry = this.store.get(key);\n    if (!entry) { this.stats.misses++; return null; }\n    if (Date.now() > entry.expiry) { this.store.delete(key); this.stats.misses++; return null; }\n    this.stats.hits++;\n    return entry.value;\n  }\n  set(key, value, ttl = this.defaultTtl) {\n    this.store.set(key, { value, expiry: Date.now() + ttl });\n  }\n  del(key) { this.store.delete(key); }\n  flushPattern(prefix) {\n    for (const k of this.store.keys()) if (k.startsWith(prefix)) this.store.delete(k);\n  }\n}\nmodule.exports = new MemoryCache();"
            },
            {
                "title": "9.2 Cache Middleware & Response Headers (routes/tasks.js)",
                "desc": "Intercepts GET requests, serving cached JSON when available with X-Cache: HIT / MISS response headers.",
                "code": "const cache = require('../cache');\n\nrouter.get('/', async (req, res, next) => {\n  const cacheKey = `tasks:${req.user.id}`;\n  const cached = cache.get(cacheKey);\n  if (cached) {\n    res.set('X-Cache', 'HIT');\n    return res.json(cached);\n  }\n  const tasks = await Task.find({ user: req.user.id });\n  cache.set(cacheKey, tasks, 30000);\n  res.set('X-Cache', 'MISS');\n  res.json(tasks);\n});"
            },
            {
                "title": "9.3 Cache Invalidation on Mutations",
                "desc": "Automatically invalidates cached user task keys on POST, PUT, and DELETE mutations to ensure data consistency.",
                "code": "router.post('/', async (req, res, next) => {\n  const task = await Task.create({ ...req.body, user: req.user.id });\n  cache.del(`tasks:${req.user.id}`);\n  res.status(201).json(task);\n});"
            }
        ],
        "supplementary": [
            {"label": "Debug Cache Statistics Endpoint", "detail": "Exposed GET /debug/cache displaying realtime hit/miss ratios and memory key allocations."},
            {"label": "Performance Benchmark Script", "detail": "Benchmark script showed response latency dropped from ~45ms on cache MISS to under 2ms on cache HIT."}
        ],
        "questions": [
            {
                "q": "Why must the cache be invalidated on every write operation, and what would happen to data correctness if it were not?",
                "a": "If write operations (create, update, delete) do not invalidate the cache, subsequent read queries will continue returning stale data from memory rather than reflecting the newly committed database updates. This produces phantom records, inconsistent state, and severe data corruption in client applications."
            },
            {
                "q": "What is a reasonable TTL (time-to-live) for cached data in a task management context, and what trade-off does TTL length represent?",
                "a": "For a personal task dashboard, a TTL between 30 and 60 seconds is reasonable when combined with immediate write invalidation. TTL represents an engineering trade-off: a longer TTL maximizes database offloading and cache hit ratios, while a shorter TTL minimizes the impact of stale reads if an invalidation event is somehow missed."
            },
            {
                "q": "Why is in-memory caching limited to single-instance backends, and what alternative would be needed for a load-balanced setup?",
                "a": "In-memory caches reside within the private heap memory of a single Node.js process. In a distributed multi-instance deployment behind a load balancer, each instance would possess an isolated, out-of-sync cache. To scale horizontally, a centralized external cache store such as Redis or Memcached is required so all instances access identical cached data."
            }
        ],
        "result": "Successfully implemented server-side memory caching with custom TTL, automated write invalidation, and measured a 95%+ drop in read response latency."
    },
    10: {
        "aim": "To implement asynchronous background processing using Node.js native EventEmitter without external dependencies.",
        "steps": [
            {
                "title": "10.1 Central Event Hub (backend/events.js)",
                "desc": "Instantiates and exports a singleton EventEmitter instance for application-wide event dispatching.",
                "code": "const EventEmitter = require('events');\nclass AppEmitter extends EventEmitter {}\nmodule.exports = new AppEmitter();"
            },
            {
                "title": "10.2 Event Listeners & Notification Simulation (backend/listeners.js)",
                "desc": "Registers listeners for 'task:created' and 'task:deleted' events, simulating non-blocking async background notifications.",
                "code": "const emitter = require('./events');\n\nemitter.on('task:created', (task) => {\n  console.log(`[Event: task:created] Task ID: ${task._id} | Title: '${task.title}'`);\n  // Simulating external email / push notification async dispatch\n  setTimeout(() => {\n    console.log(`[Notification Service] Asynchronous notification dispatched for task: '${task.title}'`);\n  }, 2000);\n});\n\nemitter.on('task:deleted', (taskId) => {\n  console.log(`[Event: task:deleted] Cleanup and log event for task ID: ${taskId}`);\n});"
            },
            {
                "title": "10.3 Dispatching Events from Route Handlers",
                "desc": "Dispatches events immediately after database operations without delaying the HTTP response.",
                "code": "router.post('/', async (req, res, next) => {\n  const task = await Task.create({ ...req.body, user: req.user.id });\n  res.status(201).json(task);\n  // Dispatched after response is sent\n  emitter.emit('task:created', task);\n});"
            }
        ],
        "supplementary": [
            {"label": "Global Error Event Handling", "detail": "Configured emitter.on('error') listener to safeguard against uncaught unhandled event errors crashing the server."},
            {"label": "Decoupled Architecture", "detail": "Completely separated email/notification delivery concerns from HTTP controller logic."}
        ],
        "questions": [
            {
                "q": "Why does emitting an event not block the API response, even though both run on the same Node.js process?",
                "a": "In our architecture, the HTTP response `res.status(201).json(task)` is transmitted to the client before or concurrently with the event dispatch. Furthermore, the event listener delegates slow operations (like email sending or database audit writes) to asynchronous timers (`setTimeout`) or async I/O. The asynchronous work is queued onto the libuv event loop, allowing the API request-response cycle to conclude immediately."
            },
            {
                "q": "What would happen to API response time if the notification logic were placed directly inside the POST route instead of in an event handler?",
                "a": "Placing notification logic synchronously inside the route handler would force the client to wait for external email SMTP connections or notification gateways before receiving an HTTP response. The response time would jump from 15ms to several seconds, drastically degrading perceived application speed and exhausting HTTP connection pools."
            },
            {
                "q": "Why is EventEmitter a reasonable choice for this scale of application, but not for a production system handling millions of events per day?",
                "a": "EventEmitter is ideal for single-instance, moderate-scale applications because it is built into the Node.js standard library with zero runtime overhead or external dependencies. However, in enterprise distributed architectures, EventEmitter lacks persistent message queues, acknowledgment protocols, consumer retry mechanisms, and cross-server routing. Heavy production workloads require enterprise message brokers like RabbitMQ or Apache Kafka."
            }
        ],
        "result": "Successfully implemented asynchronous background processing using Node.js native EventEmitter, achieving decoupled event listeners and instantaneous API responses."
    },
    11: {
        "aim": "To containerize the full-stack application using Docker and orchestrate services using Docker Compose.",
        "steps": [
            {
                "title": "11.1 Multi-Stage Frontend Dockerfile (docker/frontend.Dockerfile)",
                "desc": "Employs multi-stage builds: Stage 1 builds the Vite React assets with Node 22; Stage 2 serves static files with lightweight Nginx (~50MB).",
                "code": "FROM node:22-alpine AS build\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\nCOPY . .\nARG VITE_API_URL=\nENV VITE_API_URL=$VITE_API_URL\nRUN npm run build\n\nFROM nginx:1.27-alpine\nCOPY --from=build /app/dist /usr/share/nginx/html\nEXPOSE 80\nCMD [\"nginx\", \"-g\", \"daemon off;\"]"
            },
            {
                "title": "11.2 Backend Dockerfile (docker/backend.Dockerfile)",
                "desc": "Containerizes Express API using Alpine Linux, utilizing npm ci for deterministic dependency installation.",
                "code": "FROM node:22-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci --omit=dev\nCOPY . .\nENV NODE_ENV=production PORT=5000\nEXPOSE 5000\nCMD [\"node\", \"server.js\"]"
            },
            {
                "title": "11.3 Multi-Service Orchestration (docker-compose.yml)",
                "desc": "Defines and interconnects frontend, backend, and MongoDB services over an isolated bridge network with health checks and persistent volumes.",
                "code": "services:\n  mongodb:\n    image: mongo:7\n    ports: [\"27017:27017\"]\n    volumes: [mongo-data:/data/db]\n    healthcheck:\n      test: [\"CMD\", \"mongosh\", \"--quiet\", \"--eval\", \"db.adminCommand('ping')\"]\n      interval: 5s\n      retries: 20\n  api:\n    build: { context: ./backend, dockerfile: Dockerfile }\n    ports: [\"5000:5000\"]\n    environment:\n      MONGO_URI: \"mongodb://mongodb:27017/taskmanager\"\n    depends_on:\n      mongodb: { condition: service_healthy }\n  frontend:\n    build: { context: ./frontend, dockerfile: Dockerfile }\n    ports: [\"5173:80\"]"
            }
        ],
        "supplementary": [
            {"label": ".dockerignore Files", "detail": "Configured .dockerignore excluding node_modules, .git, and local logs from Docker build contexts to accelerate build speeds."},
            {"label": "Persistent Named Volumes", "detail": "Configured mongo-data volume ensuring database documents persist across container recreation cycles."}
        ],
        "questions": [
            {
                "q": "Why does the backend container need to reference the MongoDB container by its service name (e.g., mongodb) rather than localhost?",
                "a": "In Docker Compose, each container runs inside its own isolated network namespace with its own `localhost` (127.0.0.1) loopback adapter. Connecting to `localhost` inside the backend container would query the backend container itself. Docker's embedded DNS server automatically resolves container service names (such as `mongodb`) to the internal IP address of the target container on the shared bridge network."
            },
            {
                "q": "What is the difference between EXPOSE in a Dockerfile and the ports mapping in docker-compose.yml?",
                "a": "`EXPOSE` serves as internal container documentation specifying which ports the application inside listens on; it does not publish or open ports to the host machine. In contrast, the `ports` mapping (e.g. `\"3000:80\"`) actively binds a host port to the container port, opening firewall pathways and routing external traffic into the container."
            },
            {
                "q": "Why is it considered bad practice to copy node_modules into a Docker image instead of running npm install inside the container?",
                "a": "Local `node_modules` folders often contain platform-dependent native binaries compiled specifically for the host operating system (e.g. Windows x64). Copying them into a Linux Alpine container causes binary incompatibilities and runtime crashes. Installing inside the container via `npm ci` ensures packages compile against the exact target Linux architecture."
            }
        ],
        "result": "Successfully containerized the React frontend, Express API, and MongoDB database using multi-stage Dockerfiles and orchestrated the full stack with Docker Compose."
    },
    12: {
        "aim": "To automate testing and deployment of the application using a CI/CD pipeline.",
        "steps": [
            {
                "title": "12.1 Automated Test Suite with Jest and Supertest (backend/tests/tasks.test.js)",
                "desc": "Written unit and integration tests covering CRUD operations, status codes, and database interaction.",
                "code": "const request = require('supertest');\nconst app = require('../app');\nconst mongoose = require('mongoose');\n\ndescribe('Task API Endpoints', () => {\n  beforeAll(async () => {\n    await mongoose.connect(process.env.MONGO_URI);\n  });\n  afterAll(async () => {\n    await mongoose.connection.close();\n  });\n  \n  it('should return 200 and task array on GET /tasks', async () => {\n    const res = await request(app).get('/tasks');\n    expect(res.statusCode).toEqual(200);\n    expect(Array.isArray(res.body)).toBe(true);\n  });\n});"
            },
            {
                "title": "12.2 GitHub Actions Workflow (.github/workflows/ci.yml)",
                "desc": "Configured CI workflow executing on every push and pull request with linting and MongoDB service containers.",
                "code": "name: CI Pipeline\non: [push, pull_request]\njobs:\n  lint-and-test:\n    runs-on: ubuntu-latest\n    services:\n      mongodb:\n        image: mongo:7\n        ports: ['27017:27017']\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: { node-version: 22 }\n      - name: Install Dependencies\n        run: cd practical-12/backend && npm ci\n      - name: Run ESLint\n        run: cd practical-12/backend && npm run lint\n      - name: Run Tests with Jest\n        run: cd practical-12/backend && npm test\n        env:\n          MONGO_URI: mongodb://localhost:27017/ci_test"
            },
            {
                "title": "12.3 Separation of app.js and server.js",
                "desc": "Refactored Express setup: app.js exports the configured app instance for Supertest, while server.js handles process port listening.",
                "code": "// backend/app.js - exports express app without app.listen()\nmodule.exports = app;\n\n// backend/server.js - standalone server entry point\nconst app = require('./app');\napp.listen(PORT, () => console.log(`Server listening on ${PORT}`));"
            }
        ],
        "supplementary": [
            {"label": "ESLint Integration", "detail": "Configured ESLint rules catching unhandled variables and syntax issues prior to test execution."},
            {"label": "10/10 Test Pass Rate", "detail": "All 10 unit and API integration tests verified passing cleanly in under 4 seconds."}
        ],
        "questions": [
            {
                "q": "What is the difference between Continuous Integration and Continuous Deployment, and which one does this practical actually demonstrate?",
                "a": "Continuous Integration (CI) is the practice of automatically integrating, building, linting, and testing code on every commit to verify that changes don't break existing functionality. Continuous Deployment (CD) automatically releases validated code into production environments without manual intervention. This practical demonstrates Continuous Integration (CI)."
            },
            {
                "q": "Why does running tests automatically on every push catch problems earlier than testing manually before a release?",
                "a": "Automated CI testing provides immediate feedback within minutes of pushing code. The developer has the recent code changes fresh in memory, making bug identification effortless. In contrast, manual testing before releases accumulates weeks of merged changes, making root-cause discovery tedious and bug fixes significantly more expensive."
            },
            {
                "q": "What would happen to the pipeline if the test file path were incorrect would the workflow fail at the same step as a genuine test failure?",
                "a": "If the test path is configured incorrectly, Jest exits with an error status (e.g. 'No tests found') and the workflow fails at the test step. However, the diagnostic output will clearly state file discovery failure rather than assertion failure, allowing the engineer to immediately differentiate configuration errors from code regressions."
            }
        ],
        "result": "Successfully created an automated CI pipeline with GitHub Actions, integrating ESLint linting, Jest/Supertest automated tests, and containerized MongoDB test services."
    },
    13: {
        "aim": "To integrate an external AI service into the existing application and understand responsible AI usage.",
        "steps": [
            {
                "title": "13.1 Server-Side AI Gateway Route (backend/routes/tasks.js)",
                "desc": "Implements protected backend endpoint calling the AI service while keeping API keys confidential.",
                "code": "router.post('/ai-suggest', auth, async (req, res, next) => {\n  const { title } = req.body;\n  if (!title) return res.status(400).json({ error: 'Title required' });\n  \n  const apiKey = process.env.OPENAI_API_KEY;\n  if (!apiKey) {\n    // Graceful degradation fallback\n    return res.json({\n      description: `Task focused on: ${title}. Complete all requirements and verify outcomes.`,\n      priority: 'medium',\n      fallback: true\n    });\n  }\n  \n  try {\n    const aiRes = await callOpenAISuggestion(title, apiKey);\n    res.json(aiRes);\n  } catch (err) {\n    // Graceful fallback on API error or rate limits\n    res.json({ description: `Action item for: ${title}`, priority: 'medium', fallback: true });\n  }\n});"
            },
            {
                "title": "13.2 Frontend 'Suggest with AI' Button (src/components/TaskForm.jsx)",
                "desc": "Provides one-click AI generation for descriptions and priority with reviewable, editable fields.",
                "code": "const handleAiSuggest = async () => {\n  if (!title) return;\n  setAiLoading(true);\n  try {\n    const suggestion = await fetchAiSuggestion(title);\n    setDescription(suggestion.description);\n    setPriority(suggestion.priority);\n  } catch (err) {\n    showToast('AI suggestion service currently unavailable', 'warning');\n  } finally {\n    setAiLoading(false);\n  }\n};"
            },
            {
                "title": "13.3 Responsible AI Disclaimer & Fallback Handling",
                "desc": "Displays clear AI badges, allows full user review before persisting to database, and enforces rate limiting.",
                "code": "<div className=\"ai-card\">\n  <small>✨ Suggested by AI - Please review before saving</small>\n  <textarea value={description} onChange={(e) => setDescription(e.target.value)} />\n</div>"
            }
        ],
        "supplementary": [
            {"label": "Client Rate Limiting", "detail": "Restricted AI generation requests to 1 request per task per minute to control API costs."},
            {"label": "Graceful Fallback Mode", "detail": "Verified application continues full functionality even when OPENAI_API_KEY is omitted or offline."}
        ],
        "questions": [
            {
                "q": "Why must the AI API key be called from the backend rather than directly from the React frontend?",
                "a": "Any secret key embedded in a frontend application (even within environment variables) is compiled into client JavaScript bundles and can be extracted easily by inspecting browser network requests or source maps. Calling AI APIs exclusively from the Express backend keeps secret keys secure on the server and allows strict rate limiting, user authentication, and prompt sanitization."
            },
            {
                "q": "What does 'graceful degradation' mean in this context, and why does it matter for a feature that depends on a third-party service outside your control?",
                "a": "Graceful degradation ensures that when an external dependency (such as an AI API) experiences outages, rate limit rejections, or missing API keys, the core application remains fully operational. Rather than crashing with an unhandled 500 error, the app provides a sensible default suggestion and informs the user, maintaining positive user experience."
            },
            {
                "q": "What are the privacy and governance implications of sending task data to an external AI API, and what kind of data should never be sent this way?",
                "a": "Transmitting user data to third-party AI APIs can breach data privacy regulations (such as GDPR or HIPAA) if proprietary, medical, or personally identifiable information (PII) is shared without consent. Passwords, personal contact details, health records, financial tokens, and proprietary intellectual property must never be sent to external AI services."
            }
        ],
        "result": "Successfully integrated AI task suggestion capabilities into the web application via secure backend endpoints, implementing graceful degradation and responsible AI guidelines."
    }
}

def main():
    out_dir = os.path.join(os.path.dirname(__file__), 'submission')
    os.makedirs(out_dir, exist_ok=True)
    print(f"Generating 13 submission PDFs in: {out_dir}")

    for i in range(1, 14):
        filename = f"{STUDENT_ID}_Prac{i}_AWDF.pdf"
        output_path = os.path.join(out_dir, filename)
        data = PRACTICALS_DATA[i]
        build_practical_pdf(i, data, output_path)

    print("All 13 practical submission PDFs generated successfully!")

if __name__ == '__main__':
    main()
