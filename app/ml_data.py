"""
ML Foundation - Datasets for AI Placement Preparation
No external APIs required - pure data-driven ML logic
"""

# ============================================================================
# 1. COMPREHENSIVE SKILLS DATABASE
# ============================================================================
SKILLS_DATABASE = {
    # Programming Languages
    "python": {"category": "language", "level": 1},
    "java": {"category": "language", "level": 1},
    "javascript": {"category": "language", "level": 1},
    "typescript": {"category": "language", "level": 2},
    "cpp": {"category": "language", "level": 2},
    "go": {"category": "language", "level": 2},
    "rust": {"category": "language", "level": 3},
    "csharp": {"category": "language", "level": 1},
    "sql": {"category": "language", "level": 1},
    
    # Web Technologies
    "react": {"category": "web", "level": 2},
    "angular": {"category": "web", "level": 2},
    "vue": {"category": "web", "level": 2},
    "html": {"category": "web", "level": 1},
    "css": {"category": "web", "level": 1},
    "node": {"category": "web", "level": 2},
    "flask": {"category": "web", "level": 2},
    "django": {"category": "web", "level": 2},
    "spring": {"category": "web", "level": 2},
    
    # Databases
    "mysql": {"category": "database", "level": 1},
    "postgresql": {"category": "database", "level": 2},
    "mongodb": {"category": "database", "level": 2},
    "redis": {"category": "database", "level": 2},
    "elasticsearch": {"category": "database", "level": 3},
    "cassandra": {"category": "database", "level": 3},
    
    # Data Science & ML
    "machine learning": {"category": "ml", "level": 3},
    "deep learning": {"category": "ml", "level": 3},
    "numpy": {"category": "ml", "level": 2},
    "pandas": {"category": "ml", "level": 2},
    "tensorflow": {"category": "ml", "level": 3},
    "pytorch": {"category": "ml", "level": 3},
    "scikit-learn": {"category": "ml", "level": 2},
    "nlp": {"category": "ml", "level": 3},
    "computer vision": {"category": "ml", "level": 3},
    
    # Cloud & DevOps
    "aws": {"category": "cloud", "level": 2},
    "gcp": {"category": "cloud", "level": 2},
    "azure": {"category": "cloud", "level": 2},
    "docker": {"category": "devops", "level": 2},
    "kubernetes": {"category": "devops", "level": 3},
    "jenkins": {"category": "devops", "level": 2},
    "git": {"category": "devops", "level": 1},
    "ci/cd": {"category": "devops", "level": 2},
    
    # Other Tools
    "linux": {"category": "tools", "level": 1},
    "git": {"category": "tools", "level": 1},
    "microservices": {"category": "architecture", "level": 2},
    "rest api": {"category": "architecture", "level": 1},
    "system design": {"category": "architecture", "level": 3},
    "design patterns": {"category": "architecture", "level": 2},
}

# ============================================================================
# 2. ROLE MAPPING - Skills required for each role
# ============================================================================
ROLE_SKILLS_MAP = {
    "Data Scientist": {
        "required": ["python", "sql", "pandas", "numpy", "machine learning", "statistics"],
        "preferred": ["tensorflow", "pytorch", "nlp", "aws"],
        "level": "intermediate"
    },
    "Web Developer": {
        "required": ["html", "css", "javascript", "rest api"],
        "preferred": ["react", "node", "database"],
        "level": "intermediate"
    },
    "Backend Developer": {
        "required": ["python", "java", "sql", "rest api", "design patterns"],
        "preferred": ["microservices", "docker", "aws", "ci/cd"],
        "level": "intermediate"
    },
    "Frontend Developer": {
        "required": ["javascript", "html", "css", "react"],
        "preferred": ["typescript", "node", "rest api"],
        "level": "intermediate"
    },
    "ML Engineer": {
        "required": ["python", "machine learning", "tensorflow", "sql"],
        "preferred": ["pytorch", "deep learning", "docker", "aws"],
        "level": "advanced"
    },
    "DevOps Engineer": {
        "required": ["docker", "kubernetes", "linux", "git", "ci/cd"],
        "preferred": ["aws", "jenkins", "ansible", "monitoring"],
        "level": "advanced"
    },
    "Full Stack Developer": {
        "required": ["python", "javascript", "html", "css", "sql", "rest api"],
        "preferred": ["react", "node", "docker", "aws"],
        "level": "advanced"
    },
    "System Design": {
        "required": ["system design", "design patterns", "microservices", "database"],
        "preferred": ["kubernetes", "aws", "cache", "messaging"],
        "level": "advanced"
    }
}

