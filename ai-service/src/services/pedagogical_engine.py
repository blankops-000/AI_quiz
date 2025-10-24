"""
Pedagogical Engine - Core component for adaptive learning
Implements IRT (Item Response Theory) and Bloom's Taxonomy integration
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class BloomsLevel(Enum):
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6

@dataclass
class Question:
    id: str
    text: str
    difficulty: float  # IRT b parameter (-4 to 4)
    discrimination: float = 1.0  # IRT a parameter
    guessing: float = 0.0  # IRT c parameter
    blooms_level: BloomsLevel = BloomsLevel.REMEMBER
    subject: str = ""
    topic: str = ""
    correct_answer: str = ""
    options: List[str] = None

@dataclass
class StudentProfile:
    user_id: str
    ability_level: float = 0.0  # IRT theta parameter
    blooms_progress: Dict[BloomsLevel, float] = None
    subject_abilities: Dict[str, float] = None
    learning_style: str = "adaptive"
    
    def __post_init__(self):
        if self.blooms_progress is None:
            self.blooms_progress = {level: 0.0 for level in BloomsLevel}
        if self.subject_abilities is None:
            self.subject_abilities = {}

class PedagogicalEngine:
    """
    Core pedagogical engine implementing IRT and Bloom's Taxonomy
    for adaptive quiz generation and personalized learning
    """
    
    def __init__(self):
        self.min_ability = -4.0
        self.max_ability = 4.0
        self.default_discrimination = 1.0
        self.convergence_threshold = 0.01
        self.max_iterations = 50
    
    def calculate_probability(self, ability: float, difficulty: float, 
                            discrimination: float = 1.0, guessing: float = 0.0) -> float:
        """
        Calculate probability of correct response using 3PL IRT model
        P(correct) = c + (1-c) / (1 + exp(-a(θ-b)))
        """
        try:
            exponent = -discrimination * (ability - difficulty)
            if exponent > 700:  # Prevent overflow
                return guessing
            elif exponent < -700:
                return 1.0
            
            probability = guessing + (1 - guessing) / (1 + math.exp(exponent))
            return max(0.0, min(1.0, probability))
        except (OverflowError, ValueError):
            return 0.5  # Default probability
    
    def estimate_ability(self, responses: List[Tuple[bool, float, float, float]]) -> Tuple[float, float]:
        """
        Estimate student ability using Maximum Likelihood Estimation
        Returns: (ability_estimate, standard_error)
        """
        if not responses:
            return 0.0, 1.0
        
        ability = 0.0  # Initial estimate
        
        for iteration in range(self.max_iterations):
            first_derivative = 0.0
            second_derivative = 0.0
            
            for correct, difficulty, discrimination, guessing in responses:
                prob = self.calculate_probability(ability, difficulty, discrimination, guessing)
                
                # Prevent division by zero
                if prob <= 0.001:
                    prob = 0.001
                elif prob >= 0.999:
                    prob = 0.999
                
                # First derivative (score function)
                score_numerator = discrimination * (1 - guessing) * math.exp(-discrimination * (ability - difficulty))
                score_denominator = (1 + math.exp(-discrimination * (ability - difficulty))) ** 2
                score_term = score_numerator / score_denominator
                
                if correct:
                    first_derivative += score_term / prob
                else:
                    first_derivative -= score_term / (1 - prob)
                
                # Second derivative (information function)
                info_term = discrimination ** 2 * (1 - guessing) * math.exp(-discrimination * (ability - difficulty))
                info_denominator = (1 + math.exp(-discrimination * (ability - difficulty))) ** 2
                information = info_term / info_denominator
                
                second_derivative -= information * (prob * (1 - prob)) / (prob ** 2 * (1 - prob) ** 2)
            
            # Newton-Raphson update
            if abs(second_derivative) < 1e-10:
                break
                
            ability_change = first_derivative / (-second_derivative)
            ability += ability_change
            
            # Constrain ability within bounds
            ability = max(self.min_ability, min(self.max_ability, ability))
            
            if abs(ability_change) < self.convergence_threshold:
                break
        
        # Calculate standard error
        information_sum = 0.0
        for correct, difficulty, discrimination, guessing in responses:
            prob = self.calculate_probability(ability, difficulty, discrimination, guessing)
            if 0.001 <= prob <= 0.999:
                info_term = discrimination ** 2 * (1 - guessing) * math.exp(-discrimination * (ability - difficulty))
                info_denominator = (1 + math.exp(-discrimination * (ability - difficulty))) ** 2
                information = info_term / info_denominator
                information_sum += information
        
        standard_error = 1.0 / math.sqrt(max(information_sum, 0.1))
        
        return ability, standard_error
    
    def select_next_question(self, student_profile: StudentProfile, 
                           available_questions: List[Question],
                           target_blooms_level: Optional[BloomsLevel] = None) -> Optional[Question]:
        """
        Select the most informative question for the student
        Considers both IRT information and Bloom's Taxonomy progression
        """
        if not available_questions:
            return None
        
        best_question = None
        best_score = -float('inf')
        
        for question in available_questions:
            # Calculate IRT information
            prob = self.calculate_probability(
                student_profile.ability_level,
                question.difficulty,
                question.discrimination,
                question.guessing
            )
            
            # Fisher information
            information = question.discrimination ** 2 * prob * (1 - prob)
            
            # Bloom's Taxonomy consideration
            blooms_weight = 1.0
            if target_blooms_level:
                if question.blooms_level == target_blooms_level:
                    blooms_weight = 2.0  # Prefer target level
                elif abs(question.blooms_level.value - target_blooms_level.value) == 1:
                    blooms_weight = 1.5  # Adjacent levels are good too
            
            # Subject-specific ability consideration
            subject_ability = student_profile.subject_abilities.get(question.subject, student_profile.ability_level)
            subject_prob = self.calculate_probability(subject_ability, question.difficulty)
            subject_information = question.discrimination ** 2 * subject_prob * (1 - subject_prob)
            
            # Combined score
            score = (information + subject_information) * blooms_weight
            
            if score > best_score:
                best_score = score
                best_question = question
        
        return best_question
    
    def update_student_profile(self, student_profile: StudentProfile, 
                             question: Question, correct: bool, response_time: float = 0.0):
        """
        Update student profile based on response
        """
        # Update overall ability using simple adaptation
        expected_prob = self.calculate_probability(
            student_profile.ability_level,
            question.difficulty,
            question.discrimination,
            question.guessing
        )
        
        learning_rate = 0.1
        ability_change = learning_rate * (correct - expected_prob)
        student_profile.ability_level += ability_change
        student_profile.ability_level = max(self.min_ability, min(self.max_ability, student_profile.ability_level))
        
        # Update Bloom's level progress
        current_progress = student_profile.blooms_progress[question.blooms_level]
        if correct:
            student_profile.blooms_progress[question.blooms_level] = min(1.0, current_progress + 0.1)
        else:
            student_profile.blooms_progress[question.blooms_level] = max(0.0, current_progress - 0.05)
        
        # Update subject-specific ability
        if question.subject not in student_profile.subject_abilities:
            student_profile.subject_abilities[question.subject] = student_profile.ability_level
        else:
            subject_ability = student_profile.subject_abilities[question.subject]
            subject_expected = self.calculate_probability(subject_ability, question.difficulty)
            subject_change = learning_rate * (correct - subject_expected)
            student_profile.subject_abilities[question.subject] += subject_change
    
    def generate_adaptive_quiz(self, student_profile: StudentProfile,
                             question_pool: List[Question],
                             target_questions: int = 10,
                             target_blooms_distribution: Dict[BloomsLevel, float] = None) -> List[Question]:
        """
        Generate an adaptive quiz based on student profile and learning objectives
        """
        if target_blooms_distribution is None:
            # Default distribution emphasizing higher-order thinking
            target_blooms_distribution = {
                BloomsLevel.REMEMBER: 0.1,
                BloomsLevel.UNDERSTAND: 0.2,
                BloomsLevel.APPLY: 0.3,
                BloomsLevel.ANALYZE: 0.2,
                BloomsLevel.EVALUATE: 0.1,
                BloomsLevel.CREATE: 0.1
            }
        
        selected_questions = []
        remaining_questions = question_pool.copy()
        
        # Calculate target counts for each Bloom's level
        target_counts = {level: int(target_questions * weight) 
                        for level, weight in target_blooms_distribution.items()}
        
        # Ensure we have at least target_questions total
        total_targeted = sum(target_counts.values())
        if total_targeted < target_questions:
            target_counts[BloomsLevel.APPLY] += target_questions - total_targeted
        
        # Select questions for each Bloom's level
        for blooms_level, count in target_counts.items():
            level_questions = [q for q in remaining_questions if q.blooms_level == blooms_level]
            
            for _ in range(min(count, len(level_questions))):
                question = self.select_next_question(student_profile, level_questions, blooms_level)
                if question:
                    selected_questions.append(question)
                    remaining_questions.remove(question)
                    level_questions.remove(question)
        
        # Fill remaining slots with best available questions
        while len(selected_questions) < target_questions and remaining_questions:
            question = self.select_next_question(student_profile, remaining_questions)
            if question:
                selected_questions.append(question)
                remaining_questions.remove(question)
            else:
                break
        
        return selected_questions
    
    def analyze_performance(self, responses: List[Tuple[Question, bool, float]]) -> Dict:
        """
        Analyze student performance across different dimensions
        """
        if not responses:
            return {}
        
        # Overall performance
        total_correct = sum(1 for _, correct, _ in responses)
        accuracy = total_correct / len(responses)
        
        # Performance by Bloom's level
        blooms_performance = {}
        for level in BloomsLevel:
            level_responses = [(q, correct) for q, correct, _ in responses if q.blooms_level == level]
            if level_responses:
                level_correct = sum(1 for _, correct in level_responses)
                blooms_performance[level.name.lower()] = level_correct / len(level_responses)
        
        # Difficulty analysis
        difficulties = [q.difficulty for q, _, _ in responses]
        avg_difficulty = np.mean(difficulties) if difficulties else 0
        
        # Response time analysis
        response_times = [rt for _, _, rt in responses if rt > 0]
        avg_response_time = np.mean(response_times) if response_times else 0
        
        # Ability estimation
        irt_responses = [(correct, q.difficulty, q.discrimination, q.guessing) 
                        for q, correct, _ in responses]
        final_ability, standard_error = self.estimate_ability(irt_responses)
        
        return {
            'accuracy': accuracy,
            'total_questions': len(responses),
            'correct_answers': total_correct,
            'blooms_performance': blooms_performance,
            'average_difficulty': avg_difficulty,
            'average_response_time': avg_response_time,
            'estimated_ability': final_ability,
            'ability_standard_error': standard_error,
            'performance_level': self._classify_performance_level(accuracy, final_ability)
        }
    
    def _classify_performance_level(self, accuracy: float, ability: float) -> str:
        """Classify overall performance level"""
        if accuracy >= 0.9 and ability >= 2.0:
            return "excellent"
        elif accuracy >= 0.8 and ability >= 1.0:
            return "good"
        elif accuracy >= 0.7 and ability >= 0.0:
            return "satisfactory"
        elif accuracy >= 0.6 and ability >= -1.0:
            return "needs_improvement"
        else:
            return "requires_support"