# Enhanced queries for better Llama3 understanding
EVALUATION_CRITERIA = [
    {
        "name": "Functionality",
        "description": "Does the code work as intended? Are all features implemented correctly and completely?",
        "query": "working features, implementation completeness, functionality, bugs, errors, correct output, feature implementation"
    },
    {
        "name": "Code Quality",
        "description": "Is the code clean, readable, and well-organized? Follows best practices?",
        "query": "code structure, readability, naming conventions, organization, modularity, clean code principles"
    },
    {
        "name": "Security",
        "description": "Are security best practices followed? Any vulnerabilities like hardcoded secrets, injection risks?",
        "query": "authentication, passwords, tokens, encryption, SQL injection, XSS, security headers, secure coding"
    },
    {
        "name": "Documentation",
        "description": "Is the code well-documented? Are there README, comments, and API documentation?",
        "query": "README, comments, docstrings, documentation, instructions, API docs, setup guide, usage examples"
    },
    {
        "name": "Error Handling",
        "description": "How well are errors and edge cases handled? Graceful failure?",
        "query": "try catch, except, error handling, validation, edge cases, exceptions, error messages, logging"
    },
    {
        "name": "Performance",
        "description": "Is the code efficient and optimized? Consider time/space complexity",
        "query": "performance, optimization, loops, algorithms, complexity, caching, database queries, response time"
    },
    {
        "name": "Testing",
        "description": "Are there tests? How comprehensive are they? Test coverage?",
        "query": "test, pytest, unittest, test cases, assertions, coverage, integration tests, test suite"
    },
    {
        "name": "Dependencies",
        "description": "Are dependencies properly managed? Up-to-date? Minimal?",
        "query": "requirements.txt, package.json, dependencies, imports, versions, dependency management, package.json"
    },
    {
        "name": "Architecture",
        "description": "Is the project structure logical and scalable? Follows design patterns?",
        "query": "folder structure, MVC, architecture, design patterns, separation of concerns, modular design"
    },
    {
        "name": "UI/UX",
        "description": "Is the user interface intuitive and user-friendly? Good design?",
        "query": "UI, UX, interface, design, CSS, HTML, user experience, responsiveness, accessibility, styling"
    },
    {
        "name": "Innovation",
        "description": "How creative or innovative is the solution? Unique approach?",
        "query": "innovation, creativity, unique approach, novel solution, original, creative problem solving"
    },
    {
        "name": "Maintainability",
        "description": "How easy is it to maintain and extend the code? Technical debt?",
        "query": "maintainability, extensibility, technical debt, complexity, reuse, scalability, modifiability"
    },
    {
        "name": "Best Practices",
        "description": "Does it follow industry best practices and conventions?",
        "query": "best practices, standards, conventions, guidelines, patterns, coding standards, industry standards"
    }
]