# ============================================================================
# 3. QUESTION BANK - Skills → Interview Questions
# ============================================================================
QUESTION_BANK = {
    "python": {
        "easy": [
            "Explain the difference between list and tuple in Python",
            "What is the difference between == and is in Python?",
            "How do you create a dictionary in Python?",
        ],
        "medium": [
            "Explain decorators in Python with an example",
            "What is the difference between args and kwargs?",
            "How does garbage collection work in Python?",
        ],
        "hard": [
            "Explain metaclasses in Python",
            "How does the Global Interpreter Lock (GIL) work?",
            "Design a thread-safe singleton pattern in Python",
        ]
    },
    "sql": {
        "easy": [
            "Write a query to find the second highest salary",
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "How do you use GROUP BY with WHERE clause?",
        ],
        "medium": [
            "Explain window functions in SQL",
            "How do you optimize a slow database query?",
            "Design a schema for an e-commerce system",
        ],
        "hard": [
            "Explain query optimization techniques",
            "How do you handle deadlocks in databases?",
            "Design a distributed database schema",
        ]
    },
    "system design": {
        "easy": [
            "Design a simple URL shortener",
            "How would you design a cache system?",
            "What is horizontal vs vertical scaling?",
        ],
        "medium": [
            "Design a chat application",
            "How would you design a hotel booking system?",
            "Design a distributed cache system",
        ],
        "hard": [
            "Design YouTube",
            "Design Instagram",
            "Design a real-time notification system at scale",
        ]
    },
    "machine learning": {
        "easy": [
            "What is the difference between regression and classification?",
            "Explain what a confusion matrix is",
            "What are the main steps in an ML pipeline?",
        ],
        "medium": [
            "Explain overfitting and underfitting",
            "How do you handle imbalanced datasets?",
            "What is cross-validation and why is it important?",
        ],
        "hard": [
            "How would you approach a new ML problem from scratch?",
            "Explain regularization techniques (L1, L2, Dropout)",
            "How do you deploy an ML model to production?",
        ]
    },
    "rest api": {
        "easy": [
            "What is REST and what are its principles?",
            "Explain HTTP methods (GET, POST, PUT, DELETE)",
            "What is the difference between PUT and PATCH?",
        ],
        "medium": [
            "How do you handle authentication in REST APIs?",
            "Explain pagination and rate limiting",
            "How do you version an API?",
        ],
        "hard": [
            "Design a scalable REST API architecture",
            "How do you handle concurrent requests efficiently?",
            "Explain API gateway and load balancing",
        ]
    },
    "docker": {
        "easy": [
            "What is Docker and why is it used?",
            "Explain the difference between images and containers",
            "How do you create a Dockerfile?",
        ],
        "medium": [
            "How do Docker networking and volumes work?",
            "Explain Docker compose",
            "How do you optimize Docker images?",
        ],
        "hard": [
            "Design a microservices architecture with Docker",
            "How do you handle logging and monitoring in Docker?",
            "Explain container orchestration strategies",
        ]
    },
}

# ============================================================================
# 4. ANSWER KEYWORDS - Expected keywords for evaluation
# ============================================================================
ANSWER_KEYWORDS = {
    "Explain the difference between list and tuple in Python": {
        "keywords": ["mutable", "immutable", "ordered", "hashable", "performance"],
        "ideal": "Lists are mutable (can be changed) while tuples are immutable (cannot be changed). Tuples are hashable and can be used as dictionary keys. Lists have more overhead but tuples are faster.",
        "depth_keywords": ["memory", "use cases", "indexing", "slicing", "iteration"]
    },
    "What is the difference between == and is in Python?": {
        "keywords": ["equality", "identity", "value", "reference", "object"],
        "ideal": "== checks if values are equal, while is checks if objects are the same in memory. Use == for value comparison and is for identity comparison (like None).",
        "depth_keywords": ["memory addressing", "singleton", "identity operator", "comparison operator"]
    },
    "Explain decorators in Python with an example": {
        "keywords": ["function", "wrapper", "higher-order", "@", "functools"],
        "ideal": "Decorators are functions that modify or enhance other functions without changing their source code. They use the @ syntax and are useful for logging, authentication, and caching.",
        "depth_keywords": ["closure", "wraps", "arguments", "return value", "syntax sugar"]
    },
    "What is the difference between INNER JOIN and LEFT JOIN?": {
        "keywords": ["rows", "matching", "both tables", "left table", "null"],
        "ideal": "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from left table and matching rows from right table (nulls for non-matches).",
        "depth_keywords": ["outer join", "right join", "cross join", "performance", "on clause"]
    },
    "Design a URL shortener": {
        "keywords": ["hash", "database", "encoding", "redirect", "unique"],
        "ideal": "Use a unique hash/encoding to map long URLs to short codes. Store in database with redirect logic. Handle collisions, track analytics, and ensure high throughput.",
        "depth_keywords": ["scalability", "caching", "distributed", "rate limiting", "analytics"]
    }
}

