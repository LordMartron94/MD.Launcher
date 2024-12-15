# MD.Launcher

Utility tool for the launching of my projects using the Component-Based Architecture Foundation I created.
See: https://github.com/LordMartron94/Component-Architecture-Foundation

Once again, the launcher has its own logger instance instead of relying on the logging component. 
This is because the launcher has to start the logger component, and thus it's illogical to rely on that one for logging.