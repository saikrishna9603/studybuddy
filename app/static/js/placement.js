/**
 * Placement Assistant JavaScript
 * Handles interview practice sessions, answer submission, and feedback display
 */

class PlacementAssistant {
    constructor() {
        this.currentSession = null;
        this.currentQuestion = null;
        this.questions = [];
        this.currentQuestionIndex = 0;
    }

    /**
     * Start a new interview practice session
     */
    async startSession(resumeId, company, role) {
        try {
            const response = await fetch('/api/placement/session/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resumeId, company, role })
            });
            
            const data = await response.json();
            if (data.session_id) {
                this.currentSession = data.session_id;
                await this.generateQuestions();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error starting session:', error);
            return false;
        }
    }

    /**
     * Generate interview questions for current session
     */
    async generateQuestions() {
        try {
            const response = await fetch('/api/placement/questions/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.currentSession })
            });
            
            const data = await response.json();
            if (data.questions) {
                this.questions = data.questions;
                this.currentQuestionIndex = 0;
                this.displayQuestion(0);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error generating questions:', error);
            return false;
        }
    }

    /**
     * Display a specific question
     */
    displayQuestion(index) {
        if (index >= this.questions.length) {
            this.completeSession();
            return;
        }

        this.currentQuestion = this.questions[index];
        const container = document.getElementById('practice-area');
        
        const difficultyStars = '⭐'.repeat(this.currentQuestion.difficulty);
        
        container.innerHTML = `
            <div class="question-display">
                <div class="question-meta">
                    <span class="question-number">Question ${index + 1} of ${this.questions.length}</span>
                    <div>
                        <span class="question-type">${this.currentQuestion.type}</span>
                        <span class="question-difficulty">${difficultyStars}</span>
                    </div>
                </div>
                
                <div class="question-text">${this.currentQuestion.question}</div>
                
                <textarea 
                    id="answer-input" 
                    class="answer-input"
                    placeholder="Type your answer here..."
                    onkeyup="showCharCount()"
                ></textarea>
                <div class="character-count">
                    <span id="charCount">0</span> characters
                </div>
                
                <div class="button-group">
                    <button class="btn-submit" onclick="placement.submitAnswer()">
                        ${index === this.questions.length - 1 ? 'Submit & Complete' : 'Submit Answer'}
                    </button>
                    <button class="btn-skip" onclick="placement.skipQuestion()">
                        ${index === this.questions.length - 1 ? 'Skip & Complete' : 'Skip Question'}
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Submit user's answer
     */
    async submitAnswer() {
        const answerText = document.getElementById('answer-input').value.trim();
        
        if (!answerText) {
            alert('Please provide an answer before submitting.');
            return;
        }

        try {
            // Submit answer
            const submitResponse = await fetch('/api/placement/answers/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.currentSession,
                    question_id: this.currentQuestion.id,
                    answer_text: answerText
                })
            });

            const submitData = await submitResponse.json();
            if (submitData.answer_id) {
                // Start evaluation in background
                this.evaluateAnswer(submitData.answer_id);
                
                // Move to next question
                this.currentQuestionIndex++;
                this.displayQuestion(this.currentQuestionIndex);
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Error submitting answer. Please try again.');
        }
    }

    /**
     * Evaluate an answer (runs in background)
     */
    evaluateAnswer(answerId) {
        fetch(`/api/placement/answers/${answerId}/evaluate`)
            .then(r => r.json())
            .then(data => {
                // Store evaluation for later retrieval
                sessionStorage.setItem(`eval_${answerId}`, JSON.stringify(data));
            })
            .catch(e => console.error('Error evaluating answer:', e));
    }

    /**
     * Skip current question
     */
    skipQuestion() {
        this.currentQuestionIndex++;
        this.displayQuestion(this.currentQuestionIndex);
    }

    /**
     * Complete the session and show results
     */
    async completeSession() {
        try {
            const response = await fetch(`/api/placement/session/${this.currentSession}/results`);
            const data = await response.json();
            
            // Redirect to feedback page
            window.location.href = `/placement/feedback?session=${this.currentSession}`;
        } catch (error) {
            console.error('Error completing session:', error);
        }
    }

    /**
     * Load and display session results/feedback
     */
    async loadSessionResults(sessionId) {
        try {
            const response = await fetch(`/api/placement/session/${sessionId}/results`);
            const data = await response.json();
            
            if (data.success) {
                this.displaySessionFeedback(data);
            }
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }

    /**
     * Display comprehensive feedback for session
     */
    displaySessionFeedback(data) {
        const container = document.getElementById('feedback-area') || document.body;
        const session = data.session;
        const evaluations = data.evaluations || [];

        let scoreClass = 'score-excellent';
        if (session.average_score < 5) scoreClass = 'score-poor';
        else if (session.average_score < 6) scoreClass = 'score-average';
        else if (session.average_score < 8) scoreClass = 'score-good';

        let html = `
            <div class="feedback-header">
                <div>
                    <h2>${session.company} - ${session.role}</h2>
                    <p>${session.total_questions} questions answered</p>
                </div>
                <div class="overall-score">
                    <div class="score-circle ${scoreClass}">
                        ${session.average_score.toFixed(1)}
                    </div>
                    <div class="score-label">Overall Score</div>
                </div>
            </div>
        `;

        // Show individual evaluations
        evaluations.forEach((eval, idx) => {
            const scores = eval.scores || {};
            html += `
                <div class="feedback-section">
                    <h3>Question ${idx + 1} - Feedback</h3>
                    
                    <div class="scores-grid">
                        <div class="score-item">
                            <div class="score-item-label">Correctness</div>
                            <div class="score-item-value">${scores.correctness || 0}</div>
                            <div class="score-bar">
                                <div class="score-bar-fill" style="width: ${(scores.correctness || 0) * 10}%"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <div class="score-item-label">Clarity</div>
                            <div class="score-item-value">${scores.clarity || 0}</div>
                            <div class="score-bar">
                                <div class="score-bar-fill" style="width: ${(scores.clarity || 0) * 10}%"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <div class="score-item-label">Depth</div>
                            <div class="score-item-value">${scores.depth || 0}</div>
                            <div class="score-bar">
                                <div class="score-bar-fill" style="width: ${(scores.depth || 0) * 10}%"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <div class="score-item-label">Communication</div>
                            <div class="score-item-value">${scores.communication || 0}</div>
                            <div class="score-bar">
                                <div class="score-bar-fill" style="width: ${(scores.communication || 0) * 10}%"></div>
                            </div>
                        </div>
                    </div>

                    ${eval.strengths && eval.strengths.length > 0 ? `
                        <div class="feedback-section">
                            <h4>Strengths</h4>
                            <ul class="strengths">
                                ${eval.strengths.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${eval.weaknesses && eval.weaknesses.length > 0 ? `
                        <div class="feedback-section">
                            <h4>Areas for Improvement</h4>
                            <ul class="weaknesses">
                                ${eval.weaknesses.map(w => `<li>${w}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${eval.model_answer ? `
                        <div class="model-answer">
                            <div class="model-answer-title">Model Answer</div>
                            <p>${eval.model_answer}</p>
                        </div>
                    ` : ''}

                    ${eval.tips && eval.tips.length > 0 ? `
                        <div class="tips">
                            <h4>Tips for Next Time</h4>
                            <ul>
                                ${eval.tips.map(t => `<li>${t}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        });

        html += `
            <div class="button-group" style="margin-top: 30px;">
                <button class="btn-submit" onclick="window.location.href='/placement/roadmap'">
                    View Preparation Roadmap
                </button>
                <button class="btn-skip" onclick="window.location.href='/placement/dashboard'">
                    Back to Dashboard
                </button>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Load and display roadmap
     */
    async loadRoadmap(roadmapId) {
        try {
            const response = await fetch(`/api/placement/roadmap/${roadmapId}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayRoadmap(data.roadmap);
            }
        } catch (error) {
            console.error('Error loading roadmap:', error);
        }
    }

    /**
     * Display roadmap with daily plan
     */
    displayRoadmap(roadmap) {
        const container = document.getElementById('roadmap-area') || document.body;
        
        const weakAreasHtml = roadmap.weak_areas.length > 0 
            ? `<ul>${roadmap.weak_areas.map(w => `<li>${w}</li>`).join('')}</ul>`
            : '<p>No weak areas identified. Keep up the good work!</p>';

        let html = `
            <div class="roadmap-header">
                <h2>Your Personalized Preparation Roadmap</h2>
                <p>Targeting: <strong>${roadmap.company}</strong></p>
                <p>Progress: <strong>${roadmap.progress || 0}%</strong></p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${roadmap.progress || 0}%"></div>
                </div>
            </div>

            <div class="feedback-section">
                <h3>📋 Focus Areas</h3>
                ${weakAreasHtml}
            </div>

            <div class="roadmap-timeline">
                <h3>📅 Daily Study Plan</h3>
        `;

        if (roadmap.daily_plan && roadmap.daily_plan.length > 0) {
            roadmap.daily_plan.forEach((day, idx) => {
                html += `
                    <div class="roadmap-day">
                        <div class="day-number">Day ${idx + 1}</div>
                        <div class="day-content">
                            <h4>${day.topic}</h4>
                            <p><strong>Activity:</strong> ${day.activity} (${day.duration})</p>
                            <p>${day.description}</p>
                            <ul class="day-tasks">
                                ${day.tasks.map(t => `<li>${t}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            });
        }

        html += `
            </div>

            ${roadmap.resources && Object.keys(roadmap.resources).length > 0 ? `
                <div class="feedback-section">
                    <h3>📚 Learning Resources</h3>
                    ${Object.entries(roadmap.resources).map(([topic, resources]) => `
                        <div>
                            <h4>${topic}</h4>
                            <ul>
                                ${resources.map(r => `<li>${r}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            <div class="button-group" style="margin-top: 30px;">
                <button class="btn-submit" onclick="location.reload()">Mark as Complete</button>
                <button class="btn-skip" onclick="window.location.href='/placement/dashboard'">Back to Dashboard</button>
            </div>
        `;

        container.innerHTML = html;
    }
}

// Global instance
const placement = new PlacementAssistant();

/**
 * Update character count for answer
 */
function showCharCount() {
    const textarea = document.getElementById('answer-input');
    const count = textarea ? textarea.value.length : 0;
    const counter = document.getElementById('charCount');
    if (counter) counter.textContent = count;
}

/**
 * Extract query parameters
 */
function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

/**
 * Initialize page based on context
 */
document.addEventListener('DOMContentLoaded', function() {
    const sessionId = getQueryParam('session');
    const roadmapId = getQueryParam('roadmap');
    
    if (window.location.pathname.includes('/placement/practice') && sessionId) {
        placement.currentSession = parseInt(sessionId);
        placement.generateQuestions();
    } else if (window.location.pathname.includes('/placement/feedback') && sessionId) {
        placement.loadSessionResults(parseInt(sessionId));
    } else if (window.location.pathname.includes('/placement/roadmap') && roadmapId) {
        placement.loadRoadmap(parseInt(roadmapId));
    }
});