# ============================================================================
# 5. EXPERIENCE LEVEL CLASSIFICATION
# ============================================================================
EXPERIENCE_LEVELS = {
    "fresher": {"min_skills": 0, "max_skills": 3},
    "junior": {"min_skills": 3, "max_skills": 6},
    "intermediate": {"min_skills": 6, "max_skills": 10},
    "senior": {"min_skills": 10, "max_skills": 20},
    "expert": {"min_skills": 20, "max_skills": 999}
}

# ============================================================================
# 6. LEARNING ROADMAP - Topics for improvement
# ============================================================================
ROADMAP_TOPICS = {
    "Data Structures": {
        "subtopics": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Hash Maps"],
        "projects": ["Implement custom data structures", "Solve LeetCode medium problems"],
        "duration_days": 14
    },
    "Algorithms": {
        "subtopics": ["Sorting", "Searching", "Dynamic Programming", "Greedy", "BFS/DFS"],
        "projects": ["Solve algorithmic problems", "Optimize solutions"],
        "duration_days": 21
    },
    "System Design": {
        "subtopics": ["Scalability", "Load Balancing", "Caching", "Database Sharding", "Message Queues"],
        "projects": ["Design HLD for real systems", "Document architecture"],
        "duration_days": 21
    },
    "Database Design": {
        "subtopics": ["Normalization", "Indexing", "Query Optimization", "Transactions", "Concurrency"],
        "projects": ["Design schemas", "Optimize queries"],
        "duration_days": 14
    },
    "API Design": {
        "subtopics": ["REST principles", "Authentication", "Rate Limiting", "Versioning", "Documentation"],
        "projects": ["Build REST APIs", "API documentation"],
        "duration_days": 10
    },
    "Machine Learning": {
        "subtopics": ["Statistics", "Supervised Learning", "Unsupervised Learning", "Model Evaluation"],
        "projects": ["End-to-end ML projects", "Kaggle competitions"],
        "duration_days": 30
    },
}

# ============================================================================
# 7. DIFFICULTY MAPPING
# ============================================================================
DIFFICULTY_LEVELS = {
    "easy": {"score_multiplier": 1.0, "time_estimate_min": 5},
    "medium": {"score_multiplier": 1.5, "time_estimate_min": 15},
    "hard": {"score_multiplier": 2.0, "time_estimate_min": 30}
}

# ============================================================================
# 8. SCORING RUBRIC - For answer evaluation
# ============================================================================
SCORING_RUBRIC = {
    "correctness": {
        "weight": 0.3,
        "levels": {
            "poor": 1,
            "fair": 3,
            "good": 7,
            "excellent": 10
        }
    },
    "completeness": {
        "weight": 0.25,
        "levels": {
            "incomplete": 1,
            "partial": 3,
            "mostly_complete": 7,
            "complete": 10
        }
    },
    "clarity": {
        "weight": 0.25,
        "levels": {
            "unclear": 1,
            "somewhat_clear": 3,
            "clear": 7,
            "very_clear": 10
        }
    },
    "depth": {
        "weight": 0.2,
        "levels": {
            "surface": 1,
            "basic": 3,
            "detailed": 7,
            "expert": 10
        }
    }
}

# ============================================================================
# 9. COMMON INTERVIEW MISTAKES
# ============================================================================
COMMON_MISTAKES = {
    "technical": [
        "Not asking clarifying questions before solution",
        "Jumping to complex solution without explaining approach",
        "Not considering edge cases",
        "Poor time/space complexity analysis",
        "Inefficient algorithm choice"
    ],
    "behavioral": [
        "Not providing specific examples using STAR method",
        "Talking too much about failures without learning",
        "Not asking about company specifics",
        "Appearing overconfident or unsure",
        "Not discussing metrics and impact"
    ],
    "communication": [
        "Speaking too fast or unclearly",
        "Using too much jargon without explanation",
        "Not engaging with interviewer",
        "Not listening carefully to hints",
        "Poor body language or eye contact"
    ]
}

# ============================================================================
# 10. STRENGTHS INDICATORS
# ============================================================================
STRENGTHS_INDICATORS = {
    "technical": [
        "Strong grasp of core concepts",
        "Good problem-solving approach",
        "Considers multiple solutions",
        "Analyzes complexity properly",
        "Handles edge cases well"
    ],
    "communication": [
        "Clear explanation of concepts",
        "Asks clarifying questions",
        "Discusses trade-offs",
        "Provides examples effectively",
        "Listens and adapts"
    ],
    "behavioral": [
        "Demonstrates growth mindset",
        "Shows ownership and accountability",
        "Collaborates effectively",
        "Learns from feedback",
        "Balances confidence with humility"
    ]
}
