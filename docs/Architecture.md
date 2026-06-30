# Architecture

MarkdownToHtml follows Clean Architecture and SOLID principles.

## Directories
- `src/ui/`: Contains all PySide6 Views, Widgets, and styling components.
- `src/controllers/`: Mediators that tie UI interactions to backend services.
- `src/services/`: Core logic (file saving, auto-save timers, settings injection).
- `src/rendering/`: markdown-it-py adapters, Jinja2 template loading.
- `src/models/`: Dataclasses representing document state and application config.
