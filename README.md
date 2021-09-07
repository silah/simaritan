# simaritan

This is the Simaritan Incident Management tool.
The application is created to help incident manager track tasks, timeline events, incident members and other related data pertaining to the management of IT Incidents.

The tool allows for storage, tracking and export of Incident Management data and can be used to gather information and give a constant situational overview to any interested stakeholders, as well as aide in the creation of Incident reports.

The application relies on Python Flask (requirements for the venv is in requirements.txt) and is available on the docker hub under simaritan/simaritan:dev.

To run the application, install docker and execute 
"docker run --name simaritandev -d -p 8080:5000 simaritan/simaritan:dev"
This will start the application listening on port 8080.

By default, a standard SQLite database is provided with a dummy user and a dummy incident. Use the dummy user to create your own accounts and delete afterwards.

Username: test_user
Password: test123
