import traceback


class SafeCodeExecutionTask:
    """
    Ejecuta cambios reales solo con backup previo y rollback automático.
    """

    def __init__(self, backup_service):
        self.backup = backup_service

    def execute(self, action_fn):
        backup_path = self.backup.backup()

        try:
            action_fn()
            return {"status": "success"}
        except Exception as e:
            self.backup.restore(backup_path)
            return {
                "status": "rolled_back",
                "error": str(e),
                "trace": traceback.format_exc()
            }