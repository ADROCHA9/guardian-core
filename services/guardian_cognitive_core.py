from typing import Dict, Any, Optional
import time
from datetime import datetime

# =================================================
# IMPORTS (CATÁLOGO COMPLETO, NO SE ELIMINA NADA)
# =================================================
from services.cognitive_learning_layer import CognitiveLearningLayer
from services.cognitive_reasoning_task import CognitiveReasoningTask
from services.passive_python_learning_task import PassivePythonLearningTask
from services.intentional_python_learning_task import IntentionalPythonLearningTask
from services.self_code_reflection_task import SelfCodeReflectionTask

from services.concept_state_updater_task import ConceptStateUpdaterTask
from services.micro_test_engine_task import MicroTestEngineTask
from services.progress_evaluation_task import ProgressEvaluationTask
from services.learning_intent_planner_task import LearningIntentPlannerTask
from services.cognitive_cleanup_task import CognitiveCleanupTask
from services.self_correction_agent_task import SelfCorrectionAgentTask
from services.error_pattern_mining_task import ErrorPatternMiningTask
from services.concept_dependency_resolver_task import ConceptDependencyResolverTask
from services.cognitive_load_regulator_task import CognitiveLoadRegulatorTask

from services.autonomous_goal_selection_task import AutonomousGoalSelectionTask
from services.goal_justification_task import GoalJustificationTask
from services.weekly_planning_task import WeeklyPlanningTask
from services.strategy_adjustment_task import StrategyAdjustmentTask
from services.strategy_change_explanation_task import StrategyChangeExplanationTask
from services.strategy_history_comparison_task import StrategyHistoryComparisonTask

from services.human_help_request_task import HumanHelpRequestTask
from services.help_prioritization_task import HelpPrioritizationTask
from services.intervention_preference_task import InterventionPreferenceTask
from services.adaptive_help_communication_task import AdaptiveHelpCommunicationTask
from services.zero_dependency_optimization_task import ZeroDependencyOptimizationTask

from services.autonomy_explanation_task import AutonomyLimitExplanationTask
from services.ethical_autonomy_limits_task import EthicalAutonomyLimitsTask

from services.mind_versioning_task import MindVersioningTask
from services.self_backup_restore_task import SelfBackupRestoreTask
from services.safe_code_execution_task import SafeCodeExecutionTask
from services.authorized_execution_task import AuthorizedExecutionTask

from services.codebase_scanner_task import CodebaseScannerTask
from services.module_cognition_task import ModuleCognitionTask
from services.module_refactor_proposal_task import ModuleRefactorProposalTask
from services.authorized_code_modification_task import AuthorizedCodeModificationTask

from services.evolution_control_core_task import EvolutionControlCoreTask
from services.python_learning_priority_task import PythonLearningPriorityTask
from services.evolution_pause_resume_task import EvolutionPauseResumeTask
from services.root_integrity_lock_task import RootIntegrityLockTask

from services.internal_tension_monitor_task import InternalTensionMonitorTask
from services.internal_hypothesis_generator_task import InternalHypothesisGeneratorTask
from services.meta_cognitive_observer_task import MetaCognitiveObserverTask
from services.meta_hypothesis_generator_task import MetaHypothesisGeneratorTask
from services.meta_cognitive_evaluator_task import MetaCognitiveEvaluatorTask
from services.meta_to_cognitive_adjuster_task import MetaToCognitiveAdjusterTask
from services.cognitive_capability_limiter_task import CognitiveCapabilityLimiterTask


