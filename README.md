
# Exam flow 
- Student starts exam
- Server creates an Exam Attempt
- Student requests next question
- Student submits answer
- Repeat until last question
- Student submits final exam

# Frontend behavior (Flutter / React)
- Start Exam
- Load Question
- User selects option
- Auto-save answer
- Load next question
- Timer shown (server-based)
- Final submit

# Alembic migration commands
# 1. Generate migration from model changes
alembic revision --autogenerate -m "Add attendance tracking"

# 2. Review the generated migration
#    Check the file in alembic/versions/ before running!

# 3. Run migration (development)
alembic upgrade head

# 4. Rollback if needed
alembic downgrade -1

# 5. Production deployment
alembic upgrade head  # Run this in deployment script