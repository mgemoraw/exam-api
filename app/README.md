Admin Panel (Web)
   |
   |  Upload .docx / .md
   v
FastAPI Backend
   |
   |-- File Storage (S3 / GCS / Local)
   |-- Parsing Service
   |-- Chapter & Section Generator
   v
PostgreSQL
   |
   |-- Courses
   |-- Modules
   |-- Chapters
   |-- Sections
   |-- Content Blocks
   v
Mobile App (Flutter)

## Content Model
Course
- id (UUID)
- title
- description

Module
- id
- course_id
- title
- order

Chapter
- id
- module_id
- title
- order

Section
- id
- chapter_id
- title
- order


ContentBlock
- id
- section_id
- type (TEXT, CODE, IMAGE, LIST, FORMULA)
- content (JSON / TEXT)
- order

## Accepted formats
- .docx
- .md
- .html

## Upload flow
Admin uploads file
→ Save original file (audit + reprocessing)
→ Parse to structured content
→ Save parsed chapters/sections/blocks


# Storage

## Production options

- AWS S3 (recommended)
- MinIO (self-hosted)
- Local (dev only)

# Parsing Strategy
## Markdown Parsing
markdown
mistune
markdown-it-py

##  Heading rules
```
# = Chapter
## = Section
### = Subsection
#### = Sub
```

```
# Pseudocode
for token in markdown_tokens:
    if token.level == 1:
        create_chapter()
    elif token.level == 2:
        create_section()
    else:
        create_content_block()
```

## DOCX Parsing
- use python-docx

## Rules
| DOCX Element | Maps to    |
| ------------ | ---------- |
| Heading 1    | Chapter    |
| Heading 2    | Section    |
| Paragraph    | Text block |
| Bullet list  | List block |
| Code style   | Code block |

```

from docx import Document

doc = Document(file_path)

for p in doc.paragraphs:
    if p.style.name == "Heading 1":
        chapter = create_chapter(p.text)
    elif p.style.name == "Heading 2":
        section = create_section(p.text)
    else:
        create_text_block(p.text)

```

## Parsing as a Background Task (Production Rule)
Use:
- BackgroundTasks (small)
- Clery + Redis (recommended)

```
Upload → 202 Accepted
→ Background parsing
→ Status: PROCESSING / COMPLETED / FAILED
```
## API Design (Clean & Mobile Friendly)
```
POST /admin/modules/{module_id}/notes/upload

# Response
{
  "status": "processing",
  "task_id": "uuid"
}

# Get chapters
GET /mobile/modules/{module_id}/chapters

# Response
[
  {
    "id": "...",
    "title": "Introduction",
    "order": 1
  }
]

# Get Chapter Content 
GET /mobile/chapters/{chapter_id}

# Response
{
  "title": "Introduction",
  "sections": [
    {
      "title": "Definition",
      "blocks": [
        {
          "type": "TEXT",
          "content": "A computer is..."
        },
        {
          "type": "LIST",
          "content": ["Input", "Processing", "Output"]
        }
      ]
    }
  ]
}
```

## Mobile App Rendering Strategy (Flutter)
| Block Type | Flutter Widget       |
| ---------- | -------------------- |
| TEXT       | `SelectableText`     |
| LIST       | `ListView`           |
| CODE       | `CodeView`           |
| IMAGE      | `CachedNetworkImage` |
| FORMULA    | `Text`               |

### for offiline use
- store ContentBlock locally (SQLite / Drift)
- Sync via updated_at

## Versioning & Re-uploads (Very Important)
content_version
is_active


## Security & Permissions
- Only admins upload
- Students read-only
- Signed URLs for files
- Rate limit content APIs

## Future-Proof Enhancements
This design supports:
✅ AI summarization per chapter
✅ Highlighting & notes
✅ Audio narration
✅ In-chapter quizzes
✅ Search engine (Postgres FTS / Meilisearch)