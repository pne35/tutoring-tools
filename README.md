tutoring-tools
A Python toolkit for managing a private tutoring business. Built because I actually run one — so every feature here solves a real problem.
What it does

Client tracker — add and manage students, rates, and contact details
Session logger — log each session with date, duration, topic covered, and payment status
Earnings tracker — weekly and monthly income summaries
Invoice generator — produce PDF invoices per client (coming soon)
Progress dashboard — visualise student session history over time (coming soon)

Why I built this
I tutor GCSE Maths students at £15/hour. Managing 4–8 clients across a spreadsheet gets messy fast — tracking who's paid, what we covered, and what I've earned each week. This toolkit replaces that with clean Python and a persistent JSON data store.
Tech

Python 3
JSON for data persistence
CLI interface (web dashboard planned)

Project status
Active. Starting with the core client tracker and session logger, building out from there.
Run it
bashgit clone https://github.com/pne35/tutoring-tools
cd tutoring-tools
python main.py
About
Built by Harry Smalley — A-Level Maths, Further Maths & Computing student at LUSoM Sixth Form, Lancaster.
https://pne35.github.io/HarrySmalley/