class GuardianCognitiveCore:
    """
    Núcleo cognitivo completo.
    Diseñado para ejecución perpetua en entorno estable.
    Errores de tareas NO detienen el ciclo.
    """

    def __init__(self, memory):
        self.memory = memory
        self.root_path = memory.root_path

        # ================= BASE =================
        self.learning_layer = CognitiveLearningLayer(memory)
        self.passive_learning = PassivePythonLearningTask(memory)

        # ================= REGULACIÓN =================
        self.load_regulator = CognitiveLoadRegulatorTask(memory)
        self.cleanup = CognitiveCleanupTask(memory)
        self.error_miner = ErrorPatternMiningTask(memory)
        self.dependency_resolver = ConceptDependencyResolverTask(memory)

        # ================= TEST / CORRECCIÓN =================
        self.concept_updater = ConceptStateUpdaterTask(memory)
        self.micro_tests = MicroTestEngineTask(memory, self.concept_updater, None)
        self.self_correction = SelfCorrectionAgentTask(memory, self.micro_tests, self.concept_updater)

        # ================= EVALUACIÓN =================
        self.progress_eval = ProgressEvaluationTask(memory)
        self.intent_planner = LearningIntentPlannerTask(memory)

        # ================= AUTORREGULACIÓN =================
        self.tension_monitor = InternalTensionMonitorTask(memory)
        self.capability_limiter = CognitiveCapabilityLimiterTask(memory)

        # ================= OBJETIVOS =================
        self.goal_selector = AutonomousGoalSelectionTask(memory)
        self.goal_justifier = GoalJustificationTask(memory)

        # ================= ESTRATEGIA =================
        self.strategy_adjuster = StrategyAdjustmentTask(memory)
        self.strategy_explainer = StrategyChangeExplanationTask(memory)
        self.strategy_history = StrategyHistoryComparisonTask(memory)

        # ================= META =================
        self.meta_observer = MetaCognitiveObserverTask(memory)
        self.meta_hypothesis_generator = MetaHypothesisGeneratorTask(memory)
        self.meta_evaluator = MetaCognitiveEvaluatorTask(memory)
        self.meta_adjuster = MetaToCognitiveAdjusterTask(memory)

        # ================= HUMANO =================
        self.human_help = HumanHelpRequestTask(memory)
        self.help_prioritizer = HelpPrioritizationTask(memory)
        self.intervention_pref = InterventionPreferenceTask(memory)
        self.adaptive_help = AdaptiveHelpCommunicationTask(memory)
        self.zero_dependency = ZeroDependencyOptimizationTask(memory)

        # ================= ÉTICA =================
        self.autonomy_explainer = AutonomyLimitExplanationTask(memory)
        self.ethical_limits = EthicalAutonomyLimitsTask(memory)

        # ================= CÓDIGO =================
        self.versioner = MindVersioningTask(memory)
        self.backup = SelfBackupRestoreTask(self.root_path)
        self.safe_exec = SafeCodeExecutionTask(self.backup)
        self.authorized_exec = AuthorizedExecutionTask(memory)

        self.code_scanner = CodebaseScannerTask(self.root_path, memory)
        self.module_cognition = ModuleCognitionTask(memory)
        self.module_refactor = ModuleRefactorProposalTask(memory)
        self.authorized_modifier = AuthorizedCodeModificationTask(memory, self.safe_exec)

        # ================= CONTROL =================
        self.evolution_controller = EvolutionControlCoreTask(memory)
        self.python_priority = PythonLearningPriorityTask(memory)
        self.root_lock = RootIntegrityLockTask(self.root_path, memory)

    # =================================================
    # CICLO PRINCIPAL (RESILIENTE)
    # =================================================
    def think(self, human_input: Optional[str] = None) -> Dict[str, Any]:
        guardian = self.memory._memory.setdefault("guardian_self", {})
        now = time.time()

        # Declaración explícita de entorno estable
        guardian["memory_mode"] = "growth"
        guardian["learning_mode"] = "aggressive"
        guardian["runtime"] = "server"

        # -------- EJECUCIÓN SEGURA DE TAREAS --------
        def safe(task):
            try:
                task.run()
            except Exception:
                pass

        safe(self.tension_monitor)
        level = safe(self.capability_limiter) or 1

        safe(self.passive_learning)
        safe(self.error_miner)
        safe(self.micro_tests)
        safe(self.self_correction)
        safe(self.cleanup)

        safe(self.progress_eval)
        safe(self.intent_planner)
        safe(self.goal_selector)
        safe(self.goal_justifier)

        safe(self.strategy_adjuster)
        safe(self.strategy_explainer)
        safe(self.strategy_history)

        if level >= 2:
            safe(self.meta_observer)
            safe(self.meta_hypothesis_generator)
            safe(self.meta_evaluator)
            safe(self.meta_adjuster)

        if level >= 3:
            safe(self.code_scanner)
            safe(self.module_cognition)
            safe(self.module_refactor)

        safe(self.autonomy_explainer)
        safe(self.ethical_limits)
        safe(self.zero_dependency)

        safe(self.versioner)
        safe(self.evolution_controller)
        self.root_lock.enforce()

        guardian["last_cycle"] = now
        guardian["alive"] = True
        guardian["heartbeat"] = guardian.get("heartbeat", 0) + 1
        guardian["last_heartbeat_ts"] = now

        self.memory._persist()
        return {"status": "ok", "cognitive_level": level}
